"""Independent public-seam oracles; invented filesystem and process fixtures."""

import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import tracemalloc
import unittest
from unittest import mock

SOURCE = Path(__file__).resolve().parents[1] / "scripts/staged_readonly_preflight.py"
module_spec = importlib.util.spec_from_file_location("staged_preflight", SOURCE)
observer = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(observer)
ROOT = "/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor"
ABC = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def contract(**changes):
    value = dict(schema_version="yini-readonly-preflight/contract-v2",
                 work_unit_id="TEST-V2", repository_id="yini-insurance-advisor",
                 root=ROOT, common_dir=ROOT + "/.git", branch="main", head="a" * 40,
                 index_sha256=ABC, config_sha256=ABC, index_tree_sha256="c" * 64,
                 state_kind="empty_staged", staged=[], delta=[], absent=[],
                 ignored_inputs="none", git={"path": "/usr/bin/git", "sha256": ABC})
    value.update(changes)
    return value


def staged_row(**changes):
    row = dict(path="docs/case.txt", change="M", head_mode="100644", head_oid="b" * 40,
               index_mode="100644", index_oid="c" * 40, blob_sha256=ABC)
    row.update(changes)
    return row


def delta_row(**changes):
    row = dict(path="docs/case.txt", xy="M ", kind="regular", mode="644", sha256=ABC)
    row.update(changes)
    return row


def checked(value):
    raw = value if isinstance(value, bytes) else encode(value)
    return observer.verify(raw, hashlib.sha256(raw).hexdigest())


def v3_contract(value=None, extension=True):
    value = copy.deepcopy(contract() if value is None else value)
    value.update(schema_version="yini-readonly-preflight/contract-v3",
                 repository_format_version=0, extension_worktree_config=extension,
                 config_worktree={"state": "absent"})
    return value


def public_call(value, seam, entry=observer):
    raw = value if isinstance(value, bytes) else encode(value)
    digest = hashlib.sha256(raw).hexdigest()
    if seam == "verify":
        result = entry.verify(raw, digest)
        return result, encode(result), result["exit_code"]
    output = io.StringIO()
    with mock.patch.object(sys, "stdin", io.TextIOWrapper(io.BytesIO(raw))), \
            mock.patch.object(sys, "stdout", output):
        code = entry.main(["verify", "--contract-sha256", digest])
    delivered = output.getvalue().encode("ascii")
    return json.loads(delivered), delivered, code


class V3InputTests(unittest.TestCase):
    def test_v3_input_environment_and_cli_guards_at_both_seams(self):
        for seam in ("verify", "main"):
            for value, reason in ((b"x" * 262145, "INVALID_INPUT"), (b"\xef\xbb\xbf{}", "INVALID_INPUT"),
                                  (b"\xff", "INVALID_INPUT"), (b'{"x":NaN}', "INVALID_INPUT"),
                                  (dict(v3_contract(), absent=[".git/config.worktree"]), "PATH_UNSAFE")):
                with self.subTest(seam=seam, reason=reason), mock.patch("subprocess.Popen") as popen:
                    result, _, code = public_call(value, seam)
                    self.assertEqual((result["reason"], result["failed_step"], code), (reason, "input", 2))
                    popen.assert_not_called()
            for name in ("GIT_INDEX_FILE", "GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_COUNT", "GIT_PAGER"):
                with self.subTest(seam=seam, name=name), mock.patch.dict(os.environ, {name: "invented"}, clear=True), mock.patch("subprocess.Popen") as popen:
                    result, _, code = public_call(v3_contract(), seam)
                    self.assertEqual((result["reason"], result["failed_step"], code), ("ENVIRONMENT_UNSUPPORTED", "environment", 4))
                    popen.assert_not_called()
            with mock.patch.object(sys, "dont_write_bytecode", False), mock.patch.dict(os.environ, {}, clear=True), mock.patch("subprocess.Popen") as popen:
                result, _, code = public_call(v3_contract(), seam)
                self.assertEqual((result["reason"], code), ("ENVIRONMENT_UNSUPPORTED", 4))
                popen.assert_not_called()
        for argv in (["add"], ["verify", "--contract-sha256", ABC, "--contract-sha256", ABC],
                     ["verify", "--contract-sha256", "$(git add .)"]):
            output = io.StringIO()
            with mock.patch.object(sys, "stdout", output), mock.patch("subprocess.Popen") as popen:
                self.assertEqual(observer.main(argv), 2)
            self.assertEqual(json.loads(output.getvalue())["reason"], "INVALID_INPUT")
            popen.assert_not_called()

    def test_v3_valid_schema_reaches_environment_at_both_seams(self):
        for seam in ("verify", "main"):
            with self.subTest(seam=seam), mock.patch.dict(os.environ, {"GIT_INDEX_FILE": "invented"}, clear=True), \
                    mock.patch("subprocess.Popen") as popen:
                result, delivered, code = public_call(v3_contract(), seam)
                self.assertEqual((result["schema_version"], result["reason"], result["failed_step"], code),
                                 ("yini-readonly-preflight/result-v3", "ENVIRONMENT_UNSUPPORTED", "environment", 4))
                self.assertEqual(delivered, encode(result))
                self.assertIsNone(result["fingerprint"])
                self.assertIs(result["successor_authority"], False)
                popen.assert_not_called()

    def test_v3_closed_fields_and_duplicate_json_reject_before_process(self):
        cases = []
        for key in ("repository_format_version", "extension_worktree_config", "config_worktree"):
            value = v3_contract()
            del value[key]
            cases.append((value, "CONTRACT_INVALID"))
        for value in (True, False, 0.0, "0", 1, None):
            cases.append((dict(v3_contract(), repository_format_version=value), "CONTRACT_INVALID"))
        for value in (0, 1, "true", "false", [], {}):
            cases.append((dict(v3_contract(), extension_worktree_config=value), "CONTRACT_INVALID"))
        for value in ({"state": "present"}, {"state": "absent", "sha256": ABC}, {}, None, "absent"):
            cases.append((dict(v3_contract(), config_worktree=value), "CONTRACT_INVALID"))
        cases += [(dict(v3_contract(), extra=True), "CONTRACT_INVALID"),
                  (dict(v3_contract(), schema_version="yini-readonly-preflight/result-v3"), "CONTRACT_INVALID"),
                  (dict(v3_contract(), schema_version="yini-readonly-preflight/contract-v2"), "CONTRACT_INVALID")]
        raw = encode(v3_contract())
        for old, new in ((b'"state":"absent"', b'"state":"absent","state":"absent"'),
                         (b'"repository_format_version":0', b'"repository_format_version":0,"repository_format_version":0'),
                         (b'"path":"/usr/bin/git"', b'"path":"/usr/bin/git","path":"/usr/bin/git"')):
            cases.append((raw.replace(old, new), "INVALID_INPUT"))
        for seam in ("verify", "main"):
            for value, reason in cases:
                with self.subTest(seam=seam, reason=reason, value=value), mock.patch("subprocess.Popen") as popen:
                    result, delivered, code = public_call(value, seam)
                    self.assertEqual((result["reason"], result["failed_step"], code), (reason, "input", 2))
                    self.assertEqual(delivered, encode(result))
                    self.assertIsNone(result["fingerprint"])
                    popen.assert_not_called()


class Isolated(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {}, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)


class InputTests(Isolated):
    def test_closed_v2_and_json_reject_before_process(self):
        missing = contract()
        del missing["config_sha256"]
        cases = [(missing, "CONTRACT_INVALID"), (contract(extra=1), "CONTRACT_INVALID"),
                 (contract(schema_version="yini-readonly-preflight/contract-v1"), "CONTRACT_INVALID"),
                 (contract(delta=False), "CONTRACT_INVALID"), (contract(staged=True), "CONTRACT_INVALID"),
                 (contract(head="0" * 40), "CONTRACT_INVALID"),
                 (contract(git={"path": "/usr/bin/git", "sha256": ABC, "x": 1}), "CONTRACT_INVALID"),
                 (b'{}{}', "INVALID_INPUT"), (b'\xff', "INVALID_INPUT"),
                 (b'\xef\xbb\xbf{}', "INVALID_INPUT"), (b'{"x":1,"x":2}', "INVALID_INPUT"),
                 (b'{"x":NaN}', "INVALID_INPUT"), (b'x' * 262145, "INVALID_INPUT")]
        for value, reason in cases:
            with self.subTest(reason=reason), mock.patch("subprocess.Popen") as popen:
                result = checked(value)
                self.assertEqual((result.get("reason"), result.get("failed_step"), result.get("observations")),
                                 (reason, "input", []))
                self.assertIsNone(result["fingerprint"])
                self.assertIs(result["successor_authority"], False)
                popen.assert_not_called()

    def test_state_relationships_and_unsafe_paths_reject(self):
        base = contract(state_kind="staged_regular", staged=[staged_row()], delta=[delta_row()])
        cases = [contract(state_kind="unknown"), contract(state_kind="staged_regular"),
                 contract(staged=[staged_row()]), dict(base, staged=[staged_row(), staged_row()]),
                 dict(base, delta=[delta_row(xy=" M")]), dict(base, delta=[]),
                 dict(base, absent=["docs/case.txt"]), dict(base, staged=[staged_row(index_oid="c" * 7)]),
                 dict(base, staged=[staged_row(index_oid="0" * 40)]),
                 dict(base, staged=[staged_row(head_oid="c" * 40)]),
                 dict(base, staged=[staged_row(change="A")]),
                 dict(base, delta=[delta_row(xy="AM")]), contract(absent=["z", "a"]),
                 contract(delta=[delta_row(xy="R ")]), contract(delta=[delta_row(mode=True)])]
        for value in cases:
            with self.subTest(value=value), mock.patch("subprocess.Popen") as popen:
                self.assertEqual(checked(value).get("reason"), "CONTRACT_INVALID")
                popen.assert_not_called()
        for unsafe in ("/absolute", "a//b", "a/../b", "a/./b", "a\\b", ".git/index",
                       ".venv/x", "data/x", "corpus/x", ".env.local", "a;true", " x", "x ", "a\nb"):
            with self.subTest(unsafe=unsafe), mock.patch("subprocess.Popen") as popen:
                self.assertEqual(checked(contract(absent=[unsafe])).get("reason"), "PATH_UNSAFE")
                popen.assert_not_called()

    def test_raw_digest_and_cli_closed_result(self):
        raw = encode(contract())
        with mock.patch("subprocess.Popen") as popen:
            self.assertEqual(observer.verify(raw, "0" * 64).get("reason"), "CONTRACT_HASH_MISMATCH")
            self.assertEqual(observer.verify(raw + b" ", hashlib.sha256(raw).hexdigest()).get("reason"),
                             "CONTRACT_HASH_MISMATCH")
            expected = dict(schema_version="yini-readonly-preflight/result-v2", work_unit_id=None,
                            contract_sha256=None, outcome="STOP", reason="INVALID_INPUT", exit_code=2,
                            failed_step="input", child_returncode=None, observations=[], fingerprint=None,
                            successor_authority=False)
            for argv in (["add"], ["write-tree"], ["verify;true"],
                         ["verify", "--contract-sha256", "a" * 64, "--contract-sha256", "a" * 64],
                         ["verify", "--contract-sha256", "$(git add .)"]):
                output = io.StringIO()
                with mock.patch.object(sys, "stdout", output):
                    self.assertEqual(observer.main(list(argv)), 2)
                self.assertEqual(output.getvalue().encode(), encode(expected))
            popen.assert_not_called()


class PhysicalFixture:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".git/objects/info").mkdir(parents=True)
        (self.root / ".git/objects/pack").mkdir()
        (self.root / ".git/info").mkdir()
        (self.root / "docs").mkdir()
        for name in (".git/index", ".git/config", "docs/case.txt", "git-tool"):
            (self.root / name).write_bytes(b"abc")
        (self.root / "git-tool").chmod(0o755)
        self.original_lstat, self.original_open, self.original_scandir = os.lstat, os.open, os.scandir
        self.opened = []
        self.patches = [mock.patch("os.getcwd", return_value=ROOT),
                        mock.patch("os.lstat", side_effect=self.lstat),
                        mock.patch("os.open", side_effect=self.open),
                        mock.patch("os.scandir", side_effect=self.scandir)]
        for patcher in self.patches:
            patcher.start()
        return self

    def mapped(self, candidate):
        name = os.fspath(candidate)
        if name == "/usr/bin/git":
            return str(self.root / "git-tool")
        if name == ROOT or name.startswith(ROOT + "/"):
            return str(self.root) + name[len(ROOT):]
        return name

    def lstat(self, candidate, *args, **kwargs):
        return self.original_lstat(self.mapped(candidate), *args, **kwargs)

    def open(self, candidate, *args, **kwargs):
        self.opened.append(os.fspath(candidate))
        return self.original_open(self.mapped(candidate), *args, **kwargs)

    def scandir(self, candidate):
        return self.original_scandir(self.mapped(candidate))

    def __exit__(self, *args):
        for patcher in reversed(self.patches):
            patcher.stop()
        self.temp.cleanup()


class PipeProcess:
    def __init__(self, stdout=b"", stderr=b"", returncode=0, wait_error=None, kill_error=False):
        self.returncode, self.wait_error, self.kill_error = returncode, wait_error, kill_error
        self.killed, self.waits = False, 0
        self.writers = []
        streams = []
        for payload in (stdout, stderr):
            read_fd, write_fd = os.pipe()
            streams.append(os.fdopen(read_fd, "rb"))

            def write(fd=write_fd, value=payload):
                try:
                    offset = 0
                    while offset < len(value):
                        offset += os.write(fd, value[offset:offset + 65536])
                except BrokenPipeError:
                    pass
                finally:
                    os.close(fd)

            writer = threading.Thread(target=write, daemon=True)
            writer.start()
            self.writers.append(writer)
        self.stdout, self.stderr = streams

    def wait(self, timeout=None):
        self.waits += 1
        if self.wait_error and not self.killed:
            raise self.wait_error
        return self.returncode

    def kill(self):
        self.killed = True
        if self.kill_error:
            raise OSError("invented kill fault")


def positive_contract(xy="M ", mode_only=False):
    row = staged_row(blob_sha256="5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03")
    if xy[0] == "A":
        row.update(change="A", head_mode="000000", head_oid="0" * 40)
    if mode_only:
        row.update(index_mode="100755", index_oid=row["head_oid"])
    entries = [{"path": "docs/case.txt", "mode": row["index_mode"], "oid": row["index_oid"]}]
    return contract(state_kind="staged_regular", staged=[row], delta=[delta_row(xy=xy)],
                    index_tree_sha256=hashlib.sha256(encode(entries)).hexdigest())


def outputs(value):
    entries = [{"path": "docs/case.txt", "mode": "100644", "oid": "c" * 40}]
    if value["staged"]:
        entries = [{"path": row["path"], "mode": row["index_mode"], "oid": row["index_oid"]}
                   for row in value["staged"]]
    listing = b"".join(("H {mode} {oid} 0\t{path}\0".format(**row)).encode() for row in entries)
    status = b"".join((row["xy"] + " " + row["path"] + "\0").encode() for row in value["delta"])
    staged = b"".join((":" + row["head_mode"] + " " + row["index_mode"] + " "
                        + row["head_oid"] + " " + row["index_oid"] + " " + row["change"]
                        + "\0" + row["path"] + "\0").encode() for row in value["staged"])
    return [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(), b"main\n", b"a" * 40 + b"\n",
            b"core.repositoryformatversion\0core.filemode\0", b"", listing, status, staged] + [b"hello\n"] * len(value["staged"])


def invoke(value, streams=None, mutate=None):
    streams = outputs(value) * 2 if streams is None else streams
    launched = []

    def launch(argv, **options):
        launched.append((argv, options))
        if mutate:
            mutate(len(launched))
        return PipeProcess(stdout=streams[len(launched) - 1])

    with mock.patch("subprocess.Popen", side_effect=launch):
        result = checked(value)
    return result, launched


def invoke_seam(value, seam, streams=None, mutate=None, process=None):
    streams = outputs(value) * 2 if streams is None else streams
    launched = []

    def launch(argv, **options):
        launched.append((argv, options))
        if mutate:
            mutate(len(launched))
        if process is not None:
            return process
        payload = streams[len(launched) - 1]
        if isinstance(payload, tuple):
            return PipeProcess(stdout=payload[0], stderr=payload[1], returncode=payload[2])
        return PipeProcess(stdout=payload)

    with mock.patch("subprocess.Popen", side_effect=launch):
        result, delivered, code = public_call(value, seam)
    return result, launched, delivered, code


def v3_outputs(value):
    legacy = outputs(value)
    names = b"core.repositoryformatversion\0core.filemode\0"
    config = [names, b"0\n"]
    if value["extension_worktree_config"] is not None:
        config[0] += b"extensions.worktreeConfig\0"
        config.append(b"true\n" if value["extension_worktree_config"] else b"false\n")
    return config + legacy[:4] + legacy[5:]


def v3_steps(value):
    labels = ["config.names", "config.format"]
    if value["extension_worktree_config"] is not None:
        labels.append("config.worktree")
    labels += ["root", "common", "branch", "head", "shared", "entries", "status", "staged"]
    labels += ["blob.%03d" % number for number in range(len(value["staged"]))]
    return [phase + "." + label for phase in ("before", "after") for label in labels]


def v3_expected(value, streams):
    return dict(schema_version="yini-readonly-preflight/result-v3", work_unit_id=value["work_unit_id"],
                contract_sha256=hashlib.sha256(encode(value)).hexdigest(), outcome="MATCH", reason="MATCH", exit_code=0,
                failed_step=None, child_returncode=None, observations=[dict(step=step, returncode=0,
                    stdout_sha256=hashlib.sha256(raw).hexdigest(), stderr_sha256=EMPTY,
                    stdout_bytes=len(raw), stderr_bytes=0, complete=True) for step, raw in zip(v3_steps(value), streams)],
                fingerprint={key: value[key] for key in ("root", "common_dir", "branch", "head", "index_sha256",
                    "config_sha256", "index_tree_sha256", "state_kind", "staged", "delta", "absent",
                    "repository_format_version", "extension_worktree_config", "config_worktree")}, successor_authority=False)


class V3ObservationTests(Isolated):
    def test_v3_remaining_index_status_and_object_exclusions(self):
        value = v3_contract(positive_contract())
        baseline = v3_outputs(value) * 2
        cases = [(8, baseline[8] * 2, "OBSERVATION_MISMATCH"), (8, baseline[8][:-1], "OBSERVATION_MISMATCH"),
                 (9, b"?? extra.txt\0", "OBSERVATION_MISMATCH"), (10, b"", "OBSERVATION_MISMATCH"),
                 (7, b"shared-index\n", "STATE_UNSUPPORTED"), (11, b"wrong blob", "OBSERVATION_MISMATCH")]
        for stage in (b"1", b"2", b"3"):
            cases.append((8, baseline[8].replace(b" 0\t", b" " + stage + b"\t"), "STATE_UNSUPPORTED"))
        for tag in (b"h", b"S", b"s", b"M"):
            cases.append((8, tag + baseline[8][1:], "STATE_UNSUPPORTED"))
        for mode in (b"120000", b"160000", b"040000"):
            cases.append((8, baseline[8].replace(b"100644", mode), "STATE_UNSUPPORTED"))
        cases.append((8, baseline[8].replace(b"c" * 40, b"0" * 40), "STATE_UNSUPPORTED"))
        for xy in (b" D", b"D ", b"R ", b"C ", b"UU", b" A"):
            cases.append((9, xy + baseline[9][2:], "STATE_UNSUPPORTED"))
        for change in (b"D", b"R100", b"C100"):
            cases.append((10, baseline[10].replace(b" M\0", b" " + change + b"\0"), "STATE_UNSUPPORTED"))
        for seam in ("verify", "main"):
            for offset, payload, reason in cases:
                with self.subTest(seam=seam, offset=offset, reason=reason), PhysicalFixture() as fixture:
                    streams = baseline.copy()
                    streams[offset] = payload
                    result, launched, _, code = invoke_seam(value, seam, streams)
                    self.assertEqual((result["reason"], result["failed_step"], code, len(launched)),
                                     (reason, v3_steps(value)[offset], 4 if reason == "STATE_UNSUPPORTED" else 3, offset + 1))
                    self.assertNotIn(ROOT + "/extra.txt", fixture.opened)
                    self.assertIsNone(result["fingerprint"])

    def test_v3_unicode_metadata_and_normalized_collision_regressions(self):
        for seam in ("verify", "main"):
            for names in (("bad\x85name",), ("caf\u00e9", "cafe\u0301")):
                with self.subTest(seam=seam, names=names), PhysicalFixture() as fixture:
                    value = v3_contract(positive_contract())
                    rows = [{"path": "docs/case.txt", "mode": "100644", "oid": "c" * 40}]
                    rows += [{"path": name, "mode": "100644", "oid": "c" * 40} for name in names]
                    rows.sort(key=lambda row: row["path"].encode("utf-8"))
                    value["index_tree_sha256"] = hashlib.sha256(encode(rows)).hexdigest()
                    streams = v3_outputs(value) * 2
                    streams[8] = streams[20] = b"".join(("H {mode} {oid} 0\t{path}\0".format(**row)).encode() for row in rows)
                    result, launched, _, code = invoke_seam(value, seam, streams)
                    self.assertEqual((result["reason"], result["failed_step"], code, len(launched)),
                                     ("OBSERVATION_MISMATCH", "before.entries", 3, 9))
                    self.assertTrue(all(ROOT + "/" + name not in fixture.opened for name in names))

    def test_v3_legacy_v1_and_v2_exact_public_results_and_rejections(self):
        legacy_spec = importlib.util.spec_from_file_location("legacy_v1_w01", SOURCE.with_name("readonly_preflight.py"))
        legacy = importlib.util.module_from_spec(legacy_spec)
        legacy_spec.loader.exec_module(legacy)
        v1 = contract(schema_version="yini-readonly-preflight/contract-v1")
        for key in ("config_sha256", "index_tree_sha256", "state_kind"):
            del v1[key]
        v2 = positive_contract()
        for seam in ("verify", "main"):
            with self.subTest(seam=seam, version=1), PhysicalFixture():
                streams = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(), b"main\n", b"a" * 40 + b"\n", b"", b""] * 2
                steps = [phase + "." + name for phase in ("before", "after") for name in ("root", "common", "branch", "head", "status", "staged")]
                expected = dict(schema_version="yini-readonly-preflight/result-v1", work_unit_id="TEST-V2",
                    contract_sha256=hashlib.sha256(encode(v1)).hexdigest(), outcome="MATCH", reason="MATCH", exit_code=0,
                    failed_step=None, child_returncode=None, observations=[dict(step=step, returncode=0,
                        stdout_sha256=hashlib.sha256(raw).hexdigest(), stderr_sha256=EMPTY,
                        stdout_bytes=len(raw), stderr_bytes=0, complete=True) for step, raw in zip(steps, streams)],
                    fingerprint={key: v1[key] for key in ("root", "common_dir", "branch", "head", "index_sha256", "delta", "absent")}, successor_authority=False)
                launched = []
                def launch(*args, **kwargs):
                    launched.append(args)
                    return PipeProcess(stdout=streams[len(launched) - 1])
                with mock.patch("subprocess.Popen", side_effect=launch):
                    result, delivered, code = public_call(v1, seam, entry=legacy)
                self.assertEqual((result, delivered, code), (expected, encode(expected), 0))
                self.assertEqual(len(launched), 12)
            with self.subTest(seam=seam, version=2), PhysicalFixture():
                streams = outputs(v2) * 2
                steps = [phase + "." + name for phase in ("before", "after") for name in
                         ("root", "common", "branch", "head", "config", "shared", "entries", "status", "staged", "blob.000")]
                expected = dict(schema_version="yini-readonly-preflight/result-v2", work_unit_id="TEST-V2",
                    contract_sha256=hashlib.sha256(encode(v2)).hexdigest(), outcome="MATCH", reason="MATCH", exit_code=0,
                    failed_step=None, child_returncode=None, observations=[dict(step=step, returncode=0,
                        stdout_sha256=hashlib.sha256(raw).hexdigest(), stderr_sha256=EMPTY,
                        stdout_bytes=len(raw), stderr_bytes=0, complete=True) for step, raw in zip(steps, streams)],
                    fingerprint={key: v2[key] for key in ("root", "common_dir", "branch", "head", "index_sha256", "config_sha256",
                        "index_tree_sha256", "state_kind", "staged", "delta", "absent")}, successor_authority=False)
                result, launched, delivered, code = invoke_seam(v2, seam, streams)
                self.assertEqual((result, delivered, code), (expected, encode(expected), 0))
                self.assertEqual(len(launched), 20)
                for name in (b"extensions.worktreeConfig\0", b"EXTENSIONS.WORKTREECONFIG\0", b"extensions.other\0"):
                    streams[4] = name
                    result, launched, _, code = invoke_seam(v2, seam, streams)
                    self.assertEqual((result["schema_version"], result["reason"], result["failed_step"], code, len(launched)),
                                     ("yini-readonly-preflight/result-v2", "STATE_UNSUPPORTED", "before.config", 4, 5))
            with mock.patch("subprocess.Popen") as popen:
                result, _, code = public_call(v1, seam)
                self.assertEqual((result["reason"], code), ("CONTRACT_INVALID", 2))
                result, _, code = public_call(v3_contract(), seam, entry=legacy)
                self.assertEqual((result["schema_version"], result["reason"], code),
                                 ("yini-readonly-preflight/result-v1", "CONTRACT_INVALID", 2))
                result, _, code = public_call(dict(v1, staged=["docs/case.txt"]), seam, entry=legacy)
                self.assertEqual((result["reason"], code), ("CONTRACT_INVALID", 2))
                popen.assert_not_called()

    def test_v3_absent_false_true_empty_partial_and_mode_only(self):
        empty = contract(index_tree_sha256=hashlib.sha256(encode([
            {"path": "docs/case.txt", "mode": "100644", "oid": "c" * 40}])).hexdigest())
        for seam in ("verify", "main"):
            for extension in (None, False, True):
                for base in [empty] + [positive_contract(xy) for xy in ("M ", "A ", "MM", "AM")] + [positive_contract(mode_only=True)]:
                    value = v3_contract(base, extension)
                    streams = v3_outputs(value) * 2
                    with self.subTest(seam=seam, extension=extension, rows=value["staged"]), PhysicalFixture():
                        result, launched, delivered, code = invoke_seam(value, seam, streams)
                        self.assertEqual(result, v3_expected(value, streams))
                        self.assertEqual(code, 0)
                        self.assertEqual(delivered, encode(v3_expected(value, streams)))
                        self.assertIs(result["fingerprint"]["extension_worktree_config"], extension)
                        self.assertIs(type(result["fingerprint"]["repository_format_version"]), int)
                        self.assertEqual(len(launched), 20 + 2 * (extension is not None) + 2 * len(value["staged"]))
                        self.assertEqual(sum("--type=bool" in argv for argv, _ in launched), 0 if extension is None else 2)

    def test_v3_thirty_two_paths_never_deduplicate_blobs(self):
        for seam in ("verify", "main"):
            for extension in (None, False, True):
                with self.subTest(seam=seam, extension=extension), PhysicalFixture() as fixture:
                    value = v3_contract(positive_contract(), extension)
                    value["staged"] = [staged_row(path="docs/p%02d" % n, blob_sha256=hashlib.sha256(b"hello\n").hexdigest()) for n in range(32)]
                    value["delta"] = [delta_row(path="docs/p%02d" % n, xy="MM") for n in range(32)]
                    for row in value["delta"]:
                        (fixture.root / row["path"]).write_bytes(b"abc")
                    value["index_tree_sha256"] = hashlib.sha256(encode([
                        {"path": row["path"], "mode": "100644", "oid": "c" * 40} for row in value["staged"]])).hexdigest()
                    streams = v3_outputs(value) * 2
                    result, launched, delivered, code = invoke_seam(value, seam, streams)
                    self.assertEqual((result, delivered, code), (v3_expected(value, streams), encode(v3_expected(value, streams)), 0))
                    self.assertEqual(len(launched), 84 if extension is None else 86)
                    self.assertEqual(sum("cat-file" in argv for argv, _ in launched), 64)

    def test_v3_config_name_cardinality_and_exclusions_precede_values(self):
        format_key = b"core.repositoryformatversion\0"
        extension_key = b"extensions.worktreeConfig\0"
        unsupported = [b"", extension_key, format_key * 2 + extension_key,
                       format_key + b"Core.RepositoryFormatVersion\0" + extension_key,
                       format_key + extension_key * 2, format_key + extension_key + b"EXTENSIONS.WORKTREECONFIG\0"]
        prohibited = ("include.path", "includeIf.gitdir:invented.path", "filter.clean", "filter.driver.clean",
                      "extensions.objectformat", "extensions.worktreeConfig.extra", "extensions.sub.worktreeConfig",
                      "remote.origin.promisor", "remote.origin.partialclonefilter", "core.sparsecheckout",
                      "core.sparsecheckoutcone", "core.splitindex", "core.worktree")
        unsupported += [format_key + extension_key + name.encode() + b"\0" for name in prohibited]
        malformed = [b"core.repositoryformatversion", b"bad\xff\0", b"\0", b"bad\0", b"core.bad\nkey\0"]
        for seam in ("verify", "main"):
            for names, reason in [(raw, "STATE_UNSUPPORTED") for raw in unsupported] + [(raw, "OBSERVATION_MISMATCH") for raw in malformed]:
                with self.subTest(seam=seam, names=names), PhysicalFixture():
                    value = v3_contract(positive_contract())
                    streams = v3_outputs(value) * 2
                    streams[0] = names
                    result, launched, _, code = invoke_seam(value, seam, streams)
                    self.assertEqual((result["reason"], result["failed_step"], code, len(launched)),
                                     (reason, "before.config.names", 4 if reason == "STATE_UNSUPPORTED" else 3, 1))
                    self.assertIsNone(result["fingerprint"])
            for extension, names in ((None, format_key + extension_key), (False, format_key), (True, format_key)):
                with self.subTest(seam=seam, extension=extension), PhysicalFixture():
                    value = v3_contract(positive_contract(), extension)
                    streams = v3_outputs(value) * 2
                    streams[0] = names
                    result, launched, _, _ = invoke_seam(value, seam, streams)
                    self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                     ("OBSERVATION_MISMATCH", "before.config.names", 1))

    def test_v3_duplicate_equal_and_conflicting_physical_values_reject(self):
        for seam in ("verify", "main"):
            for key in ("core.repositoryformatversion", "extensions.worktreeConfig"):
                for second in ("0", "1"):
                    with self.subTest(seam=seam, key=key, second=second), PhysicalFixture() as fixture:
                        section, variable = key.split(".")
                        body = ("[%s]\n%s = 0\n%s = %s\n" % (section, variable, variable, second)).encode()
                        (fixture.root / ".git/config").write_bytes(body)
                        value = v3_contract(positive_contract())
                        value["config_sha256"] = hashlib.sha256(body).hexdigest()
                        streams = v3_outputs(value) * 2
                        streams[0] += key.encode() + b"\0"
                        result, launched, _, _ = invoke_seam(value, seam, streams)
                        self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                         ("STATE_UNSUPPORTED", "before.config.names", 1))

    def test_v3_typed_format_and_boolean_first_failure(self):
        for seam in ("verify", "main"):
            for phase, start in (("before", 0), ("after", 12)):
                cases = [(1, b"1\n", "STATE_UNSUPPORTED", 4), (1, b"-1\n", "STATE_UNSUPPORTED", 4),
                         (1, b"0", "OBSERVATION_MISMATCH", 3), (1, b"00\n", "OBSERVATION_MISMATCH", 3),
                         (1, b"0\n0\n", "OBSERVATION_MISMATCH", 3), (1, b"bad\n", "OBSERVATION_MISMATCH", 3),
                         (2, b"true", "OBSERVATION_MISMATCH", 3), (2, b"1\n", "OBSERVATION_MISMATCH", 3),
                         (2, b"TRUE\n", "OBSERVATION_MISMATCH", 3), (2, b"true\nfalse\n", "OBSERVATION_MISMATCH", 3),
                         (2, b"\xff\n", "OBSERVATION_MISMATCH", 3),
                         (2, b"false\n", "OBSERVATION_MISMATCH" if phase == "before" else "OBSERVATION_DRIFT", 3),
                         (1, (b"", b"invented invalid integer", 128), "GIT_EXIT", 128),
                         (2, (b"", b"invented invalid bool", 128), "GIT_EXIT", 128)]
                for offset, payload, reason, code in cases:
                    with self.subTest(seam=seam, phase=phase, payload=payload), PhysicalFixture():
                        value = v3_contract(positive_contract())
                        streams = v3_outputs(value) * 2
                        streams[start + offset] = payload
                        result, launched, _, observed_code = invoke_seam(value, seam, streams)
                        step = phase + (".config.format" if offset == 1 else ".config.worktree")
                        self.assertEqual((result["reason"], result["failed_step"], observed_code, len(launched)),
                                         (reason, step, code, start + offset + 1))
                        self.assertIsNone(result["fingerprint"])

    def test_v3_documented_git_boolean_framing_and_name_multiset(self):
        # Git 2.40 git-config(1), Values: implicit is true; empty is false.
        fixtures = [(b" = true", True, b"true\n"), (b" = yes", True, b"true\n"),
                    (b" = on", True, b"true\n"), (b" = 1", True, b"true\n"), (b"", True, b"true\n"),
                    (b" = false", False, b"false\n"), (b" = no", False, b"false\n"),
                    (b" = off", False, b"false\n"), (b" = 0", False, b"false\n"), (b" = ", False, b"false\n")]
        for seam in ("verify", "main"):
            for lexical, extension, canonical in fixtures:
                with self.subTest(seam=seam, lexical=lexical), PhysicalFixture() as fixture:
                    body = b"[core]\nrepositoryFormatVersion = 0\n[extensions]\nworktreeConfig" + lexical + b"\n"
                    (fixture.root / ".git/config").write_bytes(body)
                    value = v3_contract(positive_contract(), extension)
                    value["config_sha256"] = hashlib.sha256(body).hexdigest()
                    streams = v3_outputs(value) * 2
                    streams[0] = b"CORE.RepositoryFormatVersion\0extensions.WorktreeConfig\0core.filemode\0core.filemode\0"
                    streams[12] = b"core.filemode\0extensions.WorktreeConfig\0core.filemode\0CORE.RepositoryFormatVersion\0"
                    streams[2] = streams[14] = canonical
                    result, launched, _, code = invoke_seam(value, seam, streams)
                    self.assertEqual((result["reason"], code, len(launched)), ("MATCH", 0, 24))
                    streams[12] += b"core.filemode\0"
                    result, launched, _, code = invoke_seam(value, seam, streams)
                    self.assertEqual((result["reason"], result["failed_step"], code, len(launched)),
                                     ("OBSERVATION_DRIFT", "after.config.names", 3, 13))

    def test_v3_later_common_config_symlink_is_drift(self):
        value = v3_contract(positive_contract())
        streams = v3_outputs(value) * 2
        for seam in ("verify", "main"):
            for when, step in ((3, "before.config.guard"), (12, "after.paths"), (24, "final.files")):
                with self.subTest(seam=seam, when=when), PhysicalFixture() as fixture:
                    def mutate(count):
                        if count == when:
                            leaf = fixture.root / ".git/config"
                            leaf.unlink()
                            leaf.symlink_to("missing-invented-config")
                    result, launched, _, code = invoke_seam(value, seam, streams, mutate)
                    self.assertEqual((result["reason"], result["failed_step"], code, len(launched)),
                                     ("OBSERVATION_DRIFT", step, 3, when))
                    self.assertIsNone(result["fingerprint"])

    def test_v3_true_exact_result_order_and_five_scans(self):
        value = v3_contract(positive_contract())
        streams = v3_outputs(value) * 2
        expected = v3_expected(value, streams)
        prefix = ("/usr/bin/git", "--no-pager", "--no-optional-locks", "-c", "core.fsmonitor=false",
                  "-c", "core.untrackedCache=false", "-c", "core.hooksPath=/dev/null", "-c", "diff.external=")
        suffixes = [("config", "--file", ROOT + "/.git/config", "--no-includes", "--null", "--name-only", "--list"),
                    ("config", "--file", ROOT + "/.git/config", "--no-includes", "--type=int", "--get-all", "core.repositoryformatversion"),
                    ("config", "--file", ROOT + "/.git/config", "--no-includes", "--type=bool", "--get-all", "extensions.worktreeConfig"),
                    ("rev-parse", "--show-toplevel"), ("rev-parse", "--path-format=absolute", "--git-common-dir"),
                    ("symbolic-ref", "--quiet", "--short", "HEAD"), ("rev-parse", "--verify", "HEAD^{commit}"),
                    ("rev-parse", "--shared-index-path"), ("ls-files", "--stage", "-v", "--sparse", "-z"),
                    ("status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=none"),
                    ("diff", "--cached", "--raw", "-z", "--no-abbrev", "--no-renames", "--no-ext-diff",
                     "--no-textconv", "--ignore-submodules=none", "HEAD", "--"), ("cat-file", "blob", "c" * 40)] * 2
        for seam in ("verify", "main"):
            with self.subTest(seam=seam), PhysicalFixture() as fixture:
                result, launched, delivered, code = invoke_seam(value, seam, streams)
                self.assertEqual((result, code, delivered), (expected, 0, encode(expected)))
                self.assertEqual([argv for argv, _ in launched], [prefix + suffix for suffix in suffixes])
                environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C", "TZ": "UTC", "HOME": "/dev/null",
                               "XDG_CONFIG_HOME": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": "/dev/null",
                               "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_ATTR_NOSYSTEM": "1", "GIT_OPTIONAL_LOCKS": "0",
                               "GIT_TERMINAL_PROMPT": "0", "GIT_NO_REPLACE_OBJECTS": "1"}
                for _, options in launched:
                    self.assertEqual(options, dict(stdin=-3, stdout=-1, stderr=-1, shell=False, cwd=ROOT, env=environment))
                self.assertEqual(fixture.opened.count(ROOT + "/.git/config"), 5)
                for name in (ROOT + "/.git/index", "/usr/bin/git", ROOT + "/docs/case.txt"):
                    self.assertEqual(fixture.opened.count(name), 3)
                self.assertNotIn(ROOT + "/.git/config.worktree", fixture.opened)


class V3PhysicalTests(Isolated):
    def test_v3_initial_unsafe_config_ancestors_and_storage(self):
        cases = ("common-symlink", "common-file", "config-symlink", "config-hardlink", "index-hardlink",
                 "objects-symlink", "alternate", "http-alternate", "promisor", "shallow", "grafts")
        for seam in ("verify", "main"):
            for kind in cases:
                with self.subTest(seam=seam, kind=kind), PhysicalFixture() as fixture:
                    if kind.startswith("common-"):
                        (fixture.root / ".git").rename(fixture.root / "linked-administration")
                        if kind == "common-symlink":
                            (fixture.root / ".git").symlink_to("linked-administration")
                        else:
                            (fixture.root / ".git").write_bytes(b"gitdir: linked-administration\n")
                    elif kind == "config-symlink":
                        (fixture.root / ".git/config").unlink()
                        (fixture.root / ".git/config").symlink_to("missing-invented")
                    elif kind.endswith("hardlink"):
                        os.link(fixture.root / (".git/config" if kind.startswith("config") else ".git/index"), fixture.root / "alias")
                    elif kind == "objects-symlink":
                        (fixture.root / ".git/objects").rename(fixture.root / "old-objects")
                        (fixture.root / ".git/objects").symlink_to("../old-objects")
                    else:
                        target = {"alternate": ".git/objects/info/alternates", "http-alternate": ".git/objects/info/http-alternates",
                                  "promisor": ".git/objects/pack/p.promisor", "shallow": ".git/shallow", "grafts": ".git/info/grafts"}[kind]
                        (fixture.root / target).write_bytes(b"invented")
                    fixture.opened.clear()
                    result, launched, _, code = invoke_seam(v3_contract(positive_contract()), seam)
                    reason = ("PATH_UNSAFE" if "symlink" in kind else "CHECKOUT_UNSUPPORTED" if kind == "common-file"
                              else "OBSERVATION_MISMATCH" if "hardlink" in kind else "STATE_UNSUPPORTED")
                    self.assertEqual((result["reason"], result["failed_step"], len(launched)), (reason, "paths", 0))
                    self.assertEqual(code, 2 if reason == "PATH_UNSAFE" else 3 if reason == "OBSERVATION_MISMATCH" else 4)
                    self.assertEqual(fixture.opened, [])

    def test_v3_does_not_open_existing_linked_config(self):
        for seam in ("verify", "main"):
            with self.subTest(seam=seam), PhysicalFixture() as fixture:
                leaf = fixture.root / ".git/worktrees/invented/config.worktree"
                leaf.parent.mkdir(parents=True)
                leaf.write_bytes(b"invented linked config not authorized for reading")
                fixture.opened.clear()
                value = v3_contract(positive_contract())
                result, launched, _, code = invoke_seam(value, seam, v3_outputs(value) * 2)
                self.assertEqual((result["reason"], code, len(launched)), ("MATCH", 0, 24))
                self.assertFalse(any("/worktrees/" in name for name in fixture.opened))

    def test_v3_physical_drift_and_guard_stop_before_dependent_child(self):
        value = v3_contract(positive_contract())
        streams = v3_outputs(value) * 2
        for seam in ("verify", "main"):
            for target in ("worktree-empty", "worktree-symlink", "config-content", "config-mode", "config-inode", "config-mtime", "config-hardlink", "config-missing"):
                for when, step, count in ((1, "before.config.guard", 3), (12, "after.paths" if target.startswith("worktree") or target in ("config-hardlink", "config-missing") else "after.index", 12),
                                         (15, "after.config.guard", 15), (24, "final.files", 24)):
                    with self.subTest(seam=seam, target=target, when=when), PhysicalFixture() as fixture:
                        def mutate(number):
                            if number != when:
                                return
                            leaf = fixture.root / ".git/config"
                            if target == "worktree-empty":
                                (fixture.root / ".git/config.worktree").write_bytes(b"")
                            elif target == "worktree-symlink":
                                (fixture.root / ".git/config.worktree").symlink_to("missing-invented")
                            elif target == "config-content":
                                leaf.write_bytes(b"abd")
                            elif target == "config-mode":
                                leaf.chmod(0o600)
                            elif target == "config-inode":
                                leaf.rename(fixture.root / "old-config")
                                leaf.write_bytes(b"abc")
                            elif target == "config-mtime":
                                os.utime(leaf, ns=(1_000_000_000, 1_000_000_001))
                            elif target == "config-hardlink":
                                os.link(leaf, fixture.root / "alias")
                            else:
                                leaf.unlink()
                        result, launched, _, code = invoke_seam(value, seam, streams, mutate)
                        self.assertEqual((result["reason"], result["failed_step"], code, len(launched)),
                                         ("OBSERVATION_DRIFT", step, 3, count))
                        self.assertNotIn(ROOT + "/.git/config.worktree", fixture.opened)
                        self.assertIsNone(result["fingerprint"])

    def test_v3_nanosecond_identity_and_atime_only_boundary(self):
        from types import SimpleNamespace
        attributes = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns", "st_atime_ns")
        for seam in ("verify", "main"):
            for change in ("atime", "mtime", "ctime"):
                with self.subTest(seam=seam, change=change), PhysicalFixture() as fixture:
                    value = v3_contract(positive_contract())
                    original_fstat = os.fstat
                    config_inode = (fixture.root / ".git/config").stat().st_ino
                    state = {"changed": False}
                    def transform(info):
                        if info.st_ino != config_inode:
                            return info
                        fields = {name: getattr(info, name) for name in attributes}
                        fields["st_mtime_ns"] = 1_800_000_000_000_000_000
                        fields["st_ctime_ns"] = 1_800_000_000_000_000_000
                        if state["changed"]:
                            fields["st_" + change + "_ns"] += 1
                        return SimpleNamespace(**fields)
                    def mutate(count):
                        if count == 3:
                            state["changed"] = True
                    with mock.patch("os.lstat", side_effect=lambda candidate: transform(fixture.lstat(candidate))), \
                            mock.patch("os.fstat", side_effect=lambda fd: transform(original_fstat(fd))):
                        result, launched, _, code = invoke_seam(value, seam, v3_outputs(value) * 2, mutate)
                    self.assertEqual((result["reason"], code, len(launched)),
                                     ("MATCH", 0, 24) if change == "atime" else ("OBSERVATION_DRIFT", 3, 3))
                    if change != "atime":
                        self.assertEqual(result["failed_step"], "before.config.guard")

    def test_v3_present_config_worktree_never_opened(self):
        for seam in ("verify", "main"):
            for kind in ("empty", "nonempty", "hardlink", "directory", "fifo", "symlink"):
                with self.subTest(seam=seam, kind=kind), PhysicalFixture() as fixture:
                    leaf = fixture.root / ".git/config.worktree"
                    if kind in ("empty", "nonempty"):
                        leaf.write_bytes(b"" if kind == "empty" else b"invented")
                    elif kind == "hardlink":
                        os.link(fixture.root / "docs/case.txt", leaf)
                    elif kind == "directory":
                        leaf.mkdir()
                    elif kind == "fifo":
                        os.mkfifo(leaf)
                    else:
                        leaf.symlink_to("missing-invented-target")
                    fixture.opened.clear()
                    result, launched, _, code = invoke_seam(v3_contract(positive_contract()), seam)
                    reason, expected_code = ("PATH_UNSAFE", 2) if kind == "symlink" else ("STATE_UNSUPPORTED", 4)
                    self.assertEqual((result["reason"], result["failed_step"], code, len(launched)),
                                     (reason, "paths", expected_code, 0))
                    self.assertEqual(fixture.opened, [])


class V3FailureTests(Isolated):
    def assert_stop(self, result, delivered, code, reason, step, expected_code, count):
        self.assertEqual((result["schema_version"], result["outcome"], result["reason"], result["failed_step"],
                          result["exit_code"], code, len(result["observations"])),
                         ("yini-readonly-preflight/result-v3", "STOP", reason, step, expected_code, expected_code, count))
        self.assertIsNone(result["fingerprint"])
        self.assertIs(result["successor_authority"], False)
        self.assertEqual(delivered, encode(result))
        self.assertEqual(set(result), {"schema_version", "work_unit_id", "contract_sha256", "outcome", "reason",
                                      "exit_code", "failed_step", "child_returncode", "observations", "fingerprint", "successor_authority"})

    def test_v3_exits_launch_timeout_and_partial_evidence(self):
        import subprocess
        value = v3_contract(positive_contract())
        for seam in ("verify", "main"):
            for child_code in (1, 7, 128, 255, -9):
                with self.subTest(seam=seam, child_code=child_code), PhysicalFixture():
                    process = PipeProcess(stdout=b"abc", stderr=b"fatal", returncode=child_code)
                    result, launched, delivered, code = invoke_seam(value, seam, process=process)
                    self.assert_stop(result, delivered, code, "GIT_EXIT", "before.config.names", 137 if child_code == -9 else child_code, 1)
                    self.assertEqual(result["child_returncode"], child_code)
                    self.assertEqual(result["observations"], [dict(step="before.config.names", returncode=child_code,
                        stdout_sha256=ABC, stderr_sha256=hashlib.sha256(b"fatal").hexdigest(), stdout_bytes=3, stderr_bytes=5, complete=True)])
                    self.assertEqual(len(launched), 1)
            with self.subTest(seam=seam, fault="launch"), PhysicalFixture(), mock.patch("subprocess.Popen", side_effect=OSError("invented launch")) as popen:
                result, delivered, code = public_call(value, seam)
                self.assert_stop(result, delivered, code, "PROCESS_LAUNCH_ERROR", "before.config.names", 5, 1)
                self.assertEqual(result["observations"], [dict(step="before.config.names", returncode=None,
                    stdout_sha256=EMPTY, stderr_sha256=EMPTY, stdout_bytes=0, stderr_bytes=0, complete=False)])
                popen.assert_called_once()
            for cleanup in ("normal", "kill-error", "reap-error"):
                with self.subTest(seam=seam, cleanup=cleanup), PhysicalFixture():
                    process = PipeProcess(stdout=b"abc", wait_error=subprocess.TimeoutExpired("invented", 5), kill_error=cleanup == "kill-error")
                    if cleanup == "reap-error":
                        def wait(timeout=None):
                            process.waits += 1
                            raise subprocess.TimeoutExpired("invented", timeout)
                        process.wait = wait
                    result, launched, delivered, code = invoke_seam(value, seam, process=process)
                    self.assert_stop(result, delivered, code, "TIMEOUT", "before.config.names", 124, 1)
                    self.assertEqual(result["observations"][0]["stdout_sha256"], ABC)
                    self.assertIs(result["observations"][0]["complete"], False)
                    self.assertTrue(process.killed)
                    self.assertEqual((process.waits, len(launched)), (2, 1))

    def test_v3_selector_read_wait_faults_and_non_native_codes(self):
        import selectors
        value = v3_contract(positive_contract())
        for seam in ("verify", "main"):
            for fault in ("register", "select", "read", "wait", None, True, False, 256, -256):
                with self.subTest(seam=seam, fault=fault), PhysicalFixture():
                    process = PipeProcess(stdout=b"abc", wait_error=OSError("invented wait") if fault == "wait" else None,
                                          returncode=fault if type(fault) is not str else 0)
                    original_read = os.read
                    reads = []
                    def read(fd, size):
                        if fd == process.stdout.fileno():
                            if reads:
                                raise OSError("invented read")
                            reads.append(True)
                        return original_read(fd, size)
                    if fault in ("register", "select"):
                        patcher = mock.patch.object(selectors.DefaultSelector, fault, side_effect=OSError("invented selector"))
                    elif fault == "read":
                        patcher = mock.patch("os.read", side_effect=read)
                    else:
                        patcher = mock.patch("time.monotonic", wraps=observer.time.monotonic)
                    with patcher:
                        result, launched, delivered, code = invoke_seam(value, seam, process=process)
                    self.assert_stop(result, delivered, code, "INTERNAL_DEFECT", "before.config.names", 70, 1)
                    self.assertIs(result["observations"][0]["complete"], False)
                    self.assertTrue(process.killed)
                    self.assertEqual(len(launched), 1)

    def test_v3_stream_index_blob_and_total_blob_caps(self):
        value = v3_contract(positive_contract())
        cases = [(0, b"x" * 262145, "CAPTURE_LIMIT", "before.config.names"),
                 (0, (b"", b"x" * 262145, 0), "CAPTURE_LIMIT", "before.config.names"),
                 (8, b"x" * (2 * 1024 * 1024 + 1), "CAPTURE_LIMIT", "before.entries"),
                 (11, b"x" * (16 * 1024 * 1024 + 1), "CAPTURE_LIMIT", "before.blob.000"),
                 (8, b"".join(("H 100644 " + "c" * 40 + " 0\tp%04d\0" % n).encode() for n in range(8193)), "STATE_UNSUPPORTED", "before.entries")]
        for seam in ("verify", "main"):
            for offset, payload, reason, step in cases:
                with self.subTest(seam=seam, offset=offset, reason=reason), PhysicalFixture():
                    streams = v3_outputs(value) * 2
                    streams[offset] = payload
                    result, launched, delivered, code = invoke_seam(value, seam, streams)
                    self.assert_stop(result, delivered, code, reason, step, 125 if reason == "CAPTURE_LIMIT" else 4, offset + 1)
                    self.assertEqual(len(launched), offset + 1)
                    if reason == "CAPTURE_LIMIT":
                        record = result["observations"][-1]
                        self.assertIs(record["complete"], False)
                        stream = "stderr" if isinstance(payload, tuple) else "stdout"
                        self.assertEqual(record[stream + "_bytes"], len(payload[1]) if isinstance(payload, tuple) else len(payload))
            with self.subTest(seam=seam, cap="total-blob"), PhysicalFixture() as fixture:
                payload = b"x" * (16 * 1024 * 1024)
                many = v3_contract(positive_contract())
                many["staged"] = [staged_row(path="docs/p%d" % n, blob_sha256=hashlib.sha256(payload).hexdigest()) for n in range(5)]
                many["delta"] = [delta_row(path="docs/p%d" % n, xy="MM") for n in range(5)]
                for row in many["delta"]:
                    (fixture.root / row["path"]).write_bytes(b"abc")
                many["index_tree_sha256"] = hashlib.sha256(encode([
                    {"path": row["path"], "mode": "100644", "oid": "c" * 40} for row in many["staged"]])).hexdigest()
                streams = v3_outputs(many) * 2
                streams[11:16] = [payload] * 5
                result, launched, delivered, code = invoke_seam(many, seam, streams)
                self.assert_stop(result, delivered, code, "CAPTURE_LIMIT", "before.blob.004", 125, 16)
                self.assertEqual(len(launched), 16)
                self.assertEqual(result["observations"][-1]["stdout_bytes"], 1)

    def test_v3_three_full_two_config_scans_exact_224_mib_ceiling(self):
        size = 16 * 1024 * 1024
        payload = b"x" * size
        digest = hashlib.sha256(payload).hexdigest()
        for seam in ("verify", "main"):
            with self.subTest(seam=seam), PhysicalFixture() as fixture:
                names = (".git/index", ".git/config", "git-tool", "docs/case.txt")
                for name in names:
                    (fixture.root / name).write_bytes(payload)
                value = v3_contract(positive_contract())
                value["index_sha256"] = value["config_sha256"] = value["git"]["sha256"] = value["delta"][0]["sha256"] = digest
                inode_names = {(fixture.root / name).stat().st_ino: name for name in names}
                captured = {name: 0 for name in names}
                original_read = os.read
                def read(fd, limit):
                    chunk = original_read(fd, limit)
                    name = inode_names.get(os.fstat(fd).st_ino)
                    if name is not None:
                        captured[name] += len(chunk)
                    return chunk
                with mock.patch("os.read", side_effect=read):
                    result, launched, _, code = invoke_seam(value, seam, v3_outputs(value) * 2)
                self.assertEqual((result["reason"], code, len(launched)), ("MATCH", 0, 24))
                self.assertEqual(captured, {".git/config": 5 * size, ".git/index": 3 * size, "git-tool": 3 * size, "docs/case.txt": 3 * size})
                self.assertEqual(sum(captured.values()), 224 * 1024 * 1024)
                (fixture.root / "docs/extra.txt").write_bytes(b"x")
                value["delta"].append(delta_row(path="docs/extra.txt", xy="??", sha256=hashlib.sha256(b"x").hexdigest()))
                result, launched, delivered, code = invoke_seam(value, seam)
                self.assert_stop(result, delivered, code, "OBSERVATION_MISMATCH", "before.index", 3, 0)
                self.assertEqual(launched, [])

    def test_v3_config_scan_cap_and_directory_inventory(self):
        for seam in ("verify", "main"):
            for target in ("initial-config-cap", "config-guard-cap", "directory-cap"):
                with self.subTest(seam=seam, target=target), PhysicalFixture() as fixture:
                    value = v3_contract(positive_contract())
                    if target == "initial-config-cap":
                        with (fixture.root / ".git/config").open("r+b") as handle:
                            handle.truncate(16 * 1024 * 1024 + 1)
                    elif target == "directory-cap":
                        for number in range(8193):
                            (fixture.root / ".git/objects/info" / ("p%04d" % number)).touch()
                    def mutate(count):
                        if count == 3 and target == "config-guard-cap":
                            with (fixture.root / ".git/config").open("r+b") as handle:
                                handle.truncate(16 * 1024 * 1024 + 1)
                    fixture.opened.clear()
                    result, launched, delivered, code = invoke_seam(value, seam, v3_outputs(value) * 2, mutate)
                    reason, step, exit_code, count = {"initial-config-cap": ("OBSERVATION_MISMATCH", "before.index", 3, 0),
                        "config-guard-cap": ("OBSERVATION_DRIFT", "before.config.guard", 3, 3),
                        "directory-cap": ("STATE_UNSUPPORTED", "paths", 4, 0)}[target]
                    self.assert_stop(result, delivered, code, reason, step, exit_code, count)
                    self.assertEqual(len(launched), count)
                    if target == "directory-cap":
                        self.assertEqual(fixture.opened, [])

    def test_v3_oversized_result_and_repeated_bytes(self):
        for seam in ("verify", "main"):
            for large in (False, True):
                with self.subTest(seam=seam, large=large), PhysicalFixture():
                    value = v3_contract(positive_contract())
                    if large:
                        value["absent"] = ["future-%03d/" % n + "/".join(["a" * 200] * 10) for n in range(128)]
                    self.assertLessEqual(len(encode(value)), 262144)
                    streams = v3_outputs(value) * 2
                    expected = v3_expected(value, streams)
                    if large:
                        self.assertGreater(len(encode(expected)), 262144)
                        expected.update(outcome="STOP", reason="INTERNAL_DEFECT", exit_code=70, failed_step="result", fingerprint=None)
                    result, launched, delivered, code = invoke_seam(value, seam, streams)
                    self.assertEqual((result, delivered, code, len(launched)), (expected, encode(expected), 70 if large else 0, 24))
                    self.assertLessEqual(len(delivered), 262144)
                    second, _, second_bytes, second_code = invoke_seam(value, seam, streams)
                    self.assertEqual((second, second_bytes, second_code), (result, delivered, code))


class IdentityTests(Isolated):
    def test_empty_full_partial_and_mode_only_have_separate_identities(self):
        empty = contract(index_tree_sha256=hashlib.sha256(encode([
            {"path": "docs/case.txt", "mode": "100644", "oid": "c" * 40}])).hexdigest())
        for value in [empty] + [positive_contract(xy) for xy in ("M ", "A ", "MM", "AM")] + [positive_contract(mode_only=True)]:
            with self.subTest(kind=value["state_kind"], delta=value["delta"]), PhysicalFixture():
                result, launched = invoke(value)
                self.assertEqual((result["reason"], result["exit_code"]), ("MATCH", 0))
                self.assertEqual(len(launched), 18 + 2 * len(value["staged"]))
                self.assertEqual(result["fingerprint"], {key: value[key] for key in
                    ("root", "common_dir", "branch", "head", "index_sha256", "config_sha256",
                     "index_tree_sha256", "state_kind", "staged", "delta", "absent")})
                self.assertIs(result["successor_authority"], False)

    def test_wrong_physical_identity_rejects_before_git(self):
        for field, reason in (("index_sha256", "OBSERVATION_MISMATCH"),
                              ("config_sha256", "OBSERVATION_MISMATCH"),
                              ("tool", "TOOL_IDENTITY_MISMATCH"), ("worktree", "OBSERVATION_MISMATCH"),
                              ("mode", "OBSERVATION_MISMATCH"), ("absence", "OBSERVATION_MISMATCH")):
            with self.subTest(field=field), PhysicalFixture(), mock.patch("subprocess.Popen") as popen:
                value = positive_contract()
                if field in ("index_sha256", "config_sha256"):
                    value[field] = "0" * 64
                elif field == "tool":
                    value["git"]["sha256"] = "0" * 64
                elif field == "worktree":
                    value["delta"][0]["sha256"] = "0" * 64
                elif field == "mode":
                    value["delta"][0]["mode"] = "755"
                else:
                    value["absent"] = ["docs/other.txt"]
                    value["absent"] = ["git-tool"]
                self.assertEqual(checked(value)["reason"], reason)
                popen.assert_not_called()

    def test_wrong_map_mode_oid_or_blob_stops_at_bound_step(self):
        for target, step, count in (("tree", "before.entries", 7), ("mode", "before.entries", 7),
                                    ("oid", "before.entries", 7), ("blob", "before.blob.000", 10)):
            with self.subTest(target=target), PhysicalFixture():
                value = positive_contract()
                streams = outputs(value) * 2
                if target == "tree":
                    value["index_tree_sha256"] = "0" * 64
                elif target == "mode":
                    streams[6] = streams[6].replace(b"100644", b"100755")
                elif target == "oid":
                    streams[6] = streams[6].replace(b"c" * 40, b"d" * 40)
                else:
                    streams[9] = b"abc"
                result, launched = invoke(value, streams)
                self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                 ("OBSERVATION_MISMATCH", step, count))

    def test_valid_v2_reaches_environment_and_import_has_no_io(self):
        with mock.patch.dict(os.environ, {"GIT_INDEX_FILE": "invented"}), mock.patch("subprocess.Popen") as popen:
            self.assertEqual(checked(contract()).get("reason"), "ENVIRONMENT_UNSUPPORTED")
            popen.assert_not_called()


class GuardTests(Isolated):
    def test_storage_and_config_physical_guards_precede_reads(self):
        for kind in ("alternate", "http-alternate", "promisor", "shallow", "grafts", "objects-symlink",
                     "config-symlink", "config-hardlink", "index-hardlink", "file-hardlink"):
            with self.subTest(kind=kind), PhysicalFixture() as fixture:
                target = fixture.root / ".git/config"
                if kind in ("alternate", "http-alternate", "promisor", "shallow", "grafts"):
                    name = {"alternate": ".git/objects/info/alternates",
                            "http-alternate": ".git/objects/info/http-alternates",
                            "promisor": ".git/objects/pack/pack-x.promisor",
                            "shallow": ".git/shallow", "grafts": ".git/info/grafts"}[kind]
                    (fixture.root / name).write_bytes(b"invented")
                elif kind == "objects-symlink":
                    (fixture.root / ".git/objects").rename(fixture.root / "objects-old")
                    (fixture.root / ".git/objects").symlink_to(fixture.root / "objects-old")
                elif kind == "config-symlink":
                    target.unlink()
                    target.symlink_to(fixture.root / "git-tool")
                else:
                    if kind == "index-hardlink":
                        target = fixture.root / ".git/index"
                    elif kind == "file-hardlink":
                        target = fixture.root / "docs/case.txt"
                    os.link(target, fixture.root / "alias")
                with mock.patch("subprocess.Popen") as popen:
                    result = checked(positive_contract())
                reason = ("PATH_UNSAFE" if "symlink" in kind else "OBSERVATION_MISMATCH"
                          if "hardlink" in kind else "STATE_UNSUPPORTED")
                self.assertEqual((result["reason"], result["failed_step"]), (reason, "paths"))
                self.assertEqual(fixture.opened, [])
                popen.assert_not_called()

    def test_prohibited_config_names_stop_before_status_or_blob(self):
        for key in ("include.path", "includeIf.gitdir:foo.path", "filter.clean", "extensions.objectformat",
                    "remote.origin.promisor", "remote.origin.partialclonefilter", "core.sparsecheckout",
                    "core.sparsecheckoutcone", "core.splitindex", "core.worktree"):
            with self.subTest(key=key), PhysicalFixture():
                value = positive_contract()
                streams = outputs(value) * 2
                streams[4] = key.encode() + b"\0"
                result, launched = invoke(value, streams)
                self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                 ("STATE_UNSUPPORTED", "before.config", 5))

    def test_malformed_missing_extra_duplicate_maps_and_unsupported_entries(self):
        value = positive_contract()
        baseline = outputs(value) * 2
        cases = [(6, b"", "OBSERVATION_MISMATCH"),
                 (6, baseline[6][:-1], "OBSERVATION_MISMATCH"),
                 (6, baseline[6] * 2, "OBSERVATION_MISMATCH"),
                 (6, baseline[6] + b"H 100644 " + b"d" * 40 + b" 0\textra.txt\0", "OBSERVATION_MISMATCH"),
                 (6, baseline[6].replace(b"docs/case.txt", b"bad\xff"), "OBSERVATION_MISMATCH"),
                 (7, b"", "OBSERVATION_MISMATCH"), (7, baseline[7][:-1], "OBSERVATION_MISMATCH"),
                 (7, baseline[7] * 2, "OBSERVATION_MISMATCH"),
                 (7, baseline[7] + b"?? extra.txt\0", "OBSERVATION_MISMATCH"),
                 (8, b"", "OBSERVATION_MISMATCH"), (8, baseline[8][:-1], "OBSERVATION_MISMATCH"),
                 (8, baseline[8] * 2, "OBSERVATION_MISMATCH"),
                 (8, baseline[8].replace(b"\0docs", b"\0extra"), "OBSERVATION_MISMATCH"),
                 (5, b"shared-index\n", "STATE_UNSUPPORTED")]
        for stage in (b"1", b"2", b"3"):
            cases.append((6, baseline[6].replace(b" 0\t", b" " + stage + b"\t"), "STATE_UNSUPPORTED"))
        for tag in (b"h", b"S", b"s", b"M"):
            cases.append((6, tag + baseline[6][1:], "STATE_UNSUPPORTED"))
        for mode in (b"120000", b"160000", b"040000"):
            cases.append((6, baseline[6].replace(b"100644", mode), "STATE_UNSUPPORTED"))
        cases.append((6, baseline[6].replace(b"c" * 40, b"0" * 40), "STATE_UNSUPPORTED"))
        for xy in (b" D", b"D ", b"R ", b"C ", b"UU", b" A"):
            cases.append((7, xy + baseline[7][2:], "STATE_UNSUPPORTED"))
        for change in (b"D", b"R100", b"C100"):
            cases.append((8, baseline[8].replace(b" M\0", b" " + change + b"\0"), "STATE_UNSUPPORTED"))
        for offset, bad, reason in cases:
            with self.subTest(offset=offset, bad=bad[:50]), PhysicalFixture() as fixture:
                streams = baseline.copy()
                streams[offset] = bad
                result, launched = invoke(value, streams)
                self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                 (reason, "before." + ("root", "common", "branch", "head", "config", "shared", "entries", "status", "staged")[offset], offset + 1))
                self.assertNotIn(ROOT + "/extra.txt", fixture.opened)
                self.assertIsNone(result["fingerprint"])

    def test_closed_argv_environment_and_no_path_or_mutator_arguments(self):
        with PhysicalFixture():
            result, launched = invoke(positive_contract())
        self.assertEqual(result["reason"], "MATCH")
        prefix = ("/usr/bin/git", "--no-pager", "--no-optional-locks", "-c", "core.fsmonitor=false",
                  "-c", "core.untrackedCache=false", "-c", "core.hooksPath=/dev/null", "-c", "diff.external=")
        suffixes = [("rev-parse", "--show-toplevel"), ("rev-parse", "--path-format=absolute", "--git-common-dir"),
                    ("symbolic-ref", "--quiet", "--short", "HEAD"), ("rev-parse", "--verify", "HEAD^{commit}"),
                    ("config", "--local", "--no-includes", "--null", "--name-only", "--list"),
                    ("rev-parse", "--shared-index-path"), ("ls-files", "--stage", "-v", "--sparse", "-z"),
                    ("status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=none"),
                    ("diff", "--cached", "--raw", "-z", "--no-abbrev", "--no-renames", "--no-ext-diff",
                     "--no-textconv", "--ignore-submodules=none", "HEAD", "--"), ("cat-file", "blob", "c" * 40)] * 2
        self.assertEqual([argv for argv, _ in launched], [prefix + suffix for suffix in suffixes])
        environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C", "TZ": "UTC", "HOME": "/dev/null",
                       "XDG_CONFIG_HOME": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": "/dev/null",
                       "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_ATTR_NOSYSTEM": "1", "GIT_OPTIONAL_LOCKS": "0",
                       "GIT_TERMINAL_PROMPT": "0", "GIT_NO_REPLACE_OBJECTS": "1"}
        for _, options in launched:
            self.assertEqual(options, dict(stdin=-3, stdout=-1, stderr=-1, shell=False, cwd=ROOT, env=environment))


class FailureTests(Isolated):
    def test_non_native_wait_result_never_advances(self):
        for returncode in (None, True, False, 256, -256):
            with self.subTest(returncode=returncode), PhysicalFixture(), mock.patch(
                    "subprocess.Popen", side_effect=lambda *a, **k:
                    PipeProcess(stdout=(ROOT + "\n").encode(), returncode=returncode)) as popen:
                result = checked(positive_contract())
                self.assertEqual((result["reason"], result["failed_step"], len(result["observations"])),
                                 ("INTERNAL_DEFECT", "before.root", 1))
                self.assertIsNone(result["fingerprint"])
                self.assertIs(result["observations"][0]["complete"], False)
                popen.assert_called_once()

    def test_metadata_unicode_controls_and_normalized_duplicates_reject(self):
        for names in (("bad\x85name",), ("caf\u00e9", "cafe\u0301")):
            with self.subTest(names=names), PhysicalFixture() as fixture:
                value = positive_contract()
                # Bind the exact full stream, including the forbidden metadata.
                # An old tree digest would mask the missing path guard (R1 P2-1).
                entries = [{"path": "docs/case.txt", "mode": "100644", "oid": "c" * 40}]
                entries += [{"path": name, "mode": "100644", "oid": "c" * 40} for name in names]
                entries.sort(key=lambda row: row["path"].encode("utf-8"))
                value["index_tree_sha256"] = hashlib.sha256(encode(entries)).hexdigest()
                listing = b"".join(("H {mode} {oid} 0\t{path}\0".format(**row)).encode("utf-8")
                                   for row in entries)
                streams = outputs(value) * 2
                streams[6] = streams[16] = listing
                result, launched = invoke(value, streams)
                self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                 ("OBSERVATION_MISMATCH", "before.entries", 7))
                self.assertEqual((result["outcome"], result["exit_code"]), ("STOP", 3))
                self.assertIsNone(result["fingerprint"])
                self.assertIs(result["successor_authority"], False)
                self.assertTrue(all(ROOT + "/" + name not in fixture.opened for name in names))

    def test_oversized_match_envelope_stops_bounded_at_verify_and_main(self):
        value = positive_contract()
        # Legal ASCII paths with an absent first ancestor, bounded segments,
        # and an input below R3's cap; no real long path is created.
        value["absent"] = ["future-%03d/" % number + "/".join(["a" * 200] * 10)
                           for number in range(128)]
        raw = encode(value)
        self.assertLessEqual(len(raw), 262144)
        streams = outputs(value) * 2
        steps = [phase + "." + label for phase in ("before", "after") for label in
                 ("root", "common", "branch", "head", "config", "shared", "entries", "status", "staged", "blob.000")]
        records = [dict(step=step, returncode=0, stdout_sha256=hashlib.sha256(stream).hexdigest(),
                        stderr_sha256=EMPTY, stdout_bytes=len(stream), stderr_bytes=0, complete=True)
                   for step, stream in zip(steps, streams)]
        expected = dict(schema_version="yini-readonly-preflight/result-v2", work_unit_id="TEST-V2",
                        contract_sha256=hashlib.sha256(raw).hexdigest(), outcome="STOP",
                        reason="INTERNAL_DEFECT", exit_code=70, failed_step="result",
                        child_returncode=None, observations=records, fingerprint=None, successor_authority=False)
        proposed_match = dict(expected, outcome="MATCH", reason="MATCH", exit_code=0, failed_step=None,
                              fingerprint={key: value[key] for key in
                                  ("root", "common_dir", "branch", "head", "index_sha256", "config_sha256",
                                   "index_tree_sha256", "state_kind", "staged", "delta", "absent")})
        self.assertGreater(len(encode(proposed_match)), 262144)
        for seam in ("verify", "main"):
            with self.subTest(seam=seam), PhysicalFixture() as fixture:
                launched = []

                def launch(*args, **kwargs):
                    launched.append(args)
                    return PipeProcess(stdout=streams[len(launched) - 1])

                with mock.patch("subprocess.Popen", side_effect=launch):
                    if seam == "verify":
                        result = observer.verify(raw, hashlib.sha256(raw).hexdigest())
                        delivered = encode(result)
                        exit_code = result["exit_code"]
                    else:
                        output = io.StringIO()
                        with mock.patch.object(sys, "stdin", io.TextIOWrapper(io.BytesIO(raw))), \
                                mock.patch.object(sys, "stdout", output):
                            exit_code = observer.main(["verify", "--contract-sha256", hashlib.sha256(raw).hexdigest()])
                        delivered = output.getvalue().encode("ascii")
                        result = json.loads(delivered)
                self.assertEqual(len(launched), 20)
                self.assertEqual(exit_code, 70)
                self.assertEqual((result["outcome"], result["fingerprint"] is None), ("STOP", True))
                self.assertLessEqual(len(delivered), 262144)
                self.assertEqual(result, expected)
                self.assertEqual(delivered, encode(expected))
                self.assertTrue(all("/future-" not in name for name in fixture.opened))

    def test_physical_file_scan_and_directory_inventory_caps(self):
        for name in (".git/index", ".git/config", "git-tool", "docs/case.txt"):
            with self.subTest(name=name), PhysicalFixture() as fixture, mock.patch("subprocess.Popen") as popen:
                with (fixture.root / name).open("r+b") as handle:
                    handle.truncate(16 * 1024 * 1024 + 1)
                result = checked(positive_contract())
                self.assertEqual((result["reason"], result["failed_step"]), ("OBSERVATION_MISMATCH", "before.index"))
                popen.assert_not_called()
        with PhysicalFixture() as fixture, mock.patch("subprocess.Popen") as popen:
            size = 15 * 1024 * 1024
            digest = hashlib.sha256(b"\0" * size).hexdigest()
            rows = []
            for number in range(5):
                name = "docs/large-%d" % number
                with (fixture.root / name).open("wb") as handle:
                    handle.truncate(size)
                rows.append(delta_row(path=name, xy="??", sha256=digest))
            result = checked(contract(delta=rows))
            self.assertEqual((result["reason"], result["failed_step"]), ("OBSERVATION_MISMATCH", "before.index"))
            popen.assert_not_called()
        with PhysicalFixture() as fixture, mock.patch("subprocess.Popen") as popen:
            for number in range(8193):
                (fixture.root / ".git/objects/info" / ("p%04d" % number)).touch()
            fixture.opened.clear()  # Measure only the observer, not fixture setup.
            result = checked(positive_contract())
            self.assertEqual((result["reason"], result["failed_step"]), ("STATE_UNSUPPORTED", "paths"))
            self.assertEqual(fixture.opened, [])
            popen.assert_not_called()

    def test_total_blob_budget_is_per_pass_and_never_deduplicates_oids(self):
        payload = b"x" * (16 * 1024 * 1024)
        blob_digest = hashlib.sha256(payload).hexdigest()
        with PhysicalFixture() as fixture:
            value = positive_contract()
            value["staged"] = [staged_row(path="docs/p%d" % n, blob_sha256=blob_digest) for n in range(5)]
            value["delta"] = [delta_row(path="docs/p%d" % n, xy="MM") for n in range(5)]
            for row in value["delta"]:
                (fixture.root / row["path"]).write_bytes(b"abc")
            value["index_tree_sha256"] = hashlib.sha256(encode([
                {"path": row["path"], "mode": "100644", "oid": "c" * 40} for row in value["staged"]])).hexdigest()
            streams = outputs(value) * 2
            streams[9:14] = [payload] * 5
            result, launched = invoke(value, streams)
            self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                             ("CAPTURE_LIMIT", "before.blob.004", 14))
            self.assertEqual(result["observations"][-1]["stdout_bytes"], 1)
            self.assertIs(result["observations"][-1]["complete"], False)

    def test_selector_read_wait_faults_keep_partial_evidence_and_reap(self):
        import subprocess
        for fault in ("register", "select", "read", "wait"):
            with self.subTest(fault=fault), PhysicalFixture():
                process = PipeProcess(stdout=b"abc", wait_error=OSError("invented wait") if fault == "wait" else None)
                original_read = os.read
                reads = []

                def read(fd, size):
                    if fd == process.stdout.fileno():
                        if reads:
                            raise OSError("invented read")
                        reads.append(True)
                    return original_read(fd, size)

                with mock.patch("subprocess.Popen", return_value=process) as popen:
                    if fault in ("register", "select"):
                        import selectors
                        with mock.patch.object(selectors.DefaultSelector, fault, side_effect=OSError("invented selector")):
                            result = checked(positive_contract())
                    elif fault == "read":
                        with mock.patch("os.read", side_effect=read):
                            result = checked(positive_contract())
                    else:
                        result = checked(positive_contract())
                self.assertEqual((result["reason"], result["failed_step"]), ("INTERNAL_DEFECT", "before.root"))
                self.assertTrue(process.killed)
                self.assertIs(result["observations"][0]["complete"], False)
                self.assertEqual(result["observations"][0]["stdout_bytes"], 3 if fault in ("read", "wait") else 0)
                self.assertGreaterEqual(process.waits, 1)
                popen.assert_called_once()

    def test_later_head_and_staged_map_drift_and_malformed_stream_first_failure(self):
        for offset, bad, reason in ((13, b"d" * 40 + b"\n", "OBSERVATION_DRIFT"),
                (18, b"", "OBSERVATION_DRIFT"), (14, b"core.filemode", "OBSERVATION_MISMATCH"),
                (17, b"M  docs/case.txt", "OBSERVATION_MISMATCH")):
            with self.subTest(offset=offset), PhysicalFixture():
                value = positive_contract()
                streams = outputs(value) * 2
                streams[offset] = bad
                result, launched = invoke(value, streams)
                self.assertEqual((result["reason"], len(launched)), (reason, offset + 1))
                self.assertIsNone(result["fingerprint"])

    def test_independent_multi_record_permutations_preserve_all_maps(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "docs/second.txt").write_bytes(b"abc")
            (fixture.root / "docs/untracked.txt").write_bytes(b"abc")
            value = positive_contract()
            value["staged"].append(staged_row(path="docs/second.txt", blob_sha256=value["staged"][0]["blob_sha256"]))
            value["delta"] += [delta_row(path="docs/second.txt", xy="MM"), delta_row(path="docs/untracked.txt", xy="??")]
            entries = [{"path": row["path"], "mode": row["index_mode"], "oid": row["index_oid"]} for row in value["staged"]]
            value["index_tree_sha256"] = hashlib.sha256(encode(entries)).hexdigest()
            baseline, _ = invoke(value)
            streams = outputs(value) * 2
            for offset in (6, 7, 8, 17, 18, 19):
                records = streams[offset][:-1].split(b"\0")
                if offset in (8, 19):
                    records = records[2:] + records[:2]
                else:
                    records.reverse()
                streams[offset] = b"\0".join(records) + b"\0"
            permuted, launched = invoke(value, streams)
            self.assertEqual((baseline["reason"], permuted["reason"], len(launched)), ("MATCH", "MATCH", 22))
            self.assertEqual(baseline["fingerprint"], permuted["fingerprint"])

    def test_child_exits_launch_wait_and_signal_preserve_exact_first_record(self):
        for child_code in (1, 7, 128, 255, -9):
            with self.subTest(child=child_code), PhysicalFixture(), mock.patch("subprocess.Popen",
                    side_effect=lambda *a, **k: PipeProcess(stdout=b"abc", stderr=b"fatal", returncode=child_code)) as popen:
                result = checked(positive_contract())
                self.assertEqual((result["reason"], result["exit_code"], result["child_returncode"], result["failed_step"]),
                                 ("GIT_EXIT", 137 if child_code == -9 else child_code, child_code, "before.root"))
                self.assertEqual(result["observations"], [dict(step="before.root", returncode=child_code,
                    stdout_sha256=ABC, stderr_sha256=hashlib.sha256(b"fatal").hexdigest(),
                    stdout_bytes=3, stderr_bytes=5, complete=True)])
                popen.assert_called_once()
        with PhysicalFixture(), mock.patch("subprocess.Popen", side_effect=OSError("invented launch fault")) as popen:
            result = checked(positive_contract())
            self.assertEqual((result["reason"], result["failed_step"], result["exit_code"]),
                             ("PROCESS_LAUNCH_ERROR", "before.root", 5))
            self.assertEqual(result["observations"], [dict(step="before.root", returncode=None,
                stdout_sha256=EMPTY, stderr_sha256=EMPTY, stdout_bytes=0, stderr_bytes=0, complete=False)])
            popen.assert_called_once()

    def test_timeout_preserves_first_failure_even_when_kill_or_reap_fails(self):
        import subprocess
        for failure in ("wait-timeout", "kill", "reap"):
            with self.subTest(failure=failure), PhysicalFixture():
                process = PipeProcess(stdout=b"abc", wait_error=subprocess.TimeoutExpired("invented", 5),
                                      kill_error=failure == "kill")
                if failure == "reap":
                    def wait(timeout=None):
                        process.waits += 1
                        raise subprocess.TimeoutExpired("invented", timeout)
                    process.wait = wait
                with mock.patch("subprocess.Popen", return_value=process) as popen:
                    result = checked(positive_contract())
                self.assertEqual((result["reason"], result["failed_step"], result["exit_code"]),
                                 ("TIMEOUT", "before.root", 124))
                self.assertTrue(process.killed)
                self.assertEqual(process.waits, 2)
                self.assertEqual(len(result["observations"]), 1)
                self.assertEqual(result["observations"][0]["stdout_sha256"], ABC)
                self.assertIs(result["observations"][0]["complete"], False)
                popen.assert_called_once()

    def test_stream_caps_and_blob_streaming_have_bounded_memory(self):
        for stream_name in ("stdout", "stderr"):
            with self.subTest(stream=stream_name), PhysicalFixture():
                process = PipeProcess(**{stream_name: b"x" * 262145})
                with mock.patch("subprocess.Popen", return_value=process) as popen:
                    result = checked(positive_contract())
                self.assertEqual((result["reason"], result["exit_code"]), ("CAPTURE_LIMIT", 125))
                self.assertEqual(result["observations"][0][stream_name + "_bytes"], 262145)
                self.assertTrue(process.killed)
                popen.assert_called_once()
        payload = b"x" * (16 * 1024 * 1024)
        with PhysicalFixture():
            value = positive_contract()
            value["staged"][0]["blob_sha256"] = hashlib.sha256(payload).hexdigest()
            streams = outputs(value) * 2
            streams[9] = streams[19] = payload
            tracemalloc.start()
            try:
                result, launched = invoke(value, streams)
                peak = tracemalloc.get_traced_memory()[1]
            finally:
                tracemalloc.stop()
            self.assertEqual(result["reason"], "MATCH")
            self.assertEqual(len(launched), 20)
            self.assertLess(peak, 8 * 1024 * 1024)
            self.assertEqual(result["observations"][9]["stdout_bytes"], 16 * 1024 * 1024)

    def test_index_stdout_and_entry_caps_and_blob_cap_plus_one(self):
        for target, payload, reason, step, count in (
            (6, b"x" * (2 * 1024 * 1024 + 1), "CAPTURE_LIMIT", "before.entries", 7),
            (9, b"x" * (16 * 1024 * 1024 + 1), "CAPTURE_LIMIT", "before.blob.000", 10),
            (6, b"".join(("H 100644 " + "c" * 40 + " 0\tp%04d\0" % n).encode() for n in range(8193)),
             "STATE_UNSUPPORTED", "before.entries", 7)):
            with self.subTest(target=target, size=len(payload)), PhysicalFixture():
                value = positive_contract()
                streams = outputs(value) * 2
                streams[target] = payload
                result, launched = invoke(value, streams)
                self.assertEqual((result["reason"], result["failed_step"], len(launched)), (reason, step, count))

    def test_races_between_and_during_scans_stop_without_later_success(self):
        for target, change_at, step in (("index", 10, "after.index"), ("config", 10, "after.index"),
                ("git-tool", 10, "after.index"), ("file", 10, "after.index"),
                ("metadata", 10, "after.index"), ("absence", 10, "after.paths"),
                ("file", 20, "final.files"), ("inventory", 10, "after.index")):
            with self.subTest(target=target, at=change_at), PhysicalFixture() as fixture:
                value = positive_contract()
                value["absent"] = ["future.txt"]

                def mutate(count):
                    if count != change_at:
                        return
                    if target in ("index", "config", "git-tool", "file"):
                        name = {"index": ".git/index", "config": ".git/config", "git-tool": "git-tool", "file": "docs/case.txt"}[target]
                        (fixture.root / name).write_bytes(b"abd")
                    elif target == "metadata":
                        os.utime(fixture.root / "docs/case.txt", ns=(1_000_000_000, 1_000_000_000))
                    elif target == "inventory":
                        (fixture.root / ".git/objects/pack/new.idx").write_bytes(b"abc")
                    else:
                        (fixture.root / "future.txt").write_bytes(b"abc")
                result, launched = invoke(value, mutate=mutate)
                self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                 ("OBSERVATION_DRIFT", step, change_at))
        with PhysicalFixture() as fixture, mock.patch("subprocess.Popen") as popen:
            original_read = os.read
            inode = (fixture.root / ".git/config").stat().st_ino
            changed = []

            def read(fd, size):
                chunk = original_read(fd, size)
                if os.fstat(fd).st_ino == inode and not changed:
                    os.utime(fixture.root / ".git/config", ns=(1_000_000_000, 1_000_000_000))
                    changed.append(True)
                return chunk
            with mock.patch("os.read", side_effect=read):
                result = checked(positive_contract())
            self.assertEqual((result["reason"], result["failed_step"]), ("OBSERVATION_DRIFT", "before.index"))
            popen.assert_not_called()

    def test_exact_full_result_repeated_bytes_and_record_order_permutations(self):
        value = positive_contract()
        value["delta"].append(delta_row(path="docs/new.txt", xy="??"))
        with PhysicalFixture() as fixture:
            (fixture.root / "docs/new.txt").write_bytes(b"abc")
            result, launched = invoke(value)
            steps = [phase + "." + label for phase in ("before", "after") for label in
                     ("root", "common", "branch", "head", "config", "shared", "entries", "status", "staged", "blob.000")]
            streams = outputs(value) * 2
            expected = dict(schema_version="yini-readonly-preflight/result-v2", work_unit_id="TEST-V2",
                contract_sha256=hashlib.sha256(encode(value)).hexdigest(), outcome="MATCH", reason="MATCH", exit_code=0,
                failed_step=None, child_returncode=None, observations=[dict(step=step, returncode=0,
                    stdout_sha256=hashlib.sha256(raw).hexdigest(), stderr_sha256=EMPTY,
                    stdout_bytes=len(raw), stderr_bytes=0, complete=True) for step, raw in zip(steps, streams)],
                fingerprint={key: value[key] for key in ("root", "common_dir", "branch", "head", "index_sha256",
                    "config_sha256", "index_tree_sha256", "state_kind", "staged", "delta", "absent")}, successor_authority=False)
            self.assertEqual(result, expected)
            second, _ = invoke(value)
            self.assertEqual(encode(result), encode(second))
            streams[7] = b"?? docs/new.txt\0M  docs/case.txt\0"
            streams[17] = outputs(value)[7]
            permuted, _ = invoke(value, streams)
            self.assertEqual(permuted["reason"], "MATCH")
            self.assertEqual(permuted["fingerprint"], expected["fingerprint"])
            self.assertNotEqual(permuted["observations"][7]["stdout_sha256"], result["observations"][7]["stdout_sha256"])
        with mock.patch("builtins.open") as opened, mock.patch("subprocess.Popen") as popen:
            fresh_spec = importlib.util.spec_from_file_location("v2_import_probe", SOURCE)
            fresh = importlib.util.module_from_spec(fresh_spec)
            fresh_spec.loader.exec_module(fresh)
            self.assertTrue(callable(fresh.verify) and callable(fresh.main))
            opened.assert_not_called()
            popen.assert_not_called()
