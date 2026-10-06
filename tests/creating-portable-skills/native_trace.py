"""Bounded Codex 0.160 native trace inspection for completed cat-only cells."""
import json
import shlex
from pathlib import Path


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate native JSON key')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def command_words(command):
    """Pinned native argv or shell display, restricted to one literal cat read."""
    words = shlex.split(command) if isinstance(command, str) else command
    if not isinstance(words, list) or any(not isinstance(word, str) for word in words):
        raise ValueError('Unsupported native command argv')
    if len(words) == 3 and words[0] in ('/bin/zsh', '/bin/bash', '/bin/sh') and words[1] in ('-c', '-lc'):
        words = shlex.split(words[2])
    if (len(words) != 2 or words[0] not in ('cat', '/bin/cat', '/usr/bin/cat')
            or any(char in words[1] for char in '$`*?{}~;|&<>\n\r()')):
        raise ValueError('Opaque or unsupported command read provenance')
    return ['cat', words[1]]


def output_signature(item):
    """Compare pinned model output fields, excluding transport-only metadata."""
    if item.get('type') == 'message' and item.get('role') == 'assistant':
        content = item['content']
        if not isinstance(content, list) or any(not isinstance(p, dict) or p.get('type') != 'output_text'
                                              or not isinstance(p.get('text'), str) for p in content):
            raise ValueError('Unsupported native assistant output')
        return ('message', item['id'], item['phase'], ''.join(p['text'] for p in content))
    if item.get('type') == 'custom_tool_call':
        return ('custom_tool_call', item['id'], item['call_id'], item['name'], item['input'])
    if item.get('type') == 'reasoning':
        return None
    raise ValueError('Unsupported native inference output')


def inspect(root, thread, turn, commands, facades):
    matches = []
    for path in Path(root).glob('*/manifest.json'):
        header = load(path)
        if header.get('root_thread_id') == thread:
            matches.append((path.parent, header))
    if len(matches) != 1:
        raise ValueError('Missing or ambiguous matching native trace')
    directory, header = matches[0]
    if header.get('schema_version') != 1 or header.get('rollout_id') != thread:
        raise ValueError('Unsupported native trace identity/schema')
    def payload(reference):
        path = (directory / reference['path']).resolve()
        if directory.resolve() not in path.parents or path.is_symlink():
            raise ValueError('Native payload outside bundle')
        return load(path)
    events = [json.loads(line) for line in (directory / 'trace.jsonl').read_text().splitlines()]
    if not events or [event['seq'] for event in events] != list(range(1, len(events) + 1)):
        raise ValueError('Incomplete native event sequence')
    records = [event['payload'] for event in events]
    supported = {'rollout_started', 'rollout_ended', 'thread_started', 'thread_ended',
                 'codex_turn_started', 'codex_turn_ended', 'protocol_event_observed',
                 'inference_started', 'inference_completed', 'code_cell_started',
                 'code_cell_initial_response', 'code_cell_ended', 'tool_call_started',
                 'tool_call_ended', 'tool_call_runtime_started', 'tool_call_runtime_ended'}
    if any(record['type'] not in supported for record in records):
        raise ValueError('Unsupported native trace record')
    if records[0]['type'] != 'rollout_started' or records[-1] != {'type': 'rollout_ended', 'status': 'completed'}:
        raise ValueError('Native trace not closed')
    if any(event['schema_version'] != 1 or event['rollout_id'] != thread or
           event.get('thread_id') not in (None, thread) or event.get('codex_turn_id') not in (None, turn)
           for event in events):
        raise ValueError('Foreign native trace identity')
    def inventory(kind, key):
        selected = [record for record in records if record['type'] == kind]
        result = {record[key]: record for record in selected}
        if len(result) != len(selected):
            raise ValueError('Duplicate native trace lifecycle identity')
        return result
    positions = {id(record): index for index, record in enumerate(records)}
    def before(start, end):
        if positions[id(start)] >= positions[id(end)]:
            raise ValueError('Invalid native lifecycle ordering')
    turns = inventory('codex_turn_started', 'codex_turn_id')
    turn_ends = inventory('codex_turn_ended', 'codex_turn_id')
    if set(turns) != {turn} or set(turn_ends) != {turn} or turn_ends[turn]['status'] != 'completed':
        raise ValueError('Incomplete native turn lifecycle')
    before(turns[turn], turn_ends[turn])
    for record in records:
        if record['type'].startswith(('inference_', 'code_cell_', 'tool_call_')):
            before(turns[turn], record)
            before(record, turn_ends[turn])
    def paired(starts, ends):
        if set(starts) != set(ends):
            raise ValueError('Incomplete native lifecycle inventory')
        for key in starts:
            before(starts[key], ends[key])
    infer = inventory('inference_started', 'inference_call_id')
    if not infer or set(infer) != set(inventory('inference_completed', 'inference_call_id')):
        raise ValueError('Incomplete native inference lifecycle')
    infer_ends = inventory('inference_completed', 'inference_call_id')
    paired(infer, infer_ends)
    requests = {key: payload(record['request_payload']) for key, record in infer.items()}
    first = next(iter(requests.values()))
    def context(request):
        return [item for item in request['input'] if item.get('role') in ('system', 'developer', 'user')]
    stable = context(first)
    response_ids, output_items = {}, []
    for key, request in requests.items():
        if request['model'] != first['model']:
            raise ValueError('Native inference model changed during turn')
        current = context(request)
        previous = request.get('previous_response_id')
        if previous is not None:
            if (request.get('type') != 'response.create' or previous not in response_ids
                    or positions[id(response_ids[previous])] >= positions[id(infer[key])]
                    or current):
                raise ValueError('Native inference context/delta mismatch')
        elif current != stable:
            raise ValueError('Native inference context changed during turn')
        for item in request['input']:
            if (item.get('role') not in ('system', 'developer', 'user', 'assistant')
                    and item.get('type') not in ('reasoning', 'custom_tool_call', 'custom_tool_call_output',
                                                'function_call', 'function_call_output')):
                raise ValueError('Unsupported native inference context')
        response = payload(infer_ends[key]['response_payload'])
        if infer_ends[key].get('response_id', response.get('response_id')) != response.get('response_id'):
            raise ValueError('Native inference response identity mismatch')
        if not isinstance(response['output_items'], list) or not response.get('response_id') or response['response_id'] in response_ids:
            raise ValueError('Missing or duplicate native inference output inventory')
        for item in response['output_items']:
            output_signature(item)
        output_items.extend(response['output_items'])
        response_ids[response['response_id']] = infer_ends[key]
    sessions = [payload(record['metadata_payload']) for record in records if record['type'] == 'thread_started']
    if len(sessions) != 1:
        raise ValueError('Native session metadata unavailable')
    session = sessions[0]
    workspace = next(iter(commands.values()))['cwd'] if commands else session['cwd']
    if (session['thread_id'] != thread or session['cwd'] != workspace or session['approval_policy'] != 'never'
            or session['sandbox_policy'] != 'ReadOnly { network_access: false }' or session['model'] != first['model']):
        raise ValueError('Native effective session policy/model mismatch')
    cells = inventory('code_cell_started', 'runtime_cell_id')
    ended_cells = inventory('code_cell_ended', 'runtime_cell_id')
    initial = inventory('code_cell_initial_response', 'runtime_cell_id')
    if set(cells) != set(ended_cells) or set(cells) != set(initial):
        raise ValueError('Incomplete CodeMode cell lifecycle')
    paired(cells, initial)
    paired(initial, ended_cells)
    if {cell['model_visible_call_id'] for cell in cells.values()} != set(facades):
        raise ValueError('Native facade inventory mismatch')
    for key, cell in cells.items():
        facade = facades[cell['model_visible_call_id']]
        if facade.get('name') != 'exec' or facade.get('input') != cell['source_js']:
            raise ValueError('Native facade source mismatch')
        if ended_cells[key]['status'] != 'completed' or initial[key]['status'] != 'completed':
            raise ValueError('Yielded or failed CodeMode cell is unsupported')
        payload(ended_cells[key]['response_payload'])
    calls = inventory('tool_call_started', 'tool_call_id')
    ends = inventory('tool_call_ended', 'tool_call_id')
    runtime_starts = inventory('tool_call_runtime_started', 'tool_call_id')
    runtime_ends = inventory('tool_call_runtime_ended', 'tool_call_id')
    if not (set(calls) == set(ends) == set(runtime_starts) == set(runtime_ends) == set(commands)):
        gaps = []
        for label, observed in (('child results', ends), ('runtime starts', runtime_starts),
                                ('runtime ends', runtime_ends), ('provider commands', commands)):
            missing, extra = sorted(set(calls) - set(observed)), sorted(set(observed) - set(calls))
            if missing or extra:
                gaps.append(label + ' missing=' + json.dumps(missing) + ' extra=' + json.dumps(extra))
        raise ValueError('Native child call/command inventory mismatch: ' + '; '.join(gaps))
    paired(calls, runtime_starts)
    paired(runtime_starts, runtime_ends)
    paired(calls, ends)
    linked = {}
    for key, call in calls.items():
        if call['kind'] != {'type': 'exec_command'} or ends[key]['status'] != 'completed':
            raise ValueError('Unsupported native child tool/result')
        if call['requester'].get('type') == 'code_cell' and call['requester'].get('runtime_cell_id') not in cells:
            raise ValueError('Foreign native child cell')
        if call['requester'].get('type') != 'code_cell':
            raise ValueError('Unsupported native child requester')
        parent = call['requester']['runtime_cell_id']
        before(cells[parent], call)
        before(ends[key], ended_cells[parent])
        before(runtime_ends[key], ended_cells[parent])
        invocation = payload(call['invocation_payload'])
        if invocation.get('tool_name') != 'exec_command' or invocation['payload']['type'] != 'function':
            raise ValueError('Unsupported native invocation')
        arguments = json.loads(invocation['payload']['arguments'])
        start = payload(runtime_starts[key]['runtime_payload'])
        end = payload(runtime_ends[key]['runtime_payload'])
        item = commands[key]
        if not (command_words(start['command']) == command_words(item['command']) == command_words(arguments['cmd'])):
            raise ValueError('Native runtime command mismatch')
        if (start['call_id'] != key or end['call_id'] != key or start['turn_id'] != turn or end['turn_id'] != turn
                or start['process_id'] != end['process_id'] or start['command'] != end['command']
                or start['cwd'] != end['cwd'] or end['cwd'] != item['cwd']
                or end['exit_code'] != item['exitCode'] or end['stdout'] != item['aggregatedOutput']
                or end.get('stderr') or end.get('aggregated_output', end['stdout']) != item['aggregatedOutput']):
            raise ValueError('Native child runtime/result mismatch')
        result = payload(ends[key]['result_payload'])
        if result.get('type') != 'code_mode_response' or result['value'].get('session_id'):
            raise ValueError('Unsupported or running native child result')
        if result['value']['exit_code'] != item['exitCode'] or result['value']['output'] != item['aggregatedOutput']:
            raise ValueError('Native child output mismatch/truncation')
        linked[key] = {'name': 'exec_command', 'arguments': json.dumps(arguments)}
    return first['input'], linked, {'model': session['model'], 'reasoning': first.get('reasoning'),
                                   'cwd': session['cwd'], 'sandbox': session['sandbox_policy'],
                                   'approval_policy': session['approval_policy']}, output_items
