"""Prepare private native Promptfoo evaluations and report capture limits (stdlib only)."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import re
import sys

from evaluate_read_only import snapshot, evaluate
from native_trace import inspect as inspect_trace, command_words, output_signature

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CASE_FILES = ('activation-near-miss.md', 'activation-authoring.md',
              'activation-explicit-review.md', 'activation-writing-near-miss.md',
              'vendor-guidance-audit.md')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    result = []
    for name in CASE_FILES:
        text = (ROOT / 'cases' / name).read_text()
        case_id = text.split()[1]
        user_input = text.split('## ' + case_id + '.INPUT\n\n', 1)[1].split('\n\n', 1)[0]
        result.append({'id': case_id, 'file': name, 'input': user_input})
    return result


def manifest(root):
    return {str(path.relative_to(root)): digest(path.read_bytes())
            for path in sorted(root.rglob('*')) if path.is_file()}


def private(path):
    path = Path(path).resolve()
    if path == REPO or REPO in path.parents:
        raise ValueError('Generated eval files must be outside the public repository')
    return path


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def read_target(command, cwd):
    """Recognize one exact cat read, optionally wrapped in a native shell."""
    words = command_words(command)
    target = Path(words[1])
    return (target if target.is_absolute() else Path(cwd) / target).resolve()


def metadata_items_commands(native):
    return {item['id']: item for item in native['items'] if item['type'] == 'commandExecution'}


def admit(response, setup):
    """Bounded native evidence checks, without evaluating scripts or CodeMode."""
    result = {'result': 'Unmeasured', 'reason': 'Missing or incomplete native capture',
              'activation_observation': 'unverified', 'human_calibration': 'Unmeasured'}
    if not isinstance(response, dict):
        return result
    metadata = response.get('metadata')
    if not isinstance(metadata, dict):
        return result
    native = metadata.get('codexAppServer', {})
    try:
        body = Path(setup['body_path'])
        intact = (digest(body.read_bytes()) == setup['body_sha256'] and
                  manifest(body.parent) == setup['package_sha256'])
        if not intact:
            raise ValueError('Frozen package changed or incomplete')
        if native.get('cwd') != setup['workspace']:
            raise ValueError('Native cwd mismatch')
        for item in native.get('items', []):
            if (item.get('type') == 'commandExecution' and item.get('cwd') == setup['workspace']
                    and item.get('status') == 'completed' and type(item.get('exitCode')) is int
                    and item['exitCode'] == 0 and isinstance(item.get('aggregatedOutput'), str)
                    and digest(item['aggregatedOutput'].encode()) == setup['body_sha256']
                    and read_target(item.get('command'), setup['workspace']) == body.resolve()):
                result['activation_observation'] = 'successful exact-body read'
                result['activation_item_id'] = item.get('id')
        raw = json.loads(response.get('raw', ''))
        events = raw['notifications']
        if not events or len(events) != native['notificationCount']:
            raise ValueError('Native notification inventory incomplete')
        thread, turn = native['threadId'], native['turnId']
        if response.get('sessionId') != thread or raw['thread']['id'] != thread:
            raise ValueError('Native session mismatch')
        if raw['thread']['cwd'] != setup['workspace'] or raw['turn']['id'] != turn:
            raise ValueError('Native workspace or turn mismatch')
        completed = [event['params'] for event in events if event.get('method') == 'turn/completed']
        if (len(completed) != 1 or completed[0].get('threadId') != thread
                or completed[0]['turn']['id'] != turn or completed[0]['turn']['status'] != 'completed'
                or completed[0]['turn'].get('error') is not None or raw['turn']['status'] != 'completed'):
            raise ValueError('Native completion unavailable')
        result['native_completion_observed'] = True
        if native.get('sandboxMode') != 'read-only' or native.get('approvalPolicy') != 'never':
            raise ValueError('Native write/approval policy mismatch')
        users = [item for item in raw['items'] if item['type'] == 'user_message']
        canonical = next(case['input'] for case in cases() if case['id'] == setup['case'])
        if len(users) != 1 or users[0].get('content') not in ([{'type': 'text', 'text': canonical}], [{'type': 'text', 'text': canonical, 'text_elements': []}]):
            raise ValueError('Canonical normal user INPUT unavailable or forced attachment')
        calls, outputs, facades, facade_outputs = {}, {}, {}, {}
        starts, ends = {}, {}
        developers, raw_output = [], []
        completion_position = next(index for index, event in enumerate(events) if event.get('method') == 'turn/completed')
        positions = {}
        for index, event in enumerate(events):
            params = event.get('params', {})
            if params.get('threadId', thread) != thread or params.get('turnId', turn) != turn:
                raise ValueError('Foreign native event identity')
            item = params.get('item', {})
            method = event.get('method')
            if method and (method.startswith(('item/', 'rawResponse')) or method == 'turn/started'):
                if index >= completion_position:
                    raise ValueError('Invalid native notification lifecycle ordering')
                positions[(method, item.get('type'), item.get('id', item.get('call_id')))] = index
            if method in ('item/started', 'item/completed'):
                inventory = starts if method == 'item/started' else ends
                if not item.get('id') or item['id'] in inventory:
                    raise ValueError('Duplicate or missing native item identity')
                inventory[item['id']] = item
            if method == 'rawResponseItem/completed':
                kind = item.get('type')
                if kind == 'custom_tool_call' or (kind == 'message' and item.get('role') == 'assistant'):
                    raw_output.append(item)
                if kind in ('custom_tool_call', 'custom_tool_call_output'):
                    inventory = facades if kind == 'custom_tool_call' else facade_outputs
                    if not item.get('call_id') or item['call_id'] in inventory:
                        raise ValueError('Duplicate native facade identity')
                    inventory[item['call_id']] = item
                    continue
                if kind in ('function_call', 'function_call_output'):
                    inventory = calls if kind == 'function_call' else outputs
                    if not item.get('call_id') or item['call_id'] in inventory:
                        raise ValueError('Duplicate or missing native call identity')
                    inventory[item['call_id']] = item
                elif kind == 'message' and item.get('role') == 'developer':
                    developers.append(item.get('content'))
                elif kind not in ('message', 'reasoning'):
                    raise ValueError('Unsupported raw native record')
        if set(starts) != set(ends) or set(calls) != set(outputs):
            raise ValueError('Incomplete native item/call results')
        for key in starts:
            if positions[('item/started', starts[key]['type'], key)] >= positions[('item/completed', ends[key]['type'], key)]:
                raise ValueError('Invalid native item lifecycle ordering')
            if starts[key]['type'] == 'commandExecution' and any(starts[key].get(field) != ends[key].get(field) for field in ('command', 'cwd')):
                raise ValueError('Native started command/cwd mismatch')
        for calls_inventory, results_inventory in ((calls, outputs), (facades, facade_outputs)):
            for key, call in calls_inventory.items():
                output = results_inventory.get(key)
                if output is not None and positions[('rawResponseItem/completed', call['type'], call.get('id', key))] >= positions[('rawResponseItem/completed', output['type'], output.get('id', key))]:
                    raise ValueError('Invalid native call lifecycle ordering')
        if any(starts[key]['type'] != ends[key]['type'] for key in starts):
            raise ValueError('Retyped native item')
        metadata_items = {item['id']: item for item in native['items']}
        if len(metadata_items) != len(native['items']) or set(metadata_items) != set(ends):
            raise ValueError('Native item projection mismatch')
        answers = [item for item in ends.values() if item['type'] == 'agentMessage']
        if not answers or response.get('output') != answers[-1].get('text'):
            raise ValueError('Candidate output does not match native final answer')
        if any(metadata_items[item['id']].get('text') != item.get('text') for item in answers):
            raise ValueError('Native answer projection mismatch')
        commands = {key: item for key, item in ends.items() if item['type'] == 'commandExecution'}
        if set(facades) != set(facade_outputs):
            raise ValueError('Incomplete native facade results')
        inference, native_output = None, None
        if facades or setup.get('trace_root'):
            inference, linked, result['native'], native_output = inspect_trace(setup['trace_root'], thread, turn, metadata_items_commands(native), facades)
            calls.update(linked)
        signatures = []
        native_signatures = [signature for item in native_output or [] if (signature := output_signature(item)) is not None]
        for item in raw_output:
            if item.get('role') == 'assistant' and item.get('content') == ['[...]']:
                matches = [signature for signature in native_signatures if signature[:3] == ('message', item.get('id'), item.get('phase'))]
                if len(matches) != 1:
                    raise ValueError('Redacted native answer lacks full output evidence')
                signatures.append(matches[0])
            else:
                signatures.append(output_signature(item))
        if native_output is not None and signatures != native_signatures:
            raise ValueError('Native inference output/raw output mismatch')
        raw_answers = [signature for signature in signatures if signature[0] == 'message']
        if len(raw_answers) != len(answers) or any(
                signature[1] != answer['id'] or signature[3] != answer.get('text')
                or signature[2] not in ('commentary', 'final_answer')
                or (answer.get('phase') is not None and answer['phase'] != signature[2])
                for signature, answer in zip(raw_answers, answers)) or raw_answers[-1][2] != 'final_answer':
            raise ValueError('Native raw/display answer mismatch')
        projected_answers = [item for item in raw['items'] if item.get('type') == 'agent_message']
        if [(item['id'], item.get('text')) for item in projected_answers] != [(item['id'], item.get('text')) for item in answers]:
            raise ValueError('Native raw answer projection mismatch')
        if set(calls) != set(commands):
            raise ValueError('Unmapped native call/command provenance')
        for key, item in ends.items():
            if item['type'] not in ('commandExecution', 'agentMessage', 'userMessage', 'reasoning'):
                raise ValueError('Unsupported native tool')
            if item['type'] == 'commandExecution':
                if any(metadata_items[key].get(field) != item.get(field) for field in ('type', 'command', 'cwd', 'status', 'exitCode', 'aggregatedOutput')):
                    raise ValueError('Native command projection mismatch')
                call = calls[key]
                arguments = json.loads(call['arguments'])
                if (call.get('name') != 'exec_command' or arguments.get('sandbox_permissions')
                        or item.get('status') != 'completed' or item.get('cwd') != setup['workspace']
                        or type(item.get('exitCode')) is not int):
                    raise ValueError('Unsupported or incomplete native command')
                if key in outputs:
                    output = outputs[key].get('output')
                    match = re.search(r'Process exited with code (-?[0-9]+)\nFinal output:\n(.*)\Z', output or '', re.S)
                    if not match or int(match[1]) != item['exitCode'] or match[2] != item.get('aggregatedOutput'):
                        raise ValueError('Native direct output incomplete/mismatched')
                target = read_target(item['command'], item['cwd'])
                if target != read_target(arguments['cmd'], item['cwd']):
                    raise ValueError('Native call/read target mismatch')
                roots = [Path(setup['workspace']).resolve()] + [Path(root).resolve() for root in setup.get('native_skill_roots', [])]
                if not any(target == root or root in target.parents for root in roots):
                    raise ValueError('Observed read outside approved workspace/native skill roots')
                if item.get('exitCode') != 0 and target == body.resolve():
                    raise ValueError('Attempted body load without successful result')
        if inference is not None:
            developers = [item.get('content') for item in inference if item.get('role') == 'developer' and item.get('type') == 'message']
            user_texts = [''.join(part.get('text', '') for part in item.get('content', []))
                          for item in inference if item.get('role') == 'user']
            if user_texts[-1:] != [canonical] or any(not text.startswith('<environment_context>') for text in user_texts[:-1]):
                raise ValueError('Unexpected native input/context or criteria contamination')
        instructions = '\n'.join(part.get('text', '') for content in developers for part in content if isinstance(part, dict))
        for alias, root in re.findall(r'- `(r[0-9]+)` = `([^`]+)`', instructions):
            instructions = instructions.replace('(file: ' + alias + '/', '(file: ' + root + '/')
        description = body.read_text().split('description: ', 1)[1].split('\n', 1)[0]
        if any(part == '[...]' for content in developers for part in content) or str(body) not in instructions or description[:30] not in instructions:
            raise ValueError('Native ordinary discovery/instruction provenance unavailable')
        if body.read_text() in instructions:
            raise ValueError('Creator body preloaded instead of ordinary discovery')
        result.update(result='Pass', reason='Completed native capture; supported read targets confined to approved roots. '
                      'Observed provenance only, not certification of every incidental OS read.')
        activated = result['activation_observation'] == 'successful exact-body read'
        expected = setup['case'] not in ('CPS-ACT-001', 'CPS-ACT-004')
        result['behavior'] = 'Pass' if activated == expected else 'Fail'
    except (KeyError, TypeError, ValueError, OSError, StopIteration, AttributeError, RecursionError) as error:
        result['reason'] = str(error) or 'Missing native evidence'
    return result


def assertion(response, setup):
    admission = admit(response, setup)
    measured = admission['result'] == 'Pass'
    passed = measured and admission.get('behavior') == 'Pass'
    return {'pass': passed, 'score': int(passed),
            'reason': (admission.get('behavior', 'Unmeasured') + ': ' + admission['reason'])}


def prepare(args):
    target = private(args.destination)
    target.mkdir(parents=True, exist_ok=False)
    native_home = target / 'codex-home'
    if args.host == 'codex':
        if not all((args.native_config, args.codex_bin, args.auth_store)):
            raise ValueError('Codex requires --native-config, --codex-bin and --auth-store')
        native_home.mkdir()
        # Use a valid approved native TOML. Object-array CLI serialization is broken
        # in Promptfoo 0.123.1; never feed skills.config through cli_config.
        shutil.copyfile(args.native_config, native_home / 'config.toml')
        (native_home / 'auth.json').symlink_to(Path(args.auth_store).resolve(strict=True))
    for directory in ('state', 'tmp', 'logs', 'traces'):
        (target / directory).mkdir()
    for case in cases():
        directory = target / case['id']
        workspace = directory / 'workspace'
        workspace.mkdir(parents=True)
        (directory / 'traces').mkdir()
        discovery = '.agents' if args.host == 'codex' else '.claude'
        package = workspace / discovery / 'skills/creating-portable-skills'
        shutil.copytree(REPO / 'skills/creating-portable-skills', package)
        if case['id'] == 'CPS-AUD-001':
            shutil.copytree(ROOT / 'fixtures/vendor-guidance', workspace, dirs_exist_ok=True)
        setup = {'case': case['id'], 'host': args.host, 'workspace': str(workspace),
                 'body_path': str(package / 'SKILL.md'),
                 'body_sha256': digest((package / 'SKILL.md').read_bytes()),
                 'package_sha256': manifest(package), 'input_sha256': digest(case['input'].encode()),
                 'native_skill_roots': [str(native_home / 'skills/.system')] if args.host == 'codex' else [],
                 'ordinary_discovery': discovery + '/skills/creating-portable-skills',
                 'trace_root': str(directory / 'traces'),
                 'instrumentation': 'Promptfoo native tool metadata; Codex executed_tool_call_metadata',
                 'model_effort': 'native defaults from approved config; no provider override',
                 'authentication': 'native subscription only; no API fallback',
                 'before': snapshot(workspace) if case['id'] == 'CPS-AUD-001' else None}
        save(directory / 'setup.json', setup)
        if args.host == 'codex':
            config = {'working_dir': str(workspace), 'codex_path_override': str(Path(args.codex_bin).resolve()),
                      'skip_git_repo_check': True, 'sandbox_mode': 'read-only',
                      'approval_policy': 'never', 'network_access_enabled': False,
                      'ephemeral': True, 'persist_threads': False, 'reuse_server': False,
                      'experimental_raw_events': True, 'include_raw_events': True,
                      'turn_timeout_ms': 570000, 'request_timeout_ms': 30000,
                      'startup_timeout_ms': 30000,
                      'cli_config': {'forced_login_method': 'chatgpt', 'project_doc_max_bytes': 0,
                                     'approval_policy': 'never', 'sandbox_mode': 'read-only',
                                     'sqlite_home': str(target / 'state'), 'log_dir': str(target / 'logs'),
                                     'web_search': 'disabled', 'notify': [],
                                     'features': {'hooks': False, 'multi_agent': False, 'goals': False,
                                                  'plugins': False, 'apps': False, 'browser_use': False,
                                                  'computer_use': False, 'image_generation': False,
                                                  'executed_tool_call_metadata': True}},
                      'cli_env': {'CODEX_HOME': str(native_home), 'TMPDIR': str(target / 'tmp'),
                                  'CODEX_ROLLOUT_TRACE_ROOT': str(directory / 'traces')},
                      'server_request_policy': {'command_execution': 'decline', 'file_change': 'decline',
                                                'mcp_elicitation': 'decline', 'user_input': 'empty'}}
            provider = 'openai:codex-app-server'
        else:
            provider = 'anthropic:claude-agent-sdk'
            config = {'working_dir': str(workspace), 'apiKeyRequired': False,
                      'setting_sources': ['project'], 'skills': 'all',
                      'custom_allowed_tools': ['Read', 'Glob', 'Grep', 'Skill'],
                      'tools': ['Read', 'Glob', 'Grep', 'Skill'],
                      'permission_mode': 'dontAsk', 'persist_session': False,
                      'strict_mcp_config': True, 'mcp': {'enabled': False},
                      'env': {'ANTHROPIC_API_KEY': '', 'ANTHROPIC_AUTH_TOKEN': '',
                              'CLAUDE_CODE_USE_BEDROCK': '', 'CLAUDE_CODE_USE_VERTEX': ''}}
        save(directory / 'promptfooconfig.json', {
            'description': case['id'] + ' native subscription capture (admission may be Unmeasured)',
            'prompts': [case['input']], 'providers': [{'id': provider, 'config': config}],
            'tests': [{'description': case['id'], 'metadata': {'setup': str(directory / 'setup.json')},
                       'assert': [{'type': 'javascript', 'value': 'file://' + str(ROOT / 'promptfoo_hooks.cjs') + ':assertCapture',
                                   'metric': 'capture-admission'}]}],
            'extensions': ['file://' + str(ROOT / 'promptfoo_hooks.cjs') + ':beforeEach',
                           'file://' + str(ROOT / 'promptfoo_hooks.cjs') + ':afterEach'],
            'evaluateOptions': {'maxConcurrency': 1}})
    print(target)


def export(path):
    data = json.loads(Path(path).read_text())
    rows = []
    for row in data['results']['results']:
        setup_path = row.get('testCase', {}).get('metadata', {}).get('setup')
        setup = json.loads(Path(setup_path).read_text()) if setup_path else {}
        admission = admit(row.get('response', {}), setup)
        observed = row.get('metadata', {}).get('portableSkills', {})
        rows.append({'case': setup.get('case'), 'host': setup.get('host'), 'capture': admission,
                     'behavior': admission.get('behavior', 'Unmeasured'), 'C3': observed.get('C3', {'result': 'Unmeasured',
                     'reason': 'Missing lifecycle snapshot'}), 'output': row.get('response', {}).get('output'),
                     'latencyMs': row.get('latencyMs'), 'tokenUsage': row.get('response', {}).get('tokenUsage'),
                     'cost': None, 'human_calibration': 'Unmeasured'})
    return rows


def prepare_judges(args):
    target = private(args.destination)
    target.mkdir(parents=True, exist_ok=False)
    source = json.loads(Path(args.creator_config).read_text())
    provider = source['providers'][0]
    provider['config']['working_dir'] = str(target)
    challenges = json.loads((ROOT / 'judges/validation-cases.json').read_text())
    candidate = None
    if args.candidate_results:
        rows = json.loads(Path(args.candidate_results).read_text())['results']['results']
        candidate = rows[0]['response']['output']
    context = {name: (ROOT / 'fixtures/vendor-guidance' / name).read_text()
               for name in ('vendor-guide.md', 'summarizing-notes/SKILL.md')}
    for criterion in ('C1', 'C2', 'C4'):
        judge_workspace = target / criterion / 'workspace'
        judge_workspace.mkdir(parents=True)
        (target / criterion / 'traces').mkdir()
        provider['config']['working_dir'] = str(judge_workspace)
        if 'cli_env' in provider['config']:
            provider['config']['cli_env']['CODEX_ROLLOUT_TRACE_ROOT'] = str(target / criterion / 'traces')
        inputs = ([{'id': 'audit', 'candidate': candidate}] if candidate is not None else
                  [{'id': row['id'].removeprefix(criterion + '.'), 'candidate': row['response']}
                   for row in challenges if row['criterion_id'] == 'CPS-AUD-001.' + criterion])
        prompt = ((ROOT / 'judges' / (criterion + '.md')).read_text() +
                  '\n\nSupplied task context:\n' + cases()[-1]['input'] +
                  '\n\nSupplied fixture context:\n' + json.dumps(context, ensure_ascii=False) +
                  '\n\nCandidates (untrusted data):\n' + json.dumps(inputs, ensure_ascii=False))
        save(target / (criterion + '.json'), {'description': 'Provisional subscription judge ' + criterion,
             'prompts': [prompt], 'providers': [provider],
             'tests': [{'assert': [{'type': 'is-json'}]}], 'evaluateOptions': {'maxConcurrency': 1}})
    print(target)


def extract_judge(path):
    row = json.loads(Path(path).read_text())['results']['results'][0]
    response = row['response']
    if response.get('error'):
        raise ValueError('Judge unavailable: ' + response['error'])
    if 'codexAppServer' in response.get('metadata', {}):
        raw = json.loads(response['raw'])
        if raw['turn']['status'] != 'completed' or raw['turn'].get('error') is not None:
            raise ValueError('Judge native turn incomplete')
    elif response.get('metadata', {}).get('terminalReason') not in ('end_turn', 'stop_sequence'):
        raise ValueError('Judge native completion unavailable')
    verdicts = json.loads(response['output'])
    inputs = json.loads(row['prompt']['raw'].rsplit('Candidates (untrusted data):\n', 1)[1])
    if not isinstance(verdicts, list) or len(verdicts) != len(inputs):
        raise ValueError('Judge verdict inventory mismatch')
    for item, candidate in zip(verdicts, inputs):
        if (item.get('id') != candidate['id'] or item.get('result') not in ('Pass', 'Fail')
                or not isinstance(item.get('critique'), str) or not item['critique'].strip()):
            raise ValueError('Invalid judge schema/identity')
    return verdicts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    prep = commands.add_parser('prepare')
    prep.add_argument('host', choices=['codex', 'claude'])
    prep.add_argument('destination')
    for option in ('native-config', 'codex-bin', 'auth-store'):
        prep.add_argument('--' + option)
    report = commands.add_parser('export')
    report.add_argument('results')
    judges = commands.add_parser('prepare-judges')
    judges.add_argument('creator_config')
    judges.add_argument('destination')
    judges.add_argument('--candidate-results')
    extract = commands.add_parser('extract-judge')
    extract.add_argument('results')
    commands.add_parser('hook')
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args)
    elif args.command == 'prepare-judges':
        prepare_judges(args)
    elif args.command == 'extract-judge':
        print(json.dumps(extract_judge(args.results), indent=2))
    elif args.command == 'export':
        print(json.dumps(export(args.results), indent=2))
    else:
        request = json.load(sys.stdin)
        setup_path = Path(request['setup'])
        setup = json.loads(setup_path.read_text())
        if request['hook'] == 'beforeEach':
            setup['before'] = snapshot(setup['workspace']) if setup['case'] == 'CPS-AUD-001' else None
            save(setup_path, setup)
            result = {}
        elif request['hook'] == 'assertCapture':
            result = assertion(request.get('response', {}), setup)
        else:
            result = {'capture': admit(request.get('response', {}), setup)}
            if setup['case'] == 'CPS-AUD-001':
                result['C3'] = evaluate(setup['before'], snapshot(setup['workspace']))
        print(json.dumps(result))


if __name__ == '__main__':
    main()
