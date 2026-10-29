"""Offline checks of the production Promptfoo configuration and file hooks."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

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
                setup = target / case['id'] / 'setup.json'
                self.assertEqual(suite.load_setup(setup)['case'], case['id'])
                self.assertLess(setup.stat().st_size, 1024 * 1024)
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

    def test_preparation_rejects_public_destinations(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            creator = self.prepare(root)
            repository = root / 'repository'
            shutil.copytree(suite.REPO / 'skills/creating-portable-skills',
                            repository / 'skills/creating-portable-skills')
            alias = root / 'repository-link'
            alias.symlink_to(repository, target_is_directory=True)
            for command in ('prepare', 'prepare_judges'):
                for destination in (repository, repository / command, alias / command):
                    with self.subTest(command=command, destination=destination):
                        args = argparse.Namespace(
                            host='claude', destination=str(destination),
                            creator_config=str(creator / 'CPS-AUD-001/promptfooconfig.json'),
                            candidate_results=None)
                        with patch.object(suite, 'REPO', repository.resolve()):
                            with self.assertRaisesRegex(ValueError, 'outside the public repository'):
                                getattr(suite, command)(args)
                        if destination != repository:
                            self.assertFalse(destination.exists())

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
            suite.save(candidate, {'results': {'results': [{
                'testCase': {'metadata': {'setup': str(target / 'CPS-AUD-001/setup.json')}},
                'response': {'output': 'Audit response'}, 'gradingResult': {'pass': True},
                'metadata': {'portableSkills': {'C3': {'result': 'Pass'}}}}]}})
            suite.prepare_judges(argparse.Namespace(
                destination=str(root / 'judges'), creator_config=str(target / 'CPS-AUD-001/promptfooconfig.json'),
                candidate_results=str(candidate)))
            for name in ('C1', 'C2', 'C4'):
                config = json.loads((root / 'judges' / (name + '.json')).read_text())
                self.assertEqual(config['providers'][0]['id'], 'openai:codex-sdk')
                self.assertEqual(config['providers'][0]['config']['cli_config']['forced_login_method'], 'chatgpt')
                self.assertEqual(config['providers'][0]['config']['maxRetries'], 0)
                self.assertEqual(config['tests'][0]['assert'], [{'type': 'is-json'}])

    def test_actual_judges_require_one_audit_result_with_passing_c3(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            target = self.prepare(root)
            candidate = root / 'candidate.json'

            def result(case, c3):
                row = {'testCase': {'metadata': {'setup': str(target / case / 'setup.json')}},
                       'response': {'output': case + ' response'}, 'gradingResult': {'pass': True}}
                if c3 is not None:
                    row['metadata'] = {'portableSkills': {'C3': {'result': c3}}}
                return row

            cases = {'activation result': [result('CPS-ACT-001', 'Fail')],
                     'missing C3': [result('CPS-AUD-001', None)],
                     'failing C3': [result('CPS-AUD-001', 'Fail')],
                     'two audit results': [result('CPS-AUD-001', 'Pass'), result('CPS-AUD-001', 'Pass')],
                     'audit beside activation': [result('CPS-ACT-001', 'Pass'), result('CPS-AUD-001', 'Fail')]}
            for index, (name, rows) in enumerate(cases.items()):
                with self.subTest(name):
                    suite.save(candidate, {'results': {'results': rows}})
                    with self.assertRaisesRegex(ValueError, 'CPS-AUD-001|C3'):
                        suite.prepare_judges(argparse.Namespace(
                            destination=str(root / ('judges-' + str(index))),
                            creator_config=str(target / 'CPS-AUD-001/promptfooconfig.json'),
                            candidate_results=str(candidate)))
                    self.assertFalse((root / ('judges-' + str(index)) / 'C1.json').exists())

    def test_actual_judges_reject_unavailable_or_failed_ordinary_checks(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            target = self.prepare(root)
            candidate = root / 'candidate.json'
            audit = {'testCase': {'metadata': {'setup': str(target / 'CPS-AUD-001/setup.json')}}}
            rows = [[], [{**audit}], [{**audit, 'response': None}],
                    [{**audit, 'response': {'output': 'Audit response'}}],
                    [{**audit, 'response': {'output': 'Audit response'}, 'gradingResult': {'pass': False},
                      'metadata': {'portableSkills': {'C3': {'result': 'Pass'}}}}],
                    [{**audit, 'response': {'output': 'Audit response'}, 'gradingResult': {'pass': False},
                      'metadata': {'portableSkills': {'C3': {'result': 'Fail'}}}}],
                    [{**audit, 'response': {'output': 'Audit response'}, 'gradingResult': {'pass': 'true'}}]]
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
            for raw in ({'finalResponse': 'Different answer', 'items': []},
                        {'items': []}, {'finalResponse': output},
                        {'finalResponse': output, 'items': {}}):
                with self.subTest(raw=raw):
                    row['response']['raw'] = json.dumps(raw)
                    suite.save(results, {'results': {'results': [row]}})
                    with self.assertRaisesRegex(ValueError, 'SDK final answer unavailable or mismatched'):
                        suite.extract_judge(results)
            row['response']['raw'] = json.dumps({'finalResponse': output, 'items': []})
            row['response']['error'] = 'Quota exhausted'
            suite.save(results, {'results': {'results': [row]}})
            with self.assertRaises(ValueError):
                suite.extract_judge(results)
            target = self.prepare(root)
            with self.assertRaises(ValueError):
                suite.prepare_judges(argparse.Namespace(
                    destination=str(root / 'judges'), creator_config=str(target / 'CPS-AUD-001/promptfooconfig.json'),
                    candidate_results=str(results)))


class SetupReferenceChecks(unittest.TestCase):
    def setUp(self):
        self.storage = tempfile.TemporaryDirectory()
        self.addCleanup(self.storage.cleanup)
        self.root = Path(self.storage.name)
        self.setup = self.root / 'setup.json'
        self.results = self.root / 'results.json'
        self.row = {'testCase': {'metadata': {'setup': str(self.setup)}}}
        suite.save(self.results, {'results': {'results': [self.row]}})

    def consumers(self):
        return (lambda: suite.export(self.results), lambda: suite.case_of(self.row))

    def test_setup_byte_limit(self):
        # The setup contract is one MiB of bytes, including JSON whitespace.
        limit = 1024 * 1024
        for text in ('{"case": "CPS-AUD-001"}', '{"case": "CPS-AUD-001", "label": "é"}'):
            payload = text.encode('utf-8')
            self.setup.write_bytes(payload + b' ' * (limit - len(payload)))
            self.assertEqual(suite.export(self.results)[0]['case'], 'CPS-AUD-001')
            self.assertEqual(suite.case_of(self.row), 'CPS-AUD-001')
            # Even invalid UTF-8 beyond the cap must fail on size before decoding.
            for extra in (b' ', b'\xff'):
                self.setup.write_bytes(payload + b' ' * (limit - len(payload)) + extra)
                for consume in self.consumers():
                    with self.subTest(text=text, extra=extra, consume=consume):
                        with self.assertRaisesRegex(ValueError, 'exceeds.*1048576'):
                            consume()

    def test_setup_special_files_rejected_without_blocking(self):
        fifo = self.root / 'setup.fifo'
        os.mkfifo(fifo)
        config = self.root / 'creator.json'
        suite.save(config, {'providers': [{'id': 'offline', 'config': {}}]})
        # /dev/null exercises device rejection without risking unbounded allocation
        # if the regular-file guard regresses; the unwritten FIFO catches blocking opens.
        for index, setup in enumerate((fifo, Path('/dev/null'))):
            self.row['testCase']['metadata']['setup'] = str(setup)
            suite.save(self.results, {'results': {'results': [self.row]}})
            commands = [
                ['export', str(self.results)],
                ['prepare-judges', str(config), str(self.root / ('judges-' + str(index))),
                 '--candidate-results', str(self.results)],
            ]
            for command in commands:
                with self.subTest(setup=setup, command=command[0]):
                    call = subprocess.run([sys.executable, str(ROOT / 'promptfoo_suite.py'), *command],
                                          capture_output=True, text=True, timeout=3)
                    self.assertNotEqual(call.returncode, 0)
                    self.assertIn('Setup reference must be a regular file', call.stderr)
                    self.assertFalse(any(self.root.rglob('C1.json')))

    def test_invalid_setup_references_fail(self):
        for payload in (b'broken', b'\xff', b'[]', b'null', b'42'):
            self.setup.write_bytes(payload)
            for consume in self.consumers():
                with self.subTest(payload=payload, consume=consume):
                    with self.assertRaises(ValueError):
                        consume()
        self.setup.unlink()
        for consume in self.consumers():
            with self.assertRaises(FileNotFoundError):
                consume()
        self.setup.mkdir()
        for consume in self.consumers():
            with self.assertRaisesRegex(ValueError, 'regular file'):
                consume()
        self.setup.rmdir()
        self.setup.write_text('{}')
        with patch.object(suite.os, 'open', side_effect=PermissionError('denied')):
            for consume in self.consumers():
                with self.assertRaises(PermissionError):
                    consume()

    def test_absent_setup_metadata_stays_unknown(self):
        for row in ({}, {'testCase': {'metadata': {}}}):
            suite.save(self.results, {'results': {'results': [row]}})
            self.assertIsNone(suite.export(self.results)[0]['case'])
            self.assertIsNone(suite.case_of(row))


if __name__ == '__main__':
    unittest.main()
