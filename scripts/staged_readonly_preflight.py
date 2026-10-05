"""Bounded, deterministic observation of one owner-bound principal checkout."""

import hashlib
import json
import os
import re
import selectors
import stat
import subprocess
import sys
import time
import unicodedata


ROOT = "/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor"
COMMON = ROOT + "/.git"
INPUT_LIMIT = 262144
FILE_LIMIT = 16 * 1024 * 1024
SCAN_LIMIT = 64 * 1024 * 1024
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
ID = re.compile(r"[A-Za-z0-9_.-]{1,128}\Z")
SEGMENT = re.compile(r"[A-Za-z0-9._ -]+\Z")
FORBIDDEN = {".git", ".venv", "data", "corpus"}
FIELDS = {"schema_version", "work_unit_id", "repository_id", "root", "common_dir", "branch", "head", "index_sha256", "staged", "delta", "absent", "ignored_inputs", "git", "config_sha256", "index_tree_sha256", "state_kind"}
V3_FIELDS = {"repository_format_version", "extension_worktree_config", "config_worktree"}
ROW_FIELDS = {"path", "xy", "kind", "mode", "sha256"}
ENV = {
    "PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C", "TZ": "UTC",
    "HOME": "/dev/null", "XDG_CONFIG_HOME": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": "/dev/null",
    "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_ATTR_NOSYSTEM": "1",
    "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0",
    "GIT_NO_REPLACE_OBJECTS": "1",
}
GIT_PREFIX = ("--no-pager", "--no-optional-locks", "-c", "core.fsmonitor=false",
              "-c", "core.untrackedCache=false", "-c", "core.hooksPath=/dev/null",
              "-c", "diff.external=")
CAPTURE_LIMIT = 262144
PROCESS_SECONDS = 5


class Stop(Exception):
    def __init__(self, reason, step=None, child=None, code=None):
        self.reason = reason
        self.step = step
        self.child = child
        self.code = code


def _result(raw_hash=None):
    return {
        "schema_version": "yini-readonly-preflight/result-v2",
        "work_unit_id": None, "contract_sha256": raw_hash,
        "outcome": "STOP", "reason": "INTERNAL_DEFECT", "exit_code": 70,
        "failed_step": None, "child_returncode": None, "observations": [],
        "fingerprint": None, "successor_authority": False,
    }


def _stop(result, error):
    result["outcome"] = "STOP"
    result["fingerprint"] = None
    result["reason"] = error.reason
    result["failed_step"] = error.step
    result["child_returncode"] = error.child
    result["exit_code"] = error.code if error.code is not None else {
        "INVALID_INPUT": 2, "CONTRACT_HASH_MISMATCH": 2,
        "CONTRACT_INVALID": 2, "PATH_UNSAFE": 2,
        "ENVIRONMENT_UNSUPPORTED": 4, "CHECKOUT_UNSUPPORTED": 4,
        "TOOL_IDENTITY_MISMATCH": 4, "STATE_UNSUPPORTED": 4, "OBSERVATION_MISMATCH": 3,
        "OBSERVATION_DRIFT": 3, "FILESYSTEM_ERROR": 5,
        "PROCESS_LAUNCH_ERROR": 5, "TIMEOUT": 124,
        "CAPTURE_LIMIT": 125, "INTERNAL_DEFECT": 70,
    }[error.reason]
    return result


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _bad_constant(_value):
    raise ValueError("non-finite number")


def _is_hex(value, pattern):
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def _safe_path(value):
    if not isinstance(value, str) or not value or value.startswith("/"):
        return False
    segments = value.split("/")
    return all(segment not in (".", "..") and segment not in FORBIDDEN
               and not segment.startswith(".env") and segment == segment.strip(" ")
               and SEGMENT.fullmatch(segment) is not None for segment in segments)


def _ordered(group):
    return group == sorted(set(group), key=lambda item: item.encode("utf-8"))


def _oid(value):
    return _is_hex(value, HEX40) and value != "0" * 40


def _schema(raw, expected, result):
    if not isinstance(raw, bytes) or len(raw) > INPUT_LIMIT or raw.startswith(b"\xef\xbb\xbf"):
        raise Stop("INVALID_INPUT", "input")
    if not _is_hex(expected, HEX64):
        raise Stop("INVALID_INPUT", "input")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected:
        raise Stop("CONTRACT_HASH_MISMATCH", "input")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_bad_constant)
    except (UnicodeError, ValueError, TypeError):
        raise Stop("INVALID_INPUT", "input") from None
    v3 = isinstance(data, dict) and data.get("schema_version") == "yini-readonly-preflight/contract-v3"
    if v3:
        result["schema_version"] = "yini-readonly-preflight/result-v3"
    if not isinstance(data, dict) or set(data) != (FIELDS | V3_FIELDS if v3 else FIELDS):
        raise Stop("CONTRACT_INVALID", "input")
    if v3 and not (type(data["repository_format_version"]) is int
                   and data["repository_format_version"] == 0
                   and (data["extension_worktree_config"] is None
                        or type(data["extension_worktree_config"]) is bool)
                   and type(data["config_worktree"]) is dict
                   and data["config_worktree"] == {"state": "absent"}):
        raise Stop("CONTRACT_INVALID", "input")
    checks = (
        v3 or data["schema_version"] == "yini-readonly-preflight/contract-v2",
        isinstance(data["work_unit_id"], str) and ID.fullmatch(data["work_unit_id"]) is not None,
        data["repository_id"] == "yini-insurance-advisor",
        data["root"] == ROOT, data["common_dir"] == COMMON, data["branch"] == "main",
        _oid(data["head"]),
        all(_is_hex(data[key], HEX64) for key in ("index_sha256", "config_sha256", "index_tree_sha256")),
        isinstance(data["staged"], list) and len(data["staged"]) <= 32,
        isinstance(data["delta"], list) and len(data["delta"]) <= 128,
        isinstance(data["absent"], list) and len(data["absent"]) <= 128,
        data["ignored_inputs"] == "none",
        isinstance(data["git"], dict) and set(data["git"]) == {"path", "sha256"},
    )
    if not all(checks):
        raise Stop("CONTRACT_INVALID", "input")
    if not ((data["state_kind"] == "empty_staged" and not data["staged"])
            or (data["state_kind"] == "staged_regular" and data["staged"])):
        raise Stop("CONTRACT_INVALID", "input")
    git = data["git"]
    if not isinstance(git["path"], str) or not git["path"].startswith("/") or not _is_hex(git["sha256"], HEX64):
        raise Stop("CONTRACT_INVALID", "input")
    staged_fields = {"path", "change", "head_mode", "head_oid", "index_mode", "index_oid", "blob_sha256"}
    for row in data["delta"]:
        if not isinstance(row, dict) or set(row) != ROW_FIELDS:
            raise Stop("CONTRACT_INVALID", "input")
        if (row["xy"] not in (" M", "??", "M ", "MM", "A ", "AM")
                or row["kind"] != "regular" or row["mode"] not in ("644", "755")
                or not _is_hex(row["sha256"], HEX64)):
            raise Stop("CONTRACT_INVALID", "input")
    for row in data["staged"]:
        if not isinstance(row, dict) or set(row) != staged_fields:
            raise Stop("CONTRACT_INVALID", "input")
        if (row["change"] not in ("A", "M") or row["index_mode"] not in ("100644", "100755")
                or not _oid(row["index_oid"]) or not _is_hex(row["blob_sha256"], HEX64)):
            raise Stop("CONTRACT_INVALID", "input")
        if row["change"] == "A":
            valid = row["head_mode"] == "000000" and row["head_oid"] == "0" * 40
        else:
            valid = (row["head_mode"] in ("100644", "100755") and _oid(row["head_oid"])
                     and (row["head_mode"], row["head_oid"]) != (row["index_mode"], row["index_oid"]))
        if not valid:
            raise Stop("CONTRACT_INVALID", "input")
    groups = [[row["path"] for row in data["delta"]],
              [row["path"] for row in data["staged"]], data["absent"]]
    if not all(_safe_path(name) for group in groups for name in group):
        raise Stop("PATH_UNSAFE", "input")
    if not all(_ordered(group) for group in groups):
        raise Stop("CONTRACT_INVALID", "input")
    if set(data["absent"]) & (set(groups[0]) | set(groups[1])):
        raise Stop("CONTRACT_INVALID", "input")
    changed = {row["path"]: row["xy"][0] for row in data["delta"] if row["xy"][0] in ("A", "M")}
    if changed != {row["path"]: row["change"] for row in data["staged"]}:
        raise Stop("CONTRACT_INVALID", "input")
    return data, digest


def _environment():
    if not sys.dont_write_bytecode:
        raise Stop("ENVIRONMENT_UNSUPPORTED", "environment")
    if any(key.startswith("GIT_") and (key != "GIT_OPTIONAL_LOCKS" or value != "0")
           for key, value in os.environ.items()):
        raise Stop("ENVIRONMENT_UNSUPPORTED", "environment")


def _components(candidate, step):
    if not isinstance(candidate, str) or not candidate.startswith("/") or os.path.normpath(candidate) != candidate:
        raise Stop("PATH_UNSAFE", step)
    current = "/"
    for segment in candidate.split("/")[1:]:
        current = os.path.join(current, segment)
        try:
            info = os.lstat(current)
        except FileNotFoundError:
            return None
        except OSError:
            raise Stop("FILESYSTEM_ERROR", step) from None
        if stat.S_ISLNK(info.st_mode):
            raise Stop("PATH_UNSAFE", step)
        if current != candidate and not stat.S_ISDIR(info.st_mode):
            raise Stop("PATH_UNSAFE", step)
    return info


def _read_regular(candidate, step, remaining, executable=False):
    info = _components(candidate, step)
    if info is None or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise Stop("TOOL_IDENTITY_MISMATCH" if executable and step == "before.index"
                   else "OBSERVATION_MISMATCH", step)
    if info.st_size > FILE_LIMIT or info.st_size > remaining:
        raise Stop("OBSERVATION_MISMATCH", step)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
        try:
            opened = os.fstat(descriptor)
            if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                raise Stop("OBSERVATION_DRIFT", step)
            digest = hashlib.sha256()
            length = 0
            while True:
                chunk = os.read(descriptor, min(65536, FILE_LIMIT + 1 - length))
                if not chunk:
                    break
                length += len(chunk)
                if length > FILE_LIMIT or length > remaining:
                    raise Stop("OBSERVATION_MISMATCH", step)
                digest.update(chunk)
            finished = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except OSError:
        raise Stop("FILESYSTEM_ERROR", step) from None
    identity = lambda item: (item.st_dev, item.st_ino, item.st_mode, item.st_nlink,
                             item.st_size, item.st_mtime_ns, item.st_ctime_ns)
    if identity(info) != identity(opened) or identity(opened) != identity(finished):
        raise Stop("OBSERVATION_DRIFT", step)
    if executable and not (info.st_mode & 0o111):
        raise Stop("TOOL_IDENTITY_MISMATCH", step)
    return digest.hexdigest(), length, identity(info), stat.S_IMODE(info.st_mode)


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _storage(step):
    identities = []
    for name in ("/objects", "/objects/info", "/objects/pack", "/info"):
        candidate = COMMON + name
        initial = _components(candidate, step)
        if initial is None or not stat.S_ISDIR(initial.st_mode):
            raise Stop("STATE_UNSUPPORTED", step)
        records = []
        try:
            with os.scandir(candidate) as iterator:
                for entry in iterator:
                    if len(records) == 8192:
                        raise Stop("STATE_UNSUPPORTED", step)
                    if name == "/objects/pack" and entry.name.endswith(".promisor"):
                        raise Stop("STATE_UNSUPPORTED", step)
                    # Inventory metadata only; never traverse loose objects or read packs.
                    info = _components(candidate + "/" + entry.name, step)
                    if info is None:
                        raise Stop("OBSERVATION_DRIFT", step)
                    records.append((entry.name, _identity(info)))
        except OSError:
            raise Stop("FILESYSTEM_ERROR", step) from None
        final = _components(candidate, step)
        if final is None or _identity(initial) != _identity(final):
            raise Stop("OBSERVATION_DRIFT", step)
        identities.append((_identity(initial), sorted(records)))
    for suffix in ("/objects/info/alternates", "/objects/info/http-alternates", "/shallow", "/info/grafts"):
        if _components(COMMON + suffix, step) is not None:
            raise Stop("STATE_UNSUPPORTED", step)
    return identities


def _worktree_absent(step, later=False):
    try:
        info = _components(COMMON + "/config.worktree", step)
    except Stop as error:
        if later and error.reason == "PATH_UNSAFE":
            raise Stop("OBSERVATION_DRIFT", step) from None
        raise
    if info is not None:
        raise Stop("OBSERVATION_DRIFT" if later else "STATE_UNSUPPORTED", step)


def _scan(data, step, first=None, path_step=None):
    path_step = path_step or step
    if os.getcwd() != ROOT:
        raise Stop("CHECKOUT_UNSUPPORTED", path_step)
    root = _components(ROOT, path_step)
    common = _components(COMMON, path_step)
    if root is None or common is None or not stat.S_ISDIR(root.st_mode) or not stat.S_ISDIR(common.st_mode):
        raise Stop("CHECKOUT_UNSUPPORTED", path_step)
    if data["schema_version"] == "yini-readonly-preflight/contract-v3":
        _worktree_absent(path_step, first is not None)
    total = 0
    identities = [(_identity(root), _identity(common)), _storage(path_step)]
    items = [(COMMON + "/index", data["index_sha256"], None, False),
             (COMMON + "/config", data["config_sha256"], None, False),
             (data["git"]["path"], data["git"]["sha256"], None, True)]
    items.extend((ROOT + "/" + row["path"], row["sha256"], int(row["mode"], 8), False)
                 for row in data["delta"])
    for candidate, _expected, _mode, executable in items:
        try:
            info = _components(candidate, path_step)
        except Stop as error:
            if (first is not None and data["schema_version"] == "yini-readonly-preflight/contract-v3"
                    and candidate == COMMON + "/config" and error.reason == "PATH_UNSAFE"):
                raise Stop("OBSERVATION_DRIFT", path_step) from None
            raise
        if info is None or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            if first is not None:
                raise Stop("OBSERVATION_DRIFT", path_step)
            raise Stop("TOOL_IDENTITY_MISMATCH" if executable else "OBSERVATION_MISMATCH", path_step)
    for name in data["absent"]:
        if _components(ROOT + "/" + name, path_step) is not None:
            reason = "OBSERVATION_MISMATCH" if first is None else "OBSERVATION_DRIFT"
            raise Stop(reason, path_step)
    for candidate, expected, mode, executable in items:
        try:
            digest, length, identity, actual_mode = _read_regular(candidate, step, SCAN_LIMIT - total, executable)
        except Stop as error:
            if first is not None and (error.reason in ("OBSERVATION_MISMATCH", "TOOL_IDENTITY_MISMATCH")
                                      or (data["schema_version"] == "yini-readonly-preflight/contract-v3"
                                          and candidate == COMMON + "/config" and error.reason == "PATH_UNSAFE")):
                raise Stop("OBSERVATION_DRIFT", step) from None
            raise
        total += length
        if digest != expected or (mode is not None and mode != actual_mode):
            reason = ("TOOL_IDENTITY_MISMATCH" if executable and first is None else
                      "OBSERVATION_MISMATCH" if first is None else "OBSERVATION_DRIFT")
            raise Stop(reason, step)
        identities.append(identity)
    if first is not None and identities != first:
        raise Stop("OBSERVATION_DRIFT", step)
    return identities


def _run(data, result, step, suffix, stdout_limit=CAPTURE_LIMIT, retain=True):
    captures = [{"hash": hashlib.sha256(), "length": 0, "data": bytearray()},
                {"hash": hashlib.sha256(), "length": 0, "data": bytearray()}]
    record = {"step": step, "returncode": None, "stdout_sha256": None,
              "stderr_sha256": None, "stdout_bytes": 0, "stderr_bytes": 0, "complete": False}
    child = None
    failure = None
    deadline = time.monotonic() + PROCESS_SECONDS
    try:
        try:
            child = subprocess.Popen((data["git"]["path"],) + GIT_PREFIX + suffix,
                                     stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell=False, cwd=ROOT, env=ENV)
        except OSError:
            raise Stop("PROCESS_LAUNCH_ERROR", step) from None
        with selectors.DefaultSelector() as selector:
            selector.register(child.stdout, selectors.EVENT_READ, 0)
            selector.register(child.stderr, selectors.EVENT_READ, 1)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise Stop("TIMEOUT", step)
                ready = selector.select(remaining)
                if not ready:
                    raise Stop("TIMEOUT", step)
                for key, _mask in ready:
                    capture = captures[key.data]
                    limit = stdout_limit if key.data == 0 else CAPTURE_LIMIT
                    chunk = os.read(key.fd, min(65536, limit + 1 - capture["length"]))
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    capture["hash"].update(chunk)
                    capture["length"] += len(chunk)
                    if key.data == 0 and retain:
                        capture["data"].extend(chunk)
                    if capture["length"] > limit:
                        raise Stop("CAPTURE_LIMIT", step)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise Stop("TIMEOUT", step)
        try:
            returncode = child.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            raise Stop("TIMEOUT", step) from None
        if type(returncode) is not int or not -255 <= returncode <= 255:
            raise Stop("INTERNAL_DEFECT", step)
        record.update(returncode=returncode, complete=True)
        if returncode:
            code = min(255, 128 - returncode) if returncode < 0 else returncode
            raise Stop("GIT_EXIT", step, returncode, code)
    except Stop as error:
        failure = error
    except Exception:
        failure = Stop("INTERNAL_DEFECT", step)
    finally:
        if child is not None:
            if failure is not None and not record["complete"]:
                _terminate(child)
            for stream in (child.stdout, child.stderr):
                try:
                    stream.close()
                except Exception:
                    if failure is None:
                        failure = Stop("INTERNAL_DEFECT", step)
                        record["complete"] = False
        for index, name in enumerate(("stdout", "stderr")):
            record[name + "_sha256"] = captures[index]["hash"].hexdigest()
            record[name + "_bytes"] = captures[index]["length"]
        result["observations"].append(record)
    if failure is not None:
        raise failure
    if retain:
        return bytes(captures[0]["data"])
    return record["stdout_sha256"], record["stdout_bytes"]


def _terminate(child):
    # Cleanup faults cannot overwrite the first capture/process failure.
    try:
        child.kill()
    except Exception:
        pass
    try:
        child.wait(timeout=PROCESS_SECONDS)
    except Exception:
        pass


PROBES = (
    ("root", ("rev-parse", "--show-toplevel")),
    ("common", ("rev-parse", "--path-format=absolute", "--git-common-dir")),
    ("branch", ("symbolic-ref", "--quiet", "--short", "HEAD")),
    ("head", ("rev-parse", "--verify", "HEAD^{commit}")),
    ("config", ("config", "--local", "--no-includes", "--null", "--name-only", "--list")),
    ("shared", ("rev-parse", "--shared-index-path")),
    ("entries", ("ls-files", "--stage", "-v", "--sparse", "-z")),
    ("status", ("status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=none")),
    ("staged", ("diff", "--cached", "--raw", "-z", "--no-abbrev", "--no-renames",
                "--no-ext-diff", "--no-textconv", "--ignore-submodules=none", "HEAD", "--")),
)


def _canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def _nul_records(raw):
    if raw and not raw.endswith(b"\0"):
        raise ValueError("missing terminal NUL")
    return raw[:-1].split(b"\0") if raw else []


def _metadata_path(name):
    return (bool(name) and not name.startswith("/") and "\\" not in name
            and all(part not in ("", ".", "..") for part in name.split("/"))
            and not any(unicodedata.category(char) == "Cc" for char in name))


def _entries(raw, step):
    records = _nul_records(raw)
    if len(records) > 8192:
        raise Stop("STATE_UNSUPPORTED", step)
    rows = {}
    normalized_names = set()
    for record in records:
        header, name = record.split(b"\t", 1)
        fields = header.decode("ascii").split(" ")
        if len(fields) != 4 or len(fields[0]) != 1 or not re.fullmatch(r"[0-7]{6}", fields[1]):
            raise ValueError("invalid index header")
        tag, mode, oid, stage = fields
        if not _is_hex(oid, HEX40) or stage not in ("0", "1", "2", "3"):
            raise ValueError("invalid index identity")
        if tag != "H" or stage != "0" or mode not in ("100644", "100755") or not _oid(oid):
            raise Stop("STATE_UNSUPPORTED", step)
        name = name.decode("utf-8")
        normalized = unicodedata.normalize("NFC", name)
        if not _metadata_path(name) or normalized in normalized_names:
            raise ValueError("invalid or duplicate index path")
        normalized_names.add(normalized)
        rows[name] = {"path": name, "mode": mode, "oid": oid}
    return rows


def _status_map(raw, step):
    observed = {}
    for record in _nul_records(raw):
        if len(record) < 4 or record[2:3] != b" ":
            raise ValueError("invalid status")
        xy = record[:2].decode("ascii")
        if xy not in (" M", "??", "M ", "MM", "A ", "AM"):
            raise Stop("STATE_UNSUPPORTED", step)
        name = record[3:].decode("utf-8")
        if not _safe_path(name) or name in observed:
            raise ValueError("invalid or duplicate status path")
        observed[name] = xy
    return observed


def _staged_map(raw, step):
    records = _nul_records(raw)
    if len(records) % 2:
        raise ValueError("invalid raw diff framing")
    rows = {}
    for offset in range(0, len(records), 2):
        header = records[offset].decode("ascii")
        match = re.fullmatch(r":([0-7]{6}) ([0-7]{6}) ([0-9a-f]{40}) ([0-9a-f]{40}) ([A-Z][0-9]*)", header)
        if match is None:
            raise ValueError("invalid raw diff header")
        old_mode, mode, old_oid, oid, change = match.groups()
        if change not in ("A", "M") or mode not in ("100644", "100755"):
            raise Stop("STATE_UNSUPPORTED", step)
        if ((change == "A" and (old_mode != "000000" or old_oid != "0" * 40))
                or (change == "M" and (old_mode not in ("100644", "100755") or not _oid(old_oid)))
                or not _oid(oid) or (old_mode, old_oid) == (mode, oid)):
            raise Stop("STATE_UNSUPPORTED", step)
        name = records[offset + 1].decode("utf-8")
        if not _safe_path(name) or name in rows:
            raise ValueError("invalid or duplicate staged path")
        rows[name] = {"path": name, "change": change, "head_mode": old_mode, "head_oid": old_oid,
                      "index_mode": mode, "index_oid": oid}
    return rows


def _config_names(raw, step, v3=False):
    names = []
    for record in _nul_records(raw):
        name = record.decode("utf-8")
        if not name or "." not in name or any(ord(char) < 32 or ord(char) == 127 for char in name):
            raise ValueError("malformed config name")
        normalized = name.lower()
        if (normalized.startswith(("include.", "includeif.", "filter."))
                or (normalized.startswith("extensions.")
                    and not (v3 and normalized == "extensions.worktreeconfig"))
                or (normalized.startswith("remote.") and normalized.endswith((".promisor", ".partialclonefilter")))
                or normalized in ("core.sparsecheckout", "core.sparsecheckoutcone", "core.splitindex", "core.worktree")):
            raise Stop("STATE_UNSUPPORTED", step)
        names.append(name)
    return names


def _config_guard(data, initial, step):
    # Two config-only FILE_LIMIT scans plus three full SCAN_LIMIT scans:
    # fixed aggregate ceiling 224 MiB. No index/worktree/tool rescan here.
    _worktree_absent(step, later=True)
    try:
        digest, _length, identity, _mode = _read_regular(COMMON + "/config", step, FILE_LIMIT)
    except Stop as error:
        if error.reason in ("PATH_UNSAFE", "OBSERVATION_MISMATCH"):
            raise Stop("OBSERVATION_DRIFT", step) from None
        raise
    _worktree_absent(step, later=True)
    if digest != data["config_sha256"] or identity != initial[3]:
        raise Stop("OBSERVATION_DRIFT", step)


def _configuration(data, result, phase, initial, before):
    mismatch = "OBSERVATION_MISMATCH" if phase == "before" else "OBSERVATION_DRIFT"
    step = phase + ".config.names"
    prefix = ("config", "--file", COMMON + "/config", "--no-includes")
    raw = _run(data, result, step, prefix + ("--null", "--name-only", "--list"))
    try:
        names = sorted(_config_names(raw, step, v3=True))
    except (ValueError, UnicodeError):
        raise Stop("OBSERVATION_MISMATCH", step) from None
    lowered = [name.lower() for name in names]
    if lowered.count("core.repositoryformatversion") != 1 or lowered.count("extensions.worktreeconfig") > 1:
        raise Stop("STATE_UNSUPPORTED", step)
    if before is not None and names != before["config"]:
        raise Stop("OBSERVATION_DRIFT", step)
    present = "extensions.worktreeconfig" in lowered
    if present != (data["extension_worktree_config"] is not None):
        raise Stop(mismatch, step)
    step = phase + ".config.format"
    raw = _run(data, result, step, prefix + ("--type=int", "--get-all", "core.repositoryformatversion"))
    if raw != b"0\n":
        if re.fullmatch(rb"-?[1-9][0-9]*\n", raw):
            raise Stop("STATE_UNSUPPORTED", step)
        raise Stop("OBSERVATION_MISMATCH", step)
    extension = None
    if present:
        step = phase + ".config.worktree"
        raw = _run(data, result, step, prefix + ("--type=bool", "--get-all", "extensions.worktreeConfig"))
        if raw not in (b"true\n", b"false\n"):
            raise Stop("OBSERVATION_MISMATCH", step)
        extension = raw == b"true\n"
        if extension is not data["extension_worktree_config"]:
            raise Stop(mismatch, step)
    _config_guard(data, initial, phase + ".config.guard")
    return {"config": names, "format": 0, "worktree": extension}


def _observation(data, result, phase, initial=None, before=None):
    mismatch = "OBSERVATION_MISMATCH" if phase == "before" else "OBSERVATION_DRIFT"
    maps = {}
    probes = PROBES
    if data["schema_version"] == "yini-readonly-preflight/contract-v3":
        maps = _configuration(data, result, phase, initial, before)
        probes = tuple(probe for probe in PROBES if probe[0] != "config")
    for label, suffix in probes:
        step = phase + "." + label
        raw = _run(data, result, step, suffix,
                   stdout_limit=2 * 1024 * 1024 if label == "entries" else CAPTURE_LIMIT)
        expected = {"root": data["root"], "common": data["common_dir"],
                    "branch": data["branch"], "head": data["head"]}
        try:
            if label in expected:
                if raw != (expected[label] + "\n").encode("utf-8"):
                    raise Stop(mismatch, step)
            elif label == "shared":
                if raw:
                    raise Stop("STATE_UNSUPPORTED", step)
            elif label == "config":
                maps[label] = sorted(_config_names(raw, step))
            elif label == "entries":
                rows = _entries(raw, step)
                ordered = sorted(rows.values(), key=lambda row: row["path"].encode("utf-8"))
                if hashlib.sha256(_canonical(ordered)).hexdigest() != data["index_tree_sha256"]:
                    raise Stop(mismatch, step)
                for staged in data["staged"]:
                    if rows.get(staged["path"]) != {"path": staged["path"], "mode": staged["index_mode"], "oid": staged["index_oid"]}:
                        raise Stop(mismatch, step)
                maps[label] = rows
            elif label == "status":
                rows = _status_map(raw, step)
                if rows != {row["path"]: row["xy"] for row in data["delta"]}:
                    raise Stop(mismatch, step)
                maps[label] = rows
            else:
                rows = _staged_map(raw, step)
                expected_rows = {row["path"]: {key: value for key, value in row.items() if key != "blob_sha256"}
                                 for row in data["staged"]}
                if rows != expected_rows:
                    raise Stop(mismatch, step)
                maps[label] = rows
        except (ValueError, UnicodeError):
            raise Stop("OBSERVATION_MISMATCH", step) from None
    total_blob = 0
    for number, row in enumerate(data["staged"]):
        step = phase + ".blob." + format(number, "03d")
        digest, length = _run(data, result, step, ("cat-file", "blob", row["index_oid"]),
                              stdout_limit=min(FILE_LIMIT, SCAN_LIMIT - total_blob), retain=False)
        total_blob += length
        if digest != row["blob_sha256"]:
            raise Stop(mismatch, step)
    return maps


def verify(contract_bytes: bytes, expected_sha256: str) -> dict:
    complete = isinstance(contract_bytes, bytes) and len(contract_bytes) <= INPUT_LIMIT
    result = _result(hashlib.sha256(contract_bytes).hexdigest() if complete else None)
    try:
        data, _digest = _schema(contract_bytes, expected_sha256, result)
        result["work_unit_id"] = data["work_unit_id"]
        _environment()
        initial = _scan(data, "before.index", path_step="paths")
        before = _observation(data, result, "before", initial)
        _environment()
        _scan(data, "after.index", initial, path_step="after.paths")
        after = _observation(data, result, "after", initial, before)
        if after != before:
            raise Stop("OBSERVATION_DRIFT", "after.staged")
        _environment()
        _scan(data, "final.files", initial)
        fingerprint_keys = ("root", "common_dir", "branch", "head", "index_sha256",
                            "config_sha256", "index_tree_sha256", "state_kind", "staged", "delta", "absent")
        count = 18 + 2 * len(data["staged"])
        if data["schema_version"] == "yini-readonly-preflight/contract-v3":
            fingerprint_keys += ("repository_format_version", "extension_worktree_config", "config_worktree")
            count = 20 + 2 * (data["extension_worktree_config"] is not None) + 2 * len(data["staged"])
        result.update(outcome="MATCH", reason="MATCH", exit_code=0,
                      fingerprint={key: data[key] for key in fingerprint_keys})
        if len(_canonical(result)) > INPUT_LIMIT:
            raise Stop("INTERNAL_DEFECT", "result")
        if len(result["observations"]) != count:
            raise Stop("INTERNAL_DEFECT", "result")
        return result
    except Stop as error:
        return _stop(result, error)
    except Exception:
        return _stop(result, Stop("INTERNAL_DEFECT", "result"))


def main(argv: list[str]) -> int:
    result = _result()
    if (not isinstance(argv, list) or len(argv) != 3 or argv[0] != "verify"
            or argv[1] != "--contract-sha256" or not _is_hex(argv[2], HEX64)):
        result = _stop(result, Stop("INVALID_INPUT", "input"))
    else:
        try:
            raw = sys.stdin.buffer.read(INPUT_LIMIT + 1)
            result = verify(raw, argv[2])
        except Exception:
            result = _stop(result, Stop("INTERNAL_DEFECT", "input"))
    try:
        output = _canonical(result)
        if len(output) > INPUT_LIMIT:
            result = _stop(result, Stop("INTERNAL_DEFECT", "result"))
            output = _canonical(result)
        if len(output) > INPUT_LIMIT:
            return 70
        sys.stdout.write(output.decode("ascii"))
        sys.stdout.flush()
    except (OSError, UnicodeError):
        return 70
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
