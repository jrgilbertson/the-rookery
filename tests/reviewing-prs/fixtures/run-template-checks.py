#!/usr/bin/env python3
"""Check the reviewing-prs page template and the shell steps that fill it.

The page shows text that strangers wrote, so its safety rests on two things:
the template's own rules (one policy, one nonce'd script, no HTML built from
strings) and the shell steps that put the round's data into it without
decoding or stripping the escapes. This runner fills the template with the
sample round the way the skill prescribes and checks the result as text. It
cannot tell whether the page looks right; that takes a browser.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = ROOT / "skills/reviewing-prs/assets/review-page.html"
SAMPLE = Path(__file__).resolve().parent / "sample-round.json"

# The steps the skill prescribes, run with POSIX sh. $dir holds round.json.
FILL = r"""
set -eu
nonce=$(openssl rand -hex 16)
sed -e 's/&/\\u0026/g' -e 's/</\\u003c/g' -e 's/>/\\u003e/g' "$dir/round.json" > "$dir/data.json"
sed -e "s/{{NONCE}}/$nonce/g" -e '/^{{ROUND_DATA}}$/{' -e "r $dir/data.json" -e 'd' -e '}' "$template" > "$dir/review.html"
"""

BANNED = re.compile(r"innerHTML|outerHTML|insertAdjacentHTML|document\.write|\son[a-z]+\s*=|<form\b|<iframe\b|<object\b|<embed\b|eval\(|new Function")
DATA_BLOCK = re.compile(r'<script type="application/json" id="round-data">\n(.*?)\n</script>', re.S)

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def check_template(text: str) -> None:
    head = text.split("<head>", 1)[1].lstrip() if "<head>" in text else ""
    check(head.startswith('<meta http-equiv="Content-Security-Policy"'), "the policy is not the first element in <head>")
    check(len(re.findall(r"^\{\{ROUND_DATA\}\}$", text, re.M)) == 1 and text.count("{{ROUND_DATA}}") == 1,
          "{{ROUND_DATA}} must appear once, alone on its own line")
    check(text.count("{{NONCE}}") == 2, "{{NONCE}} must appear twice: in the policy and on the script")
    check(len(re.findall(r"<script\b", text)) == 2, "the template must hold exactly the data block and one script")
    check(not BANNED.search(text), "the template uses a banned call, handler attribute, or element: " + str(BANNED.findall(text)[:3]))
    addresses = re.findall(r'(?:src|href)="([^"]*)"', text) + re.findall(r"url\(([^)]*)\)", text) + re.findall(r"@import", text)
    check(set(addresses) <= {"data:,", "#verdicts"}, f"the template loads or links something external: {addresses}")


def fill(round_data: str, scratch: Path) -> tuple[str, str]:
    (scratch / "round.json").write_text(round_data)
    subprocess.run(["sh", "-c", FILL], env={"PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin", "dir": str(scratch), "template": str(TEMPLATE)}, check=True)
    return (scratch / "review.html").read_text(), (scratch / "data.json").read_text()


def check_filled(page: str, data: str, original: dict) -> None:
    check("{{" not in page, "a placeholder is left in the filled page")
    policy = re.findall(r"'nonce-([0-9a-f]{32})'", page)
    script = re.findall(r'<script nonce="([0-9a-f]{32})">', page)
    check(len(policy) == 1 and policy == script, "the policy's nonce does not match the script's")
    match = DATA_BLOCK.search(page)
    check(match is not None, "the data block is missing")
    if not match:
        return
    block = match.group(1)
    check(block + "\n" == data, "the data block is not byte-identical to the escaped data file")
    check("<" not in block and ">" not in block and "&" not in block, "the data block holds a literal <, >, or &")
    try:
        check(json.loads(block) == original, "the data block does not decode to the round that was written")
    except json.JSONDecodeError as error:
        failures.append(f"the data block does not parse: {error}")


def main() -> int:
    template = TEMPLATE.read_text()
    check_template(template)
    raw = SAMPLE.read_text()
    original = json.loads(raw)
    check(any("</script>" in pr.get("title", "") for pr in original["prs"]), "the sample lost its hostile title")
    with tempfile.TemporaryDirectory() as scratch:
        page, data = fill(raw, Path(scratch))
        check_filled(page, data, original)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("reviewing-prs page template: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
