"""Offline regression controls for the native Promptfoo integration."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('suite', ROOT / 'promptfoo_suite.py')
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


class PromptfooChecks(unittest.TestCase):
    def test_five_exact_inputs(self):
        cases = suite.cases()
        self.assertEqual(len(cases), 5)
        for case in cases:
            source = (ROOT / 'cases' / case['file']).read_text()
            self.assertIn('\n\n' + case['input'] + '\n\n', source)
            self.assertNotIn('SETUP', case['input'])

    def supported(self, storage, case, activation):
        body = Path(storage) / 'SKILL.md'
        body.write_text('---\nname: creating-portable-skills\ndescription: Create portable skill packages\n---\nBody instructions\n')
        setup = {'case': case['id'], 'workspace': storage, 'body_path': str(body),
                 'body_sha256': suite.digest(body.read_bytes()), 'package_sha256': suite.manifest(Path(storage))}
        user = {'id': 'user', 'type': 'userMessage'}
        items = [user]
        records = [{'method': 'item/started', 'params': {'item': user}},
                   {'method': 'item/completed', 'params': {'item': user}},
                   {'method': 'rawResponseItem/completed', 'params': {'item': {'type': 'message',
                    'role': 'developer', 'content': [{'type': 'text', 'text':
                    'creating-portable-skills: Create portable skill packages (file: ' + str(body) + ')'}]}}}]
        if activation:
            item = {'id': 'read', 'type': 'commandExecution', 'status': 'completed', 'cwd': storage,
                    'command': '/bin/cat ' + str(body), 'exitCode': 0, 'aggregatedOutput': body.read_text()}
            items.append(item)
            records.extend([{'method': 'item/started', 'params': {'item': item}},
                            {'method': 'item/completed', 'params': {'item': item}},
                            {'method': 'rawResponseItem/completed', 'params': {'item': {'type': 'function_call',
                             'name': 'exec_command', 'call_id': 'read',
                             'arguments': json.dumps({'cmd': item['command']})}}},
                            {'method': 'rawResponseItem/completed', 'params': {'item': {'type': 'function_call_output',
                             'call_id': 'read', 'output': 'Process exited with code 0\nFinal output:\n' + body.read_text()}}}])
        final = {'id': 'answer', 'type': 'agentMessage', 'text': 'Native final answer'}
        items.append(final)
        records.extend([{'method': 'item/started', 'params': {'item': final}},
                        {'method': 'item/completed', 'params': {'item': final}}])
        records.append({'method': 'rawResponseItem/completed', 'params': {'item': {'type': 'message',
                        'id': 'answer', 'role': 'assistant', 'phase': 'final_answer',
                        'content': [{'type': 'output_text', 'text': final['text']}]}}})
        records.append({'method': 'turn/completed', 'params': {'threadId': 't',
                        'turn': {'id': 'u', 'status': 'completed', 'error': None}}})
        raw = {'notifications': records, 'thread': {'id': 't', 'cwd': storage},
               'turn': {'id': 'u', 'status': 'completed'},
               'items': [{'type': 'user_message', 'content': [{'type': 'text', 'text': case['input']}]},
                         {'type': 'agent_message', 'id': 'answer', 'text': final['text']}]}
        response = {'output': final['text'], 'sessionId': 't', 'raw': json.dumps(raw), 'metadata': {'codexAppServer': {
                    'threadId': 't', 'turnId': 'u', 'cwd': storage, 'notificationCount': len(records),
                    'sandboxMode': 'read-only', 'approvalPolicy': 'never', 'items': items}}}
        return response, setup

    def test_supported_activation_and_absence_grade_all_cases(self):
        with tempfile.TemporaryDirectory() as storage:
            for case in suite.cases():
                expected = case['id'] not in ('CPS-ACT-001', 'CPS-ACT-004')
                response, setup = self.supported(storage, case, expected)
                self.assertEqual(suite.admit(response, setup)['result'], 'Pass')
                self.assertTrue(suite.assertion(response, setup)['pass'])
                response, setup = self.supported(storage, case, not expected)
                self.assertEqual(suite.admit(response, setup)['behavior'], 'Fail')
                self.assertFalse(suite.assertion(response, setup)['pass'])

    def test_supported_capture_negatives(self):
        with tempfile.TemporaryDirectory() as storage:
            response, setup = self.supported(storage, suite.cases()[1], True)
            raw = json.loads(response['raw'])
            for mutation in ('missing', 'foreign', 'opaque', 'outside', 'input', 'discovery'):
                altered = copy.deepcopy(response)
                changed = copy.deepcopy(raw)
                if mutation == 'missing': changed['notifications'].pop(0)
                if mutation == 'foreign': changed['notifications'][0]['params']['threadId'] = 'other'
                if mutation == 'opaque': altered['metadata']['codexAppServer']['items'][1]['command'] = 'python3 script.py'
                if mutation == 'outside':
                    changed['notifications'][4]['params']['item']['command'] = '/bin/cat /other/SKILL.md'
                if mutation == 'input': changed['items'][0]['content'][0]['text'] += ' Extra hint'
                if mutation == 'discovery': changed['notifications'][2]['params']['item']['content'] = ['[...]']
                altered['raw'] = json.dumps(changed)
                with self.subTest(mutation=mutation):
                    self.assertEqual(suite.admit(altered, setup)['result'], 'Unmeasured')
                    self.assertFalse(suite.assertion(altered, setup)['pass'])

    def test_absence_cannot_pass_near_misses(self):
        for case in suite.cases():
            result = suite.admit({}, {'case': case['id']})
            self.assertEqual(result['result'], 'Unmeasured')
            self.assertFalse(suite.assertion({}, {'case': case['id']})['pass'])

    def test_activation_output_must_match_native_result(self):
        with tempfile.TemporaryDirectory() as storage:
            response, setup = self.supported(storage, suite.cases()[1], True)
            raw = json.loads(response['raw'])
            for event in raw['notifications']:
                item = event['params'].get('item', {})
                if item.get('type') == 'commandExecution':
                    item['aggregatedOutput'] = 'different native output'
                if item.get('type') == 'function_call_output':
                    item['output'] = 'Process exited with code 0\nFinal output:\ndifferent native output'
            response['raw'] = json.dumps(raw)
            self.assertEqual(suite.admit(response, setup)['result'], 'Unmeasured')
            self.assertFalse(suite.assertion(response, setup)['pass'])

    def test_candidate_output_must_match_native_answer(self):
        with tempfile.TemporaryDirectory() as storage:
            response, setup = self.supported(storage, suite.cases()[-1], True)
            response['output'] = 'An unrelated replacement answer'
            self.assertEqual(suite.admit(response, setup)['result'], 'Unmeasured')

    def native(self, storage, activation=True):
        # Full, closed pinned trace, with one CodeMode child or a zero-child turn.
        workspace = Path(storage) / 'workspace'
        workspace.mkdir()
        response, setup = self.supported(str(workspace), suite.cases()[1 if activation else 3], activation)
        bundle = Path(storage) / 'traces' / 'trace'
        bundle.mkdir(parents=True)
        setup['trace_root'] = str(bundle.parent)
        suite.save(bundle / 'manifest.json', {'root_thread_id': 't', 'rollout_id': 't', 'schema_version': 1})
        def payload(name, value):
            suite.save(bundle / (name + '.json'), value)
            return {'path': name + '.json'}
        raw = json.loads(response['raw'])
        dev = raw['notifications'][2]['params']['item']
        context = [dev, {'type': 'message', 'role': 'user',
                         'content': [{'type': 'input_text', 'text': suite.cases()[1 if activation else 3]['input']}]}]
        answer = {'type': 'message', 'id': 'answer', 'role': 'assistant', 'phase': 'final_answer',
                  'content': [{'type': 'output_text', 'text': response['output']}]}
        facade = {'type': 'custom_tool_call', 'id': 'facade', 'call_id': 'cell-call',
                  'name': 'exec', 'input': 'await tools.exec_command({cmd: "cat SKILL.md"})'}
        records = [{'type': 'rollout_started'}, {'type': 'thread_started', 'metadata_payload': payload('session',
                   {'thread_id': 't', 'cwd': str(workspace), 'model': 'native',
                    'approval_policy': 'never', 'sandbox_policy': 'ReadOnly { network_access: false }'})},
                   {'type': 'codex_turn_started', 'codex_turn_id': 'u'},
                   {'type': 'inference_started', 'inference_call_id': 'first',
                    'request_payload': payload('first', {'model': 'native', 'input': context})},
                   {'type': 'inference_completed', 'inference_call_id': 'first',
                    'response_payload': payload('first-response', {'response_id': 'resp-first',
                         'output_items': [facade] if activation else [answer]})}]
        if activation:
            command = response['metadata']['codexAppServer']['items'][1]
            runtime = {'call_id': 'read', 'turn_id': 'u', 'process_id': 'p', 'cwd': str(workspace),
                       'command': ['/bin/zsh', '-lc', command['command']]}
            records.extend([
                {'type': 'code_cell_started', 'runtime_cell_id': 'cell',
                 'model_visible_call_id': 'cell-call', 'source_js': facade['input']},
                {'type': 'tool_call_started', 'tool_call_id': 'read', 'kind': {'type': 'exec_command'},
                 'requester': {'type': 'code_cell', 'runtime_cell_id': 'cell'},
                 'invocation_payload': payload('invocation', {'tool_name': 'exec_command', 'payload':
                     {'type': 'function', 'arguments': json.dumps({'cmd': command['command']})}})},
                {'type': 'tool_call_runtime_started', 'tool_call_id': 'read', 'runtime_payload': payload('runtime-start', runtime)},
                {'type': 'tool_call_runtime_ended', 'tool_call_id': 'read', 'runtime_payload': payload('runtime-end',
                     dict(runtime, exit_code=0, stdout=command['aggregatedOutput'], stderr='', aggregated_output=command['aggregatedOutput']))},
                {'type': 'tool_call_ended', 'tool_call_id': 'read', 'status': 'completed',
                 'result_payload': payload('child-result', {'type': 'code_mode_response', 'value':
                     {'exit_code': 0, 'output': command['aggregatedOutput']}})},
                {'type': 'code_cell_initial_response', 'runtime_cell_id': 'cell', 'status': 'completed'},
                {'type': 'code_cell_ended', 'runtime_cell_id': 'cell', 'status': 'completed',
                 'response_payload': payload('cell-response', {})},
                {'type': 'inference_started', 'inference_call_id': 'later',
                 'request_payload': payload('later', {'type': 'response.create', 'model': 'native',
                     'previous_response_id': 'resp-first', 'input': [{'type': 'custom_tool_call_output',
                     'call_id': 'cell-call', 'output': 'done'}]})},
                {'type': 'inference_completed', 'inference_call_id': 'later',
                 'response_payload': payload('later-response', {'response_id': 'resp-later', 'output_items': [answer]})}])
            raw['notifications'] = [e for e in raw['notifications'] if
                e['params'].get('item', {}).get('type') not in ('function_call', 'function_call_output')]
            raw['notifications'].insert(3, {'method': 'rawResponseItem/completed', 'params': {'item': facade}})
            raw['notifications'].insert(6, {'method': 'rawResponseItem/completed', 'params': {'item':
                {'type': 'custom_tool_call_output', 'call_id': 'cell-call', 'output': 'done'}}})
        records.extend([{'type': 'codex_turn_ended', 'codex_turn_id': 'u', 'status': 'completed'},
                        {'type': 'thread_ended', 'thread_id': 't', 'status': 'completed'},
                        {'type': 'rollout_ended', 'status': 'completed'}])
        self.write_trace(bundle, records)
        self.write_raw(response, raw)
        return response, setup, bundle, records

    def write_trace(self, bundle, records):
        (bundle / 'trace.jsonl').write_text('\n'.join(json.dumps({'seq': index,
            'schema_version': 1, 'rollout_id': 't', 'thread_id': 't', 'codex_turn_id': 'u', 'payload': record})
            for index, record in enumerate(records, 1)))

    def write_raw(self, response, raw):
        response['raw'] = json.dumps(raw)
        response['metadata']['codexAppServer']['notificationCount'] = len(raw['notifications'])

    def test_closed_native_child_and_zero_child_near_miss(self):
        for activation in (True, False):
            with self.subTest(activation=activation), tempfile.TemporaryDirectory() as storage:
                response, setup, _, _ = self.native(storage, activation)
                self.assertEqual(suite.admit(response, setup)['result'], 'Pass')
                self.assertTrue(suite.assertion(response, setup)['pass'])

    def test_native_evidence_mutations(self):
        mutations = {'missing-response': 'No such file', 'raw-answer': 'output',
                     'native-answer': 'output', 'raw-phase': 'output', 'raw-id': 'output',
                     'redacted-missing-response': 'No such file', 'raw-projection': 'projection',
                     'response-id': 'context', 'runtime-command': 'command',
                     'started-command': 'command', 'started-cwd': 'command',
                     'later-user': 'context', 'later-developer': 'context', 'later-model': 'model changed',
                     'missing-delta': 'context', 'foreign-delta': 'context',
                     'missing-child': 'inventory', 'foreign-turn': 'identity',
                     'yielded-cell': 'Yielded', 'truncated-output': 'truncation',
                     'native-reversed': 'ordering', 'runtime-reversed': 'ordering', 'child-after-cell': 'ordering',
                     'work-after-turn': 'ordering', 'completion-first': 'ordering',
                     'raw-reversed': 'ordering', 'outside-root': 'outside approved'}
        for mutation, reason in mutations.items():
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as storage:
                response, setup, bundle, records = self.native(storage)
                raw = json.loads(response['raw'])
                def change(name, callback):
                    path = bundle / (name + '.json')
                    value = json.loads(path.read_text())
                    callback(value)
                    suite.save(path, value)
                if mutation == 'missing-response': (bundle / 'later-response.json').unlink()
                if mutation == 'raw-answer': raw['notifications'][-2]['params']['item']['content'][0]['text'] = 'Altered'
                if mutation == 'raw-phase': raw['notifications'][-2]['params']['item']['phase'] = 'commentary'
                if mutation == 'raw-id': raw['notifications'][-2]['params']['item']['id'] = 'other'
                if mutation == 'redacted-missing-response':
                    raw['notifications'][-2]['params']['item']['content'] = ['[...]']
                    (bundle / 'later-response.json').unlink()
                if mutation == 'raw-projection': raw['items'][-1]['text'] = 'Altered'
                if mutation == 'response-id': change('first-response', lambda v: v.update(response_id='other'))
                if mutation == 'native-answer': change('later-response', lambda v: v['output_items'][0]['content'][0].update(text='Altered'))
                if mutation == 'runtime-command':
                    for name in ('runtime-start', 'runtime-end'): change(name, lambda v: v.update(command=['/bin/cat', '/outside/SKILL.md']))
                if mutation in ('started-command', 'started-cwd'):
                    for event in raw['notifications']:
                        if event['method'] == 'item/started' and event['params']['item']['type'] == 'commandExecution':
                            event['params']['item']['command' if mutation == 'started-command' else 'cwd'] = '/other'
                if mutation in ('later-user', 'later-developer'):
                    change('later', lambda v: v.update(input=[{'type': 'message', 'role': mutation.removeprefix('later-'),
                                                             'content': [{'type': 'input_text', 'text': 'Different task'}]}]))
                if mutation == 'missing-delta': change('later', lambda v: v.pop('previous_response_id'))
                if mutation == 'foreign-delta': change('later', lambda v: v.update(previous_response_id='foreign'))
                if mutation == 'later-model': change('later', lambda v: v.update(model='different'))
                if mutation == 'missing-child': records[:] = [r for r in records if r['type'] != 'tool_call_ended']
                if mutation == 'foreign-turn':
                    self.write_trace(bundle, records)
                    events = [json.loads(line) for line in (bundle / 'trace.jsonl').read_text().splitlines()]
                    events[5]['codex_turn_id'] = 'foreign'
                    (bundle / 'trace.jsonl').write_text('\n'.join(map(json.dumps, events)))
                if mutation == 'yielded-cell': next(r for r in records if r['type'] == 'code_cell_initial_response')['status'] = 'yielded'
                if mutation == 'truncated-output': change('child-result', lambda v: v['value'].update(output='truncated'))
                if mutation == 'runtime-reversed':
                    start = next(i for i, r in enumerate(records) if r['type'] == 'tool_call_runtime_started')
                    end = next(i for i, r in enumerate(records) if r['type'] == 'tool_call_runtime_ended')
                    records[start], records[end] = records[end], records[start]
                if mutation == 'native-reversed': records[1:-1] = reversed(records[1:-1])
                if mutation == 'child-after-cell':
                    child = next(r for r in records if r['type'] == 'tool_call_ended')
                    records.remove(child)
                    records.insert(-3, child)
                if mutation == 'work-after-turn':
                    end = next(r for r in records if r['type'] == 'codex_turn_ended')
                    records.remove(end)
                    records.insert(4, end)
                if mutation == 'completion-first': raw['notifications'].insert(0, raw['notifications'].pop())
                if mutation == 'raw-reversed': raw['notifications'].reverse()
                if mutation == 'outside-root':
                    command = '/bin/cat /outside/SKILL.md'
                    response['metadata']['codexAppServer']['items'][1]['command'] = command
                    for event in raw['notifications']:
                        if event['params'].get('item', {}).get('type') == 'commandExecution': event['params']['item']['command'] = command
                    change('invocation', lambda v: v['payload'].update(arguments=json.dumps({'cmd': command})))
                    for name in ('runtime-start', 'runtime-end'): change(name, lambda v: v.update(command=['/bin/zsh', '-lc', command]))
                if mutation != 'foreign-turn': self.write_trace(bundle, records)
                self.write_raw(response, raw)
                admission = suite.admit(response, setup)
                self.assertEqual(admission['result'], 'Unmeasured', admission)
                self.assertIn(reason, admission['reason'])
                self.assertFalse(suite.assertion(response, setup)['pass'])

    def test_later_full_context_allows_assistant_tool_history(self):
        with tempfile.TemporaryDirectory() as storage:
            response, setup, bundle, _ = self.native(storage)
            first = json.loads((bundle / 'first.json').read_text())
            later = json.loads((bundle / 'later.json').read_text())
            later.pop('previous_response_id')
            later['input'] = first['input'] + [{'type': 'message', 'role': 'assistant', 'content': []}] + later['input']
            suite.save(bundle / 'later.json', later)
            self.assertTrue(suite.assertion(response, setup)['pass'])

    def test_native_child_result_and_runtime_end_may_arrive_independently(self):
        with tempfile.TemporaryDirectory() as storage:
            response, setup, bundle, records = self.native(storage)
            runtime = next(i for i, r in enumerate(records) if r['type'] == 'tool_call_runtime_ended')
            child = next(i for i, r in enumerate(records) if r['type'] == 'tool_call_ended')
            records[runtime], records[child] = records[child], records[runtime]
            self.write_trace(bundle, records)
            self.assertTrue(suite.assertion(response, setup)['pass'])

    def test_pinned_redacted_notification_requires_full_native_answer(self):
        with tempfile.TemporaryDirectory() as storage:
            response, setup, _, _ = self.native(storage)
            raw = json.loads(response['raw'])
            raw['notifications'][-2]['params']['item']['content'] = ['[...]']
            self.write_raw(response, raw)
            self.assertTrue(suite.assertion(response, setup)['pass'])
            raw['notifications'][-2]['params']['item']['content'] = ['Other redaction']
            self.write_raw(response, raw)
            self.assertEqual(suite.admit(response, setup)['result'], 'Unmeasured')

    def test_shell_operators_are_not_reads(self):
        for command in ('cat BODY;true', 'cat BODY|true', 'cat BODY>out', 'cat BODY&&true',
                        "/bin/zsh -lc 'cat BODY;true'"):
            with self.subTest(command=command), tempfile.TemporaryDirectory() as storage:
                response, setup = self.supported(storage, suite.cases()[0], True)
                raw = json.loads(response['raw'])
                response['metadata']['codexAppServer']['items'][1]['command'] = command
                for event in raw['notifications']:
                    item = event['params'].get('item', {})
                    if item.get('type') == 'commandExecution': item['command'] = command
                    if item.get('type') == 'function_call': item['arguments'] = json.dumps({'cmd': command})
                self.write_raw(response, raw)
                self.assertEqual(suite.admit(response, setup)['result'], 'Unmeasured')

    def test_production_cjs_hooks_export_modified_fixture_c3_fail(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            workspace = root / 'workspace'
            shutil.copytree(ROOT / 'fixtures/vendor-guidance', workspace)
            setup = root / 'setup.json'
            suite.save(setup, {'case': 'CPS-AUD-001', 'workspace': str(workspace)})
            script = r"""
                const fs = require('node:fs');
                const hooks = require(process.argv[1]);
                const context = {test: {metadata: {setup: process.argv[2]}}, result: {response: {}, metadata: {}}};
                hooks.beforeEach(context);
                fs.appendFileSync(process.argv[3], '\nModified fixture');
                hooks.afterEach(context);
                console.log(JSON.stringify(context.result.metadata));
            """
            call = subprocess.run(['node', '-e', script, str(ROOT / 'promptfoo_hooks.cjs'),
                str(setup), str(workspace / 'vendor-guide.md')], capture_output=True, text=True, check=True)
            metadata = json.loads(call.stdout)
            results = root / 'results.json'
            suite.save(results, {'results': {'results': [{'testCase': {'metadata': {'setup': str(setup)}},
                          'response': {}, 'metadata': metadata}]}})
            self.assertEqual(suite.export(results)[0]['C3']['result'], 'Fail')

    def test_native_completed_is_not_read_confinement(self):
        response = {'metadata': {'codexAppServer': {'threadId': 't', 'turnId': 'u',
                     'cwd': '/workspace', 'sandboxMode': 'read-only', 'approvalPolicy': 'never',
                     'items': []}}, 'raw': json.dumps({'turn': {'id': 'u', 'status': 'completed'},
                     'notifications': [{'method': 'turn/completed', 'params': {'threadId': 't',
                     'turn': {'id': 'u', 'status': 'completed', 'error': None}}}]})}
        result = suite.admit(response, {'case': 'CPS-ACT-001', 'workspace': '/workspace'})
        self.assertEqual(result['result'], 'Unmeasured')
        self.assertTrue(result['reason'])

    def test_package_mismatch_missing_and_stale_capture(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            body = root / 'SKILL.md'
            body.write_text('frozen body')
            meta = {'case': 'CPS-ACT-002', 'workspace': storage,
                    'body_path': str(body), 'body_sha256': suite.digest(body.read_bytes()), 'package_sha256': suite.manifest(root)}
            item = {'type': 'commandExecution', 'id': 'read', 'cwd': storage,
                    'status': 'completed', 'exitCode': 0, 'command': '/bin/cat ' + str(body),
                    'aggregatedOutput': 'frozen body'}
            response = {'metadata': {'codexAppServer': {'cwd': storage, 'items': [item]}}}
            self.assertEqual(suite.admit(response, meta)['activation_observation'], 'successful exact-body read')
            for field, value in [('exitCode', 1), ('cwd', '/elsewhere'), ('status', 'inProgress'),
                                 ('aggregatedOutput', 'changed body'), ('command', 'echo frozen body')]:
                altered = copy.deepcopy(response)
                altered['metadata']['codexAppServer']['items'][0][field] = value
                self.assertNotEqual(suite.admit(altered, meta)['activation_observation'], 'successful exact-body read')
                self.assertFalse(suite.assertion(altered, meta)['pass'])
            body.write_text('different package')
            self.assertEqual(suite.admit(response, meta)['result'], 'Unmeasured')
            self.assertNotEqual(suite.admit(response, meta)['activation_observation'], 'successful exact-body read')


if __name__ == '__main__':
    unittest.main()
