"""Prepare a private Promptfoo skill evaluation using stock subscription providers."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

from evaluate_read_only import snapshot, evaluate

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_case(path):
    text = Path(path).read_text()
    case_id = text.split()[1]
    marker = '## ' + case_id + '.INPUT\n\n'
    if marker not in text:
        raise ValueError('Case file needs a "' + marker.strip() + '" paragraph')
    return {'id': case_id, 'input': text.split(marker, 1)[1].split('\n\n', 1)[0].strip()}


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
    case = read_case(args.case)
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
    directory = target / case['id']
    workspace = directory / 'workspace'
    workspace.mkdir(parents=True)
    discovery = '.agents' if args.host == 'codex' else '.claude'
    package = workspace / discovery / 'skills/creating-portable-skills'
    shutil.copytree(REPO / 'skills/creating-portable-skills', package)
    inputs = []
    if args.fixtures:
        fixtures = Path(args.fixtures)
        inputs = sorted(str(path.relative_to(fixtures)) for path in fixtures.rglob('*') if path.is_file())
        shutil.copytree(fixtures, workspace, dirs_exist_ok=True)
    setup = {'case': case['id'], 'host': args.host, 'workspace': str(workspace),
             'body_path': str(package / 'SKILL.md'),
             'body_sha256': digest((package / 'SKILL.md').read_bytes()),
             'package_sha256': manifest(package), 'input_sha256': digest(case['input'].encode()),
             'ordinary_discovery': discovery + '/skills/creating-portable-skills',
             'evaluation': 'standard Promptfoo assertions; skill-use is heuristic',
             'model_effort': 'native defaults from approved config; no provider override',
             'authentication': 'native subscription only; no API fallback',
             'inputs': inputs, 'before': snapshot(workspace, inputs) if inputs else None}
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
        {'type': 'not-skill-used' if args.expect_no_skill_use else 'skill-used',
         'value': 'creating-portable-skills', 'metric': 'skill-use-observation'}]
    extensions = []
    if inputs:
        hooks = 'file://' + str(ROOT / 'promptfoo_hooks.cjs')
        assertions.append({'type': 'javascript', 'value': hooks + ':assertPreservation',
                           'metric': 'input-preservation'})
        extensions = [hooks + ':beforeEach', hooks + ':afterEach']
    save(directory / 'promptfooconfig.json', {
        'description': case['id'] + ' subscription skill eval (skill-use observation is heuristic)',
        'prompts': [case['input']], 'providers': [{'id': provider, 'config': config}],
        'tests': [{'description': case['id'], 'metadata': {'setup': str(directory / 'setup.json')},
                   'assert': assertions}], 'extensions': extensions,
        'evaluateOptions': {'maxConcurrency': 1}})
    print(directory)


def export(path):
    data = json.loads(Path(path).read_text())
    rows = []
    for row in data['results']['results']:
        setup_path = row.get('testCase', {}).get('metadata', {}).get('setup')
        setup = json.loads(Path(setup_path).read_text()) if setup_path else {}
        observed = row.get('metadata', {}).get('portableSkills', {})
        behavior = 'Unmeasured'
        if (not row.get('error') and not row.get('response', {}).get('error') and row.get('gradingResult')
                and observed.get('capture', {}).get('result') != 'Unmeasured'):
            behavior = 'Pass' if row['gradingResult'].get('pass') else 'Fail'
        rows.append({'case': setup.get('case'), 'host': setup.get('host'), 'checks': row.get('gradingResult'),
                     'skill_use': row.get('response', {}).get('metadata', {}).get('skillCalls', []),
                     'capture': 'Unmeasured: strict native provenance is not collected',
                     'behavior': behavior,
                     'preservation': observed.get('preservation') if setup.get('inputs') else None,
                     'output': row.get('response', {}).get('output'),
                     'latencyMs': row.get('latencyMs'), 'tokenUsage': row.get('response', {}).get('tokenUsage'),
                     'cost': None, 'human_calibration': 'Unmeasured'})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    prep = commands.add_parser('prepare')
    prep.add_argument('host', choices=['codex', 'claude'])
    prep.add_argument('case')
    prep.add_argument('destination')
    prep.add_argument('--fixtures', help='synthetic input files copied into the workspace and checked unchanged')
    prep.add_argument('--expect-no-skill-use', action='store_true')
    for option in ('native-config', 'codex-bin', 'auth-store'):
        prep.add_argument('--' + option)
    report = commands.add_parser('export')
    report.add_argument('results')
    commands.add_parser('hook')
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args)
    elif args.command == 'export':
        print(json.dumps(export(args.results), indent=2))
    else:
        request = json.load(sys.stdin)
        setup_path = Path(request['setup'])
        setup = json.loads(setup_path.read_text())
        if request['hook'] == 'beforeEach':
            setup['before'] = snapshot(setup['workspace'], setup['inputs']) if setup['inputs'] else None
            save(setup_path, setup)
            result = {}
        else:
            preservation = evaluate(setup['before'], snapshot(setup['workspace'], setup['inputs']))
            result = ({'pass': preservation['result'] == 'Pass',
                       'score': int(preservation['result'] == 'Pass'),
                       'reason': preservation['result'] + ': ' + preservation['reason']}
                      if request['hook'] == 'assertPreservation' else {'preservation': preservation})
        print(json.dumps(result))


if __name__ == '__main__':
    main()
