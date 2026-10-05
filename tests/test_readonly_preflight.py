"""Public seam regressions for the bounded read-only observer."""

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest import mock


SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "readonly_preflight.py"
spec = importlib.util.spec_from_file_location("readonly_preflight", SOURCE)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)

ROOT = "/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor"


def contract(**changes):
    value = {
        "schema_version": "yini-readonly-preflight/contract-v1",
        "work_unit_id": "TEST-1",
        "repository_id": "yini-insurance-advisor",
        "root": ROOT,
        "common_dir": ROOT + "/.git",
        "branch": "main",
        "head": "a" * 40,
        "index_sha256": "b" * 64,
        "staged": [],
        "delta": [],
        "absent": [],
        "ignored_inputs": "none",
        "git": {"path": "/usr/bin/git", "sha256": "c" * 64},
    }
    value.update(changes)
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode()


def checked(raw):
    return preflight.verify(raw, hashlib.sha256(raw).hexdigest())


class PhysicalFixture:
    """Map declared principal paths to disposable regular files at OS boundaries."""

    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".git").mkdir()
        (self.root / ".git" / "index").write_bytes(b"abc")
        (self.root / "docs").mkdir()
        (self.root / "docs" / "case.txt").write_bytes(b"abc")
        self.git = self.root / "git-tool"
        self.git.write_bytes(b"abc")
        self.git.chmod(0o755)
        self.old_lstat, self.old_open = os.lstat, os.open
        self.patches = [
            mock.patch.object(preflight.os, "getcwd", return_value=ROOT),
            mock.patch.object(preflight.os, "lstat", side_effect=self.lstat),
            mock.patch.object(preflight.os, "open", side_effect=self.open),
        ]
        for patcher in self.patches:
            patcher.start()
        return self

    def __exit__(self, *args):
        for patcher in reversed(self.patches):
            patcher.stop()
        self.temp.cleanup()

    def mapped(self, path):
        value = os.fspath(path)
        if value == "/usr/bin/git":
            return str(self.git)
        if value == ROOT or value.startswith(ROOT + "/"):
            return str(self.root) + value[len(ROOT):]
        return value

    def lstat(self, path, *args, **kwargs):
        return self.old_lstat(self.mapped(path), *args, **kwargs)

    def open(self, path, *args, **kwargs):
        return self.old_open(self.mapped(path), *args, **kwargs)


def physical_contract(**changes):
    row = {"path": "docs/case.txt", "xy": " M", "kind": "regular", "mode": "644",
           "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}
    values = {"index_sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
              "git": {"path": "/usr/bin/git", "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"},
              "delta": [row], "absent": ["out/new.txt"]}
    values.update(changes)
    return contract(**values)


class FakeInput:
    def __init__(self, data):
        self.buffer = io.BytesIO(data)


class FakeProcess:
    def __init__(self, stdout=b"", stderr=b"", returncode=0, wait_timeout=False):
        self.returncode = returncode
        self.wait_timeout = wait_timeout
        self.killed = False
        read_out, write_out = os.pipe()
        read_err, write_err = os.pipe()
        os.write(write_out, stdout)
        os.write(write_err, stderr)
        os.close(write_out)
        os.close(write_err)
        self.stdout = os.fdopen(read_out, "rb")
        self.stderr = os.fdopen(read_err, "rb")

    def wait(self, timeout=None):
        if self.wait_timeout and not self.killed:
            raise preflight.subprocess.TimeoutExpired("fixture-git", timeout)
        return self.returncode

    def poll(self):
        return self.returncode

    def kill(self):
        self.killed = True
        self.returncode = -9


class LargeFakeProcess(FakeProcess):
    def __init__(self, stream_name="stdout"):
        self.returncode = 0
        self.wait_timeout = False
        self.killed = False
        read_out, write_out = os.pipe()
        read_err, write_err = os.pipe()
        write_target = write_out if stream_name == "stdout" else write_err
        os.close(write_err if stream_name == "stdout" else write_out)
        self.stdout = os.fdopen(read_out, "rb")
        self.stderr = os.fdopen(read_err, "rb")

        def write_large_stream():
            try:
                remaining = 262145
                while remaining:
                    written = os.write(write_target, b"x" * min(65536, remaining))
                    remaining -= written
            except BrokenPipeError:
                pass
            finally:
                os.close(write_target)

        self.writer = threading.Thread(target=write_large_stream, daemon=True)
        self.writer.start()


class IsolatedEnvironmentTest(unittest.TestCase):
    def setUp(self):
        environment = mock.patch.dict(os.environ, {}, clear=True)
        environment.start()
        self.addCleanup(environment.stop)


class InputTests(IsolatedEnvironmentTest):
    def test_nested_closed_schema_and_delta_set_are_enforced(self):
        row = {"path": "docs/case.txt", "xy": " M", "kind": "regular",
               "mode": "644", "sha256": "a" * 64}
        cases = [
            contract(git={"path": "/usr/bin/git", "sha256": "c" * 64, "extra": 1}),
            contract(delta=[dict(row, extra=1)]),
            contract(delta=[row, row]),
            contract(delta=[dict(row, path="z"), row]),
            contract(delta=[row], absent=[row["path"]]),
        ]
        for raw in cases:
            with self.subTest(raw=raw), mock.patch.object(preflight.subprocess, "Popen") as popen:
                result = checked(raw)
                self.assertEqual((result["reason"], result["failed_step"], result["observations"]),
                                 ("CONTRACT_INVALID", "input", []))
                popen.assert_not_called()

    def test_cli_error_has_closed_envelope_and_delivery_failure_exits_nonzero(self):
        output = io.StringIO()
        with mock.patch.object(sys, "stdin", FakeInput(b"{}")), \
             mock.patch.object(sys, "stdout", output):
            code = preflight.main(["write-tree"])
        result = json.loads(output.getvalue())
        self.assertEqual((code, result["reason"], result["exit_code"]),
                         (2, "INVALID_INPUT", 2))
        self.assertEqual(set(result), {"schema_version", "work_unit_id", "contract_sha256",
                                       "outcome", "reason", "exit_code", "failed_step",
                                       "child_returncode", "observations", "fingerprint",
                                       "successor_authority"})
        self.assertEqual((result["observations"], result["fingerprint"],
                          result["successor_authority"]), ([], None, False))

        class BrokenOutput:
            def write(self, _text):
                raise BrokenPipeError("fixture stdout unavailable")

        with mock.patch.object(sys, "stdout", BrokenOutput()):
            self.assertEqual(preflight.main(["write-tree"]), 70)

    def test_main_reads_at_most_cap_plus_one_and_rejects_oversize(self):
        output = io.StringIO()
        with mock.patch.object(sys, "stdin", FakeInput(b"x" * 262145)), \
             mock.patch.object(sys, "stdout", output), \
             mock.patch.object(preflight.subprocess, "Popen") as popen:
            code = preflight.main(["verify", "--contract-sha256", "a" * 64])
        self.assertEqual(code, 2)
        result = json.loads(output.getvalue())
        self.assertEqual(result["reason"], "INVALID_INPUT")
        self.assertIsNone(result["contract_sha256"])
        self.assertEqual(result["failed_step"], "input")
        self.assertEqual(result["observations"], [])
        popen.assert_not_called()

    def test_cli_invalid_argv_and_oversize_stdin_have_literal_deterministic_envelopes(self):
        expected = {
            "schema_version": "yini-readonly-preflight/result-v1",
            "work_unit_id": None,
            "contract_sha256": None,
            "outcome": "STOP",
            "reason": "INVALID_INPUT",
            "exit_code": 2,
            "failed_step": "input",
            "child_returncode": None,
            "observations": [],
            "fingerprint": None,
            "successor_authority": False,
        }
        expected_bytes = (
            b'{"child_returncode":null,"contract_sha256":null,"exit_code":2,'
            b'"failed_step":"input","fingerprint":null,"observations":[],'
            b'"outcome":"STOP","reason":"INVALID_INPUT",'
            b'"schema_version":"yini-readonly-preflight/result-v1",'
            b'"successor_authority":false,"work_unit_id":null}\n'
        )
        cases = (
            (["write-tree"], b"{}"),
            (["verify", "--contract-sha256", "a" * 64, "extra"], b"{}"),
            (["verify", "--contract-sha256", "a" * 64], b"x" * 262145),
        )
        for argv, stdin_bytes in cases:
            outputs = []
            for _attempt in range(2):
                output = io.StringIO()
                with mock.patch.object(sys, "stdin", FakeInput(stdin_bytes)), \
                     mock.patch.object(sys, "stdout", output), \
                     mock.patch.object(preflight.subprocess, "Popen") as popen:
                    self.assertEqual(preflight.main(list(argv)), 2)
                payload = output.getvalue()
                self.assertEqual(json.loads(payload), expected)
                self.assertEqual(payload.encode("ascii"), expected_bytes)
                popen.assert_not_called()
                outputs.append(payload)
            self.assertEqual(outputs[0], outputs[1])

    def test_import_defines_public_seams_without_starting_process(self):
        with mock.patch.object(preflight.subprocess, "Popen") as popen:
            fresh_spec = importlib.util.spec_from_file_location("readonly_preflight_import_probe", SOURCE)
            fresh = importlib.util.module_from_spec(fresh_spec)
            fresh_spec.loader.exec_module(fresh)
            self.assertTrue(callable(fresh.verify))
            self.assertTrue(callable(fresh.main))
            popen.assert_not_called()

    def test_cli_denies_commands_and_shell_text_without_process(self):
        for argv in (["write-tree"], ["add"], ["update-index"],
                     ["verify;true"], ["verify|true"], ["verify`true`"],
                     ["verify", "--contract-sha256", "a" * 64, "extra"],
                     ["verify", "--contract-sha256", "$(git write-tree)"],
                     ["verify", "--contract-sha256", "a" * 64, "--raw-argv"]):
            with self.subTest(argv=argv), mock.patch.object(preflight.subprocess, "Popen") as popen:
                output = io.StringIO()
                with mock.patch.object(sys, "stdin", FakeInput(b"{}")), mock.patch.object(sys, "stdout", output):
                    code = preflight.main(list(argv))
                self.assertEqual(code, 2)
                self.assertEqual(json.loads(output.getvalue())["reason"], "INVALID_INPUT")
                popen.assert_not_called()

    def test_invalid_contracts_stop_before_process(self):
        missing = json.loads(contract())
        del missing["head"]
        cases = [
            (b"\xef\xbb\xbf{}", "INVALID_INPUT"),
            (b"\xff", "INVALID_INPUT"),
            (b"{" + b" " * 262144 + b"}", "INVALID_INPUT"),
            (b'{"x":1,"x":2}', "INVALID_INPUT"),
            (b'{"schema_version":"x","schema_version":"y"}', "INVALID_INPUT"),
            (b'{}{}', "INVALID_INPUT"),
            (b'{"n":NaN}', "INVALID_INPUT"),
            (json.dumps(missing).encode(), "CONTRACT_INVALID"),
            (contract(extra=1), "CONTRACT_INVALID"),
            (contract(repository_id="other"), "CONTRACT_INVALID"),
            (contract(root="/other"), "CONTRACT_INVALID"),
            (contract(staged=[False]), "CONTRACT_INVALID"),
            (contract(ignored_inputs=False), "CONTRACT_INVALID"),
            (contract(delta=False), "CONTRACT_INVALID"),
            (contract(absent=["other", "other"]), "CONTRACT_INVALID"),
            (contract(absent=["z", "a"]), "CONTRACT_INVALID"),
            (contract(delta=[{"path": "../x", "xy": "??", "kind": "regular", "mode": "644", "sha256": "a" * 64}]), "PATH_UNSAFE"),
        ]
        for unsafe in ("/absolute", "a//b", "a/./b", "a/../b", "a\\b", "a;true",
                       "a\nb", ".git/index", ".venv/lib", "data/x", "corpus/x", ".env.local"):
            cases.append((contract(absent=[unsafe]), "PATH_UNSAFE"))
        for raw, reason in cases:
            with self.subTest(raw=raw[:60]), mock.patch.object(preflight.subprocess, "Popen") as popen:
                self.assertEqual(checked(raw)["reason"], reason)
                popen.assert_not_called()
        raw = contract()
        with mock.patch.object(preflight.subprocess, "Popen") as popen:
            self.assertEqual(preflight.verify(raw, "0" * 64)["reason"], "CONTRACT_HASH_MISMATCH")
            self.assertEqual(preflight.verify(raw + b" ", hashlib.sha256(raw).hexdigest())["reason"],
                             "CONTRACT_HASH_MISMATCH")
            popen.assert_not_called()


class FileTests(IsolatedEnvironmentTest):
    def test_select_failure_and_select_timeout_keep_partial_record(self):
        class Selection:
            def __init__(self, failure):
                self.failure = failure

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def register(self, *_args):
                return None

            def get_map(self):
                return {"pending": True}

            def select(self, _timeout):
                if self.failure == "error":
                    raise OSError("fixture select failed")
                return []

        for failure, reason in (("error", "INTERNAL_DEFECT"), ("timeout", "TIMEOUT")):
            with self.subTest(failure=failure), PhysicalFixture() as fixture:
                (fixture.root / "out").mkdir()
                processes = []

                def launch(_argv, **_options):
                    process = FakeProcess(stdout=b"abc")
                    processes.append(process)
                    return process

                with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch), \
                     mock.patch.object(preflight.selectors, "DefaultSelector",
                                       side_effect=lambda: Selection(failure)):
                    result = checked(physical_contract())
                self.assertEqual((result["reason"], result["failed_step"], len(processes)),
                                 (reason, "before.root", 1))
                self.assertTrue(processes[0].killed)
                self.assertEqual(result["observations"], [{
                    "step": "before.root", "returncode": None,
                    "stdout_sha256": hashlib.sha256(b"").hexdigest(),
                    "stderr_sha256": hashlib.sha256(b"").hexdigest(),
                    "stdout_bytes": 0, "stderr_bytes": 0, "complete": False,
                }])

    def test_deadline_during_pipe_capture_preserves_partial_bytes(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            processes = []

            def launch(_argv, **_options):
                process = FakeProcess(stdout=b"abc")
                processes.append(process)
                return process

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch), \
                 mock.patch.object(preflight.time, "monotonic", side_effect=[0, 0, 6]):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(processes)),
                             ("TIMEOUT", "before.root", 1))
            self.assertTrue(processes[0].killed)
            self.assertEqual(result["observations"], [{
                "step": "before.root", "returncode": None,
                "stdout_sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
                "stderr_sha256": hashlib.sha256(b"").hexdigest(),
                "stdout_bytes": 3, "stderr_bytes": 0, "complete": False,
            }])

    def test_wait_failure_keeps_captured_bytes_when_reap_fails(self):
        class WaitFails(FakeProcess):
            def __init__(self):
                super().__init__(stdout=b"abc")
                self.waits = 0

            def wait(self, timeout=None):
                self.waits += 1
                raise preflight.subprocess.TimeoutExpired("fixture-git", timeout)

        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            processes = []

            def launch(_argv, **_options):
                process = WaitFails()
                processes.append(process)
                return process

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(processes)),
                             ("INTERNAL_DEFECT", "before.root", 1))
            self.assertTrue(processes[0].killed)
            self.assertEqual(processes[0].waits, 2)
            self.assertEqual(result["observations"], [{
                "step": "before.root", "returncode": None,
                "stdout_sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
                "stderr_sha256": hashlib.sha256(b"").hexdigest(),
                "stdout_bytes": 3, "stderr_bytes": 0, "complete": False,
            }])

    def test_wait_os_error_keeps_step_and_partial_record(self):
        class WaitOsFails(FakeProcess):
            def wait(self, timeout=None):
                raise OSError("fixture wait failed")

        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            processes = []

            def launch(_argv, **_options):
                process = WaitOsFails(stdout=b"abc")
                processes.append(process)
                return process

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(processes)),
                             ("INTERNAL_DEFECT", "before.root", 1))
            self.assertTrue(processes[0].killed)
            self.assertEqual(result["observations"], [{
                "step": "before.root", "returncode": None,
                "stdout_sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
                "stderr_sha256": hashlib.sha256(b"").hexdigest(),
                "stdout_bytes": 3, "stderr_bytes": 0, "complete": False,
            }])

    def test_capture_registration_and_kill_failure_keep_step_and_record(self):
        class KillFails(FakeProcess):
            def __init__(self):
                super().__init__(stdout=b"abc")
                self.waits = 0

            def kill(self):
                raise OSError("fixture kill failed")

            def wait(self, timeout=None):
                self.waits += 1
                return super().wait(timeout)

        class RegisterFails:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def register(self, *_args):
                raise OSError("fixture register failed")

        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            processes = []

            def launch(_argv, **_options):
                process = KillFails()
                processes.append(process)
                return process

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch), \
                 mock.patch.object(preflight.selectors, "DefaultSelector", side_effect=RegisterFails):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(processes)),
                             ("INTERNAL_DEFECT", "before.root", 1))
            self.assertEqual(processes[0].waits, 1)
            self.assertEqual(result["observations"], [{
                "step": "before.root", "returncode": None,
                "stdout_sha256": hashlib.sha256(b"").hexdigest(),
                "stderr_sha256": hashlib.sha256(b"").hexdigest(),
                "stdout_bytes": 0, "stderr_bytes": 0, "complete": False,
            }])

    def test_capture_read_error_records_partial_bytes_and_reaps(self):
        class TrackedProcess(FakeProcess):
            def __init__(self):
                super().__init__(stdout=b"abc")
                self.waits = 0

            def wait(self, timeout=None):
                self.waits += 1
                return super().wait(timeout)

        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            processes = []
            original_read = os.read
            pipe_reads = []
            regular_reads = []

            def launch(_argv, **_options):
                process = TrackedProcess()
                processes.append(process)
                return process

            def interrupted_read(descriptor, size):
                if processes and descriptor == processes[0].stdout.fileno():
                    if pipe_reads:
                        raise OSError("fixture pipe read failed")
                    pipe_reads.append(True)
                else:
                    regular_reads.append(descriptor)
                return original_read(descriptor, size)

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch), \
                 mock.patch.object(preflight.os, "read", side_effect=interrupted_read):
                regular = os.open(fixture.root / "docs" / "case.txt", os.O_RDONLY)
                try:
                    self.assertEqual(os.read(regular, 3), b"abc")
                finally:
                    os.close(regular)
                self.assertEqual(pipe_reads, [])
                self.assertEqual(len(regular_reads), 1)
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(processes)),
                             ("INTERNAL_DEFECT", "before.root", 1))
            self.assertTrue(processes[0].killed)
            self.assertEqual(processes[0].waits, 1)
            self.assertEqual(result["observations"], [{
                "step": "before.root", "returncode": None,
                "stdout_sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
                "stderr_sha256": hashlib.sha256(b"").hexdigest(),
                "stdout_bytes": 3, "stderr_bytes": 0, "complete": False,
            }])

    def test_all_declared_paths_are_guarded_before_index_hashes(self):
        with PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
            (fixture.root / "out").mkdir()
            (fixture.root / "out" / "new.txt").symlink_to(fixture.root / "missing")
            result = checked(physical_contract(index_sha256="0" * 64))
            self.assertEqual((result["reason"], result["failed_step"]),
                             ("PATH_UNSAFE", "paths"))
            popen.assert_not_called()

    def test_regular_file_guards_precede_initial_content_hashes(self):
        for target, kind in ((target, kind) for target in ("index", "executable", "delta")
                             for kind in ("missing", "directory", "hardlink")):
            with self.subTest(target=target, kind=kind), PhysicalFixture() as fixture:
                (fixture.root / "out").mkdir()
                (fixture.root / ".git" / "index").write_bytes(b"abd")
                candidate = {"index": fixture.root / ".git" / "index",
                             "executable": fixture.git,
                             "delta": fixture.root / "docs" / "case.txt"}[target]
                if kind == "missing":
                    candidate.unlink()
                elif kind == "directory":
                    candidate.unlink()
                    candidate.mkdir()
                else:
                    os.link(candidate, fixture.root / "out" / "other")
                opened = []

                def tracked_open(candidate_path, *args, **kwargs):
                    opened.append(candidate_path)
                    return fixture.open(candidate_path, *args, **kwargs)

                with mock.patch.object(preflight.os, "open", side_effect=tracked_open), \
                     mock.patch.object(preflight.subprocess, "Popen") as popen:
                    result = checked(physical_contract())
                self.assertEqual((result["reason"], result["failed_step"]),
                                 ("TOOL_IDENTITY_MISMATCH" if target == "executable"
                                  else "OBSERVATION_MISMATCH", "paths"))
                self.assertEqual(opened, [])
                popen.assert_not_called()

    def test_regular_file_guards_precede_after_content_hashes(self):
        for target, kind in ((target, kind) for target in ("index", "executable", "delta")
                             for kind in ("missing", "directory", "hardlink")):
            with self.subTest(target=target, kind=kind), PhysicalFixture() as fixture:
                (fixture.root / "out").mkdir()
                outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                           b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""]
                opened = []
                count_before_after_scan = []

                def launch(_argv, **_options):
                    if len(count_before_after_scan) == 0 and len(outputs) == 1:
                        (fixture.root / ".git" / "index").write_bytes(b"abd")
                        candidate = {"index": fixture.root / ".git" / "index",
                                     "executable": fixture.git,
                                     "delta": fixture.root / "docs" / "case.txt"}[target]
                        if kind == "missing":
                            candidate.unlink()
                        elif kind == "directory":
                            candidate.unlink()
                            candidate.mkdir()
                        else:
                            os.link(candidate, fixture.root / "out" / "other")
                        count_before_after_scan.append(len(opened))
                    return FakeProcess(stdout=outputs.pop(0))

                def tracked_open(candidate_path, *args, **kwargs):
                    opened.append(candidate_path)
                    return fixture.open(candidate_path, *args, **kwargs)

                with mock.patch.object(preflight.os, "open", side_effect=tracked_open), \
                     mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                    result = checked(physical_contract())
                self.assertEqual((result["reason"], result["failed_step"]),
                                 ("OBSERVATION_DRIFT", "after.paths"))
                self.assertEqual(len(count_before_after_scan), 1)
                self.assertEqual(len(opened), count_before_after_scan[0])
                self.assertEqual(len(result["observations"]), 6)

    def test_regular_file_changes_during_hashing_keep_the_index_phase(self):
        for process_count, expected_step, reason in (
            (0, "before.index", "OBSERVATION_MISMATCH"),
            (6, "after.index", "OBSERVATION_DRIFT"),
        ):
            for kind in ("missing", "directory", "hardlink"):
                with self.subTest(step=expected_step, kind=kind), PhysicalFixture() as fixture:
                    (fixture.root / "out").mkdir()
                    candidate = fixture.root / "docs" / "case.txt"
                    outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                               b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""]
                    launched = []
                    changed = []

                    def launch(_argv, **_options):
                        launched.append(True)
                        return FakeProcess(stdout=outputs[len(launched) - 1])

                    def change_after_guards(candidate_path, *args, **kwargs):
                        descriptor = fixture.open(candidate_path, *args, **kwargs)
                        if (candidate_path == ROOT + "/.git/index"
                                and len(launched) == process_count and not changed):
                            if kind == "missing":
                                candidate.unlink()
                            elif kind == "directory":
                                candidate.unlink()
                                candidate.mkdir()
                            else:
                                os.link(candidate, fixture.root / "out" / "other")
                            changed.append(True)
                        return descriptor

                    with mock.patch.object(preflight.os, "open", side_effect=change_after_guards), \
                         mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                        result = checked(physical_contract())
                    self.assertEqual(changed, [True])
                    self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                     (reason, expected_step, process_count))

    def test_after_paths_precedes_after_index_hashes(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                       b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""]
            launched = []

            def launch(_argv, **_options):
                launched.append(True)
                if len(launched) == 6:
                    (fixture.root / ".git" / "index").write_bytes(b"abd")
                    (fixture.root / "out" / "new.txt").symlink_to(fixture.root / "missing")
                return FakeProcess(stdout=outputs[len(launched) - 1])

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                             ("PATH_UNSAFE", "after.paths", 6))

    def test_timeout_reaps_child_that_exited_before_kill(self):
        class ExitedDuringKill(FakeProcess):
            def kill(self):
                self.killed = True
                self.returncode = 0
                raise ProcessLookupError("already exited")

        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            launched = []

            def launch(_argv, **_options):
                process = ExitedDuringKill(wait_timeout=True)
                launched.append(process)
                return process

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                             ("TIMEOUT", "before.root", 1))

    def test_metadata_change_during_file_read_stops_before_git(self):
        with PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
            (fixture.root / "out").mkdir()
            candidate = fixture.root / "docs" / "case.txt"
            target_inode = candidate.stat().st_ino
            original_read = os.read
            changed = []

            def read_and_change(descriptor, size):
                chunk = original_read(descriptor, size)
                if not changed and os.fstat(descriptor).st_ino == target_inode:
                    os.utime(candidate, ns=(1_000_000_000, 1_000_000_000))
                    changed.append(True)
                return chunk

            with mock.patch.object(preflight.os, "read", side_effect=read_and_change):
                result = checked(physical_contract())
            self.assertEqual(changed, [True])
            self.assertEqual((result["reason"], result["failed_step"]),
                             ("OBSERVATION_DRIFT", "before.index"))
            popen.assert_not_called()

    def test_aggregate_scan_limit_stops_before_process(self):
        with PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
            size = 15 * 1024 * 1024
            zero_hash = hashlib.sha256()
            for _ in range(15):
                zero_hash.update(b"\0" * (1024 * 1024))
            rows = []
            for number in range(5):
                name = "docs/large-" + str(number)
                with (fixture.root / name).open("wb") as handle:
                    handle.truncate(size)
                rows.append({"path": name, "xy": "??", "kind": "regular", "mode": "644",
                             "sha256": zero_hash.hexdigest()})
            result = checked(physical_contract(delta=rows, absent=[]))
            self.assertEqual((result["reason"], result["failed_step"]),
                             ("OBSERVATION_MISMATCH", "before.index"))
            popen.assert_not_called()

    def test_oversized_governed_file_stops_before_process(self):
        with PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
            (fixture.root / "out").mkdir()
            with (fixture.root / "docs" / "case.txt").open("r+b") as handle:
                handle.truncate(16 * 1024 * 1024 + 1)
            result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"]),
                             ("OBSERVATION_MISMATCH", "before.index"))
            popen.assert_not_called()

    def test_changed_file_between_observations_stops_before_second_git(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                       b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""]
            launched = []

            def launch(_argv, **_options):
                launched.append(True)
                if len(launched) == 6:
                    (fixture.root / "docs" / "case.txt").write_bytes(b"abd")
                return FakeProcess(stdout=outputs[len(launched) - 1])

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                             ("OBSERVATION_DRIFT", "after.index", 6))

    def test_other_bound_physical_changes_between_scans_are_drift(self):
        for kind in ("index", "executable", "mode", "absence"):
            with self.subTest(kind=kind), PhysicalFixture() as fixture:
                (fixture.root / "out").mkdir()
                outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                           b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""]
                launched = []

                def launch(_argv, **_options):
                    launched.append(True)
                    if len(launched) == 6:
                        if kind == "index":
                            (fixture.root / ".git" / "index").write_bytes(b"abd")
                        elif kind == "executable":
                            fixture.git.write_bytes(b"abd")
                        elif kind == "mode":
                            (fixture.root / "docs" / "case.txt").chmod(0o755)
                        else:
                            (fixture.root / "out" / "new.txt").write_bytes(b"abc")
                    return FakeProcess(stdout=outputs[len(launched) - 1])

                with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                    result = checked(physical_contract())
                self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                 ("OBSERVATION_DRIFT", "after.paths" if kind == "absence" else "after.index", 6))

    def test_metadata_only_change_between_scans_stops_at_its_scan(self):
        for change_at, expected_step in ((6, "after.index"), (12, "final.files")):
            with self.subTest(step=expected_step), PhysicalFixture() as fixture:
                (fixture.root / "out").mkdir()
                outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                           b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""] * 2
                launched = []

                def launch(_argv, **_options):
                    launched.append(True)
                    if len(launched) == change_at:
                        os.utime(fixture.root / "docs" / "case.txt",
                                 ns=(1_000_000_000, 1_000_000_000))
                    return FakeProcess(stdout=outputs[len(launched) - 1])

                with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                    result = checked(physical_contract())
                self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                 ("OBSERVATION_DRIFT", expected_step, change_at))

    def test_second_status_drift_stops_before_final_staged_probe(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                       b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""] * 2
            outputs[10] = b"?? extra.txt\0"
            launched = []

            def launch(_argv, **_options):
                launched.append(True)
                return FakeProcess(stdout=outputs[len(launched) - 1])

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                             ("OBSERVATION_DRIFT", "after.status", 11))

    def test_disappeared_file_between_observations_is_drift(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                       b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""]
            launched = []

            def launch(_argv, **_options):
                launched.append(True)
                if len(launched) == 6:
                    (fixture.root / "docs" / "case.txt").unlink()
                return FakeProcess(stdout=outputs[len(launched) - 1])

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                             ("OBSERVATION_DRIFT", "after.paths", 6))

    def test_changed_cwd_between_observations_fails_at_after_paths(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                       b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""]
            launched = []

            def launch(_argv, **_options):
                launched.append(True)
                return FakeProcess(stdout=outputs[len(launched) - 1])

            with mock.patch.object(preflight.os, "getcwd", side_effect=[ROOT, "/different"]), \
                 mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                             ("CHECKOUT_UNSUPPORTED", "after.paths", 6))

    def test_wrong_initial_cwd_fails_at_paths_without_git(self):
        raw = physical_contract()
        with mock.patch.object(preflight.os, "getcwd", return_value="/different"), \
             mock.patch.object(preflight.subprocess, "Popen") as popen:
            result = checked(raw)
        self.assertEqual((result["reason"], result["failed_step"]),
                         ("CHECKOUT_UNSUPPORTED", "paths"))
        popen.assert_not_called()

    def test_capture_cap_plus_one_stops_and_reaps(self):
        for stream_name in ("stdout", "stderr"):
            with self.subTest(stream=stream_name), PhysicalFixture() as fixture:
                (fixture.root / "out").mkdir()
                processes = []

                def launch(_argv, **_options):
                    process = LargeFakeProcess(stream_name)
                    processes.append(process)
                    return process

                with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                    result = checked(physical_contract())
                self.assertEqual((result["reason"], result["failed_step"], result["exit_code"]),
                                 ("CAPTURE_LIMIT", "before.root", 125))
                self.assertEqual(len(processes), 1)
                self.assertTrue(processes[0].killed)
                self.assertFalse(result["observations"][0]["complete"])
                processes[0].writer.join(timeout=1)
                self.assertFalse(processes[0].writer.is_alive())

    def test_unsafe_physical_files_stop_before_process(self):
        for kind, reason in (("symlink_file", "PATH_UNSAFE"),
                             ("symlink_ancestor", "PATH_UNSAFE"),
                             ("hardlink", "OBSERVATION_MISMATCH"),
                             ("nonregular_file", "OBSERVATION_MISMATCH"),
                             ("missing_index", "OBSERVATION_MISMATCH"),
                             ("dangling_absent", "PATH_UNSAFE")):
            with self.subTest(kind=kind), PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
                (fixture.root / "out").mkdir()
                if kind == "symlink_file":
                    (fixture.root / "docs" / "case.txt").unlink()
                    (fixture.root / "docs" / "case.txt").symlink_to(fixture.root / "git-tool")
                elif kind == "symlink_ancestor":
                    (fixture.root / "linked").symlink_to(fixture.root / "docs", target_is_directory=True)
                elif kind == "hardlink":
                    os.link(fixture.root / "docs" / "case.txt", fixture.root / "out" / "other")
                elif kind == "nonregular_file":
                    (fixture.root / "docs" / "case.txt").unlink()
                    (fixture.root / "docs" / "case.txt").mkdir()
                elif kind == "missing_index":
                    (fixture.root / ".git" / "index").unlink()
                elif kind == "dangling_absent":
                    (fixture.root / "out" / "new.txt").symlink_to(fixture.root / "missing")
                raw = (physical_contract(delta=[{"path": "linked/case.txt", "xy": " M", "kind": "regular",
                                                "mode": "644", "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}])
                       if kind == "symlink_ancestor" else physical_contract())
                result = checked(raw)
                self.assertEqual((result["reason"], result["failed_step"]), (reason, "paths"))
                popen.assert_not_called()

    def test_worktree_style_git_file_is_unsupported_before_process(self):
        with PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
            (fixture.root / ".git" / "index").unlink()
            (fixture.root / ".git").rmdir()
            (fixture.root / ".git").write_text("gitdir: elsewhere\n")
            result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"]),
                             ("CHECKOUT_UNSUPPORTED", "paths"))
            popen.assert_not_called()

    def test_malformed_or_unexpected_status_stops_at_status_probe(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            prefix = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                      b"main\n", b"a" * 40 + b"\n"]
            cases = [
                b" M docs/case.txt", b" M docs/case.txt\0 M docs/case.txt\0",
                b"?? extra.txt\0", b"", b" M docs/case.txt\0?? extra.txt\0",
                b"R  docs/case.txt\0other.txt\0", b"?? folder/\0",
                b"?? bad\xff.txt\0", b"?? ../escape\0", b"AM docs/case.txt\0",
            ]
            for bad in cases:
                launched = []

                def launch(_argv, **_options):
                    launched.append(True)
                    return FakeProcess(stdout=(prefix + [bad])[len(launched) - 1])

                with self.subTest(status=bad), mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                    result = checked(physical_contract())
                    self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                     ("OBSERVATION_MISMATCH", "before.status", 5))

    def test_unexpected_status_path_is_never_opened(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            outputs = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                       b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0?? extra.txt\0"]
            launched = []
            opened = []

            def launch(_argv, **_options):
                launched.append(True)
                return FakeProcess(stdout=outputs[len(launched) - 1])

            def tracked_open(candidate, *args, **kwargs):
                opened.append(candidate)
                return fixture.open(candidate, *args, **kwargs)

            with mock.patch.object(preflight.os, "open", side_effect=tracked_open), \
                 mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                result = checked(physical_contract())
            self.assertEqual(result["failed_step"], "before.status")
            self.assertNotIn(ROOT + "/extra.txt", opened)
            self.assertEqual(len(launched), 5)

    def test_scalar_and_staged_mismatch_stop_at_first_probe(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            baseline = [(ROOT + "\n").encode(), (ROOT + "/.git\n").encode(),
                        b"main\n", b"a" * 40 + b"\n", b" M docs/case.txt\0", b""]
            for position, bad, step in (
                (0, b"/wrong\n", "before.root"),
                (1, b"/wrong\n", "before.common"),
                (2, b"other\n", "before.branch"),
                (3, b"b" * 40 + b"\n", "before.head"),
                (5, b"M\0docs/case.txt\0", "before.staged"),
            ):
                outputs = baseline.copy()
                outputs[position] = bad
                launched = []

                def launch(_argv, **_options):
                    launched.append(True)
                    return FakeProcess(stdout=outputs[len(launched) - 1])

                with self.subTest(step=step), mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                    result = checked(physical_contract())
                    self.assertEqual((result["reason"], result["failed_step"], len(launched)),
                                     ("OBSERVATION_MISMATCH", step, position + 1))

    def test_process_signal_launch_and_timeout_stop_without_successor(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            raw = physical_contract()
            cases = [
                (lambda *_args, **_kwargs: FakeProcess(returncode=-9), "GIT_EXIT", 137, -9, True),
                (OSError("fixture launch"), "PROCESS_LAUNCH_ERROR", 5, None, False),
                (lambda *_args, **_kwargs: FakeProcess(wait_timeout=True), "TIMEOUT", 124, None, False),
            ]
            for process, reason, code, child_code, complete in cases:
                with self.subTest(reason=reason), mock.patch.object(preflight.subprocess, "Popen", side_effect=process) as popen:
                    output = io.StringIO()
                    with mock.patch.object(sys, "stdin", FakeInput(raw)), mock.patch.object(sys, "stdout", output):
                        returned = preflight.main(["verify", "--contract-sha256", hashlib.sha256(raw).hexdigest()])
                    result = json.loads(output.getvalue())
                    self.assertEqual((returned, result["reason"], result["child_returncode"], result["failed_step"]),
                                     (code, reason, child_code, "before.root"))
                    self.assertEqual(result["observations"][0]["complete"], complete)
                    popen.assert_called_once()

    def test_executable_digest_mismatch_has_distinct_reason_before_git(self):
        with PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
            (fixture.root / "out").mkdir()
            raw = physical_contract(git={"path": "/usr/bin/git", "sha256": "0" * 64})
            result = checked(raw)
            self.assertEqual((result["reason"], result["failed_step"]),
                             ("TOOL_IDENTITY_MISMATCH", "before.index"))
            popen.assert_not_called()

    def test_missing_bound_executable_has_distinct_reason_before_git(self):
        with PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
            (fixture.root / "out").mkdir()
            fixture.git.unlink()
            result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"]),
                             ("TOOL_IDENTITY_MISMATCH", "paths"))
            popen.assert_not_called()

    def test_raw_index_and_file_hash_before_any_git(self):
        with PhysicalFixture() as fixture, mock.patch.object(
            preflight.subprocess, "Popen", side_effect=lambda *_args, **_kwargs:
            FakeProcess(stdout=(ROOT + "\n").encode("ascii"))) as popen:
            (fixture.root / "out").mkdir()
            result = checked(physical_contract())
            self.assertEqual(result["failed_step"], "before.common")
            self.assertEqual(result["reason"], "OBSERVATION_MISMATCH")
            self.assertEqual(result["observations"][0]["stdout_bytes"], len(ROOT) + 1)
            self.assertTrue(result["observations"][0]["complete"])
            self.assertEqual(popen.call_count, 2)

    def test_index_file_mode_and_absence_mismatch_stay_before_git(self):
        with PhysicalFixture() as fixture, mock.patch.object(preflight.subprocess, "Popen") as popen:
            (fixture.root / "out").mkdir()
            cases = [
                (physical_contract(index_sha256="0" * 64), "OBSERVATION_MISMATCH"),
                (physical_contract(delta=[{"path": "docs/case.txt", "xy": " M", "kind": "regular", "mode": "644", "sha256": "0" * 64}]), "OBSERVATION_MISMATCH"),
                (physical_contract(delta=[{"path": "docs/case.txt", "xy": " M", "kind": "regular", "mode": "755", "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}]), "OBSERVATION_MISMATCH"),
            ]
            for raw, reason in cases:
                with self.subTest(reason=reason):
                    result = checked(raw)
                    self.assertEqual((result["reason"], result["failed_step"]),
                                     (reason, "before.index"))
            (fixture.root / "out" / "new.txt").write_bytes(b"present")
            result = checked(physical_contract())
            self.assertEqual((result["reason"], result["failed_step"]),
                             ("OBSERVATION_MISMATCH", "paths"))
            popen.assert_not_called()

    def test_git_exit_128_preserves_child_and_stops(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out").mkdir()
            launched = []
            queued = [lambda: FakeProcess(stderr=b"fatal", returncode=128),
                      lambda: FakeProcess(stdout=(ROOT + "\n").encode())]

            def launch(argv, **options):
                launched.append((argv, options))
                return queued.pop(0)()

            raw = physical_contract()
            output = io.StringIO()
            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                with mock.patch.object(sys, "stdin", FakeInput(raw)), mock.patch.object(sys, "stdout", output):
                    code = preflight.main(["verify", "--contract-sha256", hashlib.sha256(raw).hexdigest()])
            result = json.loads(output.getvalue())
            self.assertEqual(code, 128)
            self.assertEqual((result["reason"], result["child_returncode"], result["failed_step"]),
                             ("GIT_EXIT", 128, "before.root"))
            self.assertEqual(len(launched), 1)
            self.assertEqual(len(queued), 1)
            self.assertEqual(launched[0][0], (
                "/usr/bin/git", "--no-pager", "--no-optional-locks",
                "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false",
                "-c", "core.hooksPath=/dev/null", "-c", "diff.external=",
                "rev-parse", "--show-toplevel"))
            self.assertEqual(launched[0][1]["shell"], False)
            self.assertEqual(launched[0][1]["env"], {
                "PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C", "TZ": "UTC",
                "HOME": "/dev/null", "XDG_CONFIG_HOME": "/dev/null",
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": "/dev/null",
                "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_ATTR_NOSYSTEM": "1",
                "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0",
                "GIT_NO_REPLACE_OBJECTS": "1"})

    def test_positive_child_exit_codes_propagate_and_stop(self):
        for child_code in (1, 7, 255):
            with self.subTest(child_code=child_code), PhysicalFixture() as fixture:
                (fixture.root / "out").mkdir()
                raw = physical_contract()
                output = io.StringIO()
                with mock.patch.object(preflight.subprocess, "Popen",
                                       side_effect=lambda *_args, **_options:
                                       FakeProcess(returncode=child_code)) as popen, \
                     mock.patch.object(sys, "stdin", FakeInput(raw)), \
                     mock.patch.object(sys, "stdout", output):
                    code = preflight.main(["verify", "--contract-sha256",
                                           hashlib.sha256(raw).hexdigest()])
                result = json.loads(output.getvalue())
                self.assertEqual((code, result["exit_code"], result["reason"],
                                  result["child_returncode"], result["failed_step"]),
                                 (child_code, child_code, "GIT_EXIT", child_code,
                                  "before.root"))
                self.assertEqual(len(result["observations"]), 1)
                popen.assert_called_once()

    def test_environment_rejects_inherited_git_redirect_and_bytecode(self):
        raw = contract()
        for name in ("GIT_INDEX_FILE", "GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_COUNT", "GIT_PAGER"):
            with self.subTest(name=name), mock.patch.dict(preflight.os.environ, {name: "fixture-value"}), mock.patch.object(preflight.subprocess, "Popen") as popen:
                self.assertEqual(checked(raw)["reason"], "ENVIRONMENT_UNSUPPORTED")
                popen.assert_not_called()
        with mock.patch.object(sys, "dont_write_bytecode", False), mock.patch.object(preflight.subprocess, "Popen") as popen:
            self.assertEqual(checked(raw)["reason"], "ENVIRONMENT_UNSUPPORTED")
            popen.assert_not_called()

    def test_two_complete_observations_match_nonempty_status(self):
        with PhysicalFixture() as fixture:
            (fixture.root / "out" / "nested").mkdir(parents=True)
            (fixture.root / "out" / "nested" / "new.txt").write_bytes(b"abc")
            digest = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
            rows = [
                {"path": "docs/case.txt", "xy": " M", "kind": "regular", "mode": "644", "sha256": digest},
                {"path": "out/nested/new.txt", "xy": "??", "kind": "regular", "mode": "644", "sha256": digest},
            ]
            raw = physical_contract(delta=rows, absent=["out/missing.txt"])
            outputs = [
                (ROOT + "\n").encode(), (ROOT + "/.git\n").encode(), b"main\n",
                b"a" * 40 + b"\n", b" M docs/case.txt\0?? out/nested/new.txt\0", b"",
            ] * 2
            steps = [phase + "." + label for phase in ("before", "after") for label in
                     ("root", "common", "branch", "head", "status", "staged")]
            launched = []

            def launch(argv, **options):
                launched.append((argv, options))
                return FakeProcess(stdout=outputs[len(launched) - 1])

            def invoke():
                output = io.StringIO()
                with mock.patch.object(sys, "stdin", FakeInput(raw)), mock.patch.object(sys, "stdout", output):
                    code = preflight.main(["verify", "--contract-sha256", hashlib.sha256(raw).hexdigest()])
                return code, output.getvalue()

            with mock.patch.object(preflight.subprocess, "Popen", side_effect=launch):
                first_code, first_json = invoke()
                self.assertEqual(first_code, 0)
                self.assertEqual(len(launched), 12)
                prefix = ("/usr/bin/git", "--no-pager", "--no-optional-locks",
                          "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false",
                          "-c", "core.hooksPath=/dev/null", "-c", "diff.external=")
                suffixes = (
                    ("rev-parse", "--show-toplevel"),
                    ("rev-parse", "--path-format=absolute", "--git-common-dir"),
                    ("symbolic-ref", "--quiet", "--short", "HEAD"),
                    ("rev-parse", "HEAD"),
                    ("status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=all"),
                    ("diff", "--cached", "--name-status", "-z", "--no-ext-diff", "--no-textconv", "--ignore-submodules=none"),
                ) * 2
                self.assertEqual([argv for argv, _options in launched],
                                 [prefix + suffix for suffix in suffixes])
                for _argv, options in launched:
                    self.assertEqual(options["shell"], False)
                    self.assertEqual(options["cwd"], ROOT)
                    self.assertEqual(options["stdin"], preflight.subprocess.DEVNULL)
                    self.assertEqual(set(options["env"]), {
                        "PATH", "LC_ALL", "LANG", "TZ", "HOME", "XDG_CONFIG_HOME",
                        "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_SYSTEM", "GIT_CONFIG_GLOBAL",
                        "GIT_ATTR_NOSYSTEM", "GIT_OPTIONAL_LOCKS", "GIT_TERMINAL_PROMPT",
                        "GIT_NO_REPLACE_OBJECTS"})
                self.assertEqual(json.loads(first_json), {
                    "schema_version": "yini-readonly-preflight/result-v1",
                    "work_unit_id": "TEST-1", "contract_sha256": hashlib.sha256(raw).hexdigest(),
                    "outcome": "MATCH", "reason": "MATCH", "exit_code": 0,
                    "failed_step": None, "child_returncode": None,
                    "observations": [
                        {"step": step, "returncode": 0,
                         "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
                         "stderr_sha256": hashlib.sha256(b"").hexdigest(),
                         "stdout_bytes": len(stdout), "stderr_bytes": 0, "complete": True}
                        for step, stdout in zip(steps, outputs)],
                    "fingerprint": {"root": ROOT, "common_dir": ROOT + "/.git",
                                    "branch": "main", "head": "a" * 40,
                                    "index_sha256": digest, "delta": rows,
                                    "absent": ["out/missing.txt"]},
                    "successor_authority": False,
                })
                launched.clear()
                second_code, second_json = invoke()
                self.assertEqual(second_code, 0)
                self.assertEqual(first_json, second_json)
                launched.clear()
                outputs[4] = b"?? out/nested/new.txt\0 M docs/case.txt\0"
                outputs[10] = outputs[4]
                reordered_code, reordered_json = invoke()
            self.assertEqual(reordered_code, 0)
            self.assertEqual(len(launched), 12)
            self.assertEqual(json.loads(reordered_json)["fingerprint"], json.loads(first_json)["fingerprint"])
            self.assertEqual((fixture.root / ".git" / "index").read_bytes(), b"abc")
            self.assertEqual((fixture.root / "docs" / "case.txt").read_bytes(), b"abc")
if __name__ == "__main__":
    unittest.main()
