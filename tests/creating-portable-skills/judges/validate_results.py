#!/usr/bin/env python3
"""Check provisional judge output against synthetic specification oracles."""
import argparse
import json
from pathlib import Path


def check(verdicts, criterion, references):
    """Validate schema/IDs and count synthetic agreements, not human alignment."""
    if not isinstance(verdicts, list):
        raise ValueError('Verdicts must be an array')
    observed = {}
    for item in verdicts:
        if not isinstance(item, dict) or set(item) != {'id', 'critique', 'result'}:
            raise ValueError('Each verdict requires exactly id, critique, result')
        if not isinstance(item['id'], str) or not item['id'] or item['id'] in observed:
            raise ValueError('Verdict IDs must be nonempty and unique')
        if not isinstance(item['critique'], str) or not item['critique'].strip():
            raise ValueError('Critique must be nonempty text')
        if item['result'] not in ('Pass', 'Fail'):
            raise ValueError('Result must be Pass or Fail')
        observed[item['id']] = item
    selected = [r for r in references if r['criterion_id'] == criterion]
    if not selected:
        raise ValueError('Unknown criterion')
    prefix = criterion.rsplit('.', 1)[-1] + '.'
    expected = {r['id'].removeprefix(prefix): r['reference_label'] for r in selected}
    # A first-pass packet also contains both actual response IDs; a challenge-only packet has neither.
    actual = {'response-a', 'response-b'}
    if set(observed) - set(expected) - actual:
        raise ValueError('Unexpected candidate ID')
    if actual & set(observed) not in (set(), actual):
        raise ValueError('First-pass packet requires both response-a and response-b verdicts')
    if set(expected) - set(observed):
        raise ValueError('Missing challenge verdicts')
    counts = {label: {'correct': 0, 'total': 0} for label in ('Pass', 'Fail')}
    disagreements = []
    for identifier, label in expected.items():
        counts[label]['total'] += 1
        counts[label]['correct'] += observed[identifier]['result'] == label
        if observed[identifier]['result'] != label:
            disagreements.append({'id': identifier, 'expected': label,
                                  'actual': observed[identifier]['result'],
                                  'critique': observed[identifier]['critique']})
    return {'criterion_id': criterion, 'synthetic_challenges': counts,
            'disagreements': disagreements,
            'human_calibration': 'Unmeasured: synthetic oracles are not human labels'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('criterion', choices=['CPS-AUD-001.C1', 'CPS-AUD-001.C2', 'CPS-AUD-001.C4'])
    parser.add_argument('verdicts', type=Path)
    args = parser.parse_args()
    try:
        references = json.loads(Path(__file__).with_name('validation-cases.json').read_text())
        result = check(json.loads(args.verdicts.read_text()), args.criterion, references)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Invalid judge evidence: {error}\n')
    print(json.dumps(result, indent=2))
    return bool(result['disagreements'])


if __name__ == '__main__':
    raise SystemExit(main())
