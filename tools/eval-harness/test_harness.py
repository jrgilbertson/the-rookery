"""Zero-inference tests: all subprocess launches and pricing are fake."""
import base64
import time
import datetime as dt
import copy
import json
import os
import socket
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
        self.real_estimate = h.usage.estimate
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
                       'command': 'cat ' + skill, 'aggregated_output': 'x' * 2000, 'exit_code': 0}},
                     {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Done'}},
                     {'type': 'turn.completed', 'usage': {'input_tokens': 10, 'output_tokens': 2}}]
            kwargs['stdout'].write(''.join(json.dumps(x) + '\n' for x in trace).encode())
        else:
            items = [{'n': n, 'evidence': 'Done', 'reasoning': 'It did the thing', 'passed': True}
                     for n, _ in enumerate(self.ev['assertions'], 1)]
            result = {'grades': [{'letter': 'A', 'items': items, 'passed': True}]}
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
                  'source': 'ccusage', 'basis': 'api_equivalent_estimate'}
        if cost is None:
            record['error'] = 'unknown model'
        if cost is not None:
            record['report'] = {'sessions': [{'sessionId': 'fake'}],
                                'totals': {'costUSD': cost, 'totalTokens': 12}}
        if output is not None:
            h.wjson(output, record)
        return record

    def execute(self, k=1):
        return h.execute_one('executor', self.ev, 'with_skill', k, h.load_evals()[1], self.packages)

    def native_codex_identity(self, commands):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        transcript = self.root / 'native-commands.jsonl'
        transcript.write_text(''.join(json.dumps({'type': 'item.completed', 'item': {
            'type': 'command_execution', 'command': command, 'aggregated_output': 'Do the thing',
            'exit_code': 0}}) + '\n' for command in commands))
        return h.identity(h.parse(adapter, transcript, None), ws, adapter, argv), ws

    def test_interrupted_json_replace_preserves_existing_artifact(self):
        path = self.root / 'private' / 'artifact.json'
        h.wjson(path, {'version': 1})
        original = path.read_bytes()
        def interrupted_dump(data, stream, indent=None):
            stream.write('{"partial":')
            raise KeyboardInterrupt('interrupted write')
        with patch.object(h.json, 'dump', side_effect=interrupted_dump):
            with self.assertRaisesRegex(KeyboardInterrupt, 'interrupted write'):
                h.wjson(path, {'version': 2})
        self.assertEqual(path.read_bytes(), original)
        with patch.object(h.os, 'replace', side_effect=KeyboardInterrupt('interrupted write')):
            with self.assertRaisesRegex(KeyboardInterrupt, 'interrupted write'):
                h.wjson(path, {'version': 2})
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(h.rjson(path), {'version': 1})
        self.assertEqual(list(path.parent.glob(f'.{path.name}.*.tmp')), [])

    def test_pending_attempt_cannot_be_settled_without_ccusage_evidence(self):
        self.costs = [None]
        with self.assertRaises(h.Budget):
            self.execute()
        record = h.run_dir('executor', self.ev, 'with_skill', 1) / 'cost.json'
        row = h.rjson(record)
        h.wjson(record, {**row, 'state': 'settled', 'cost_usd': 0.0, 'total_tokens': 0})
        with self.assertRaises(h.Budget):
            h.allowance()
        with self.assertRaises(h.Budget):
            self.execute(2)
        self.assertEqual(len(self.process_calls), 1)

    def test_cost_record_shape_and_ccusage_evidence(self):
        self.execute()
        record = h.run_dir('executor', self.ev, 'with_skill', 1) / 'cost.json'
        for change in ({'total_tokens': None}, {'basis': None}, {'errors': ['pricing incomplete']},
                       {'cost_usd': 0.0}):
            original = h.rjson(record)
            h.wjson(record, {**original, **change})
            with self.subTest(change=change), self.assertRaises(h.Budget):
                h.allowance()
            h.wjson(record, original)

    def test_real_estimator_result_settles_execution_and_grade(self):
        trace = self.root / 'pricing-trace'
        trace.write_text('{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":2}}\n')
        report = {'sessions': [{'sessionId': 'fake'}], 'totals': {'costUSD': .25, 'totalTokens': 12}}
        responses = [subprocess.CompletedProcess([], 0, 'ccusage test', ''),
                     subprocess.CompletedProcess([], 0, json.dumps(report), '')]
        with patch.object(h.usage.subprocess, 'run', side_effect=responses):
            cost = self.real_estimate('codex', trace, None, None, ['fake-ccusage'], self.root,
                                      model='executor-model')
        self.assertEqual(cost['cost_usd'], .25)
        self.assertNotIn('errors', cost)
        self.assertNotIn('error', cost)
        with patch.object(h.usage, 'estimate', return_value=cost):
            self.assertEqual(self.execute(), 'ok')
            self.assertTrue(h.grade_one('executor', self.ev))
        self.assertEqual(h.spent(), .5)
        self.assertEqual(h.report(['executor'])[0].parent.name, 'benchmark')

    def test_recovered_attempt_cost_supplies_report_tokens_without_timing_copy(self):
        self.costs = [None]
        with self.assertRaises(h.Budget):
            self.execute()
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        self.assertFalse((rd / 'timing.json').exists())
        record = rd / 'cost.json'
        pending = h.rjson(record)
        self.assertEqual(pending['state'], 'unknown')
        pending.pop('error', None)
        h.wjson(record, {**pending, 'state': 'settled', 'basis': 'api_equivalent_estimate',
                         'cost_usd': .25, 'total_tokens': 12, 'errors': [],
                         'report': {'sessions': [{'sessionId': 'fake'}],
                                    'totals': {'costUSD': .25, 'totalTokens': 12}}})
        self.assertEqual(h.spent(), .25)
        self.costs = [.25]
        self.assertTrue(h.grade_one('executor', self.ev))
        path = h.report(['executor'])[0]
        self.assertEqual(path.parent.name, 'benchmark')
        report = h.rjson(path)
        self.assertEqual(report['runs'][0]['result']['tokens'], 12)
        self.assertEqual(report['runs'][0]['result']['cost_usd'], .25)
        self.assertEqual(len(self.process_calls), 2)

    def test_one_attempt_record_is_the_accounting_source(self):
        self.execute()
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        record = h.rjson(rd / 'cost.json')
        self.assertEqual({key: record[key] for key in ('kind', 'target', 'eval', 'arm', 'run', 'state')},
                         {'kind': 'exec', 'target': 'executor', 'eval': 1,
                          'arm': 'with_skill', 'run': 1, 'state': 'settled'})
        self.assertEqual(record['report']['totals']['costUSD'], .25)
        self.assertFalse((h.iteration_dir() / '_ledger.jsonl').exists())
        self.assertFalse((rd / 'timing.json').exists())
        self.assertFalse((rd / 'metrics.json').exists())

    def test_symlinked_attempt_ancestor_cannot_supply_accounting(self):
        self.execute()
        eval_directory = h.run_dir('executor', self.ev, 'with_skill', 1).parent.parent
        saved = self.root / 'outside-attempt'
        eval_directory.rename(saved)
        eval_directory.symlink_to(saved, target_is_directory=True)
        with self.assertRaises(h.Budget):
            h.spent()

    def test_legacy_ledger_round_requires_its_archived_runner_before_launch(self):
        legacy = h.iteration_dir() / '_ledger.jsonl'
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_text('{"legacy":true}\n')
        with self.assertRaisesRegex(h.Halt, 'frozen archived runner'):
            self.execute()
        self.assertFalse((h.iteration_dir() / 'runner').exists())
        self.assertEqual(self.process_calls, [])

    def test_legacy_report_refuses_without_writing_evidence(self):
        self.execute()
        legacy = h.iteration_dir() / '_ledger.jsonl'
        legacy.write_text('{"legacy":true}\n')
        before = {str(p): p.read_bytes() for p in h.iteration_dir().rglob('*') if p.is_file()}
        with self.assertRaisesRegex(h.Halt, 'frozen archived runner'):
            h.report(['executor'])
        after = {str(p): p.read_bytes() for p in h.iteration_dir().rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_old_or_missing_runner_source_requires_archived_reporter(self):
        self.execute()
        for name in ('harness.py', 'usage.py'):
            for mutation in ('changed', 'missing'):
                with self.subTest(name=name, mutation=mutation):
                    source = h.iteration_dir() / 'runner' / name
                    original = source.read_bytes()
                    if mutation == 'changed':
                        source.write_bytes(b'# earlier runner format\n')
                    else:
                        source.unlink()
                    try:
                        with self.assertRaisesRegex(h.Halt, 'frozen archived runner'):
                            h.report(['executor'])
                    finally:
                        source.write_bytes(original)

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

    def test_package_file_metadata_changes_invalidate_report_identity(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        package = h.iteration_dir() / 'packages/with_skill/demo'
        skill = package / 'SKILL.md'
        original = skill.stat()
        before = h.tree_hash(package)
        for change in ('mtime', 'nonexecuting_mode'):
            with self.subTest(change=change):
                if change == 'mtime':
                    os.utime(skill, ns=(original.st_atime_ns, original.st_mtime_ns + 1_000_000_000))
                else:
                    skill.chmod((original.st_mode & 0o777) ^ 0o040)
                self.assertNotEqual(h.tree_hash(package), before)
                path = h.report(['executor'])[0]
                self.assertEqual(path.parent.name, 'incomplete')
                self.assertFalse(h.rjson(path)['metadata']['identity_verified'])
                skill.chmod(original.st_mode & 0o777)
                os.utime(skill, ns=(original.st_atime_ns, original.st_mtime_ns))
                self.assertEqual(h.tree_hash(package), before)

    def test_package_staging_preserves_file_and_directory_identity(self):
        package = h.iteration_dir() / 'packages/with_skill/demo'
        empty = package / 'empty'
        empty.mkdir()
        baseline = h.tree_hash(package)
        ws = h.stage(self.ev, 'with_skill', h.ADAPTERS['codex'])
        try:
            self.assertEqual(h.tree_hash(ws['install']), baseline)
            self.assertTrue((ws['install'] / 'empty').is_dir())
        finally:
            h.drop_home(ws['home'])
            h.shutil.rmtree(ws['parent'])
        for directory in (empty, package):
            original = directory.stat()
            with self.subTest(directory=directory, change='mode'):
                directory.chmod((original.st_mode & 0o777) ^ 0o040)
                self.assertNotEqual(h.tree_hash(package), baseline)
                directory.chmod(original.st_mode & 0o777)
            with self.subTest(directory=directory, change='mtime'):
                os.utime(directory, ns=(original.st_atime_ns, original.st_mtime_ns + 1_000_000_000))
                self.assertNotEqual(h.tree_hash(package), baseline)
                os.utime(directory, ns=(original.st_atime_ns, original.st_mtime_ns))
            self.assertEqual(h.tree_hash(package), baseline)
        empty.rmdir()
        self.assertNotEqual(h.tree_hash(package), baseline)

    def test_package_hash_distinguishes_regular_file_from_matching_symlink(self):
        package = self.root / 'package'
        package.mkdir()
        external = self.root / 'external-skill.md'
        external.write_text('same contents')
        skill = package / 'SKILL.md'
        h.shutil.copy2(external, skill)
        package_stat = package.stat()
        before = h.tree_hash(package)
        skill.unlink()
        skill.symlink_to(external)
        os.utime(package, ns=(package_stat.st_atime_ns, package_stat.st_mtime_ns))
        self.assertNotEqual(h.tree_hash(package), before)

    def test_package_hash_handles_special_entry_without_reading_it(self):
        package = self.root / 'package'
        package.mkdir()
        before = h.tree_hash(package)
        os.mkfifo(package / 'pipe')
        self.assertNotEqual(h.tree_hash(package), before)

    def test_package_hash_does_not_walk_symlinked_root(self):
        external = self.root / 'external'
        external.mkdir()
        (external / 'file').write_text('before')
        package = self.root / 'package-link'
        package.symlink_to(external, target_is_directory=True)
        before = h.tree_hash(package)
        (external / 'file').write_text('after')
        self.assertEqual(h.tree_hash(package), before)

    def test_assertion_free_grade_is_saved_without_a_score(self):
        self.ev['assertions'] = []
        h.wjson(Path(h.CFG['repo_path']) / 'skills/demo/evals/evals.json', {'evals': [self.ev]})
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        grading = h.rjson(h.run_dir('executor', self.ev, 'with_skill', 1) / 'grading.json')
        self.assertEqual(grading['summary'], {'passed': 0, 'failed': 0, 'total': 0, 'pass_rate': None})
        path = h.report(['executor'])[0]
        report = h.rjson(path)
        self.assertEqual(path.parent.name, 'incomplete')
        self.assertTrue(report['runs'][0]['needs_operator_review'])

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

    def test_report_selects_targets_from_frozen_config_after_live_rename(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        h.CFG['targets']['renamed'] = h.CFG['targets'].pop('executor')
        path = h.report(None)[0]
        report = h.rjson(path)
        self.assertEqual(path.parent.name, 'incomplete')
        self.assertEqual(report['metadata']['executor_model'], 'executor-model')
        self.assertFalse(report['metadata']['identity_verified'])

    def test_report_rejects_explicit_target_absent_from_frozen_config(self):
        self.execute()
        h.CFG['targets']['renamed'] = h.CFG['targets'].pop('executor')
        with self.assertRaisesRegex(ValueError, 'frozen'):
            h.report(['renamed'])

    def test_report_command_uses_frozen_target_after_live_rename(self):
        self.execute()
        h.CFG['targets']['renamed'] = h.CFG['targets'].pop('executor')
        h.wjson(self.config, h.CFG)
        argv = ['harness.py', 'report', '--round', str(self.config)]
        with patch.object(h.sys, 'argv', argv):
            self.assertEqual(h.main(), 0)
        self.assertEqual(len(list((h.iteration_dir() / 'executor/incomplete').glob('*.json'))), 1)

    def test_report_command_uses_frozen_target_after_live_executor_removed(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        del h.CFG['targets']['executor']
        h.wjson(self.config, h.CFG)
        with patch.object(h.sys, 'argv', ['harness.py', 'report', '--round', str(self.config)]):
            self.assertEqual(h.main(), 0)
        report = h.rjson(next((h.iteration_dir() / 'executor/incomplete').glob('*.json')))
        self.assertFalse(report['metadata']['identity_verified'])
        self.assertEqual(report['metadata']['executor_model'], 'executor-model')

    def test_report_command_uses_frozen_grader_after_live_grader_removed(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        del h.CFG['targets']['judge']
        h.wjson(self.config, h.CFG)
        with patch.object(h.sys, 'argv', ['harness.py', 'report', '--round', str(self.config)]):
            self.assertEqual(h.main(), 0)
        report = h.rjson(next((h.iteration_dir() / 'executor/incomplete').glob('*.json')))
        self.assertFalse(report['metadata']['identity_verified'])
        self.assertEqual(report['metadata']['grader'], 'judge-model')

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
        packet, _ = h.build_packet(self.ev, runs[0])
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

    def test_dangling_symlink_added_to_staged_package_discards_and_persists_slot(self):
        original = self.fake_process
        def with_symlink(argv, **kwargs):
            result = original(argv, **kwargs)
            skill = Path(argv[-1].split('Read ', 1)[1].split(' and follow', 1)[0])
            (skill.parent / 'broken-link').symlink_to('missing-target')
            return result
        h.subprocess.Popen.side_effect = with_symlink
        self.assertEqual(self.execute(), 'discarded')
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        self.assertEqual(h.rjson(rd / 'status.json')['status'], 'discarded')
        self.assertFalse(h.rjson(rd / 'outputs/observations.json')['skill_package_unchanged'])
        self.assertEqual(self.execute(), 'discarded')
        self.assertEqual(len(self.process_calls), 1)

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
        self.assertIsNone(h.attempt_records()[0]['cost_usd'])
        self.assertTrue((h.run_dir('executor', self.ev, 'with_skill', 1) / 'sessions/marker.json').exists())

    def test_interrupt_reaps_process_group_and_leaves_charge_unsettled(self):
        class InterruptedProcess:
            pid = 424242
            waits = 0

            def wait(self, timeout=None):
                self.waits += 1
                if self.waits == 1:
                    raise KeyboardInterrupt('operator interrupted')
                if self.waits == 2:
                    raise KeyboardInterrupt('again during reaping')
                return -9

        process = InterruptedProcess()
        h.subprocess.Popen.side_effect = lambda *args, **kwargs: process
        with patch.object(h.os, 'killpg') as kill:
            with self.assertRaisesRegex(KeyboardInterrupt, 'operator interrupted'):
                self.execute()
        kill.assert_called_once()
        self.assertEqual(process.waits, 3)
        self.assertEqual(self.estimates, [])
        self.assertIsNone(h.attempt_records()[0]['cost_usd'])
        self.assertIsNone(h.rjson(h.run_dir('executor', self.ev, 'with_skill', 1) / 'cost.json')['cost_usd'])
        self.assertEqual(self.execute(), 'unavailable')
        self.assertEqual(process.waits, 3)

    def test_model_and_effort_must_be_nonempty_cli_strings(self):
        for target in ('executor', 'judge'):
            for field in ('model', 'effort'):
                original = h.CFG['targets'][target][field]
                for value in (123, None, True, [], {}, '', '   ', 'bad\0value'):
                    with self.subTest(target=target, field=field, value=value):
                        h.CFG['targets'][target][field] = value
                        with self.assertRaisesRegex(ValueError, field):
                            h.validate_config(self.config)
                        self.assertEqual(self.process_calls, [])
                        self.assertFalse(h.run_dir('executor', self.ev, 'with_skill', 1).exists())
                h.CFG['targets'][target][field] = original
        h.validate_config(self.config)

    def test_iteration_requires_a_positive_integer(self):
        for value in (True, False, 0, -1, 1.5, '1'):
            with self.subTest(value=value):
                h.CFG['iteration'] = value
                with self.assertRaisesRegex(ValueError, 'iteration'):
                    h.validate_config(self.config)
                self.assertEqual(self.process_calls, [])
        h.CFG['iteration'] = 1
        h.validate_config(self.config)

    def test_invalid_timeout_is_rejected_before_launch(self):
        for value in (None, True, False, 0, -1, float('nan'), float('inf'), '10'):
            with self.subTest(value=value):
                h.CFG['cap_seconds'] = value
                with self.assertRaisesRegex(ValueError, 'cap_seconds'):
                    h.validate_config(self.config)
                self.assertEqual(self.process_calls, [])
        h.CFG['cap_seconds'] = .5
        h.validate_config(self.config)

    def test_unexpected_wait_error_reaps_process_and_leaves_charge_unsettled(self):
        class FaultyProcess:
            pid = 424242
            waits = 0

            def wait(self, timeout=None):
                self.waits += 1
                if self.waits == 1:
                    raise TypeError('unexpected wait failure')
                return -9

        process = FaultyProcess()
        h.subprocess.Popen.side_effect = lambda *args, **kwargs: process
        with patch.object(h.os, 'killpg') as kill:
            with self.assertRaisesRegex(TypeError, 'unexpected wait failure'):
                self.execute()
        kill.assert_called_once()
        self.assertEqual(process.waits, 2)
        self.assertEqual(self.estimates, [])
        self.assertIsNone(h.attempt_records()[0]['cost_usd'])

    def test_special_project_artifacts_discard_settled_run(self):
        original = self.fake_process
        for kind in ('fifo', 'socket'):
            with self.subTest(kind=kind):
                self.process_calls.clear()
                def with_special(argv, **kwargs):
                    result = original(argv, **kwargs)
                    path = Path(kwargs['cwd']) / ('named.pipe' if kind == 'fifo' else 'local.socket')
                    if kind == 'fifo':
                        os.mkfifo(path)
                    else:
                        previous = Path.cwd()
                        try:
                            os.chdir(kwargs['cwd'])
                            with socket.socket(socket.AF_UNIX) as server:
                                server.bind(path.name)
                        finally:
                            os.chdir(previous)
                    return result
                h.subprocess.Popen.side_effect = with_special
                run = 1 if kind == 'fifo' else 2
                self.assertEqual(self.execute(run), 'discarded')
                rd = h.run_dir('executor', self.ev, 'with_skill', run)
                status = h.rjson(rd / 'status.json')
                self.assertEqual(status['status'], 'discarded')
                self.assertIn('capture_error', status)
                self.assertEqual(h.attempt_records()[-1]['cost_usd'], .25)
                self.assertEqual(h.spent(), .25 * run)
                self.assertEqual(self.execute(run), 'discarded')
                self.assertEqual(len(self.process_calls), 1)
        report = h.rjson(h.report(['executor'])[0])
        self.assertTrue(report['metadata']['cost_available'])
        self.assertEqual(report['metadata']['cost_usd'], .5)

    def test_symlinked_project_root_is_discarded_without_copying_target(self):
        outside = self.root / 'outside-project'
        outside.mkdir()
        (outside / 'secret.txt').write_text('outside fake data')
        original = self.fake_process
        def replace_project(argv, **kwargs):
            result = original(argv, **kwargs)
            project = Path(kwargs['cwd'])
            h.shutil.rmtree(project)
            project.symlink_to(outside, target_is_directory=True)
            return result
        h.subprocess.Popen.side_effect = replace_project
        self.assertEqual(self.execute(), 'discarded')
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        self.assertIn('capture_error', h.rjson(rd / 'status.json'))
        self.assertFalse((rd / 'outputs/project/secret.txt').exists())
        self.assertEqual(h.attempt_records()[0]['cost_usd'], .25)
        self.assertEqual(self.execute(), 'discarded')
        self.assertEqual(len(self.process_calls), 1)

    def test_grok_execution_requires_reported_tool_inventory(self):
        h.CFG['targets']['executor']['adapter'] = 'grok'
        adapter = h.ADAPTERS['grok']
        def grok_process(argv, **kwargs):
            self.process_calls.append((argv, kwargs))
            home = Path(kwargs['env']['HOME'])
            h.wjson(home / '.grok/sessions/marker.json', {'fake': True})
            install = argv[argv.index('-p') + 1].split('Read ', 1)[1].split(' and follow', 1)[0]
            events = []
            inventories = {2: dict.fromkeys(adapter.allowed(argv), True),
                           3: [{'name': tool} for tool in adapter.allowed(argv)],
                           4: adapter.allowed(argv)}
            if len(self.process_calls) in inventories:
                events.append({'type': 'available_commands', 'tools': inventories[len(self.process_calls)]})
            events.extend([
                {'type': 'tool_call', 'toolCallId': 'read-1', 'toolName': 'read_file',
                 'rawInput': {'path': install}},
                {'type': 'tool_call_update', 'toolCallId': 'read-1', 'rawOutput': {'content': 'Do the thing'}},
                {'type': 'text', 'data': 'Done'},
                {'type': 'end', 'usage': {'total_tokens': 12}, 'total_cost_usd': 9},
            ])
            kwargs['stdout'].write(''.join(json.dumps(event) + '\n' for event in events).encode())
            return FakeProcess(0)
        h.subprocess.Popen.side_effect = grok_process
        self.assertEqual(self.execute(1), 'discarded')
        self.assertIsNone(h.rjson(h.run_dir('executor', self.ev, 'with_skill', 1) / 'status.json')['identity']['init_surface_ok'])
        for run in (2, 3):
            with self.subTest(run=run):
                self.assertEqual(self.execute(run), 'discarded')
                rd = h.run_dir('executor', self.ev, 'with_skill', run)
                self.assertFalse(h.rjson(rd / 'status.json')['identity']['init_surface_ok'])
                self.assertEqual(h.attempt_records()[-1]['cost_usd'], .25)
                self.assertEqual(self.execute(run), 'discarded')
        self.assertEqual(self.execute(4), 'ok')
        self.assertEqual(len(self.process_calls), 4)

    def test_cost_totals_include_all_providers_and_failed_grading(self):
        self.costs = [0.25, 0.75]
        self.execute()
        self.fail_grader = True
        self.assertFalse(h.grade_one('executor', self.ev))
        self.assertEqual(h.spent(), 1)
        rows = h.attempt_records()
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

    def test_malformed_existing_grade_blocks_retry_and_reports_incomplete(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        grade = h.run_dir('executor', self.ev, 'with_skill', 1) / 'grading.json'
        original = grade.read_text()
        calls = len(self.process_calls)
        for broken in ('{"summary":', '{}\n', json.dumps({**json.loads(original), 'summary':
                       {'passed': 1, 'failed': 0, 'total': 1, 'pass_rate': 0.0}})):
            with self.subTest(broken=broken):
                grade.write_text(broken)
                self.assertFalse(h.grade_one('executor', self.ev))
                self.assertEqual(grade.read_text(), broken)
                self.assertEqual(len(self.process_calls), calls)
                path = h.report(['executor'])[0]
                report = h.rjson(path)
                self.assertEqual(path.parent.name, 'incomplete')
                self.assertTrue(report['runs'][0]['needs_operator_review'])
                self.assertIsNone(report['runs'][0]['result']['pass_rate'])
                self.assertTrue(any('grading' in note.lower() for note in report['notes']))
        grade.write_text(original)
        self.assertTrue(h.grade_one('executor', self.ev))

    def test_malformed_run_status_is_unavailable_without_relaunch(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        status = rd / 'status.json'
        original = status.read_text()
        calls = len(self.process_calls)
        for broken in ('{"status":', '[]\n', '{"status":"ready"}\n'):
            with self.subTest(broken=broken):
                status.write_text(broken)
                self.assertEqual(self.execute(), 'unavailable')
                self.assertFalse(h.grade_one('executor', self.ev))
                path = h.report(['executor'])[0]
                report = h.rjson(path)
                self.assertEqual(path.parent.name, 'incomplete')
                self.assertEqual(report['runs'][0]['status'], 'unavailable')
                self.assertTrue(report['runs'][0]['needs_operator_review'])
                self.assertTrue(any('status.json' in note for note in report['notes']))
                self.assertEqual(report['metadata']['cost_usd'], .5)
                self.assertEqual(status.read_text(), broken)
                self.assertEqual(len(self.process_calls), calls)
        status.unlink()
        self.assertEqual(self.execute(), 'unavailable')
        self.assertEqual(len(self.process_calls), calls)
        status.write_text(original)

    def test_malformed_per_run_evidence_yields_incomplete_report(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        cases = [('invocation.json', '{"duration_ms":'), ('invocation.json', '{"duration_ms":"bad"}'),
                 ('invocation.json', '{"duration_ms":-1}'),
                 ('invocation.json', '{"duration_ms":Infinity}'),
                 ('trace.json', '[]'), ('trace.json', '{}'),
                 ('trace.json', '{"tool_calls":[],"errors":"bad"}'),
                 ('trace.json', '{"tool_calls":true,"errors":0}'),
                 ('trace.json', '{"tool_calls":[],"errors":-1}'),
                 ('trace.json', '{"tool_calls":[],"errors":0.5}'),
                 ('build.json', '{"model":')]
        for name, broken in cases:
            with self.subTest(name=name, broken=broken):
                path = rd / name
                original = path.read_text()
                path.write_text(broken)
                try:
                    report_path = h.report(['executor'])[0]
                    report = h.rjson(report_path)
                    self.assertEqual(report_path.parent.name, 'incomplete')
                    self.assertTrue(report['runs'][0]['needs_operator_review'])
                    self.assertTrue(any(name in note for note in report['notes']))
                    self.assertEqual(report['metadata']['cost_usd'], .5)
                    self.assertEqual(path.read_text(), broken)
                finally:
                    path.write_text(original)
        self.assertEqual(h.report(['executor'])[0].parent.name, 'benchmark')

    def test_missing_completed_run_evidence_yields_incomplete_report(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        calls = len(self.process_calls)
        for name in ('invocation.json', 'trace.json', 'build.json'):
            with self.subTest(name=name):
                path = rd / name
                original = path.read_bytes()
                path.unlink()
                try:
                    report_path = h.report(['executor'])[0]
                    report = h.rjson(report_path)
                    self.assertEqual(report_path.parent.name, 'incomplete')
                    self.assertTrue(report['runs'][0]['needs_operator_review'])
                    self.assertTrue(any(name in note for note in report['notes']))
                    self.assertEqual(report['metadata']['cost_usd'], .5)
                    if name == 'invocation.json':
                        self.assertIsNone(report['runs'][0]['result']['time_seconds'])
                    self.assertFalse(path.exists())
                    self.assertEqual(len(self.process_calls), calls)
                finally:
                    path.write_bytes(original)

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
        h.CFG['targets']['executor']['adapter'] = 'claude'
        with self.assertRaisesRegex(ValueError, 'Invalid target'):
            h.validate_config(self.config)
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
        self.assertEqual(len(h.attempt_records()), 1)
        self.assertEqual(h.status_of(h.run_dir('executor', self.ev, 'with_skill', 1)), 'error')

    def test_cli_preflight_missing_binary_allows_retry(self):
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        with patch.object(h.shutil, 'which', return_value=None), self.assertRaises(h.Halt):
            self.execute()
        self.assertFalse(rd.exists())
        self.assertEqual(h.attempt_records(), [])
        self.assertEqual(self.process_calls, [])
        self.assertFalse(any(Path(h.CFG['workspace_root']).iterdir()))
        self.assertEqual(self.execute(), 'ok')

    def test_cli_preflight_version_failure_allows_retry(self):
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        with patch.object(h, 'cli_version', side_effect=h.Halt('version unavailable')), self.assertRaises(h.Halt):
            self.execute()
        self.assertFalse(rd.exists())
        self.assertEqual(h.attempt_records(), [])
        self.assertEqual(self.process_calls, [])
        self.assertFalse(any(Path(h.CFG['workspace_root']).iterdir()))
        self.assertEqual(self.execute(), 'ok')

    def test_grader_cli_preflight_cleans_credentials_and_scratch(self):
        self.execute()
        gdir = h.iteration_dir() / 'executor/grading/eval-1-sample'
        for failure in ('missing', 'version'):
            with self.subTest(failure=failure):
                if failure == 'missing':
                    guard = patch.object(h.shutil, 'which', return_value=None)
                else:
                    guard = patch.object(h, 'cli_version', side_effect=h.Halt('version unavailable'))
                with guard, self.assertRaises(h.Halt):
                    h.grade_one('executor', self.ev)
                self.assertFalse((gdir / 'attempt-1').exists())
                self.assertFalse(any(Path(h.CFG['workspace_root']).iterdir()))
                self.assertEqual(len(h.attempt_records()), 1)
        self.assertTrue(h.grade_one('executor', self.ev))

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

    def test_config_rejects_repeat_execution(self):
        for value in (2, True, 0):
            with self.subTest(value=value):
                h.CFG['runs'] = value
                with self.assertRaisesRegex(ValueError, 'one execution per case'):
                    h.validate_config(self.config)
                self.assertEqual(self.process_calls, [])
        h.CFG['runs'] = 1
        h.validate_config(self.config)

    def test_config_selects_only_its_changed_arm(self):
        h.CFG['arms']['old_skill'] = 'deadbeef'
        h.CFG['run_arms'] = ['old_skill']
        with self.assertRaisesRegex(ValueError, 'changed arm once'):
            h.validate_config(self.config)
        self.assertEqual(self.process_calls, [])

    def test_target_names_match_benchmark_suffix(self):
        original = copy.deepcopy(h.CFG)
        for name in ('Codex', 'codex_gpt', 'codex..sol', '-codex'):
            with self.subTest(rejected=name):
                h.CFG = copy.deepcopy(original)
                h.CFG['targets'][name] = h.CFG['targets'].pop('executor')
                with self.assertRaisesRegex(ValueError, 'Invalid target'):
                    h.validate_config(self.config)
        for name in ('codex.gpt-6-sol', 'grok-4.7'):
            with self.subTest(accepted=name):
                h.CFG = copy.deepcopy(original)
                h.CFG['targets'][name] = h.CFG['targets'].pop('executor')
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

    def test_missing_attempt_record_cannot_make_existing_attempt_free(self):
        self.execute()
        (h.run_dir('executor', self.ev, 'with_skill', 1) / 'cost.json').unlink()
        with self.assertRaises(h.Budget):
            h.allowance()

    def test_unrelated_cost_files_do_not_count_as_calls(self):
        self.execute()
        package = h.iteration_dir() / 'packages/with_skill/demo/cost.json'
        output = h.run_dir('executor', self.ev, 'with_skill', 1) / 'outputs/project/cost.json'
        h.wjson(package, {'fixture': True})
        h.wjson(output, {'agent_output': True})
        self.assertEqual(h.spent(), .25)
        self.assertEqual(h.allowance(), 1)

    def test_missing_attempt_record_makes_report_incomplete(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        (h.run_dir('executor', self.ev, 'with_skill', 1) / 'cost.json').unlink()
        path = h.report(['executor'])[0]
        report = h.rjson(path)
        self.assertEqual(path.parent.name, 'incomplete')
        self.assertFalse(report['metadata']['cost_available'])
        self.assertTrue(all(row['needs_operator_review'] for row in report['runs']))

    def test_unattributable_attempt_blocks_spending_and_report_cost(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        run_cost = h.run_dir('executor', self.ev, 'with_skill', 1) / 'cost.json'
        grade_cost = h.iteration_dir() / 'executor/grading/eval-1-sample/attempt-1/cost.json'
        for field, value in [('kind', None), ('target', None), ('run', '1'),
                             ('executor', None), ('attempt', '1')]:
            with self.subTest(field=field):
                cost_file = run_cost if field in ('kind', 'target', 'run') else grade_cost
                original = h.rjson(cost_file)
                h.wjson(cost_file, {**original, field: value})
                try:
                    with self.assertRaises(h.Budget):
                        h.spent()
                    path = h.report(['executor'])[0]
                    report = h.rjson(path)
                    self.assertEqual(path.parent.name, 'incomplete')
                    self.assertFalse(report['metadata']['cost_available'])
                    self.assertNotIn('cost_usd', report['metadata'])
                finally:
                    h.wjson(cost_file, original)

    def test_torn_or_malformed_attempt_makes_report_incomplete_and_blocks_inference(self):
        self.execute()
        self.assertTrue(h.grade_one('executor', self.ev))
        record = h.run_dir('executor', self.ev, 'with_skill', 1) / 'cost.json'
        original = record.read_text()
        for broken in ('{"kind":', '[]\n', '{"kind":"exec"}\n'):
            with self.subTest(broken=broken):
                record.write_text(broken)
                with self.assertRaises((h.Budget, ValueError, TypeError, AttributeError)):
                    h.allowance()
                path = h.report(['executor'])[0]
                report = h.rjson(path)
                self.assertEqual(path.parent.name, 'incomplete')
                self.assertFalse(report['metadata']['cost_available'])
                self.assertNotIn('cost_usd', report['metadata'])
                self.assertIsNone(report['runs'][0]['result']['cost_usd'])
                self.assertTrue(report['runs'][0]['needs_operator_review'])
                self.assertTrue(any('attempt' in note.lower() for note in report['notes']))
        record.write_text(original)

    def test_scrub_preserves_short_arm_names_in_evidence(self):
        h.CFG['arms'] = {'with_skill': 'main', 'without_skill': 'dev'}
        build = {'skill_revision': 'abc12345'}
        self.assertEqual(h.scrub('remain device abc12345', build), 'remain device <rev>')

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

    def test_fixture_mode_change_invalidates_frozen_inputs(self):
        fixture = Path(h.CFG['repo_path']) / 'skills/demo/evals/files/script.sh'
        fixture.parent.mkdir()
        fixture.write_text('#!/bin/sh\nexit 0\n')
        fixture.chmod(0o644)
        self.ev['files'] = ['evals/files/script.sh']
        h.wjson(fixture.parents[1] / 'evals.json', {'evals': [self.ev]})
        before = h.load_evals()[1]
        h.freeze_inputs()
        fixture.chmod(0o755)
        self.assertNotEqual(h.load_evals()[1], before)
        with self.assertRaises(h.Halt):
            h.freeze_inputs()

    def test_fixture_mtime_change_invalidates_frozen_inputs(self):
        fixture = Path(h.CFG['repo_path']) / 'skills/demo/evals/files/input.txt'
        fixture.parent.mkdir()
        fixture.write_text('original')
        self.ev['files'] = ['evals/files/input.txt']
        h.wjson(fixture.parents[1] / 'evals.json', {'evals': [self.ev]})
        before = h.load_evals()[1]
        h.freeze_inputs()
        stat = fixture.stat()
        os.utime(fixture, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
        self.assertNotEqual(h.load_evals()[1], before)
        with self.assertRaises(h.Halt):
            h.freeze_inputs()

    def test_report_attributes_grading_to_its_executor_only(self):
        h.CFG['targets']['other'] = {'adapter': 'codex', 'model': 'other-model', 'grader': 'judge', 'effort': 'high'}
        self.execute()
        h.grade_one('executor', self.ev)
        h.execute_one('other', self.ev, 'with_skill', 1, h.load_evals()[1], self.packages)
        h.grade_one('other', self.ev)
        path = h.report(['executor'])[0]
        report = h.rjson(path)
        self.assertEqual(report['metadata']['cost_usd'], .5)
        self.assertEqual(report['metadata']['archive_ref'], 'sample/demo/iteration-1/executor')
        self.assertNotIn(str(self.root), json.dumps(report))
        self.assertRegex(path.name, r'^\d{4}-\d{2}-\d{2}-abc12345--iteration-1-executor\.json$')

    def test_reports_from_distinct_iterations_have_distinct_names(self):
        self.execute()
        h.grade_one('executor', self.ev)
        first = h.report(['executor'])[0]
        source = h.iteration_dir()
        h.CFG['iteration'] = 2
        h.shutil.copytree(source, h.iteration_dir())
        h.wjson(h.iteration_dir() / 'round.json', h.CFG)
        second = h.report(['executor'])[0]
        self.assertNotEqual(first.name, second.name)
        self.assertIn('--iteration-2-', second.name)

    def test_packet_blind_and_full_tool_evidence(self):
        self.execute()
        runs, _ = h.counted_runs('executor', self.ev)
        packet, key = h.build_packet(self.ev, runs[0])
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
        tr['tool_calls'] = [{'name': 'command_execution', 'input': {'command': 'cat notes.md'},
                             'output': str(h.REAL_HOME / '.agents/skills') + ' codex exec hello'}]
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        self.assertFalse(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'][0]['input']['command'] = 'cat ' + str(h.REAL_HOME / '.agents/skills/demo/SKILL.md')
        self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'][0]['input']['command'] = 'codex exec hello'
        self.assertTrue(h.identity(tr, ws, adapter, argv)['nested_agent_cli'])

    def test_shell_options_outside_literal_contract_are_unverified(self):
        identity, ws = self.native_codex_identity(["bash --noprofile -c 'cat /etc/hosts'"])
        self.assertTrue(identity['unverified_access'])
        identity, _ = self.native_codex_identity(["bash --noprofile --norc -lc 'cat /etc/hosts' extra"])
        self.assertTrue(identity['unverified_access'])
        skill = ws['install'] / 'SKILL.md'
        identity, _ = self.native_codex_identity([f"bash --noprofile -c 'cat {skill}'"])
        self.assertTrue(identity['unverified_access'])
        identity, _ = self.native_codex_identity([f"bash -lc 'cat {skill}'"])
        self.assertTrue(identity['loaded_paths'])
        self.assertFalse(identity['unverified_access'])
        identity, _ = self.native_codex_identity(["bash --unsupported -c 'cat /etc/hosts'"])
        self.assertTrue(identity['unverified_access'])

    def test_prefixed_shell_wrapper_is_unverified_without_interpreting_it(self):
        _, ws = self.native_codex_identity([])
        for command in ("env bash -c 'cat /etc/hosts'",
                        "env FOO=bar bash -lc 'cat /etc/hosts'",
                        "/usr/bin/env -i sh -c 'cat /etc/hosts'",
                        f"cd {ws['project']} && env bash -c 'cat /etc/hosts'",
                        "FOO=1 bash -c 'cat /etc/hosts'"):
            with self.subTest(command=command):
                identity, _ = self.native_codex_identity([command])
                self.assertTrue(identity['unverified_access'])
        identity, ws = self.native_codex_identity(['env FOO=bar printenv FOO'])
        self.assertFalse(identity['unverified_access'])
        identity, _ = self.native_codex_identity([f"bash -c 'cat {ws['install'] / 'SKILL.md'}'"])
        self.assertTrue(identity['loaded_paths'])
        self.assertFalse(identity['unverified_access'])

    def test_assignment_shell_after_valid_skill_read_discards_paid_run(self):
        original = self.fake_process
        def with_assignment_shell(argv, **kwargs):
            result = original(argv, **kwargs)
            kwargs['stdout'].write((json.dumps({'type': 'item.completed', 'item': {
                'type': 'command_execution', 'command': "FOO=1 bash -c 'cat /etc/hosts'",
                'aggregated_output': 'outside', 'exit_code': 0}}) + '\n').encode())
            return result
        h.subprocess.Popen.side_effect = with_assignment_shell
        self.assertEqual(self.execute(), 'discarded')
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        self.assertTrue(h.rjson(rd / 'status.json')['identity']['unverified_access'])
        self.assertEqual(h.spent(), .25)
        self.assertEqual(self.execute(), 'discarded')
        self.assertEqual(len(self.process_calls), 1)

    def test_native_quoted_nested_cli_names_are_rejected(self):
        _, ws = self.native_codex_identity([])
        read = f"cat {ws['install'] / 'SKILL.md'}"
        for command in ("'codex' exec hello", '"grok" -p prompt',
                        'codex -c \'model="gpt-5"\' exec hello',
                        'codex --model gpt-5 exec hello', 'grok --model fake -p hello',
                        'claude --model fake -p hello'):
            with self.subTest(command=command):
                identity, _ = self.native_codex_identity([read, command])
                self.assertTrue(identity['loaded_paths'])
                self.assertTrue(identity['nested_agent_cli'])
        identity, _ = self.native_codex_identity([read, 'echo codex docs'])
        self.assertTrue(identity['loaded_paths'])
        self.assertFalse(identity['nested_agent_cli'])

    def test_native_cat_help_and_version_do_not_prove_skill_read(self):
        _, ws = self.native_codex_identity([])
        skill = ws['install'] / 'SKILL.md'
        for option in ('--help', '--version'):
            with self.subTest(option=option):
                identity, _ = self.native_codex_identity([f'cat {option} {skill}'])
                self.assertFalse(identity['loaded_paths'])
        identity, _ = self.native_codex_identity([f'cat -n {skill}'])
        self.assertTrue(identity['loaded_paths'])

    def test_grok_native_target_file_is_checked_after_skill_load(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        adapter = h.ADAPTERS['grok']
        argv = adapter.exec_argv(h.CFG['targets']['judge'], ws, 'prompt', self.root / 'final', 1, [])
        transcript = self.root / 'grok-native.jsonl'
        rows = [{'type': 'tool_call', 'toolCallId': '1', 'toolName': 'read_file',
                 'rawInput': {'target_file': str(ws['install'] / 'SKILL.md')}},
                {'type': 'tool_call_update', 'toolCallId': '1', 'status': 'completed',
                 'rawOutput': {'content': 'Do the thing'}}]
        transcript.write_text(''.join(json.dumps(row) + '\n' for row in rows))
        identity = h.identity(h.parse(adapter, transcript, None), ws, adapter, argv)
        self.assertTrue(identity['loaded_paths'])
        self.assertFalse(identity['foreign_access'])
        for tool, key in [('read_file', 'target_file'), ('list_dir', 'target_directory')]:
            for path, outside in [(str(ws['project']), False), ('/etc', True)]:
                with self.subTest(tool=tool, path=path):
                    call = {'type': 'tool_call', 'toolCallId': '2', 'toolName': tool,
                            'rawInput': {key: path}}
                    transcript.write_text(''.join(json.dumps(row) + '\n' for row in [*rows, call]))
                    identity = h.identity(h.parse(adapter, transcript, None), ws, adapter, argv)
                    self.assertTrue(identity['loaded_paths'])
                    self.assertEqual(bool(identity['foreign_access']), outside)

    def test_grok_failed_or_missing_skill_read_result_is_not_loaded(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        adapter = h.ADAPTERS['grok']
        argv = adapter.exec_argv(h.CFG['targets']['judge'], ws, 'prompt', self.root / 'final', 1, [])
        transcript = self.root / 'grok-read.jsonl'
        call = {'type': 'tool_call', 'toolCallId': '1', 'toolName': 'read_file',
                'rawInput': {'target_file': str(ws['install'] / 'SKILL.md')}}
        for updates in ([], [{'type': 'tool_call_update', 'toolCallId': '1', 'status': 'failed',
                             'rawOutput': {'error': 'permission denied'}}]):
            with self.subTest(updates=updates):
                transcript.write_text(''.join(json.dumps(row) + '\n' for row in [call, *updates]))
                self.assertFalse(h.identity(h.parse(adapter, transcript, None), ws, adapter, argv)['loaded_paths'])

    def test_nonreading_mentions_and_unverified_codex_cat_discard_execution(self):
        original = self.fake_process
        cases = [('echo {skill}', 0, 'path'), ('test -f {skill}', 0, 'path'),
                 ('ls {skill}', 0, 'path'), ('printf %s {skill}', 0, 'path'),
                 ('cat {skill}', 1, 'permission denied'), ('cat {skill}', 0, '')]
        for run, (command, exit_code, output) in enumerate(cases, 1):
            with self.subTest(command=command, exit_code=exit_code, output=output):
                def with_mention(argv, **kwargs):
                    result = original(argv, **kwargs)
                    skill = argv[-1].split('Read ', 1)[1].split(' and follow', 1)[0]
                    kwargs['stdout'].seek(0)
                    kwargs['stdout'].truncate()
                    event = {'type': 'item.completed', 'item': {
                        'type': 'command_execution', 'command': command.format(skill=skill),
                        'aggregated_output': skill if output == 'path' else output,
                        'exit_code': exit_code}}
                    kwargs['stdout'].write((json.dumps(event) + '\n' +
                        json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Done'}}) + '\n').encode())
                    return result
                h.subprocess.Popen.side_effect = with_mention
                self.assertEqual(self.execute(run), 'discarded')
                identity = h.rjson(h.run_dir('executor', self.ev, 'with_skill', run) / 'status.json')['identity']
                self.assertFalse(identity['loaded_paths'])

    def test_redirected_cat_with_later_output_does_not_prove_skill_read(self):
        original = self.fake_process
        def with_redirect(argv, **kwargs):
            result = original(argv, **kwargs)
            skill = argv[-1].split('Read ', 1)[1].split(' and follow', 1)[0]
            kwargs['stdout'].seek(0)
            kwargs['stdout'].truncate()
            command = f'cat {skill} > copy; echo done'
            event = {'type': 'item.completed', 'item': {'type': 'command_execution',
                     'command': command, 'aggregated_output': 'done', 'exit_code': 0}}
            kwargs['stdout'].write((json.dumps(event) + '\n' +
                json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Done'}}) + '\n').encode())
            return result
        h.subprocess.Popen.side_effect = with_redirect
        self.assertEqual(self.execute(), 'discarded')
        identity = h.rjson(h.run_dir('executor', self.ev, 'with_skill', 1) / 'status.json')['identity']
        self.assertFalse(identity['loaded_paths'])

    def test_simple_cd_cat_keeps_execution_valid(self):
        original = self.fake_process
        def with_cd_cat(argv, **kwargs):
            result = original(argv, **kwargs)
            kwargs['stdout'].seek(0)
            kwargs['stdout'].truncate()
            event = {'type': 'item.completed', 'item': {'type': 'command_execution',
                     'command': 'cd ../skills/demo && cat SKILL.md',
                     'aggregated_output': 'Do the thing', 'exit_code': 0}}
            kwargs['stdout'].write((json.dumps(event) + '\n' +
                json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Done'}}) + '\n').encode())
            return result
        h.subprocess.Popen.side_effect = with_cd_cat
        self.assertEqual(self.execute(), 'ok')

    def test_relative_workspace_escape_discards_execution(self):
        original = self.fake_process
        def with_escape(argv, **kwargs):
            result = original(argv, **kwargs)
            kwargs['stdout'].write((json.dumps({'type': 'item.completed', 'item': {
                'type': 'command_execution', 'command': 'cat ../../ws-other/skills/demo/SKILL.md'}}) + '\n').encode())
            return result
        h.subprocess.Popen.side_effect = with_escape
        self.assertEqual(self.execute(), 'discarded')
        identity = h.rjson(h.run_dir('executor', self.ev, 'with_skill', 1) / 'status.json')['identity']
        self.assertTrue(identity['foreign_access'])

    def test_relative_installed_skill_access_keeps_execution(self):
        original = self.fake_process
        def with_relative_skill_read(argv, **kwargs):
            result = original(argv, **kwargs)
            kwargs['stdout'].write((json.dumps({'type': 'item.completed', 'item': {
                'type': 'command_execution', 'command': 'cat ../skills/demo/SKILL.md'}}) + '\n').encode())
            return result
        h.subprocess.Popen.side_effect = with_relative_skill_read
        self.assertEqual(self.execute(), 'ok')
        identity = h.rjson(h.run_dir('executor', self.ev, 'with_skill', 1) / 'status.json')['identity']
        self.assertFalse(identity['foreign_access'])

    def test_relative_parent_scan_stays_within_staged_workspace(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        tr = h.new_trace()
        tr['tool_calls'] = [{'name': 'command_execution', 'input': {'command': 'find .. -name SKILL.md'}, 'output': ''}]
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        self.assertFalse(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'][0]['input'] = {'command': 'find ../.. -name SKILL.md'}
        self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'][0]['input'] = {'command': 'find --directory=../../ws-other -name SKILL.md'}
        self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'][0]['input'] = {'query': 'What does .. mean in prose?'}
        self.assertFalse(h.identity(tr, ws, adapter, argv)['foreign_access'])

    def test_relative_paths_use_the_tool_working_directory(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        for inp in ({'command': 'cat ../fixture.txt', 'cwd': str(ws['project'] / 'nested')},
                    {'cmd': 'cat ../fixture.txt', 'workdir': 'nested'},
                    {'command': 'cd nested && cat ../fixture.txt'},
                    {'file_path': '../fixture.txt', 'cwd': 'nested'},
                    {'command': 'cat ../skills/demo/SKILL.md'},
                    {'command': 'cd .. && cat skills/demo/SKILL.md'}):
            with self.subTest(inp=inp):
                tr = h.new_trace()
                tr['tool_calls'] = [{'name': 'command_execution', 'input': inp, 'output': ''}]
                self.assertFalse(h.identity(tr, ws, adapter, argv)['foreign_access'])
        for inp in ({'cmd': 'cat ../../../ws-other/file', 'workdir': 'nested'},
                    {'command': 'cd .. && cat ../ws-other/file'},
                    {'command': 'cat file', 'cwd': '../../ws-other'}):
            with self.subTest(inp=inp):
                tr = h.new_trace()
                tr['tool_calls'] = [{'name': 'command_execution', 'input': inp, 'output': ''}]
                self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])

    def test_loaded_skill_uses_each_tools_normalized_working_directory(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        for inp in ({'command': 'cat ../../skills/demo/SKILL.md', 'cwd': 'nested'},
                    {'cmd': 'cat ../../skills/demo/SKILL.md', 'workdir': 'nested'},
                    {'command': 'cd nested && cat ../../skills/demo/SKILL.md'}):
            with self.subTest(inp=inp):
                tr = h.new_trace()
                tr['tool_calls'] = [{'name': 'command_execution', 'input': inp, 'output': 'Do the thing'}]
                result = h.identity(tr, ws, adapter, argv)
                self.assertTrue(result['loaded_paths'])
                self.assertFalse(result['foreign_access'])

    def test_tilde_resolves_to_throwaway_home_and_rejects_credential_read(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        for adapter in (h.ADAPTERS['codex'], h.ADAPTERS['grok']):
            with self.subTest(adapter=adapter.NAME):
                target = 'executor' if adapter.NAME == 'codex' else 'judge'
                argv = adapter.exec_argv(h.CFG['targets'][target], ws, 'prompt', self.root / 'final', 1, [])
                tr = h.new_trace()
                tr['tool_calls'] = [{'name': 'command_execution', 'input': {'command': 'cat ~/.codex/auth.json'}, 'output': ''}]
                self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])

    def test_absolute_path_inputs_outside_staged_workspace_are_foreign(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        tr = h.new_trace()
        for inp in ({'file_path': '/etc/hosts'}, {'file_path': str(ws['home'] / '.codex/auth.json')},
                    {'command': 'cat /home/user/private.txt'},
                    {'command': '/bin/cat /etc/hosts'}):
            with self.subTest(inp=inp):
                tr['tool_calls'] = [{'name': 'read_file', 'input': inp, 'output': ''}]
                self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'] = [{'name': 'command_execution', 'input': {
            'command': '/bin/cat ' + str(ws['install'] / 'SKILL.md')}, 'output': ''}]
        self.assertFalse(h.identity(tr, ws, adapter, argv)['foreign_access'])

    def test_attached_redirection_discards_execution(self):
        original = self.fake_process
        def with_redirect(argv, **kwargs):
            result = original(argv, **kwargs)
            kwargs['stdout'].write((json.dumps({'type': 'item.completed', 'item': {
                'type': 'command_execution', 'command': 'cat</etc/hosts'}}) + '\n').encode())
            return result
        h.subprocess.Popen.side_effect = with_redirect
        self.assertEqual(self.execute(), 'discarded')
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        self.assertTrue(h.rjson(rd / 'status.json')['identity']['unverified_access'])
        self.assertEqual(h.rjson(rd / 'cost.json')['state'], 'settled')

    def test_deleted_install_is_discarded_and_cleaned_up(self):
        original = self.fake_process
        def with_deleted_install(argv, **kwargs):
            result = original(argv, **kwargs)
            h.shutil.rmtree(Path(kwargs['cwd']).parent / 'skills/demo')
            return result
        h.subprocess.Popen.side_effect = with_deleted_install
        self.assertEqual(self.execute(), 'discarded')
        rd = h.run_dir('executor', self.ev, 'with_skill', 1)
        self.assertEqual(h.rjson(rd / 'cost.json')['state'], 'settled')
        build = h.rjson(rd / 'build.json')
        self.assertFalse(Path(build['workspace']).exists())
        self.assertFalse(Path(build['home']).exists())
        self.assertEqual(self.execute(), 'discarded')
        self.assertEqual(len(self.process_calls), 1)

    def test_absolute_external_read_discards_execution(self):
        original = self.fake_process
        def with_external_read(argv, **kwargs):
            result = original(argv, **kwargs)
            kwargs['stdout'].write((json.dumps({'type': 'item.completed', 'item': {
                'type': 'command_execution', 'command': 'cat /etc/hosts'}}) + '\n').encode())
            return result
        h.subprocess.Popen.side_effect = with_external_read
        self.assertEqual(self.execute(), 'discarded')
        identity = h.rjson(h.run_dir('executor', self.ev, 'with_skill', 1) / 'status.json')['identity']
        self.assertTrue(identity['foreign_access'])

    def test_codex_shell_wrapper_checks_inner_literal_paths(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        tr = h.new_trace()
        for command in ("/bin/zsh -lc 'cat /etc/hosts'", "bash -c 'cat ../../../ws-other/file'",
                        "sh -c 'cd .. && cat ../ws-other/file'", "bash -c 'cat /etc/hosts' ignored",
                        "bash -lc 'cat /etc/hosts' ignored"):
            with self.subTest(command=command):
                tr['tool_calls'] = [{'name': 'command_execution', 'input': {'command': command}, 'output': ''}]
                self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])
        for command in (f"/bin/zsh -lc 'cat {ws['install'] / 'SKILL.md'}'",
                        "zsh -lc 'cd nested && cat ../fixture.txt'", "/bin/zsh -lc 'cat '/etc/hosts"):
            with self.subTest(command=command):
                tr['tool_calls'] = [{'name': 'command_execution', 'input': {'command': command}, 'output': ''}]
                h.identity(tr, ws, adapter, argv)
        tr['tool_calls'] = [{'name': 'command_execution', 'input': {
            'command': f"/bin/zsh -lc 'cat {ws['install'] / 'SKILL.md'}'"}, 'output': ''}]
        self.assertFalse(h.identity(tr, ws, adapter, argv)['foreign_access'])
        tr['tool_calls'] = [{'name': 'command_execution', 'input': {
            'command': f"bash -c 'cat {ws['install'] / 'SKILL.md'}' ignored"}, 'output': 'Do the thing'}]
        self.assertTrue(h.identity(tr, ws, adapter, argv)['loaded_paths'])

    def test_embedded_shell_input_is_unverified_without_interpreting_its_body(self):
        ws = {'parent': self.root / 'scratch/ws', 'project': self.root / 'scratch/ws/project',
              'install': self.root / 'scratch/ws/skills/demo', 'home': self.root / 'scratch/home'}
        adapter = h.ADAPTERS['codex']
        argv = adapter.exec_argv(h.CFG['targets']['executor'], ws, 'prompt', self.root / 'final', 1, [])
        tr = h.new_trace()
        body = "python3 - <<'PY'\nfrom pathlib import Path\nvalue = Path('one') / 'two'\nPY"
        for command in (body, f'/bin/zsh -lc "{body}"', body + '\ncat /etc/hosts',
                        'echo "<<PY"\ncat /etc/hosts', 'cat <<<"text"\ncat /etc/hosts',
                        'echo "\n<<PY\n"\ncat /etc/hosts'):
            with self.subTest(command=command):
                tr['tool_calls'] = [{'name': 'command_execution', 'input': {'command': command}, 'output': ''}]
                self.assertTrue(h.identity(tr, ws, adapter, argv)['unverified_access'])
        for command in ('cat /', 'find /'):
            with self.subTest(command=command):
                tr['tool_calls'] = [{'name': 'command_execution', 'input': {'command': command}, 'output': ''}]
                self.assertTrue(h.identity(tr, ws, adapter, argv)['foreign_access'])

    def test_codex_child_readout_saved_and_encrypted_dispatch_unavailable(self):
        sessions = self.root / 'sessions'
        sessions.mkdir()
        rows = [{'type': 'session_meta', 'payload': {'parent_thread_id': 'parent'}},
                {'type': 'event_msg', 'payload': {'type': 'agent_message', 'message': 'child final ' + 'x' * 1000}}]
        (sessions / 'rollout-child.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
        readout = h.child_readouts(h.ADAPTERS['codex'], sessions)[0]
        self.assertEqual(readout['final_readout'], 'child final ' + 'x' * 1000)
        self.assertIn('unavailable', readout['dispatch_prompt'])

    def test_successful_answer_about_hypothetical_quota_is_not_service_failure(self):
        trace = h.new_trace()
        trace['final_text'] = 'The hypothetical grader is out of quota; retain evidence and wait.'
        self.assertIsNone(h.service_failure(0, trace, ''))

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


class RemotePatternTests(unittest.TestCase):
    def test_local_repository_and_non_origin_remote(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.dict(h.CFG, {'repo_path': directory, 'archive_root': str(root / 'archive'),
                                   'repo': 'sample', 'skill': 'demo', 'iteration': 1}, clear=True):
                h.git('init', '--quiet')
                patterns = h.foreign_patterns(h.ADAPTERS['codex'])
                self.assertIn(directory, patterns)
                self.assertFalse(any('github.com/' in item for item in patterns))
                h.git('remote', 'add', 'upstream', 'https://github.com/example/sample.git')
                patterns = h.foreign_patterns(h.ADAPTERS['codex'])
                self.assertIn('github.com/example/sample', patterns)
                self.assertIn('raw.githubusercontent.com/example/sample', patterns)
                h.git('remote', 'add', 'origin', 'git@github.com:other/rookery.git')
                patterns = h.foreign_patterns(h.ADAPTERS['codex'])
                self.assertIn('github.com/example/sample', patterns)
                self.assertIn('raw.githubusercontent.com/example/sample', patterns)
                self.assertIn('github.com/other/rookery', patterns)
                self.assertIn('raw.githubusercontent.com/other/rookery', patterns)


class FakeProcess:
    def __init__(self, rc):
        self.rc = rc

    def wait(self, timeout=None):
        return self.rc


if __name__ == '__main__':
    unittest.main()
