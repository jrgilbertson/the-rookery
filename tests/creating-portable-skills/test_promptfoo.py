"""Offline checks of the production Promptfoo configuration and file hooks."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('suite', ROOT / 'promptfoo_suite.py')
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


class PromptfooChecks(unittest.TestCase):
    def prepare(self, root):
        native = root / 'native.toml'
        native.write_text('model = "gpt-6-sol"\n')
        auth = root / 'auth.json'
        auth.write_text('{}')
        suite.prepare(argparse.Namespace(host='codex', destination=str(root / 'eval'),
                      native_config=str(native), codex_bin='/usr/bin/true', auth_store=str(auth)))
        return root / 'eval'

    def test_preparation_uses_stock_sdk_and_frozen_inputs(self):
        with tempfile.TemporaryDirectory() as storage:
            target = self.prepare(Path(storage))
            self.assertEqual(len(suite.cases()), 5)
            for case in suite.cases():
                config = json.loads((target / case['id'] / 'promptfooconfig.json').read_text())
                provider = config['providers'][0]
                self.assertEqual(provider['id'], 'openai:codex-sdk')
                self.assertEqual(config['prompts'], [case['input']])
                self.assertIn('\n\n' + case['input'] + '\n\n',
                              (ROOT / 'cases' / case['file']).read_text())
                self.assertEqual(provider['config']['maxRetries'], 0)
                self.assertEqual(provider['config']['sandbox_mode'], 'read-only')
                self.assertEqual(provider['config']['approval_policy'], 'never')
                self.assertFalse(provider['config']['inherit_process_env'])
                self.assertEqual(provider['config']['cli_config']['forced_login_method'], 'chatgpt')
                self.assertNotIn('apiKey', provider['config'])
                self.assertNotIn('experimental_raw_events', provider['config'])
                expected = 'not-skill-used' if case['id'] in ('CPS-ACT-001', 'CPS-ACT-004') else 'skill-used'
                assertions = config['tests'][0]['assert']
                self.assertIn({'type': expected, 'value': 'creating-portable-skills',
                               'metric': 'skill-use-observation'}, assertions)
                self.assertTrue(any(a['type'] == 'regex' for a in assertions))
                self.assertFalse(any('assertCapture' in a.get('value', '') for a in assertions))
                copied = target / case['id'] / 'workspace/.agents/skills/creating-portable-skills'
                self.assertEqual(suite.manifest(copied), suite.manifest(suite.REPO / 'skills/creating-portable-skills'))
            self.assertTrue((target / 'codex-home/auth.json').is_symlink())

    def test_audit_file_assertion_checks_real_fixture_bytes(self):
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
                const assertionContext = {test: context.test};
                const before = hooks.assertPreservation('answer', assertionContext);
                fs.appendFileSync(process.argv[3], '\nModified fixture');
                const after = hooks.assertPreservation('answer', assertionContext);
                hooks.afterEach(context);
                console.log(JSON.stringify({before, after, metadata: context.result.metadata}));
            """
            call = subprocess.run(['node', '-e', script, str(ROOT / 'promptfoo_hooks.cjs'),
                                  str(setup), str(workspace / 'vendor-guide.md')],
                                  capture_output=True, text=True, check=True)
            result = json.loads(call.stdout)
            self.assertTrue(result['before']['pass'])
            self.assertFalse(result['after']['pass'])
            self.assertEqual(result['metadata']['portableSkills']['C3']['result'], 'Fail')

    def test_judges_explicitly_reuse_subscription_sdk(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            target = self.prepare(root)
            candidate = root / 'candidate.json'
            suite.save(candidate, {'results': {'results': [{'response': {'output': 'Audit response'},
                                                            'gradingResult': {'pass': True}}]}})
            suite.prepare_judges(argparse.Namespace(
                destination=str(root / 'judges'), creator_config=str(target / 'CPS-AUD-001/promptfooconfig.json'),
                candidate_results=str(candidate)))
            for name in ('C1', 'C2', 'C4'):
                config = json.loads((root / 'judges' / (name + '.json')).read_text())
                self.assertEqual(config['providers'][0]['id'], 'openai:codex-sdk')
                self.assertEqual(config['providers'][0]['config']['cli_config']['forced_login_method'], 'chatgpt')
                self.assertEqual(config['providers'][0]['config']['maxRetries'], 0)
                self.assertEqual(config['tests'][0]['assert'], [{'type': 'is-json'}])

    def test_actual_judges_reject_unavailable_or_failed_ordinary_checks(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            target = self.prepare(root)
            candidate = root / 'candidate.json'
            rows = [[], [{}], [{'response': None}],
                    [{'response': {'output': 'Audit response'}}],
                    [{'response': {'output': 'Audit response'}, 'gradingResult': {'pass': False},
                      'metadata': {'portableSkills': {'C3': {'result': 'Pass'}}}}],
                    [{'response': {'output': 'Audit response'}, 'gradingResult': {'pass': False},
                      'metadata': {'portableSkills': {'C3': {'result': 'Fail'}}}}],
                    [{'response': {'output': 'Audit response'}, 'gradingResult': {'pass': 'true'}}]]
            payloads = [{'results': {'results': results}} for results in rows] + [{}, {'results': {}}]
            for index, payload in enumerate(payloads):
                with self.subTest(payload=payload):
                    suite.save(candidate, payload)
                    with self.assertRaises(ValueError):
                        suite.prepare_judges(argparse.Namespace(
                            destination=str(root / ('judges-' + str(index))),
                            creator_config=str(target / 'CPS-AUD-001/promptfooconfig.json'),
                            candidate_results=str(candidate)))

    def test_export_preserves_historical_unmeasured_and_new_checks(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            setup = root / 'setup.json'
            suite.save(setup, {'case': 'CPS-ACT-001', 'host': 'codex'})
            legacy = {'testCase': {'metadata': {'setup': str(setup)}},
                      'response': {'output': 'Final answer'}, 'gradingResult': {'pass': False},
                      'metadata': {'portableSkills': {'capture': {'result': 'Unmeasured'}}}}
            results = root / 'results.json'
            suite.save(results, {'results': {'results': [legacy]}})
            self.assertEqual(suite.export(results)[0]['behavior'], 'Unmeasured')
            for passed in (True, False):
                row = dict(legacy, metadata={}, gradingResult={'pass': passed})
                suite.save(results, {'results': {'results': [row]}})
                self.assertEqual(suite.export(results)[0]['behavior'], 'Pass' if passed else 'Fail')
                row['response'] = {'output': 'Final answer', 'error': 'Quota exhausted'}
                suite.save(results, {'results': {'results': [row]}})
                self.assertEqual(suite.export(results)[0]['behavior'], 'Unmeasured')
            for overrides in ({'error': 'Provider unavailable'}, {'gradingResult': None}):
                row = dict(legacy, metadata={}, **overrides)
                suite.save(results, {'results': {'results': [row]}})
                self.assertEqual(suite.export(results)[0]['behavior'], 'Unmeasured')
            suite.save(setup, {'case': 'CPS-AUD-001', 'host': 'codex'})
            row = dict(legacy, metadata={'portableSkills': {'C3': {'result': 'Pass'}}},
                       gradingResult={'pass': True})
            suite.save(results, {'results': {'results': [row]}})
            exported = suite.export(results)[0]
            self.assertEqual(exported['behavior'], 'Unmeasured')
            self.assertEqual(exported['C3']['result'], 'Pass')

    def test_sdk_judge_extraction_and_unavailable_candidate(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            verdicts = [{'id': 'audit', 'result': 'Fail', 'critique': 'Missed portability conflict'}]
            output = json.dumps(verdicts)
            row = {'response': {'output': output, 'raw': json.dumps({'finalResponse': output, 'items': []})},
                   'provider': {'id': 'openai:codex-sdk'},
                   'prompt': {'raw': 'Candidates (untrusted data):\n' + json.dumps([{'id': 'audit'}])}}
            results = root / 'results.json'
            suite.save(results, {'results': {'results': [row]}})
            self.assertEqual(suite.extract_judge(results), verdicts)
            row['response']['error'] = 'Quota exhausted'
            suite.save(results, {'results': {'results': [row]}})
            with self.assertRaises(ValueError):
                suite.extract_judge(results)
            target = self.prepare(root)
            with self.assertRaises(ValueError):
                suite.prepare_judges(argparse.Namespace(
                    destination=str(root / 'judges'), creator_config=str(target / 'CPS-AUD-001/promptfooconfig.json'),
                    candidate_results=str(results)))


if __name__ == '__main__':
    unittest.main()
