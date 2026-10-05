"""Finite v1 transport. Preparation grants no authority; integration is separate."""

import hashlib
import json
import os
import re
import selectors
import stat
import subprocess
import sys
import time

ROOT = '/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor'
REQUEST_LIMIT = 524288
CONTRACT_LIMIT = 262144
RESULT_LIMIT = 2097152
TOOL_LIMIT = 16 * 1024 * 1024
STREAM_LIMIT = 262144
DEADLINE_SECONDS = 90
OBSERVATION_STEPS = tuple(phase+'.'+name for phase in ('before','after')
                          for name in ('root','common','branch','head','status','staged'))
FAILURE_STEPS = {'input','environment','paths','before.index','after.paths',
                 'after.index','final.files','result'} | set(OBSERVATION_STEPS)
REASON_CODES = {'INVALID_INPUT':2, 'CONTRACT_HASH_MISMATCH':2, 'CONTRACT_INVALID':2,
                'PATH_UNSAFE':2, 'ENVIRONMENT_UNSUPPORTED':4, 'CHECKOUT_UNSUPPORTED':4,
                'TOOL_IDENTITY_MISMATCH':4, 'OBSERVATION_MISMATCH':3,
                'OBSERVATION_DRIFT':3, 'FILESYSTEM_ERROR':5, 'PROCESS_LAUNCH_ERROR':5,
                'TIMEOUT':124, 'CAPTURE_LIMIT':125, 'INTERNAL_DEFECT':70}
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
ID = re.compile(r'[A-Za-z0-9_.-]{1,128}\Z')
CONTRACT_FIELDS = {'schema_version', 'work_unit_id', 'repository_id', 'root',
                   'common_dir', 'branch', 'head', 'index_sha256', 'staged',
                   'delta', 'absent', 'ignored_inputs', 'git'}
REQUEST_FIELDS = {'schema_version', 'source_contract_utf8', 'source_sha256',
                  'work_unit_id', 'absent', 'python', 'observer'}


def _require(condition):
    if not condition:
        raise ValueError('INPUT_ERROR')


def _pairs(pairs):
    value = {}
    for key, item in pairs:
        _require(key not in value)
        value[key] = item
    return value


def _reject_constant(value):
    raise ValueError('INPUT_ERROR')


def _parse(raw, limit):
    _require(type(raw) is bytes and len(raw) <= limit and not raw.startswith(b'\xef\xbb\xbf'))
    return json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs,
                      parse_constant=_reject_constant)


def _hex(value, length=64):
    return type(value) is str and re.fullmatch('[0-9a-f]{'+str(length)+'}', value) is not None


def _closed(value, fields):
    _require(type(value) is dict and set(value) == fields)


def _absolute(value):
    return (type(value) is str and value.startswith('/') and value != '/'
            and all(part and part not in {'.', '..'} and '\x00' not in part
                    for part in value.split('/')[1:]))


def _tool(value):
    _closed(value, {'path', 'sha256'})
    _require(_absolute(value['path']) and _hex(value['sha256']))


def _safe(value):
    return (type(value) is str and bool(value) and all(
        part not in {'.', '..', '.git', '.venv', 'data', 'corpus'}
        and not part.startswith('.env') and part == part.strip(' ')
        and re.fullmatch(r'[A-Za-z0-9._ -]+', part) is not None
        for part in value.split('/')))


def _paths(values):
    _require(type(values) is list and len(values) <= 128 and all(_safe(v) for v in values))
    _require(values == sorted(set(values), key=lambda v: v.encode('utf-8')))


def _contract(value):
    _closed(value, CONTRACT_FIELDS)
    _require(value['schema_version'] == 'yini-readonly-preflight/contract-v1'
             and value['repository_id'] == 'yini-insurance-advisor'
             and value['root'] == ROOT and value['common_dir'] == ROOT+'/.git'
             and value['branch'] == 'main' and type(value['work_unit_id']) is str
             and ID.fullmatch(value['work_unit_id']) is not None
             and _hex(value['head'], 40) and _hex(value['index_sha256'])
             and type(value['staged']) is list and value['staged'] == []
             and value['ignored_inputs'] == 'none'
             and type(value['delta']) is list and len(value['delta']) <= 128)
    _tool(value['git'])
    paths = []
    for row in value['delta']:
        _closed(row, {'path', 'xy', 'kind', 'mode', 'sha256'})
        _require(row['xy'] in (' M', '??') and row['kind'] == 'regular'
                 and row['mode'] in ('644', '755') and _hex(row['sha256']))
        paths.append(row['path'])
    _paths(paths)
    _paths(value['absent'])
    _require(not set(paths).intersection(value['absent']))


def _preparation(raw):
    request = _parse(raw, REQUEST_LIMIT)
    _closed(request, REQUEST_FIELDS)
    _require(request['schema_version'] == 'yini-execution-transport/request-v1'
             and type(request['source_contract_utf8']) is str
             and _hex(request['source_sha256']) and type(request['work_unit_id']) is str
             and ID.fullmatch(request['work_unit_id']) is not None)
    _paths(request['absent'])
    _tool(request['python'])
    _tool(request['observer'])
    original = request['source_contract_utf8'].encode('utf-8')
    _require(len(original) <= CONTRACT_LIMIT and _digest(original) == request['source_sha256'])
    source = _parse(original, CONTRACT_LIMIT)
    _contract(source)
    source['work_unit_id'] = request['work_unit_id']
    source['absent'] = request['absent']
    _contract(source)
    derived = _encode(source)
    _require(len(derived) <= CONTRACT_LIMIT)
    return request, source, derived


def _encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii') + b'\n'


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _result():
    return dict(schema_version='yini-execution-transport/result-v1',
                work_unit_id=None, outcome='STOP', classification='INPUT_ERROR',
                exit_code=2, contract_utf8=None, contract_sha256=None,
                invoked=False, process=None, observer_result=None,
                successor_authority=False)


def prepare(request_bytes):
    """Derive only work-unit ID and absent paths from owner-bound source bytes."""
    result = _result()
    try:
        request, source, raw = _preparation(request_bytes)
    except (ValueError, TypeError, UnicodeError, RecursionError):
        return result
    result.update(work_unit_id=request['work_unit_id'], outcome='PREPARED',
                  classification='NONE', exit_code=0, contract_utf8=raw.decode('ascii'),
                  contract_sha256=_digest(raw))
    return result


def literal_edit(before, old, new, expected_after_sha256):
    """Prepare one exact literal edit; callers retain their separate edit grant."""
    _require(all(type(v) is bytes and len(v) <= CONTRACT_LIMIT for v in (before, old, new)))
    _require(bool(old) and before.count(old) == 1 and _hex(expected_after_sha256))
    after = before.replace(old, new, 1)
    _require(len(after) <= CONTRACT_LIMIT and _digest(after) == expected_after_sha256)
    return after


def select_evidence(envelope, item_id):
    """Select one native item, never infer completeness of thread history."""
    def answer(kind, item=None):
        return {'kind': kind, 'item': item}

    def incomplete(value):
        if type(value) is dict:
            return (value.get('truncated') is True or value.get('complete') is False
                    or any(incomplete(v) for v in value.values()))
        return type(value) is list and any(incomplete(v) for v in value)

    if type(envelope) is not dict or type(item_id) is not str or not item_id:
        return answer('INVALID')
    if envelope.get('isError') is True:
        return answer('TOOL_ERROR')
    if 'isError' in envelope and type(envelope['isError']) is not bool:
        return answer('INVALID')
    blocks = envelope.get('content')
    if (type(blocks) is not list or len(blocks) != 1 or type(blocks[0]) is not dict
            or blocks[0].get('type') != 'text' or type(blocks[0].get('text')) is not str):
        return answer('INVALID')
    try:
        body = _parse(blocks[0]['text'].encode('utf-8'), RESULT_LIMIT)
        _require(type(body) is dict and ('turns' in body) != ('items' in body))
        if 'turns' in body:
            _require(type(body['turns']) is list)
            items = []
            for turn in body['turns']:
                _require(type(turn) is dict and type(turn.get('items')) is list)
                items.extend(turn['items'])
        else:
            items = body['items']
        _require(type(items) is list and all(type(v) is dict and type(v.get('id')) is str and v['id'] for v in items))
        ids = [v['id'] for v in items]
        _require(len(ids) == len(set(ids)))
    except (ValueError, TypeError, UnicodeError, RecursionError):
        return answer('INVALID')
    selected = next((v for v in items if v['id'] == item_id), None)
    if selected is None:
        return answer('MISSING')
    if (type(selected.get('type')) is not str
            or selected.get('type') not in {'agentMessage', 'commandExecution'}
            or selected.get('type') == 'agentMessage' and selected.get('phase') != 'final_answer'):
        return answer('INVALID')
    if selected['type'] == 'agentMessage':
        if type(selected.get('text')) is not str:
            return answer('INVALID')
    else:
        output = selected.get('output')
        state = selected.get('status')
        if (type(state) is not str or state not in {'inProgress','completed','failed','cancelled'}
                or 'exitCode' not in selected
                or selected['exitCode'] is not None and type(selected['exitCode']) is not int
                or type(output) is not dict or type(output.get('text')) is not str
                or type(output.get('truncated')) is not bool):
            return answer('INVALID')
        if state in {'inProgress','cancelled'} or selected['exitCode'] is None:
            return answer('INCOMPLETE')
    if incomplete(selected) or envelope.get('truncated') is True:
        return answer('INCOMPLETE')
    return answer('COMPLETE', selected)


class _Failure(Exception):
    def __init__(self, classification, code):
        self.classification = classification
        self.code = code


def _stop(result, classification, code):
    result.update(outcome='STOP', classification=classification, exit_code=code)
    return result


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def _physical_tool(tool, executable):
    target = tool['path']
    current = '/'
    for part in target.split('/')[1:]:
        current = os.path.join(current, part)
        info = os.lstat(current)
        if stat.S_ISLNK(info.st_mode) or current != target and not stat.S_ISDIR(info.st_mode):
            raise _Failure('DRIFT', 3)
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > TOOL_LIMIT
            or executable and not info.st_mode & 0o111):
        raise _Failure('DRIFT', 3)
    descriptor = os.open(target, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    try:
        opened = os.fstat(descriptor)
        if _identity(opened) != _identity(info):
            raise _Failure('DRIFT', 3)
        digest = hashlib.sha256()
        count = 0
        while True:
            block = os.read(descriptor, min(65536, TOOL_LIMIT+1-count))
            if not block:
                break
            count += len(block)
            if count > TOOL_LIMIT:
                raise _Failure('DRIFT', 3)
            digest.update(block)
        finished = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    if (_identity(info) != _identity(finished) or digest.hexdigest() != tool['sha256']
            or _identity(info) != _identity(os.lstat(target))):
        raise _Failure('DRIFT', 3)


def _environment():
    if not sys.dont_write_bytecode or any(
        key in {'PYTHONPATH','PYTHONHOME','LD_PRELOAD','LD_LIBRARY_PATH'} or key.startswith('DYLD_')
        for key in os.environ):
        raise _Failure('HARNESS_DEFECT', 5)
    environment = {key:value for key,value in os.environ.items() if not key.startswith('GIT_')}
    environment['GIT_OPTIONAL_LOCKS'] = '0'
    if [key for key in environment if key.startswith('GIT_')] != ['GIT_OPTIONAL_LOCKS']:
        raise _Failure('HARNESS_DEFECT', 5)
    return environment


def _record(code, output, complete):
    return dict(returncode=code, stdout_sha256=_digest(output[0]),
                stderr_sha256=_digest(output[1]), stdout_bytes=len(output[0]),
                stderr_bytes=len(output[1]), complete=complete)


def _capture(child, raw, deadline):
    output = [bytearray(), bytearray()]
    complete = False
    code = None
    sent = 0
    try:
        with selectors.DefaultSelector() as selector:
            for stream, index in ((child.stdout, 0), (child.stderr, 1)):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, index)
            os.set_blocking(child.stdin.fileno(), False)
            selector.register(child.stdin, selectors.EVENT_WRITE, 2)
            while selector.get_map():
                remaining = deadline-time.monotonic()
                if remaining <= 0:
                    raise TimeoutError
                ready = selector.select(remaining)
                if not ready:
                    raise TimeoutError
                for key, mask in ready:
                    if key.data == 2:
                        sent += os.write(key.fd, raw[sent:sent+65536])
                        if sent == len(raw):
                            selector.unregister(key.fileobj)
                            child.stdin.close()
                    else:
                        stream = output[key.data]
                        block = os.read(key.fd, min(65536, STREAM_LIMIT+1-len(stream)))
                        if not block:
                            selector.unregister(key.fileobj)
                        else:
                            stream.extend(block)
                            if len(stream) > STREAM_LIMIT:
                                raise OverflowError
            remaining = deadline-time.monotonic()
            if remaining <= 0:
                raise TimeoutError
            code = child.wait(timeout=remaining)
            if type(code) is not int:
                raise OSError('invalid process exit')
            complete = True
    except (OSError, TimeoutError, OverflowError, subprocess.TimeoutExpired, ValueError):
        try:
            child.kill()
        except OSError:
            pass
        try:
            child.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            pass
    finally:
        for stream in (child.stdin, child.stdout, child.stderr):
            try:
                stream.close()
            except OSError:
                complete = False
                code = None
    # Keep both bounded native streams alive through result classification.
    return _record(code, output, complete), (bytes(output[0]), bytes(output[1]))


def _native(raw, process, contract, digest):
    native = _parse(raw, STREAM_LIMIT)
    _closed(native, {'schema_version','work_unit_id','contract_sha256','outcome','reason',
                     'exit_code','failed_step','child_returncode','observations',
                     'fingerprint','successor_authority'})
    _require(raw == _encode(native) and native['schema_version'] == 'yini-readonly-preflight/result-v1'
             and native['successor_authority'] is False
             and type(native['exit_code']) is int and 0 <= native['exit_code'] <= 255
             and native['exit_code'] == process['returncode']
             and native['contract_sha256'] == digest
             and (native['work_unit_id'] is None or native['work_unit_id'] == contract['work_unit_id'])
             and (native['failed_step'] is None or type(native['failed_step']) is str
                  and native['failed_step'] in FAILURE_STEPS)
             and (native['child_returncode'] is None or type(native['child_returncode']) is int)
             and type(native['observations']) is list and len(native['observations']) <= 12)
    records = native['observations']
    empty = _digest(b'')
    for index, record in enumerate(records):
        _closed(record, {'step','returncode','stdout_sha256','stderr_sha256','stdout_bytes','stderr_bytes','complete'})
        _require(record['step'] == OBSERVATION_STEPS[index]
                 and (record['returncode'] is None or type(record['returncode']) is int)
                 and type(record['complete']) is bool
                 and _hex(record['stdout_sha256']) and _hex(record['stderr_sha256']))
        for stream in ('stdout','stderr'):
            count = record[stream+'_bytes']
            _require(type(count) is int and 0 <= count <= STREAM_LIMIT+1
                     and (count != 0 or record[stream+'_sha256'] == empty))
        if index < len(records)-1:
            _require(record['returncode'] == 0 and record['complete'] is True)
        _require(not record['complete'] or type(record['returncode']) is int)
    if native['outcome'] == 'MATCH':
        _require(native['reason'] == 'MATCH' and native['exit_code'] == 0
                 and native['failed_step'] is None and native['child_returncode'] is None
                 and native['work_unit_id'] == contract['work_unit_id'] and len(records) == 12
                 and native['fingerprint'] == {key:contract[key] for key in
                     ('root','common_dir','branch','head','index_sha256','delta','absent')})
        for record in records:
            _require(record['returncode'] == 0 and record['complete'] is True
                     and record['stdout_bytes'] <= STREAM_LIMIT and record['stderr_bytes'] <= STREAM_LIMIT)
            label = record['step'].split('.')[1]
            scalar_fields = {'root':'root', 'common':'common_dir', 'branch':'branch', 'head':'head'}
            if label in scalar_fields:
                expected = (contract[scalar_fields[label]]+'\n').encode('utf-8')
                _require(record['stdout_bytes'] == len(expected)
                         and record['stdout_sha256'] == _digest(expected))
            if record['step'].endswith('.staged'):
                _require(record['stdout_bytes'] == record['stderr_bytes'] == 0)
        return native
    _require(native['outcome'] == 'STOP' and native['fingerprint'] is None
             and native['exit_code'] != 0 and native['failed_step'] is not None)
    reason = native['reason']
    if reason == 'GIT_EXIT':
        code = native['child_returncode']
        _require(type(code) is int and code != 0 and bool(records)
                 and records[-1]['returncode'] == code and records[-1]['complete'] is True
                 and native['failed_step'] == records[-1]['step'])
        _require(native['exit_code'] == (min(255,128-code) if code < 0 else code))
    else:
        _require(type(reason) is str and reason in REASON_CODES
                 and native['exit_code'] == REASON_CODES[reason]
                 and native['child_returncode'] is None)
    return native


def invoke(request_bytes):
    """Launch exactly one eligible v1 observer; never retry or choose a checkout."""
    result = prepare(request_bytes)
    if result['outcome'] != 'PREPARED':
        return result
    request, contract, raw = _preparation(request_bytes)
    try:
        if os.getcwd() != ROOT or request['observer']['path'] != ROOT+'/scripts/readonly_preflight.py':
            raise _Failure('DRIFT', 3)
        environment = _environment()
        _physical_tool(request['python'], True)
        _physical_tool(request['observer'], False)
        _physical_tool(contract['git'], True)
        deadline = time.monotonic()+DEADLINE_SECONDS
        child = subprocess.Popen([request['python']['path'], '-B', request['observer']['path'],
                                  'verify', '--contract-sha256', result['contract_sha256']],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 shell=False, cwd=ROOT, env=environment)
    except _Failure as error:
        return _stop(result, error.classification, error.code)
    except PermissionError:
        return _stop(result, 'DENIAL', 4)
    except FileNotFoundError:
        return _stop(result, 'DRIFT', 3)
    except OSError:
        return _stop(result, 'HARNESS_DEFECT', 5)
    result['invoked'] = True
    process, streams = _capture(child, raw, deadline)
    result['process'] = process
    if not process['complete']:
        return _stop(result, 'OUTPUT_MISSING', 6)
    try:
        native = _native(streams[0], process, contract, result['contract_sha256'])
    except (ValueError, TypeError, UnicodeError, RecursionError):
        return _stop(result, 'OUTPUT_MISSING', 6)
    result['observer_result'] = native
    if native['outcome'] == 'STOP':
        return _stop(result, 'OBSERVER_STOP', native['exit_code'])
    result.update(outcome='MATCH', classification='NONE', exit_code=0)
    return result


def main(argv):
    """Closed stdin/stdout CLI; failed delivery always returns a nonzero exit."""
    result = _result()
    try:
        if type(argv) is list and len(argv) == 1 and argv[0] in ('prepare','invoke'):
            chunks = bytearray()
            while len(chunks) <= REQUEST_LIMIT:
                block = sys.stdin.buffer.read(min(65536, REQUEST_LIMIT+1-len(chunks)))
                if not block:
                    break
                chunks.extend(block)
            if len(chunks) <= REQUEST_LIMIT:
                result = prepare(bytes(chunks)) if argv[0] == 'prepare' else invoke(bytes(chunks))
        raw = _encode(result)
        if len(raw) > RESULT_LIMIT:
            return 6
        written = sys.stdout.buffer.write(raw)
        if written != len(raw):
            return 6
        sys.stdout.buffer.flush()
    except (OSError, ValueError, TypeError, RecursionError):
        return 6
    return result['exit_code']


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
