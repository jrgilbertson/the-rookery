"""Zero-inference tests: all subprocess launches and pricing are fake."""
import base64
import time
import datetime as dt
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import harness as h


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.original = h.CFG, h.ARGS, h.REAL_HOME
        h.ARGS = None
        h.REAL_HOME = self.root / 'user'
        h.CFG = {'repo': 'sample', 'skill': 'demo', 'repo_path': str(self.root / 'repo'),
                 'archive_root': str(self.root / 'archive'), 'workspace_root': str(self.root / 'scratch'),
                 'iteration': 1, 'arms': {'with_skill': 'abc12345'}, 'changed_arm': 'with_skill',
                 'budget_usd': 10, 'call_allowance_usd': 1, 'targets': {
                     'executor': {'adapter': 'codex', 'model': 'executor-model', 'grader': 'judge'},
                     'judge': {'adapter': 'grok', 'model': 'judge-model'}}}
        self.config = self.root / 'private' / 'round.json'
        h.validate_config(self.config)
        self.env = patch.dict(os.environ, {'PATH': os.defpath}, clear=True)
        self.env.start()
        payload = base64.urlsafe_b64encode(json.dumps({'exp': time.time() + 3600}).encode()).decode().rstrip('=')
        self.grok_auth = {'https://auth.x.ai::client': {'auth_mode': 'oidc', 'key': 'subscription-token',
            'expires_at': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)).isoformat()}}
        for adapter, auth in [('codex', {'auth_mode': 'chatgpt', 'tokens': {'access_token': f'header.{payload}.signature'}}),
                              ('grok', self.grok_auth)]:
            h.wjson(h.REAL_HOME / f'.{adapter}/auth.json', auth)
        Path(h.CFG['workspace_root']).mkdir()
        self.ev = {'id': 1, 'name': 'sample', 'prompt': 'Do the thing', 'expected_output': 'Done',
                   'assertions': ['Does the thing'], 'files': []}
        h.wjson(Path(h.CFG['repo_path']) / 'skills/demo/evals/evals.json', {'evals': [self.ev]})
        package = h.iteration_dir() / 'packages/with_skill/demo'
        package.mkdir(parents=True)
        (package / 'SKILL.md').write_text('Do the thing')
        self.packages = {'with_skill': {'skill_revision': 'abc12345', 'package_hash': h.tree_hash(package)}}
        h.wjson(h.iteration_dir() / 'packages.json', self.packages)
        self.process_calls = []
        self.estimates = []
        self.costs = [0.25]
        self.fail_grader = False
        self.quota = False
        self.json_quota = False
        self.process = patch.object(h.subprocess, 'Popen', side_effect=self.fake_process)
        self.process.start()
        self.pricing = patch.object(h.usage, 'estimate', side_effect=self.fake_estimate)
        self.pricing.start()
        self.which = patch.object(h.shutil, 'which', side_effect=lambda binary, **kw: '/fake/bin/' + binary)
        self.which.start()
        self.remote = patch.object(h, 'git', return_value='https://github.com/example/sample.git')
        self.remote.start()
        self.version = patch.object(h, 'cli_version', return_value='official-cli test-version')
        self.version.start()

    def tearDown(self):
        self.version.stop()
        self.remote.stop()
        self.which.stop()
        self.pricing.stop()
        self.process.stop()
        self.env.stop()
        h.CFG, h.ARGS, h.REAL_HOME = self.original
        self.tmp.cleanup()

    def fake_process(self, argv, **kwargs):
        self.process_calls.append((argv, kwargs))
        home = Path(kwargs['env']['HOME'])
        adapter = 'codex' if argv[0].endswith('codex') else 'grok'
        sessions = home / f'.{adapter}/sessions'
        sessions.mkdir(parents=True)
        h.wjson(sessions / 'marker.json', {'fake': True})
        # Model refreshes its isolated auth; this must never reach the user's auth.
        h.wjson(home / f'.{adapter}/auth.json', {'refreshed': True})
        if adapter == 'codex':
            prompt = argv[-1]
            skill = prompt.split('Read ', 1)[1].split(' and follow', 1)[0]
            trace = [{'type': 'item.completed', 'item': {'type': 'command_execution',
                       'command': 'cat ' + skill, 'aggregated_output': 'x' * 2000}},
                     {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Done'}},
                     {'type': 'turn.completed', 'usage': {'input_tokens': 10, 'output_tokens': 2}}]
            kwargs['stdout'].write(''.join(json.dumps(x) + '\n' for x in trace).encode())
        else:
            result = {'grades': [{'letter': 'A', 'items': [{'n': 1, 'evidence': 'Done',
                       'reasoning': 'It did the thing', 'passed': True}], 'passed': True}]}
            kwargs['stdout'].write(json.dumps({'structuredOutput': result, 'text': 'graded', 'total_cost_usd': 9}).encode())
        if self.json_quota:
            kwargs['stdout'].write(b'\n{"type":"turn.failed","error":{"message":"quota exhausted"}}\n')
        if self.quota:
            kwargs['stderr'].write(b'usage limit reached')
        return FakeProcess(1 if self.quota or self.json_quota or adapter == 'grok' and self.fail_grader else 0)

    def fake_estimate(self, adapter, transcript, sessions, output, command, scratch_root, model=None):
        self.assertTrue(transcript.exists())
        self.assertTrue((sessions / 'marker.json').exists())
        self.estimates.append((adapter, model, sessions))
        cost = self.costs.pop(0) if len(self.costs) > 1 else self.costs[0]
        record = {'cost_usd': cost, 'total_tokens': 12 if cost is not None else None,
                  'source': 'ccusage', 'basis': 'api_equivalent_estimate',
                  'errors': [] if cost is not None else ['unknown model']}
        if cost is not None:
            record['report'] = {'sessions': [{'sessionId': 'fake'}],
                                'totals': {'costUSD': cost, 'totalTokens': 12}}
        h.wjson(output, record)
        return record

    def execute(self, k=1):
        return h.execute_one('executor', self.ev, 'with_skill', k, h.load_evals()[1], self.packages)

    def test_ledger_and_cost_record_must_agree_before_next_call(self):
        self.costs = [None]
        with self.assertRaises(h.Budget):
            self.execute()
        row = h.ledger_entries()[0]
        ledger = h.iteration_dir() / '_ledger.jsonl'
        row['cost_usd'] = 0.0
        ledger.write_text(json.dumps(row) + '\n')
        with self.assertRaises(h.Budget):
            h.allowance()
        with self.assertRaises(h.Budget):
            self.execute(2)
        self.assertEqual(len(self.process_calls), 1)

    def test_cost_record_shape_and_reconciliation(self):
        self.execute()
        record = h.run_dir('executor', self.ev, 'with_skill', 1) / 'cost.json'
        for change in ({'total_tokens': None}, {'basis': None}, {'errors': ['pricing incomplete']},
                       {'cost_usd': 0.0}):
            original = h.rjson(record)
            h.wjson(record, {**original, **change})
            with self.subTest(change=change), self.assertRaises(h.Budget):
                h.allowance()
            h.wjson(record, original)

    def test_changed_eval_report_uses_frozen_assertions_and_is_incomplete(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        eval_path = Path(h.CFG['repo_path']) / 'skills/demo/evals/evals.json'
        changed = h.rjson(eval_path)
        changed['evals'][0]['assertions'] = ['Assertion added after grading']
        h.wjson(eval_path, changed)
        path = h.report(['executor'])[0]
        report = h.rjson(path)
        self.assertEqual(path.parent.name, 'incomplete')
        self.assertEqual(report['runs'][0]['assertion_results'][0]['text'], 'Does the thing')
        self.assertFalse(report['metadata']['identity_verified'])

    def test_matching_frozen_report_is_a_benchmark(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        path = h.report(['executor'])[0]
        report = h.rjson(path)
        self.assertEqual(path.parent.name, 'benchmark')
        self.assertTrue(report['metadata']['identity_verified'])
        self.assertEqual(report['runs'][0]['assertion_results'][0]['text'], 'Does the thing')

    def test_changed_config_report_keeps_original_model_and_revision(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        h.CFG['targets']['executor']['model'] = 'new-model'
        h.CFG['arms']['with_skill'] = 'newrevision'
        path = h.report(['executor'])[0]
        report = h.rjson(path)
        self.assertEqual(path.parent.name, 'incomplete')
        self.assertEqual(report['metadata']['executor_model'], 'executor-model')
        self.assertIn('abc12345', path.name)

    def test_truncated_jsonl_is_archived_and_discarded(self):
        def damaged(argv, **kwargs):
            self.process_calls.append((argv, kwargs))
            home = Path(kwargs['env']['HOME'])
            sessions = home / '.codex/sessions'
            sessions.mkdir(parents=True)
            h.wjson(sessions / 'marker.json', {'fake': True})
            skill = argv[-1].split('Read ', 1)[1].split(' and follow', 1)[0]
            good = {'type': 'item.completed', 'item': {'type': 'command_execution',
                    'command': 'cat ' + skill, 'aggregated_output': 'skill content'}}
            end = {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Done'}}
            kwargs['stdout'].write((json.dumps(good) + '\n' +
                '{"type":"item.completed","item":{"type":"command_execution","command":"cat /foreign/SKILL.md"\n' +
                json.dumps(end) + '\n').encode())
            return FakeProcess(0)
        h.subprocess.Popen.side_effect = damaged
        self.assertEqual(self.execute(), 'error')
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        self.assertEqual(len((rd / 'transcript').read_text().splitlines()), 3)
        self.assertTrue((rd / 'parse-error.json').exists())
        self.assertFalse(h.counted_runs('executor', self.ev)[0])

    def test_packet_omits_skill_text_and_preserves_actions_and_project_artifacts(self):
        package = h.iteration_dir() / 'packages/with_skill/demo/SKILL.md'
        package.write_text('UNIQUE_VARIANT_MARKER_ONLY_IN_SKILL_PACKAGE')
        self.packages['with_skill']['package_hash'] = h.tree_hash(package.parent)
        original = self.fake_process
        def with_artifact_and_child(argv, **kwargs):
            result = original(argv, **kwargs)
            Path(kwargs['cwd'], 'result.txt').write_text('PROJECT_RESULT_MARKER')
            sessions = Path(kwargs['env']['HOME']) / '.codex/sessions'
            rows = [{'type': 'session_meta', 'payload': {'parent_thread_id': 'parent'}},
                    {'type': 'event_msg', 'payload': {'type': 'agent_message',
                     'message': 'CHILD_RESULT_MARKER'}}]
            (sessions / 'rollout-child.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows))
            return result
        h.subprocess.Popen.side_effect = with_artifact_and_child
        self.assertEqual(self.execute(), 'ok')
        runs, _ = h.counted_runs('executor', self.ev)
        packet, _ = h.build_packet(self.ev, runs, 'seed')
        self.assertNotIn('UNIQUE_VARIANT_MARKER_ONLY_IN_SKILL_PACKAGE', packet)
        self.assertNotIn('x' * 2000, packet)
        self.assertIn('command_execution', packet)
        self.assertIn('SKILL.md', packet)
        self.assertIn('PROJECT_RESULT_MARKER', packet)
        self.assertIn('CHILD_RESULT_MARKER', packet)
        self.assertNotIn('skills/demo/SKILL.md": {', packet)

    def test_mutated_staged_skill_is_discarded_without_exposing_body(self):
        original = self.fake_process
        def mutated(argv, **kwargs):
            result = original(argv, **kwargs)
            skill = argv[-1].split('Read ', 1)[1].split(' and follow', 1)[0]
            Path(skill).write_text('modified during execution')
            return result
        h.subprocess.Popen.side_effect = mutated
        self.assertEqual(self.execute(), 'discarded')
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        obs = h.rjson(rd / 'outputs/observations.json')
        self.assertFalse(obs['skill_package_unchanged'])
        self.assertNotIn('modified during execution', json.dumps(obs))

    def test_grade_rejects_nonstring_evidence_and_reasoning(self):
        result = {'grades': [{'letter': 'A', 'passed': True, 'items': [
            {'n': 1, 'evidence': True, 'reasoning': 42, 'passed': True}]}]}
        self.assertIsNotNone(h.validate(result, {'A': {}}, 1))

    def test_missing_cost_stops_next_call(self):
        self.costs = [None]
        with self.assertRaises(h.Budget):
            self.execute()
        with self.assertRaises(h.Budget):
            self.execute(2)
        self.assertEqual(len(self.process_calls), 1)
        self.assertIsNone(h.ledger_entries()[0]['cost_usd'])
        self.assertTrue((h.run_dir('executor', self.ev, 'with_skill', 1) / 'sessions/marker.json').exists())

    def test_cost_totals_include_all_providers_and_failed_grading(self):
        self.costs = [0.25, 0.75]
        self.execute()
        self.fail_grader = True
        self.assertFalse(h.grade_one('executor', self.ev))
        self.assertEqual(h.spent(), 1)
        rows = h.ledger_entries()
        self.assertEqual([e['provider'] for e in rows], ['openai', 'xai'])
        self.assertEqual(rows[1]['kind'], 'grade')
        self.assertEqual(rows[1]['cli_cost_usd'], 9)
        self.assertEqual(rows[1]['cost_usd'], .75)
        self.assertEqual([e[1] for e in self.estimates], ['executor-model', 'judge-model'])
        self.assertFalse(any(Path(h.CFG['workspace_root']).iterdir()))
        self.assertEqual(h.rjson(h.REAL_HOME / '.grok/auth.json'), self.grok_auth)

    def test_failed_grader_attempt_is_preserved_on_explicit_retry(self):
        self.execute()
        self.fail_grader = True
        self.assertFalse(h.grade_one('executor', self.ev))
        self.fail_grader = False
        self.assertTrue(h.grade_one('executor', self.ev))
        attempts = sorted((h.iteration_dir() / 'executor/grading/eval-1-sample').glob('attempt-*'))
        self.assertEqual(len(attempts), 2)
        self.assertTrue(all((p / 'sessions/marker.json').exists() for p in attempts))
        self.assertEqual(h.spent(), .75)

    def test_unknown_grading_cost_stops_next_inference(self):
        self.execute()
        self.costs = [None]
        with self.assertRaises(h.Budget):
            h.grade_one('executor', self.ev)
        with self.assertRaises(h.Budget):
            self.execute(2)
        self.assertEqual(len(self.process_calls), 2)

    def test_subscription_guard_rejects_env_and_config_without_fallback(self):
        for key in ('OPENAI_API_KEY', 'XAI_API_KEY', 'ANTHROPIC_API_KEY'):
            with self.subTest(key=key), patch.dict(os.environ, {key: 'fake'}):
                with self.assertRaises(h.Halt):
                    self.execute()
        h.CFG['billing'] = {'api_key': 'fake'}
        with self.assertRaises(h.Halt):
            self.execute()
        self.assertFalse(self.process_calls)

    def test_current_grok_oidc_subscription_format(self):
        h.wjson(h.REAL_HOME / '.grok/auth.json', {'https://auth.x.ai::client': {
            'auth_mode': 'oidc', 'key': 'subscription-token',
            'expires_at': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)).isoformat()}})
        h.subscription_guard(h.ADAPTERS['grok'])

    def test_expired_subscription_is_blocked_before_launch(self):
        h.wjson(h.REAL_HOME / '.grok/auth.json', {'https://auth.x.ai::client': {
            'auth_mode': 'oidc', 'key': 'subscription-token', 'expires_at': '2000-01-01T00:00:00Z'}})
        with self.assertRaises(h.Halt):
            h.subscription_guard(h.ADAPTERS['grok'])

    def test_subscription_guard_rejects_api_auth_and_unknown_auth(self):
        for adapter, auth in [('codex', {'auth_mode': 'api', 'OPENAI_API_KEY': 'fake'}),
                              ('grok', {'api_key': 'fake'}), ('grok', {'mystery': 'fake'})]:
            h.wjson(h.REAL_HOME / f'.{adapter}/auth.json', auth)
            with self.subTest(adapter=adapter), self.assertRaises(h.Halt):
                h.subscription_guard(h.ADAPTERS[adapter])
        with self.assertRaises(h.Halt):
            h.subscription_guard(h.ADAPTERS['claude'])
        self.assertFalse(self.process_calls)

    def test_quota_failure_retains_cost_and_stops_without_retry(self):
        self.quota = True
        with self.assertRaises(h.Halt):
            self.execute()
        self.assertEqual(len(self.process_calls), 1)
        self.assertEqual(h.spent(), .25)
        self.assertEqual(h.status_of(h.run_dir('executor', self.ev, 'with_skill', 1)), 'login_or_quota')

    def test_current_round_only_and_allowance_is_preflight(self):
        h.wjson(h.skill_dir() / 'iteration-2/unused.json', {})
        (h.skill_dir() / 'iteration-2/_ledger.jsonl').write_text('{"cost_usd": null}\n')
        self.assertEqual(h.spent(), 0)
        self.costs = [11]
        self.execute()
        self.assertEqual(h.spent(), 11)
        with self.assertRaises(h.Budget):
            self.execute(2)
        self.assertEqual(len(self.process_calls), 1)

    def test_failed_launch_still_gets_cost_record(self):
        h.subprocess.Popen.side_effect = OSError('fake launch failure')
        h.usage.estimate.side_effect = lambda *a, **kw: {'cost_usd': None, 'total_tokens': None, 'source': 'ccusage'}
        with self.assertRaises(h.Budget):
            self.execute()
        self.assertEqual(len(h.ledger_entries()), 1)
        self.assertEqual(h.status_of(h.run_dir('executor', self.ev, 'with_skill', 1)), 'error')

    def test_config_private_paths_and_path_escape(self):
        original = copy.deepcopy(h.CFG)
        for key in ('archive_root', 'workspace_root'):
            h.CFG = copy.deepcopy(original)
            h.CFG[key] = str(Path(h.CFG['repo_path']) / 'generated')
            with self.assertRaises(ValueError):
                h.validate_config(self.config)
        h.CFG = copy.deepcopy(original)
        with self.assertRaises(ValueError):
            h.validate_config(Path(h.CFG['repo_path']) / 'round.json')
        h.CFG['archive_root'] = str(h.H / 'archives')
        with self.assertRaises(ValueError):
            h.validate_config(self.config)
        h.CFG = copy.deepcopy(original)
        h.CFG['skill'] = '../escape'
        with self.assertRaises(ValueError):
            h.validate_config(self.config)

    def test_config_defaults_and_different_model_grader(self):
        self.assertEqual(h.CFG['runs'], 1)
        self.assertEqual(h.CFG['ccusage_command'], ['ccusage'])
        self.assertEqual(h.CFG['run_arms'], ['with_skill'])
        h.CFG['targets']['judge']['model'] = 'executor-model'
        with self.assertRaises(ValueError):
            h.validate_config(self.config)

    def test_no_threshold_and_no_concurrency_options(self):
        for key in ('thresholds', 'reuse', 'carry_forward', 'capped_providers'):
            h.CFG[key] = {}
            with self.assertRaises(ValueError):
                h.validate_config(self.config)
            del h.CFG[key]

    def test_report_raw_results_no_delta_and_includes_grade_failure_cost(self):
        self.execute()
        self.fail_grader = True
        h.grade_one('executor', self.ev)
        h.CFG['arms']['old_skill'] = 'deadbeef'
        h.CFG['run_arms'].append('old_skill')
        report = h.rjson(h.report(['executor'])[0])
        self.assertNotIn('delta', report['run_summary'])
        self.assertEqual(report['metadata']['cost_usd'], .5)
        self.assertEqual(len(report['runs']), 1)
        self.assertFalse(report['metadata']['identity_verified'])
        self.assertTrue(all(row['needs_operator_review'] for row in report['runs']))

    def test_lost_ledger_cannot_make_existing_attempt_free(self):
        self.execute()
        (h.iteration_dir() / '_ledger.jsonl').unlink()
        with self.assertRaises(h.Budget):
            h.allowance()

    def test_missing_pricing_cli_stops_main_before_inference(self):
        h.wjson(self.config, h.CFG)
        argv = ['harness.py', 'run', '--round', str(self.config)]
        with patch.object(h.sys, 'argv', argv), patch.object(h.subprocess, 'run', side_effect=FileNotFoundError()):
            with self.assertRaises(h.Halt):
                h.main()
        self.assertEqual(self.process_calls, [])

    def test_complete_text_artifact_is_not_truncated(self):
        project = self.root / 'project'
        project.mkdir()
        content = 'verified report content\n' * 300
        (project / 'report.md').write_text(content)
        self.assertEqual(h.snapshot(project)['report.md']['text'], content)

    def test_runner_snapshot_preserves_reproducible_source(self):
        self.execute()
        source = h.iteration_dir() / 'runner/harness.py'
        self.assertEqual(source.read_bytes(), (h.H / 'harness.py').read_bytes())
        source.write_text('corrupt archived source')
        with self.assertRaises(h.Halt):
            h.freeze_inputs()

    def test_fixture_changes_change_input_identity(self):
        fixture = Path(h.CFG['repo_path']) / 'skills/demo/evals/files/input.txt'
        fixture.parent.mkdir()
        fixture.write_text('original')
        self.ev['files'] = ['evals/files/input.txt']
        h.wjson(fixture.parents[1] / 'evals.json', {'evals': [self.ev]})
        before = h.load_evals()[1]
        fixture.write_text('changed')
        self.assertNotEqual(h.load_evals()[1], before)
        h.CFG['evals'] = [999]
        with self.assertRaises(ValueError):
            h.selected_evals()

    def test_report_attributes_grading_to_its_executor_only(self):
        self.execute()
        h.grade_one('executor', self.ev)
        h.charge({'kind': 'grade', 'target': 'executor', 'executor': 'other', 'cost_usd': 9})
        path = h.report(['executor'])[0]
        report = h.rjson(path)
        self.assertEqual(report['metadata']['cost_usd'], .5)
        self.assertEqual(report['metadata']['archive_ref'], 'sample/demo/iteration-1/executor')
        self.assertNotIn(str(self.root), json.dumps(report))
        self.assertRegex(path.name, r'^\d{4}-\d{2}-\d{2}-abc12345-executor\.json$')

    def test_packet_blind_and_full_tool_evidence(self):
        self.execute()
        runs, _ = h.counted_runs('executor', self.ev)
        packet, key = h.build_packet(self.ev, runs, 'seed')
        self.assertEqual(list(key), ['A'])
        self.assertNotIn('with_skill', packet)
        self.assertNotIn('abc12345', packet)
        self.assertNotIn(str(self.root), packet)
        self.assertNotIn('x' * 2000, packet)
        self.assertIn('command_execution', packet)

    def test_detector_ignores_results_but_rejects_foreign_tool_inputs(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        tr = h.new_trace()
        tr['loaded_paths'] = [str(ws['install'] / 'SKILL.md')]
        tr['tool_calls'] = [{'name': 'command_execution', 'input': {'command': 'cat notes.md'},
                             'output': str(h.REAL_HOME / '.agents/skills') + ' codex exec hello'}]
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        self.assertFalse(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'][0]['input']['command'] = 'cat ' + str(h.REAL_HOME / '.agents/skills/demo/SKILL.md')
        self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'][0]['input']['command'] = 'codex exec hello'
        self.assertTrue(h.identity(tr, ws, adapter, argv)['nested_agent_cli'])

    def test_codex_child_readout_saved_and_encrypted_dispatch_unavailable(self):
        sessions = self.root / 'sessions'
        sessions.mkdir()
        rows = [{'type': 'session_meta', 'payload': {'parent_thread_id': 'parent'}},
                {'type': 'event_msg', 'payload': {'type': 'agent_message', 'message': 'child final ' + 'x' * 1000}}]
        (sessions / 'rollout-child.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
        readout = h.child_readouts(h.ADAPTERS['codex'], sessions)[0]
        self.assertEqual(readout['final_readout'], 'child final ' + 'x' * 1000)
        self.assertIn('unavailable', readout['dispatch_prompt'])

    def test_quota_in_json_event_stops_round(self):
        self.json_quota = True
        with self.assertRaises(h.Halt):
            self.execute()
        with self.assertRaises(h.Halt):
            self.execute()
        self.assertEqual(len(self.process_calls), 1)
        self.assertEqual(h.spent(), .25)

    def test_new_codex_child_tool_schema_preserves_inputs(self):
        sessions = self.root / 'sessions'
        sessions.mkdir()
        rows = [{'type': 'session_meta', 'payload': {'source': {'subagent': {'thread_spawn': {}}}}},
                {'type': 'response_item', 'payload': {'type': 'function_call', 'name': 'exec_command',
                 'arguments': json.dumps({'cmd': 'cat child/SKILL.md'})}}]
        (sessions / 'rollout-child.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
        calls = h.ADAPTERS['codex'].subagent_calls(sessions)
        self.assertEqual(calls[0]['input'], {'cmd': 'cat child/SKILL.md'})
        self.assertEqual(calls[0]['by'], 'subagent')

    def test_estimator_exception_leaves_unknown_cost_record(self):
        h.usage.estimate.side_effect = RuntimeError('fake estimator failure')
        with self.assertRaises(h.Budget):
            self.execute()
        directory = h.run_dir('executor', self.ev, 'with_skill', 1)
        self.assertIsNone(h.rjson(directory / 'cost.json')['cost_usd'])
        self.assertTrue((directory / 'sessions/marker.json').exists())

    def test_codex_grading_persists_sessions_and_forces_chatgpt(self):
        argv = h.ADAPTERS['codex'].grade_argv(h.CFG['targets']['executor'], 'packet', self.root / 'final', 1, self.root / 'schema')
        self.assertNotIn('--ephemeral', argv)
        self.assertIn('forced_login_method="chatgpt"', argv)
        self.assertNotIn('--api-key', argv)


class FakeProcess:
    def __init__(self, rc):
        self.rc = rc

    def wait(self, timeout=None):
        return self.rc


if __name__ == '__main__':
    unittest.main()
