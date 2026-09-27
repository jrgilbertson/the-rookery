#!/usr/bin/env python3
"""Per-call ccusage accounting for a trusted, sequential eval operator."""
import argparse
import json
import math
from pathlib import Path
import re
import sys

import usage


def amount(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def balance(directory, budget):
    if not amount(budget) or budget <= 0:
        raise ValueError('Budget must be a finite positive authorized dollar amount')
    total = 0
    for path in sorted(directory.glob('*.json')):
        record = json.loads(path.read_text())
        cost = record.get('cost_usd') if isinstance(record, dict) else None
        if not amount(cost) or record.get('error'):
            raise ValueError(f'{path.name}: cost unknown; stop further calls')
        total += cost
    return budget - total


def begin(directory, name, budget):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', name):
        raise ValueError('Call name must contain only letters, digits, underscores or hyphens')
    directory.mkdir(parents=True, exist_ok=True)
    if balance(directory, budget) <= 0:
        raise ValueError('Budget exhausted; stop further calls')
    path = directory / f'{name}.json'
    with path.open('x') as stream:
        json.dump({'cost_usd': None, 'state': 'pending'}, stream)
        stream.write('\n')
    return path


def price(record, provider, transcript, sessions, model, command):
    previous = json.loads(record.read_text())
    if not isinstance(previous, dict) or previous.get('cost_usd') is not None:
        raise ValueError('Only a pending or unknown cost can be priced')
    result = usage.estimate(provider, transcript, sessions, None, command, record.parent, model)
    result.update(provider=provider, transcript=str(transcript.resolve()),
                  sessions=str(sessions.resolve()) if sessions else None, model=model)
    record.write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    for action in ('begin', 'status'):
        sub = commands.add_parser(action)
        sub.add_argument('directory', type=Path, help='Private directory containing only this budget’s cost records')
        sub.add_argument('--budget', type=float, required=True, help='Already-authorized total allowance, USD')
        if action == 'begin':
            sub.add_argument('name', help='Unique name for this executor, grader, or retry call')
    sub = commands.add_parser('price')
    sub.add_argument('record', type=Path)
    sub.add_argument('--provider', choices=['codex', 'grok', 'claude'], required=True)
    sub.add_argument('--transcript', type=Path, required=True)
    sub.add_argument('--sessions', type=Path, help='Isolated native Codex session directory, including children')
    sub.add_argument('--model', help='Recorded invocation model for tool-free ephemeral Codex calls')
    sub.add_argument('--ccusage', default='ccusage', help='Path to the ccusage executable')
    args = parser.parse_args()
    try:
        if args.action == 'begin':
            print(begin(args.directory, args.name, args.budget))
        elif args.action == 'status':
            if not args.directory.is_dir():
                raise ValueError('Accounting directory does not exist')
            remaining = balance(args.directory, args.budget)
            print(json.dumps({'remaining_usd': remaining}))
            return 0 if remaining > 0 else 1
        else:
            result = price(args.record, args.provider, args.transcript, args.sessions, args.model, [args.ccusage])
            print(json.dumps(result))
            return 0 if result['cost_usd'] is not None else 1
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
