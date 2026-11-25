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
SKILL_DIR = ROOT / "skills/reviewing-prs"
TEMPLATE = SKILL_DIR / "assets/review-page.html"
SKILL = SKILL_DIR / "SKILL.md"
SAMPLE = Path(__file__).resolve().parent / "sample-round.json"


def fill_commands() -> str:
    """The shell block the skill ships under "Build the page", run as written."""
    text = SKILL.read_text()
    section = text.split("**Build the page.**", 1)[1]
    match = re.search(r"```sh\n(.*?)```", section, re.S)
    if not match:
        raise SystemExit("FAIL SKILL.md has no shell block under 'Build the page'")
    return "set -eu\n" + match.group(1).replace("<skill-dir>", '"$skill_dir"')

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
    subprocess.run(["sh", "-c", fill_commands()], cwd=scratch, check=True,
                   env={"PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin", "skill_dir": str(SKILL_DIR)})
    page = scratch / "review.html"
    check(page.stat().st_mode & 0o077 == 0, "the filled page is readable by other users")
    return page.read_text(), (scratch / "data.json").read_text()


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
