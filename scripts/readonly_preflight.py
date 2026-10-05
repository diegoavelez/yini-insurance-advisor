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
FIELDS = {"schema_version", "work_unit_id", "repository_id", "root", "common_dir", "branch", "head", "index_sha256", "staged", "delta", "absent", "ignored_inputs", "git"}
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
        "schema_version": "yini-readonly-preflight/result-v1",
        "work_unit_id": None, "contract_sha256": raw_hash,
        "outcome": "STOP", "reason": "INTERNAL_DEFECT", "exit_code": 70,
        "failed_step": None, "child_returncode": None, "observations": [],
        "fingerprint": None, "successor_authority": False,
    }


def _stop(result, error):
    result["reason"] = error.reason
    result["failed_step"] = error.step
    result["child_returncode"] = error.child
    result["exit_code"] = error.code if error.code is not None else {
        "INVALID_INPUT": 2, "CONTRACT_HASH_MISMATCH": 2,
        "CONTRACT_INVALID": 2, "PATH_UNSAFE": 2,
        "ENVIRONMENT_UNSUPPORTED": 4, "CHECKOUT_UNSUPPORTED": 4,
        "TOOL_IDENTITY_MISMATCH": 4, "OBSERVATION_MISMATCH": 3,
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


def _schema(raw, expected):
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
    if not isinstance(data, dict) or set(data) != FIELDS:
        raise Stop("CONTRACT_INVALID", "input")
    checks = (
        data["schema_version"] == "yini-readonly-preflight/contract-v1",
        isinstance(data["work_unit_id"], str) and ID.fullmatch(data["work_unit_id"]) is not None,
        data["repository_id"] == "yini-insurance-advisor",
        data["root"] == ROOT, data["common_dir"] == COMMON,
        data["branch"] == "main", _is_hex(data["head"], HEX40),
        _is_hex(data["index_sha256"], HEX64),
        isinstance(data["staged"], list) and data["staged"] == [],
        isinstance(data["delta"], list) and len(data["delta"]) <= 128,
        isinstance(data["absent"], list) and len(data["absent"]) <= 128,
        data["ignored_inputs"] == "none",
        isinstance(data["git"], dict) and set(data["git"]) == {"path", "sha256"},
    )
    if not all(checks):
        raise Stop("CONTRACT_INVALID", "input")
    git = data["git"]
    if not isinstance(git["path"], str) or not git["path"].startswith("/") or not _is_hex(git["sha256"], HEX64):
        raise Stop("CONTRACT_INVALID", "input")
    paths = []
    for row in data["delta"]:
        if not isinstance(row, dict) or set(row) != ROW_FIELDS:
            raise Stop("CONTRACT_INVALID", "input")
        if row["xy"] not in (" M", "??") or row["kind"] != "regular" or row["mode"] not in ("644", "755") or not _is_hex(row["sha256"], HEX64):
            raise Stop("CONTRACT_INVALID", "input")
        paths.append(row["path"])
    paths.extend(data["absent"])
    if not all(_safe_path(value) for value in paths):
        raise Stop("PATH_UNSAFE", "input")
    for group in ([row["path"] for row in data["delta"]], data["absent"]):
        if group != sorted(set(group), key=lambda item: item.encode("utf-8")):
            raise Stop("CONTRACT_INVALID", "input")
    if len(set(paths)) != len(paths):
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


def _scan(data, step, first=None, path_step=None):
    path_step = path_step or step
    if os.getcwd() != ROOT:
        raise Stop("CHECKOUT_UNSUPPORTED", path_step)
    root = _components(ROOT, path_step)
    common = _components(COMMON, path_step)
    if root is None or common is None or not stat.S_ISDIR(root.st_mode) or not stat.S_ISDIR(common.st_mode):
        raise Stop("CHECKOUT_UNSUPPORTED", path_step)
    total = 0
    identities = []
    items = [(COMMON + "/index", data["index_sha256"], None, False),
             (data["git"]["path"], data["git"]["sha256"], None, True)]
    items.extend((ROOT + "/" + row["path"], row["sha256"], int(row["mode"], 8), False)
                 for row in data["delta"])
    for candidate, _expected, _mode, executable in items:
        info = _components(candidate, path_step)
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
            if first is not None and error.reason in ("OBSERVATION_MISMATCH", "TOOL_IDENTITY_MISMATCH"):
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


def _run(data, result, step, suffix):
    try:
        child = subprocess.Popen((data["git"]["path"],) + GIT_PREFIX + suffix,
                                 stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=False, cwd=ROOT, env=ENV)
    except OSError:
        result["observations"].append(_process_record(step, None, b"", b"", False))
        raise Stop("PROCESS_LAUNCH_ERROR", step) from None
    output = [bytearray(), bytearray()]
    reason = None
    deadline = time.monotonic() + PROCESS_SECONDS
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(child.stdout, selectors.EVENT_READ, 0)
            selector.register(child.stderr, selectors.EVENT_READ, 1)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    reason = "TIMEOUT"
                    break
                ready = selector.select(remaining)
                if not ready:
                    reason = "TIMEOUT"
                    break
                for key, _mask in ready:
                    stream = output[key.data]
                    chunk = os.read(key.fd, min(65536, CAPTURE_LIMIT + 1 - len(stream)))
                    if not chunk:
                        selector.unregister(key.fileobj)
                    else:
                        stream.extend(chunk)
                        if len(stream) > CAPTURE_LIMIT:
                            reason = "CAPTURE_LIMIT"
                            break
                if reason:
                    break
        if reason:
            result["observations"].append(_process_record(step, None, output[0], output[1], False))
            _terminate(child, step)
            raise Stop(reason, step)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            result["observations"].append(_process_record(step, None, output[0], output[1], False))
            _terminate(child, step)
            raise Stop("TIMEOUT", step)
        returncode = child.wait(timeout=remaining)
        result["observations"].append(_process_record(step, returncode, output[0], output[1], True))
        if returncode:
            code = min(255, 128 - returncode) if returncode < 0 else returncode
            raise Stop("GIT_EXIT", step, returncode, code)
        return bytes(output[0])
    except subprocess.TimeoutExpired:
        result["observations"].append(_process_record(step, None, output[0], output[1], False))
        _terminate(child, step)
        raise Stop("TIMEOUT", step) from None
    except OSError:
        result["observations"].append(_process_record(step, None, output[0], output[1], False))
        _terminate(child, step)
        raise Stop("INTERNAL_DEFECT", step) from None
    finally:
        child.stdout.close()
        child.stderr.close()


def _terminate(child, step):
    failed = False
    try:
        child.kill()
    except ProcessLookupError:
        pass
    except OSError:
        failed = True
    try:
        child.wait(timeout=PROCESS_SECONDS)
    except (subprocess.TimeoutExpired, OSError):
        failed = True
    if failed:
        raise Stop("INTERNAL_DEFECT", step) from None


def _process_record(step, returncode, stdout, stderr, complete):
    return {"step": step, "returncode": returncode,
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "stdout_bytes": len(stdout), "stderr_bytes": len(stderr), "complete": complete}


PROBES = (
    ("root", ("rev-parse", "--show-toplevel")),
    ("common", ("rev-parse", "--path-format=absolute", "--git-common-dir")),
    ("branch", ("symbolic-ref", "--quiet", "--short", "HEAD")),
    ("head", ("rev-parse", "HEAD")),
    ("status", ("status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=all")),
    ("staged", ("diff", "--cached", "--name-status", "-z", "--no-ext-diff", "--no-textconv", "--ignore-submodules=none")),
)


def _status_map(raw):
    if raw and not raw.endswith(b"\0"):
        raise ValueError("unterminated status")
    records = raw[:-1].split(b"\0") if raw else []
    observed = {}
    for record in records:
        if len(record) < 4 or record[2:3] != b" " or record[:2] not in (b" M", b"??"):
            raise ValueError("unsupported status")
        name = record[3:].decode("utf-8")
        if not _safe_path(name) or name in observed:
            raise ValueError("unsafe or duplicate status path")
        observed[name] = record[:2].decode("ascii")
    return observed


def _observation(data, result, phase):
    for label, suffix in PROBES:
        step = phase + "." + label
        raw = _run(data, result, step, suffix)
        expected = {
            "root": data["root"], "common": data["common_dir"],
            "branch": data["branch"], "head": data["head"],
        }
        if label in expected:
            if raw != (expected[label] + "\n").encode("utf-8"):
                raise Stop("OBSERVATION_MISMATCH" if phase == "before" else "OBSERVATION_DRIFT", step)
        elif label == "staged":
            if raw:
                raise Stop("OBSERVATION_MISMATCH" if phase == "before" else "OBSERVATION_DRIFT", step)
        else:
            try:
                actual = _status_map(raw)
            except (ValueError, UnicodeError):
                raise Stop("OBSERVATION_MISMATCH", step) from None
            expected_map = {row["path"]: row["xy"] for row in data["delta"]}
            if actual != expected_map:
                raise Stop("OBSERVATION_MISMATCH" if phase == "before" else "OBSERVATION_DRIFT", step)


def verify(contract_bytes: bytes, expected_sha256: str) -> dict:
    complete = isinstance(contract_bytes, bytes) and len(contract_bytes) <= INPUT_LIMIT
    result = _result(hashlib.sha256(contract_bytes).hexdigest() if complete else None)
    try:
        data, _digest = _schema(contract_bytes, expected_sha256)
        result["work_unit_id"] = data["work_unit_id"]
        _environment()
        initial = _scan(data, "before.index", path_step="paths")
        _observation(data, result, "before")
        _environment()
        _scan(data, "after.index", initial, path_step="after.paths")
        _observation(data, result, "after")
        _environment()
        _scan(data, "final.files", initial)
        result["outcome"] = "MATCH"
        result["reason"] = "MATCH"
        result["exit_code"] = 0
        result["fingerprint"] = {key: data[key] for key in
                                 ("root", "common_dir", "branch", "head", "index_sha256", "delta", "absent")}
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
        sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")
        sys.stdout.flush()
    except (OSError, UnicodeError):
        return 70
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
