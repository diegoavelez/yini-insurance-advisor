"""Invented public-contract oracles; no real observer or Git invocation."""

import hashlib
import importlib.util
import json
import io
import os
import tempfile
import threading
from pathlib import Path
import unittest
from unittest import mock

SOURCE = Path(__file__).resolve().parents[1] / 'scripts' / 'execution_contract.py'
spec = importlib.util.spec_from_file_location('execution_contract', SOURCE)
transport = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transport)

ROOT = '/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor'
ABC = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii') + b'\n'


def source_contract(**changes):
    value = dict(schema_version='yini-readonly-preflight/contract-v1',
                 repository_id='yini-insurance-advisor', work_unit_id='OLD',
                 root=ROOT, common_dir=ROOT+'/.git', branch='main', head='a'*40,
                 index_sha256='b'*64, staged=[], delta=[], absent=[],
                 ignored_inputs='none', git={'path': '/fixture/git', 'sha256': ABC})
    value.update(changes)
    return encoded(value)


def request(source=None, **changes):
    source = source_contract() if source is None else source
    value = dict(schema_version='yini-execution-transport/request-v1',
                 source_contract_utf8=source.decode('utf-8'),
                 source_sha256=hashlib.sha256(source).hexdigest(),
                 work_unit_id='NEW', absent=['out/result.txt'],
                 python={'path': '/fixture/python', 'sha256': ABC},
                 observer={'path': ROOT+'/scripts/readonly_preflight.py', 'sha256': ABC})
    value.update(changes)
    return encoded(value)


class PreparationTests(unittest.TestCase):
    def test_derives_only_id_and_absent_without_io(self):
        raw = source_contract()
        expected = raw.replace(b'"absent":[]', b'"absent":["out/result.txt"]').replace(b'"work_unit_id":"OLD"', b'"work_unit_id":"NEW"')
        with mock.patch('subprocess.Popen', side_effect=AssertionError('pure seam')):
            result = transport.prepare(request(raw))
        self.assertEqual(result, dict(schema_version='yini-execution-transport/result-v1',
            work_unit_id='NEW', outcome='PREPARED', classification='NONE', exit_code=0,
            contract_utf8=expected.decode('ascii'), contract_sha256=hashlib.sha256(expected).hexdigest(),
            invoked=False, process=None, observer_result=None, successor_authority=False))

    def test_closed_request_and_full_nested_v1_schema(self):
        invalid = [b'', b'\xef\xbb\xbf'+request(), request()+b'X',
            request(source_sha256='0'*64), request(extra=True), request(work_unit_id='!'),
            request(absent=['../escape']), request(absent=['z','a']),
            request(absent=['x','x']), request(python={'path': 'relative', 'sha256': ABC}),
            request(observer={'path': ROOT+'/scripts/readonly_preflight.py', 'sha256': ABC, 'extra': 1}),
            request().replace(b'"work_unit_id":"NEW"', b'"work_unit_id":"NEW","work_unit_id":"OTHER"')]
        for changes in [dict(schema_version='v2'), dict(staged=['x']), dict(extra=True),
                        dict(head=True), dict(ignored_inputs='some'), dict(branch='other'),
                        dict(root='/wrong'), dict(common_dir='/wrong'), dict(repository_id='other'),
                        dict(delta=[{'path':'x','xy':' M','mode':644,'kind':'regular','sha256':ABC}]),
                        dict(absent=['data/secret']), dict(git={'path':'relative','sha256':ABC})]:
            invalid.append(request(source_contract(**changes)))
        invalid.extend([bytearray(request()), b'x' * 524289,
                        request(source_contract()+b' ' * 262145)])
        for raw in invalid:
            with self.subTest(raw_type=type(raw).__name__, size=len(raw)):
                result = transport.prepare(raw)
                self.assertEqual((result['outcome'], result['classification'], result['exit_code'], result['invoked']),
                                 ('STOP', 'INPUT_ERROR', 2, False))


class LiteralTests(unittest.TestCase):
    def test_exact_space_preserving_replacement_and_closed_rejections(self):
        expected = b'prefix new Git,\n'
        # Oracle is the desired literal, independently hashed in the fixture.
        digest = hashlib.sha256(expected).hexdigest()
        self.assertEqual(transport.literal_edit(b'prefix old Git,\n', b'old', b'new', digest), expected)
        for before, old, new, sha in [
            (b'prefix old Git,\n', b'old', b'new\n', digest),
            (b'none', b'old', b'new', digest), (b'old old', b'old', b'new', digest),
            (b'old', b'', b'new', digest), (bytearray(b'old'), b'old', b'new', digest),
            (b'old', b'old', b'x'*262145, digest), (b'old', b'old', b'new', '0'*64)]:
            with self.subTest(size=len(before)):
                with self.assertRaisesRegex(ValueError, '^INPUT_ERROR$'):
                    transport.literal_edit(before, old, new, sha)


class EvidenceTests(unittest.TestCase):
    def test_native_item_selection_without_role_or_history_inference(self):
        final = {'id': 'final-1', 'type': 'agentMessage', 'phase': 'final_answer',
                 'text': 'literal\\n and LF\n', 'complete': True}
        reasoning = {'id': 'thought', 'type': 'reasoning', 'complete': True}
        def envelope(body):
            return {'isError': False, 'content': [{'type': 'text', 'text': json.dumps(body)}]}
        valid = envelope({'turns': [{'items': [reasoning, final]}], 'page': {'hasMore': True}})
        self.assertEqual(transport.select_evidence(valid, 'final-1'), {'kind': 'COMPLETE', 'item': final})
        command = {'id': 'cmd', 'type': 'commandExecution', 'status':'completed',
                   'exitCode':4, 'output':{'text':'native STOP\n','truncated':False}}
        self.assertEqual(transport.select_evidence(envelope({'items':[command]}), 'cmd'),
                         {'kind':'COMPLETE', 'item':command})
        for value, selected, kind in [
            ({'isError':True,'content':[]},'x','TOOL_ERROR'),
            ({'content':[{'type':'text','text':'tool failed'}]},'x','INVALID'),
            ({'content':[{'type':'image','data':'x'}]},'x','INVALID'),
            (envelope({'items': [final, final]}),'final-1','INVALID'),
            (envelope({'items': [reasoning]}),'thought','INVALID'),
            (envelope({'items': [dict(final, phase='analysis')]}),'final-1','INVALID'),
            (envelope({'items': [dict(final, truncated=True)]}),'final-1','INCOMPLETE'),
            (envelope({'items': [dict(final, complete=False)]}),'final-1','INCOMPLETE'),
            (envelope({'items': [dict(final, type=['agentMessage'])]}),'final-1','INVALID'),
            (envelope({'items': []}),'x','MISSING'),
            (envelope({'turns':[{}]}),'x','INVALID'),
            (envelope({'items': [], 'turns':[]}),'x','INVALID')]:
            with self.subTest(kind=kind):
                self.assertEqual(transport.select_evidence(value, selected), {'kind':kind,'item':None})

    def test_native_evidence_requires_terminal_state_and_complete_capture(self):
        command = {'id':'cmd','type':'commandExecution','status':'completed',
                   'exitCode':0,'output':{'text':'done\n','truncated':False}}
        final = {'id':'final','type':'agentMessage','phase':'final_answer','text':'done'}
        cases = [(command,'COMPLETE'), (dict(command,exitCode=4),'COMPLETE'),
                 (dict(command,status='failed',exitCode=1),'COMPLETE'), (final,'COMPLETE'),
                 (dict(command,status='inProgress',exitCode=None),'INCOMPLETE'),
                 (dict(command,exitCode=None),'INCOMPLETE'),
                 (dict(command,output={'text':'partial','truncated':True}),'INCOMPLETE'),
                 (dict(command,complete=False),'INCOMPLETE'),
                 ({'id':'cmd','type':'commandExecution'},'INVALID'),
                 (dict(command,status='invented'),'INVALID'),
                 (dict(command,status=[]),'INVALID'), (dict(command,exitCode=True),'INVALID'),
                 (dict(command,exitCode='0'),'INVALID'), (dict(command,output=None),'INVALID'),
                 (dict(command,output={'text':'done'}),'INVALID'),
                 (dict(command,output={'text':None,'truncated':False}),'INVALID'),
                 (dict(command,output={'text':'done','truncated':0}),'INVALID'),
                 ({'id':'final','type':'agentMessage','phase':'final_answer'},'INVALID'),
                 (dict(final,text=[]),'INVALID'),
                 ({'id':'reason','type':'reasoning','text':'x'},'INVALID')]
        actual = []
        for item,kind in cases:
            envelope = {'content':[{'type':'text','text':json.dumps({'items':[item]})}]}
            result = transport.select_evidence(envelope,item['id'])
            actual.append((result['kind'],result['item'] == item if kind=='COMPLETE' else result['item'] is None))
        self.assertEqual(actual,[(kind,True) for item,kind in cases])


class PhysicalFixture:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        for name in ('python', 'git', 'scripts/readonly_preflight.py'):
            target = self.root / name
            target.write_bytes(b'abc')
            target.chmod(0o644 if name.startswith('scripts') else 0o755)
        self.lstat_original, self.open_original = os.lstat, os.open
        self.patches = [mock.patch.object(os, 'getcwd', return_value=ROOT),
                        mock.patch.object(os, 'lstat', side_effect=self.lstat),
                        mock.patch.object(os, 'open', side_effect=self.open),
                        mock.patch.dict(os.environ, {'CUSTOM':'retained'}, clear=True)]
        for patch in self.patches:
            patch.start()
        return self

    def mapped(self, candidate):
        if candidate == ROOT or candidate.startswith(ROOT+'/'):
            return str(self.root)+candidate[len(ROOT):]
        if candidate == '/fixture' or candidate.startswith('/fixture/'):
            return str(self.root)+candidate[len('/fixture'):]
        return candidate

    def lstat(self, candidate, *args, **kwargs):
        return self.lstat_original(self.mapped(candidate), *args, **kwargs)

    def open(self, candidate, *args, **kwargs):
        return self.open_original(self.mapped(candidate), *args, **kwargs)

    def __exit__(self, *args):
        for patch in reversed(self.patches):
            patch.stop()
        self.temp.cleanup()


class FakeProcess:
    def __init__(self, stdout, stderr=b'', returncode=0):
        self.returncode = returncode
        self.killed = False
        self.reaped = False
        self.input = bytearray()
        self.threads = []
        read_in, write_in = os.pipe()
        self.stdin = os.fdopen(write_in, 'wb', buffering=0)
        def read_input():
            try:
                while True:
                    block = os.read(read_in, 65536)
                    if not block:
                        break
                    self.input.extend(block)
            finally:
                os.close(read_in)
        worker = threading.Thread(target=read_input, daemon=True)
        worker.start()
        self.threads.append(worker)
        for name, raw in [('stdout',stdout),('stderr',stderr)]:
            read_fd, write_fd = os.pipe()
            setattr(self, name, os.fdopen(read_fd, 'rb'))
            def write_output(fd=write_fd, data=raw):
                try:
                    while data:
                        written = os.write(fd, data[:65536])
                        data = data[written:]
                except BrokenPipeError:
                    pass
                finally:
                    os.close(fd)
            worker = threading.Thread(target=write_output, daemon=True)
            worker.start()
            self.threads.append(worker)

    def wait(self, timeout=None):
        self.reaped = True
        for worker in self.threads[:1]:
            worker.join(timeout=1)
        return self.returncode

    def kill(self):
        self.killed = True


def native_match():
    fingerprint = json.loads(source_contract())
    fingerprint = {key:fingerprint[key] for key in ('root','common_dir','branch','head','index_sha256','delta','absent')}
    fingerprint['absent'] = ['out/result.txt']
    derived = source_contract(work_unit_id='NEW', absent=['out/result.txt'])
    observations = []
    empty = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    # Independent native Git stdout literals required by the v1 plan.
    outputs = {'root': (ROOT+'\n').encode('utf-8'),
               'common': (ROOT+'/.git\n').encode('utf-8'),
               'branch': b'main\n', 'head': b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n',
               'status': b'', 'staged': b''}
    for phase in ('before','after'):
        for name in ('root','common','branch','head','status','staged'):
            observations.append(dict(step=phase+'.'+name,returncode=0,
                stdout_sha256=hashlib.sha256(outputs[name]).hexdigest(),
                stderr_sha256=empty,stdout_bytes=len(outputs[name]),stderr_bytes=0,complete=True))
    return dict(schema_version='yini-readonly-preflight/result-v1', work_unit_id='NEW',
        contract_sha256=hashlib.sha256(derived).hexdigest(), outcome='MATCH', reason='MATCH',
        exit_code=0, failed_step=None, child_returncode=None, observations=observations,
        fingerprint=fingerprint, successor_authority=False)


class InvocationTests(unittest.TestCase):
    def test_scalar_observation_counts_and_hashes_must_match_bound_literals(self):
        actual = []
        for index in (0,1,2,3,6,7,8,9):
            for change in ({'stdout_bytes':0,'stdout_sha256':hashlib.sha256(b'').hexdigest()},
                           {'stdout_bytes':1}, {'stdout_sha256':hashlib.sha256(b'wrong\n').hexdigest()}):
                native = native_match()
                native['observations'][index].update(change)
                with PhysicalFixture(), mock.patch('subprocess.Popen',return_value=FakeProcess(encoded(native))) as launch:
                    result = transport.invoke(request())
                actual.append((result['outcome'],result['classification'],result['exit_code'],
                               result['observer_result'],result['process']['complete'],launch.call_count))
        self.assertEqual(actual, [('STOP','OUTPUT_MISSING',6,None,True,1)]*24)

    def test_one_absolute_invocation_sanitizes_only_git_environment(self):
        native = encoded(native_match())
        with PhysicalFixture(), mock.patch.dict(os.environ, {
                'GIT_CONFIG_COUNT':'1','GIT_DIR':'bad','GIT_WORK_TREE':'bad',
                'GIT_INDEX_FILE':'bad','GIT_CONFIG_GLOBAL':'bad','GIT_OPTIONAL_LOCKS':'1'}):
            child = FakeProcess(native)
            with mock.patch('subprocess.Popen', return_value=child) as popen:
                result = transport.invoke(request())
            self.assertEqual((result['outcome'],result['classification'],result['exit_code']), ('MATCH','NONE',0))
            self.assertEqual(popen.call_count,1)
            args, kwargs = popen.call_args
            expected = source_contract(work_unit_id='NEW', absent=['out/result.txt'])
            self.assertEqual(list(args[0]), ['/fixture/python','-B',ROOT+'/scripts/readonly_preflight.py',
                              'verify','--contract-sha256',hashlib.sha256(expected).hexdigest()])
            self.assertEqual(kwargs['env'], {'CUSTOM':'retained','GIT_OPTIONAL_LOCKS':'0'})
            self.assertIs(kwargs['shell'],False)
            self.assertEqual(kwargs['cwd'],ROOT)
            self.assertEqual(bytes(child.input),expected)
            self.assertTrue(child.reaped)
            self.assertEqual(result['observer_result'],native_match())
            self.assertEqual(result['process'],dict(returncode=0,stdout_sha256=hashlib.sha256(native).hexdigest(),
                stderr_sha256='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                stdout_bytes=len(native),stderr_bytes=0,complete=True))

    def test_valid_native_stop_retains_reason_and_sanitized_capture(self):
        native = native_match()
        native.update(outcome='STOP',reason='ENVIRONMENT_UNSUPPORTED',exit_code=4,
                      failed_step='environment',fingerprint=None,observations=[])
        raw = encoded(native)
        with PhysicalFixture(), mock.patch('subprocess.Popen', return_value=FakeProcess(raw,b'private diagnostic',4)) as popen:
            result = transport.invoke(request())
        self.assertEqual((result['outcome'],result['classification'],result['exit_code']),('STOP','OBSERVER_STOP',4))
        self.assertEqual(result['observer_result'],native)
        self.assertEqual(result['process']['stderr_bytes'],18)
        self.assertNotIn('private diagnostic',json.dumps(result))
        self.assertEqual(popen.call_count,1)

    def test_invalid_native_success_is_terminal_output_missing(self):
        mutations = [dict(successor_authority=True), dict(exit_code=True), dict(extra=1),
                     dict(fingerprint={}), dict(observations=[]), dict(work_unit_id='WRONG'),
                     dict(reason='UNKNOWN'), dict(failed_step='input'), dict(child_returncode=0)]
        records = native_match()['observations']
        mutations += [dict(observations=records[::-1]),
            dict(observations=[dict(records[0], complete=False)]+records[1:]),
            dict(observations=[dict(records[0], stdout_bytes=True)]+records[1:]),
            dict(observations=records[:5]+[dict(records[5], stdout_bytes=1)]+records[6:])]
        cases = [(encoded(dict(native_match(),**change)),0) for change in mutations]
        cases += [(b'',0),(b'plain tool error',4),(encoded(native_match())+b' ',0),
                  (encoded(native_match()).replace(b'"exit_code":0',b'"exit_code":0,"exit_code":0'),0),
                  (encoded(native_match()),4),(encoded(native_match()),-9)]
        for raw,code in cases:
            with self.subTest(code=code, length=len(raw)), PhysicalFixture(), mock.patch('subprocess.Popen',return_value=FakeProcess(raw,returncode=code)) as popen:
                result = transport.invoke(request())
                self.assertEqual((result['outcome'],result['classification'],result['exit_code']),('STOP','OUTPUT_MISSING',6))
                self.assertIsNone(result['observer_result'])
                self.assertEqual(result['process']['returncode'],code)
                self.assertEqual(popen.call_count,1)

    def test_identity_and_injection_guards_stop_before_launch(self):
        for name in ['PYTHONPATH','PYTHONHOME','LD_PRELOAD','LD_LIBRARY_PATH','DYLD_INSERT_LIBRARIES','DYLD_ANY']:
            with self.subTest(variable=name), PhysicalFixture(), mock.patch.dict(os.environ,{name:'x'}), mock.patch('subprocess.Popen') as popen:
                result = transport.invoke(request())
                self.assertEqual((result['classification'],result['exit_code'],result['invoked']),('HARNESS_DEFECT',5,False))
                popen.assert_not_called()
        for change in ['cwd','python_mode','git_mode','hash','symlink','hardlink','oversized','observer_path']:
            with self.subTest(change=change), PhysicalFixture() as fixture, mock.patch('subprocess.Popen') as popen:
                raw = request()
                if change == 'cwd':
                    os.getcwd.return_value = '/wrong'
                elif change == 'python_mode':
                    (fixture.root/'python').chmod(0o644)
                elif change == 'git_mode':
                    (fixture.root/'git').chmod(0o644)
                elif change == 'hash':
                    (fixture.root/'python').write_bytes(b'changed')
                elif change == 'symlink':
                    (fixture.root/'python').unlink()
                    (fixture.root/'python').symlink_to(fixture.root/'git')
                elif change == 'hardlink':
                    os.link(fixture.root/'python',fixture.root/'second')
                elif change == 'oversized':
                    with (fixture.root/'python').open('r+b') as stream:
                        stream.truncate(16*1024*1024+1)
                else:
                    raw = request(observer={'path':ROOT+'/linked/config.worktree','sha256':ABC})
                result = transport.invoke(raw)
                self.assertEqual((result['classification'],result['exit_code'],result['invoked']),('DRIFT',3,False))
                popen.assert_not_called()

    def test_launch_error_and_denial_have_no_process_and_no_retry(self):
        for error,kind,code in [(PermissionError(),'DENIAL',4),(OSError(),'HARNESS_DEFECT',5)]:
            with PhysicalFixture(), mock.patch('subprocess.Popen',side_effect=error) as popen:
                result = transport.invoke(request())
                self.assertEqual((result['classification'],result['exit_code'],result['invoked'],result['process']),
                                 (kind,code,False,None))
                self.assertEqual(popen.call_count,1)

    def test_capture_overflow_terminates_reaps_and_hashes_partial_stream(self):
        for name in ('stdout','stderr'):
            outputs = {name:b'x'*262145}
            with self.subTest(stream=name), PhysicalFixture():
                child = FakeProcess(outputs.get('stdout',b''),outputs.get('stderr',b''))
                with mock.patch('subprocess.Popen',return_value=child) as popen:
                    result = transport.invoke(request())
                self.assertEqual((result['classification'],result['exit_code']),('OUTPUT_MISSING',6))
                self.assertIs(result['process']['complete'],False)
                self.assertIsNone(result['process']['returncode'])
                self.assertEqual(result['process'][name+'_bytes'],262145)
                self.assertEqual(result['process'][name+'_sha256'],hashlib.sha256(b'x'*262145).hexdigest())
                self.assertTrue(child.killed and child.reaped)
                self.assertEqual(popen.call_count,1)

    def test_deadline_read_and_reap_failure_never_match(self):
        with PhysicalFixture():
            child = FakeProcess(encoded(native_match()))
            with mock.patch('subprocess.Popen',return_value=child), mock.patch('time.monotonic',side_effect=[0,91]):
                result = transport.invoke(request())
            self.assertEqual(result['classification'],'OUTPUT_MISSING')
            self.assertFalse(result['process']['complete'])
            self.assertTrue(child.killed and child.reaped)


class CLITests(unittest.TestCase):
    def test_closed_cli_and_bounded_input_output(self):
        for argv,raw,outcome,code in [(['prepare'],request(),'PREPARED',0),
                ([],request(),'STOP',2),(['invoke','--retry'],request(),'STOP',2),
                (['other'],request(),'STOP',2),(['prepare'],b'x'*524289,'STOP',2)]:
            stdout = io.BytesIO()
            with self.subTest(argv=argv,size=len(raw)), mock.patch.object(transport.sys,'stdin',type('Input',(),{'buffer':io.BytesIO(raw)})()), mock.patch.object(transport.sys,'stdout',type('Output',(),{'buffer':stdout})()), mock.patch('subprocess.Popen') as popen:
                self.assertEqual(transport.main(argv),code)
                value = json.loads(stdout.getvalue())
                self.assertEqual(value['outcome'],outcome)
                self.assertEqual(stdout.getvalue(),encoded(value))
                self.assertLessEqual(len(stdout.getvalue()),2097152)
                popen.assert_not_called()
        with PhysicalFixture():
            child = FakeProcess(encoded(native_match()))
            stdout = io.BytesIO()
            with mock.patch.object(transport.sys,'stdin',type('Input',(),{'buffer':io.BytesIO(request())})()), mock.patch.object(transport.sys,'stdout',type('Output',(),{'buffer':stdout})()), mock.patch('subprocess.Popen',return_value=child) as popen:
                self.assertEqual(transport.main(['invoke']),0)
                self.assertEqual(json.loads(stdout.getvalue())['outcome'],'MATCH')
                self.assertEqual(popen.call_count,1)
        output = mock.Mock()
        output.buffer.write.side_effect = BrokenPipeError()
        with mock.patch.object(transport.sys,'stdin',type('Input',(),{'buffer':io.BytesIO(request())})()), mock.patch.object(transport.sys,'stdout',output):
            self.assertEqual(transport.main(['prepare']),6)

    def test_read_and_reap_failure_never_match(self):
        for phase in ('read','reap'):
            with self.subTest(phase=phase), PhysicalFixture():
                child = FakeProcess(encoded(native_match()))
                with mock.patch('subprocess.Popen',return_value=child):
                    if phase == 'read':
                        # Only pipe reads fail; guarded tool-file reads remain real.
                        original = os.read
                        def read(fd, size):
                            if fd in (child.stdout.fileno(),child.stderr.fileno()):
                                raise OSError('invented failure')
                            return original(fd,size)
                        with mock.patch('os.read',side_effect=read):
                            result = transport.invoke(request())
                    else:
                        with mock.patch.object(child,'wait',side_effect=OSError('invented reap failure')):
                            result = transport.invoke(request())
                self.assertEqual(result['classification'],'OUTPUT_MISSING')
                self.assertFalse(result['process']['complete'])
                self.assertTrue(child.killed)

    def test_launch_time_is_part_of_total_process_deadline(self):
        clock = [0]
        with PhysicalFixture():
            child = FakeProcess(encoded(native_match()))
            def launch(*args, **kwargs):
                clock[0] = 91
                return child
            with mock.patch('subprocess.Popen',side_effect=launch), mock.patch('time.monotonic',side_effect=lambda:clock[0]):
                result = transport.invoke(request())
            self.assertEqual(result['classification'],'OUTPUT_MISSING')
            self.assertTrue(child.killed and child.reaped)


class PreservationTests(unittest.TestCase):
    def test_delta_rows_and_exact_source_lf_are_preserved(self):
        row = {'path':'docs/fixture.txt','xy':' M','kind':'regular','mode':'644','sha256':ABC}
        source = source_contract(delta=[row])
        expected = source.replace(b'"absent":[]',b'"absent":["out/result.txt"]').replace(b'"work_unit_id":"OLD"',b'"work_unit_id":"NEW"')
        result = transport.prepare(request(source))
        self.assertEqual(result['contract_utf8'].encode('ascii'),expected)
        self.assertEqual(json.loads(result['contract_utf8'])['delta'],[row])
        wrong = request(source).replace(b'"source_sha256":"'+hashlib.sha256(source).hexdigest().encode()+b'"',b'"source_sha256":"'+hashlib.sha256(source[:-1]).hexdigest().encode()+b'"')
        self.assertEqual(transport.prepare(wrong)['classification'],'INPUT_ERROR')
        self.assertEqual(transport.prepare(request(source[:-1]+b'\\n'))['classification'],'INPUT_ERROR')

    def test_import_is_pure_and_does_not_import_observer(self):
        code = compile(SOURCE.read_bytes(),str(SOURCE),'exec')
        with mock.patch('os.open',side_effect=AssertionError('I/O on import')), mock.patch('os.lstat',side_effect=AssertionError('I/O on import')), mock.patch('subprocess.Popen',side_effect=AssertionError('launch on import')):
            namespace = {'__name__':'pure_import'}
            exec(code,namespace)
        self.assertTrue(all(callable(namespace[name]) for name in ('prepare','invoke','main','literal_edit','select_evidence')))
        self.assertFalse(any('readonly_preflight' in name for name in namespace))

    def test_linked_configs_present_do_not_replace_principal_absence(self):
        with PhysicalFixture() as fixture:
            (fixture.root/'.git/worktrees/one').mkdir(parents=True)
            (fixture.root/'.git/worktrees/two').mkdir(parents=True)
            for name in ('one','two'):
                (fixture.root/f'.git/worktrees/{name}/config.worktree').write_bytes(b'invented')
            self.assertFalse(os.path.lexists(ROOT+'/.git/config.worktree'))
            self.assertTrue(os.path.lexists(ROOT+'/.git/worktrees/one/config.worktree'))
            with mock.patch('os.open',side_effect=fixture.open) as opened, mock.patch('subprocess.Popen',return_value=FakeProcess(encoded(native_match()))):
                result = transport.invoke(request())
            self.assertEqual(result['outcome'],'MATCH')
            self.assertFalse(any('config.worktree' in str(call) for call in opened.call_args_list))

    def test_duplicate_nested_keys_and_all_path_shapes_fail_closed(self):
        invalid = [source_contract().replace(b'"branch":"main"',b'"branch":"main","branch":"main"'),
                   source_contract().replace(b'"staged":[]',b'"staged":NaN'),
                   b'\xef\xbb\xbf'+source_contract()]
        row = {'path':'docs/fixture.txt','xy':' M','kind':'regular','mode':'644','sha256':ABC}
        for changes in [dict(delta=[row,row]),dict(delta=[dict(row,path='z'),dict(row,path='a')]),
                        dict(delta=[dict(row,extra=0)]),dict(absent=['docs/fixture.txt'],delta=[row]),
                        dict(delta=[dict(row,xy='M ')]),dict(git={'path':'/fixture/git','sha256':ABC,'extra':1})]:
            invalid.append(source_contract(**changes))
        for path in ['/abs','a//b','a/../b','a/./b','a\\b','.env.local/x','x/.git/y','x/.venv/y',
                     'x/corpus/y','x/data/y','a/ b','a/b ','a/$x','a/$(x)','a/\n']:
            invalid.append(source_contract(absent=[path]))
        with mock.patch('subprocess.Popen') as popen:
            for raw in invalid:
                with self.subTest(size=len(raw)):
                    self.assertEqual(transport.prepare(request(raw))['classification'],'INPUT_ERROR')
            popen.assert_not_called()

    def test_native_reason_exit_and_record_shape_are_closed(self):
        stop = native_match()
        stop.update(outcome='STOP',reason='ENVIRONMENT_UNSUPPORTED',exit_code=4,
                    failed_step='environment',fingerprint=None,observations=[])
        cases = [dict(stop,exit_code=3),dict(stop,fingerprint=native_match()['fingerprint']),
                 dict(stop,reason='UNKNOWN'),dict(stop,failed_step='invented'),
                 dict(stop,child_returncode=True),dict(stop,successor_authority=0)]
        match = native_match()
        for changes in [dict(returncode=True),dict(extra=1),dict(stdout_sha256='bad'),dict(stdout_bytes=-1),
                        dict(stderr_bytes=262146),dict(complete='true')]:
            records = [dict(match['observations'][0],**changes)]+match['observations'][1:]
            cases.append(dict(match,observations=records))
        for native in cases:
            with self.subTest(reason=native['reason']), PhysicalFixture(), mock.patch('subprocess.Popen',return_value=FakeProcess(encoded(native),returncode=native['exit_code'])):
                self.assertEqual(transport.invoke(request())['classification'],'OUTPUT_MISSING')
        signal = dict(stop,reason='GIT_EXIT',exit_code=137,failed_step='before.root',child_returncode=-9,
                      observations=[dict(match['observations'][0],returncode=-9)])
        with PhysicalFixture(), mock.patch('subprocess.Popen',return_value=FakeProcess(encoded(signal),returncode=137)):
            result = transport.invoke(request())
        self.assertEqual((result['classification'],result['exit_code'],result['observer_result']),('OBSERVER_STOP',137,signal))
