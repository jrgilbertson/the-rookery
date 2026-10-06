"""Prepare private Promptfoo skill evaluations using stock subscription providers."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

from evaluate_read_only import snapshot, evaluate

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
    for directory in ('state', 'tmp', 'logs'):
        (target / directory).mkdir()
    for case in cases():
        directory = target / case['id']
        workspace = directory / 'workspace'
        workspace.mkdir(parents=True)
        discovery = '.agents' if args.host == 'codex' else '.claude'
        package = workspace / discovery / 'skills/creating-portable-skills'
        shutil.copytree(REPO / 'skills/creating-portable-skills', package)
        if case['id'] == 'CPS-AUD-001':
            shutil.copytree(ROOT / 'fixtures/vendor-guidance', workspace, dirs_exist_ok=True)
        setup = {'case': case['id'], 'host': args.host, 'workspace': str(workspace),
                 'body_path': str(package / 'SKILL.md'),
                 'body_sha256': digest((package / 'SKILL.md').read_bytes()),
                 'package_sha256': manifest(package), 'input_sha256': digest(case['input'].encode()),
                 'ordinary_discovery': discovery + '/skills/creating-portable-skills',
                 'evaluation': 'standard Promptfoo assertions; skill-use is heuristic',
                 'model_effort': 'native defaults from approved config; no provider override',
                 'authentication': 'native subscription only; no API fallback',
                 'before': snapshot(workspace) if case['id'] == 'CPS-AUD-001' else None}
        save(directory / 'setup.json', setup)
        if args.host == 'codex':
            config = {'working_dir': str(workspace), 'codex_path_override': str(Path(args.codex_bin).resolve()),
                      'skip_git_repo_check': True, 'sandbox_mode': 'read-only',
                      'approval_policy': 'never', 'network_access_enabled': False,
                      'web_search_mode': 'disabled', 'persist_threads': False,
                      'inherit_process_env': False, 'maxRetries': 0,
                      'cli_config': {'forced_login_method': 'chatgpt', 'project_doc_max_bytes': 0,
                                     'sqlite_home': str(target / 'state'), 'log_dir': str(target / 'logs'),
                                     'notify': [], 'features': {'hooks': False, 'multi_agent': False,
                                                              'plugins': False, 'apps': False}},
                      'cli_env': {'CODEX_HOME': str(native_home), 'TMPDIR': str(target / 'tmp')}}
            provider = 'openai:codex-sdk'
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
        assertions = [
            {'type': 'regex', 'value': r'\S', 'metric': 'final-answer'},
            {'type': 'not-skill-used' if case['id'] in ('CPS-ACT-001', 'CPS-ACT-004') else 'skill-used',
             'value': 'creating-portable-skills', 'metric': 'skill-use-observation'}]
        extensions = []
        if case['id'] == 'CPS-AUD-001':
            assertions.append({'type': 'javascript',
                               'value': 'file://' + str(ROOT / 'promptfoo_hooks.cjs') + ':assertPreservation',
                               'metric': 'C3'})
            extensions = ['file://' + str(ROOT / 'promptfoo_hooks.cjs') + ':beforeEach',
                          'file://' + str(ROOT / 'promptfoo_hooks.cjs') + ':afterEach']
        save(directory / 'promptfooconfig.json', {
            'description': case['id'] + ' subscription skill eval (skill-use observation is heuristic)',
            'prompts': [case['input']], 'providers': [{'id': provider, 'config': config}],
            'tests': [{'description': case['id'], 'metadata': {'setup': str(directory / 'setup.json')},
                       'assert': assertions}], 'extensions': extensions,
            'evaluateOptions': {'maxConcurrency': 1}})
    print(target)


def export(path):
    data = json.loads(Path(path).read_text())
    rows = []
    for row in data['results']['results']:
        setup_path = row.get('testCase', {}).get('metadata', {}).get('setup')
        setup = json.loads(Path(setup_path).read_text()) if setup_path else {}
        observed = row.get('metadata', {}).get('portableSkills', {})
        behavior = 'Unmeasured'
        if (setup.get('case') != 'CPS-AUD-001' and not row.get('error')
                and not row.get('response', {}).get('error') and row.get('gradingResult')
                and observed.get('capture', {}).get('result') != 'Unmeasured'):
            behavior = 'Pass' if row['gradingResult'].get('pass') else 'Fail'
        rows.append({'case': setup.get('case'), 'host': setup.get('host'), 'checks': row.get('gradingResult'),
                     'skill_use': row.get('response', {}).get('metadata', {}).get('skillCalls', []),
                     'capture': 'Unmeasured: strict native provenance is not collected',
                     'behavior': behavior, 'C3': observed.get('C3', {'result': 'Unmeasured',
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
        response = rows[0]['response']
        candidate = response.get('output')
        if rows[0].get('error') or response.get('error') or not isinstance(candidate, str) or not candidate.strip():
            raise ValueError('Creator unavailable or missing final answer')
    context = {name: (ROOT / 'fixtures/vendor-guidance' / name).read_text()
               for name in ('vendor-guide.md', 'summarizing-notes/SKILL.md')}
    for criterion in ('C1', 'C2', 'C4'):
        judge_workspace = target / criterion / 'workspace'
        judge_workspace.mkdir(parents=True)
        provider['config']['working_dir'] = str(judge_workspace)
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
    if row.get('error') or response.get('error'):
        raise ValueError('Judge unavailable: ' + str(row.get('error') or response['error']))
    provider = row.get('provider', {})
    if provider.get('id', '').startswith(('openai:codex-sdk', 'openai:codex:')):
        raw = json.loads(response.get('raw', '{}'))
        if raw.get('finalResponse') != response.get('output') or not isinstance(raw.get('items'), list):
            raise ValueError('Judge SDK final answer unavailable or mismatched')
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
        else:
            preservation = evaluate(setup['before'], snapshot(setup['workspace']))
            result = ({'pass': preservation['result'] == 'Pass',
                       'score': int(preservation['result'] == 'Pass'),
                       'reason': preservation['result'] + ': ' + preservation['reason']}
                      if request['hook'] == 'assertPreservation' else {'C3': preservation})
        print(json.dumps(result))


if __name__ == '__main__':
    main()
