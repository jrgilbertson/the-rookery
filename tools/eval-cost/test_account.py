import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import account


class AccountingTests(unittest.TestCase):
    def test_pending_blocks_next_call_then_actual_estimator_result_settles(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            record = account.begin(root, 'executor', 1)
            with self.assertRaisesRegex(ValueError, 'unknown'):
                account.begin(root, 'grader', 1)
            trace = root / 'transcript'
            trace.write_text('{"type":"end","modelUsage":{"test-model":{"inputTokens":60,"outputTokens":30,"cacheReadInputTokens":10,"cacheCreationInputTokens":0}}}')
            def ccusage(argv, **kwargs):
                from types import SimpleNamespace
                output = 'test-version' if '--version' in argv else json.dumps({'sessions': [{}], 'totals': {'totalCost': .25, 'totalTokens': 100}})
                return SimpleNamespace(stdout=output, stderr='')
            with patch('usage.subprocess.run', side_effect=ccusage):
                account.price(record, 'grok', trace, None, None, ['ccusage'])
            self.assertEqual(account.balance(root, 1), .75)
            self.assertTrue(account.begin(root, 'grader', 1).exists())

    def test_unknown_malformed_and_exhausted_costs_block(self):
        for value in [None, -1, True, float('nan'), 1, 1.1, '0.1']:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                (root / 'first.json').write_text(json.dumps({'cost_usd': value}))
                with self.assertRaises(ValueError):
                    account.begin(root, 'second', 1)
                self.assertFalse((root / 'second.json').exists())

    def test_duplicate_call_and_repricing_known_cost_are_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            record = root / 'first.json'
            record.write_text('{"cost_usd": 0.1}')
            with self.assertRaises(FileExistsError):
                account.begin(root, 'first', 1)
            with self.assertRaises(ValueError):
                account.price(record, 'grok', root / 'absent', None, None, ['ccusage'])
            self.assertEqual(json.loads(record.read_text())['cost_usd'], .1)

    def test_missing_usage_stays_unknown(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            record = account.begin(root, 'failed', 1)
            result = account.price(record, 'grok', root / 'absent', None, None, ['ccusage'])
            self.assertIsNone(result['cost_usd'])
            with self.assertRaises(ValueError):
                account.balance(root, 1)


if __name__ == '__main__':
    unittest.main()
