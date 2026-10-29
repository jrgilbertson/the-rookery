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

CASE = '# CPS-TEST-001 — Synthetic case\n\n## CPS-TEST-001.INPUT\n\nAudit this skill for portability.\n\n## CPS-TEST-001.NOTES\n\nNot executor input.\n'


class PromptfooChecks(unittest.TestCase):
    def prepare(self, root, host='codex', fixtures=None, expect_no_skill_use=False, destination=None):
        case = root / 'case.md'
        case.write_text(CASE)
        native = root / 'native.toml'
        native.write_text('model = "gpt-6-sol"\n')
        auth = root / 'auth.json'
        auth.write_text('{}')
        suite.prepare(argparse.Namespace(
            host=host, case=str(case), destination=str(destination or root / 'eval'),
            fixtures=fixtures and str(fixtures), expect_no_skill_use=expect_no_skill_use,
            native_config=str(native), codex_bin='/usr/bin/true', auth_store=str(auth)))
        return root / 'eval/CPS-TEST-001'

    def fixtures(self, root):
        fixtures = root / 'fixtures'
        (fixtures / 'skill').mkdir(parents=True)
        (fixtures / 'notes.md').write_text('Synthetic notes\n')
        (fixtures / 'skill/SKILL.md').write_text('---\nname: skill\ndescription: Synthetic.\n---\n')
        return fixtures

    def test_preparation_uses_stock_sdk_and_case_input(self):
        with tempfile.TemporaryDirectory() as storage:
            directory = self.prepare(Path(storage))
            setup = directory / 'setup.json'
            self.assertEqual(suite.load_setup(setup)['case'], 'CPS-TEST-001')
            self.assertLess(setup.stat().st_size, 1024 * 1024)
            config = json.loads((directory / 'promptfooconfig.json').read_text())
            provider = config['providers'][0]
            self.assertEqual(provider['id'], 'openai:codex-sdk')
            self.assertEqual(config['prompts'], ['Audit this skill for portability.'])
            self.assertEqual(provider['config']['maxRetries'], 0)
            self.assertEqual(provider['config']['sandbox_mode'], 'read-only')
            self.assertEqual(provider['config']['approval_policy'], 'never')
            self.assertFalse(provider['config']['inherit_process_env'])
            self.assertEqual(provider['config']['cli_config']['forced_login_method'], 'chatgpt')
            self.assertNotIn('apiKey', provider['config'])
            assertions = config['tests'][0]['assert']
            self.assertIn({'type': 'skill-used', 'value': 'creating-portable-skills',
                           'metric': 'skill-use-observation'}, assertions)
            self.assertTrue(any(a['type'] == 'regex' for a in assertions))
            self.assertEqual(config['extensions'], [])
            copied = directory / 'workspace/.agents/skills/creating-portable-skills'
            source_sha256 = suite.manifest(suite.REPO / 'skills/creating-portable-skills')
            self.assertEqual(suite.manifest(copied), source_sha256)
            setup = json.loads(setup.read_text())
            self.assertEqual(setup['package_sha256'], source_sha256)
            self.assertEqual(setup['input_sha256'], suite.digest(config['prompts'][0].encode()))
            self.assertTrue((directory.parent / 'codex-home/auth.json').is_symlink())

    def test_near_miss_and_fixture_options(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            directory = self.prepare(root, host='claude', fixtures=self.fixtures(root), expect_no_skill_use=True)
            config = json.loads((directory / 'promptfooconfig.json').read_text())
            self.assertEqual(config['providers'][0]['id'], 'anthropic:claude-agent-sdk')
            types = [a['type'] for a in config['tests'][0]['assert']]
            self.assertIn('not-skill-used', types)
            self.assertIn('javascript', types)
            self.assertEqual(len(config['extensions']), 2)
            setup = json.loads((directory / 'setup.json').read_text())
            self.assertEqual(setup['inputs'], ['notes.md', 'skill/SKILL.md'])
            self.assertEqual((directory / 'workspace/notes.md').read_text(), 'Synthetic notes\n')

    def test_case_without_input_paragraph_is_rejected(self):
        with tempfile.TemporaryDirectory() as storage:
            case = Path(storage) / 'case.md'
            case.write_text('# CPS-TEST-002 — Missing input\n\nNo input here.\n')
            with self.assertRaisesRegex(ValueError, 'CPS-TEST-002.INPUT'):
                suite.read_case(case)

    def test_unsafe_case_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as storage:
            case = Path(storage) / 'case.md'
            for case_id in ('../escape', '/tmp/escape', 'cps-lower'):
                with self.subTest(case_id=case_id):
                    case.write_text('# ' + case_id + ' — Unsafe\n\n## ' + case_id + '.INPUT\n\nInput.\n')
                    with self.assertRaisesRegex(ValueError, 'Case ID'):
                        suite.read_case(case)

    def test_fixtures_cannot_replace_skill_or_use_links(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            fixtures = self.fixtures(root)
            shadow = fixtures / '.agents/skills/creating-portable-skills'
            shadow.mkdir(parents=True)
            (shadow / 'SKILL.md').write_text('Replacement instructions\n')
            with self.assertRaisesRegex(ValueError, 'skill'):
                self.prepare(root, fixtures=fixtures, destination=root / 'shadowed')
            shutil.rmtree(fixtures / '.agents')
            (fixtures / 'linked').symlink_to(fixtures / 'skill', target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                self.prepare(root, fixtures=fixtures, destination=root / 'linked')
            empty = root / 'empty-fixtures'
            empty.mkdir()
            with self.assertRaisesRegex(ValueError, 'no files'):
                self.prepare(root, fixtures=empty, destination=root / 'empty')

    def test_preparation_rejects_public_destinations(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            repository = root / 'repository'
            shutil.copytree(suite.REPO / 'skills/creating-portable-skills',
                            repository / 'skills/creating-portable-skills')
            alias = root / 'repository-link'
            alias.symlink_to(repository, target_is_directory=True)
            for destination in (repository, repository / 'eval', alias / 'eval'):
                with self.subTest(destination=destination):
                    with patch.object(suite, 'REPO', repository.resolve()):
                        with self.assertRaisesRegex(ValueError, 'outside the public repository'):
                            self.prepare(root, destination=destination)
                    if destination != repository:
                        self.assertFalse(destination.exists())

    def test_preservation_assertion_checks_real_fixture_bytes(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            directory = self.prepare(root, fixtures=self.fixtures(root))
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
                                  str(directory / 'setup.json'), str(directory / 'workspace/notes.md')],
                                  capture_output=True, text=True, check=True)
            result = json.loads(call.stdout)
            self.assertTrue(result['before']['pass'])
            self.assertFalse(result['after']['pass'])
            self.assertEqual(result['metadata']['portableSkills']['preservation']['result'], 'Fail')

    def test_export_reports_checks_and_unavailable_results(self):
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            setup = root / 'setup.json'
            suite.save(setup, {'case': 'CPS-TEST-001', 'host': 'codex', 'inputs': []})
            base = {'testCase': {'metadata': {'setup': str(setup)}},
                      'response': {'output': 'Final answer'}, 'gradingResult': {'pass': False},
                      'metadata': {'portableSkills': {'capture': {'result': 'Unmeasured'}}}}
            results = root / 'results.json'
            suite.save(results, {'results': {'results': [base]}})
            self.assertEqual(suite.export(results)[0]['behavior'], 'Unmeasured')
            for passed in (True, False):
                row = dict(base, metadata={}, gradingResult={'pass': passed})
                suite.save(results, {'results': {'results': [row]}})
                self.assertEqual(suite.export(results)[0]['behavior'], 'Pass' if passed else 'Fail')
                row['response'] = {'output': 'Final answer', 'error': 'Quota exhausted'}
                suite.save(results, {'results': {'results': [row]}})
                self.assertEqual(suite.export(results)[0]['behavior'], 'Unmeasured')
            for overrides in ({'error': 'Provider unavailable'}, {'gradingResult': None}):
                row = dict(base, metadata={}, **overrides)
                suite.save(results, {'results': {'results': [row]}})
                self.assertEqual(suite.export(results)[0]['behavior'], 'Unmeasured')
            suite.save(setup, {'case': 'CPS-TEST-001', 'host': 'codex', 'inputs': ['notes.md']})
            row = dict(base, metadata={'portableSkills': {'preservation': {'result': 'Fail'}}},
                       gradingResult={'pass': False})
            suite.save(results, {'results': {'results': [row]}})
            exported = suite.export(results)[0]
            self.assertEqual(exported['behavior'], 'Fail')
            self.assertEqual(exported['preservation']['result'], 'Fail')


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
        return (lambda: suite.export(self.results),)

    def test_setup_byte_limit(self):
        # The setup contract is one MiB of bytes, including JSON whitespace.
        limit = 1024 * 1024
        for text in ('{"case": "CPS-AUD-001"}', '{"case": "CPS-AUD-001", "label": "é"}'):
            payload = text.encode('utf-8')
            self.setup.write_bytes(payload + b' ' * (limit - len(payload)))
            self.assertEqual(suite.export(self.results)[0]['case'], 'CPS-AUD-001')
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
        # /dev/null exercises device rejection without risking unbounded allocation
        # if the regular-file guard regresses; the unwritten FIFO catches blocking opens.
        for setup in (fifo, Path('/dev/null')):
            self.row['testCase']['metadata']['setup'] = str(setup)
            suite.save(self.results, {'results': {'results': [self.row]}})
            with self.subTest(setup=setup):
                call = subprocess.run([sys.executable, str(ROOT / 'promptfoo_suite.py'), 'export', str(self.results)],
                                      capture_output=True, text=True, timeout=3)
                self.assertNotEqual(call.returncode, 0)
                self.assertIn('Setup reference must be a regular file', call.stderr)

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


if __name__ == '__main__':
    unittest.main()
