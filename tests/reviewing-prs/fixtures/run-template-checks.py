#!/usr/bin/env python3
"""Check the reviewing-prs page template and the shell steps that fill it.

The page shows text that strangers wrote, so its safety rests on two things:
the template's own rules (one policy, one nonce'd script, no HTML built from
strings) and the shell steps that put the round's data into it without
decoding or stripping the escapes. This runner fills the template with the
sample round the way the skill prescribes and checks the result as text.

It then runs the page's own script in Node against a minimal stand-in for the
browser's DOM, and checks where each pull request lands: which side of the
hold line, in what order, and whether a sensitive kind is named. It cannot
tell whether the page looks right; that takes a browser.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = ROOT / "skills/reviewing-prs"
TEMPLATE = SKILL_DIR / "assets/review-page.html"
REFERENCE = SKILL_DIR / "references/review-page.md"
SAMPLE = Path(__file__).resolve().parent / "sample-round.json"


def fill_commands() -> str:
    """The shell block the skill ships under "Build the page", run as written."""
    text = REFERENCE.read_text()
    section = text.split("## Build the page", 1)[1]
    match = re.search(r"```sh\n(.*?)```", section, re.S)
    if not match:
        raise SystemExit("FAIL references/review-page.md has no shell block under 'Build the page'")
    return "set -eu\n" + match.group(1).replace("<skill-dir>", '"$skill_dir"')

BANNED = re.compile(r"innerHTML|outerHTML|insertAdjacentHTML|document\.write|\son[a-z]+\s*=|<form\b|<iframe\b|<object\b|<embed\b|eval\(|new Function")
DATA_BLOCK = re.compile(r'<script type="application/json" id="round-data">\n(.*?)\n</script>', re.S)

failures: list[str] = []

# Runs the filled page's script with a minimal DOM and prints where each pull request landed.
RENDER = r"""
const fs = require("fs"), vm = require("vm");
const html = fs.readFileSync(process.argv[2], "utf8");
const data = /<script type="application\/json" id="round-data">\n([\s\S]*?)\n<\/script>/.exec(html)[1];
const code = /<script nonce="[0-9a-f]+">([\s\S]*?)<\/script>/.exec(html)[1];
const text = (value) => ({ isText: true, textContent: String(value), children: [] });
class Node {
  constructor(tag) {
    this.tagName = tag; this.children = []; this._text = null; this.attributes = {}; this.dataset = {}; this.style = {};
    this.className = ""; this.id = "";
    const node = this;
    this.classList = {
      add: (name) => { if (!node.className.split(" ").includes(name)) node.className = (node.className + " " + name).trim(); },
      toggle: (name, on) => { const has = node.className.split(" ").includes(name); if (on ?? !has) node.classList.add(name); else node.className = node.className.split(" ").filter((c) => c !== name).join(" "); },
      contains: (name) => node.className.split(" ").includes(name),
    };
  }
  get textContent() { return this._text !== null ? this._text : this.children.map((c) => c.textContent).join(""); }
  set textContent(value) { this._text = String(value); this.children = []; }
  append(...nodes) {
    if (this._text !== null) { this.children = [text(this._text)]; this._text = null; }
    for (const n of nodes) {
      if (n && n.isFragment) { this.children.push(...n.children); n.children = []; }
      else this.children.push(typeof n === "string" ? text(n) : n);
    }
  }
  replaceChildren(...nodes) { this._text = null; this.children = []; this.append(...nodes); }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  getAttribute(k) { return k in this.attributes ? this.attributes[k] : null; }
  addEventListener() {} focus() {} select() {} replaceWith() {}
  querySelector() { return null; } querySelectorAll() { return []; }
  getBoundingClientRect() { return { top: 0, bottom: 0 }; }
}
const fixed = { "round-data": Object.assign(new Node("script"), { _text: data }) };
for (const [id, tag] of [["page", "main"], ["rail", "nav"], ["theme", "button"], ["bar-note", "span"], ["bar-progress", "a"]]) fixed[id] = new Node(tag);
const walk = (node, out = []) => { if (node && !node.isText) { out.push(node); for (const c of node.children) walk(c, out); } return out; };
const store = new Map();
const localStorage = { getItem: (k) => (store.has(k) ? store.get(k) : null), setItem: (k, v) => store.set(k, String(v)), removeItem: (k) => store.delete(k),
  key: (i) => [...store.keys()][i] ?? null, get length() { return store.size; } };
const document = {
  documentElement: { dataset: {} },
  createElement: (tag) => new Node(tag), createTextNode: text,
  createDocumentFragment: () => Object.assign(new Node("#fragment"), { isFragment: true }),
  getElementById: (id) => fixed[id] || walk(fixed.page).concat(walk(fixed.rail)).find((n) => n.id === id) || null,
  querySelector: () => null, addEventListener() {},
};
const window = { matchMedia: () => ({ matches: false, addEventListener() {} }), localStorage, innerHeight: 800, addEventListener() {} };
vm.runInNewContext(code, { window, document, navigator: { clipboard: { writeText: async () => {} } }, URL, console });
const has = (n, cls) => (n.className || "").split(" ").includes(cls);
const all = walk(fixed.page);
const groups = all.filter((n) => n.tagName === "section" && has(n, "over")).map((section) => ({
  hold: has(section, "hold"),
  subtitle: walk(section).find((n) => n.tagName === "small")?.textContent ?? "",
  rows: walk(section).filter((n) => has(n, "orow")).map((row) => ({
    title: walk(row).find((n) => has(n, "title"))?.textContent ?? "",
    kind: walk(row).find((n) => has(n, "kind"))?.textContent ?? null,
  })),
}));
const blocks = all.filter((n) => n.tagName === "article").map((a) => ({
  title: walk(a).find((n) => n.tagName === "h2")?.textContent ?? "",
  hold: has(a, "hold"),
  driver: walk(a).find((n) => has(n, "driver"))?.textContent ?? "",
}));
process.stdout.write(JSON.stringify({ groups, blocks }));
"""


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
    match = DATA_BLOCK.search(page)
    # Pull request text may hold `{{`, as a workflow's `${{ secrets.X }}` does, so only the page around the data counts.
    outside = page[:match.start(1)] + page[match.end(1):] if match else page
    check("{{" not in outside, "a placeholder is left in the filled page")
    policy = re.findall(r"'nonce-([0-9a-f]{32})'", page)
    script = re.findall(r'<script nonce="([0-9a-f]{32})">', page)
    check(len(policy) == 1 and policy == script, "the policy's nonce does not match the script's")
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


def check_rendered(page: str, scratch: Path, original: dict) -> None:
    """Run the page's script and check placement against the sample's scores and sensitive kinds."""
    node = shutil.which("node")
    if node is None:
        failures.append("node is required to run the page's script")
        return
    (scratch / "render.js").write_text(RENDER)
    (scratch / "page.html").write_text(page)
    result = subprocess.run([node, str(scratch / "render.js"), str(scratch / "page.html")], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        failures.append(f"the page's script failed to run: {result.stderr.strip()[:300]}")
        return
    rendered = json.loads(result.stdout)
    number = {pr["title"]: pr["number"] for pr in original["prs"]}
    groups = {("held" if g["hold"] else "under"): g for g in rendered["groups"]}
    held = [number.get(r["title"]) for r in groups.get("held", {}).get("rows", [])]
    under = [number.get(r["title"]) for r in groups.get("under", {}).get("rows", [])]
    # Highest V x U first; equal products break on leverage (#436 at 2.00 before #432 at 1.33);
    # #405 is held for its lockfile although V x U is 1.
    check(held == [418, 421, 131, 436, 432, 405], f"held group order: {held}")
    check(under == [134, 409], f"under-the-line group order: {under}")
    check("sensitive kind" in groups.get("held", {}).get("subtitle", ""), "the held group's subtitle does not mention sensitive kinds")
    kinds = {number.get(r["title"]): r["kind"] for g in rendered["groups"] for r in g["rows"]}
    check("dependency lockfile" in (kinds.get(405) or ""), f"#405's overview row does not name its sensitive kind: {kinds.get(405)}")
    check("money" in (kinds.get(421) or ""), f"#421's overview row does not name its sensitive kind: {kinds.get(421)}")
    check(kinds.get(418) is None, "a pull request with no sensitive kind shows one")
    blocks = {number.get(next((t for t in number if b["title"].endswith(t)), None)): b for b in rendered["blocks"]}
    lockfile = blocks.get(405, {})
    check(lockfile.get("hold") is True, "#405's block is not marked held")
    check(lockfile.get("driver", "").startswith("Held for a sensitive kind, dependency lockfile, though V × U is 1."),
          f"#405's block does not say why it is held: {lockfile.get('driver')}")
    check("Over the hold line, V × U 6, and it touches a sensitive kind: money." in blocks.get(421, {}).get("driver", ""),
          f"#421's block does not name its sensitive kind: {blocks.get(421, {}).get('driver')}")
    check(blocks.get(134, {}).get("driver", "").startswith("Under the hold line, V × U 1."), "#134's block is not under the hold line")


def main() -> int:
    template = TEMPLATE.read_text()
    check_template(template)
    raw = SAMPLE.read_text()
    original = json.loads(raw)
    check(any("</script>" in pr.get("title", "") for pr in original["prs"]), "the sample lost its hostile title")
    code_lines = [line for pr in original["prs"] for excerpt in pr.get("code", []) for line in excerpt.get("lines", [])]
    check(any("${{" in line for line in code_lines), "the sample lost its workflow line with ${{ }}")
    low_and_sensitive = [pr for pr in original["prs"] if pr.get("sensitiveKind") and pr["scores"]["verify"] * pr["scores"]["undo"] < 3]
    check(bool(low_and_sensitive), "the sample lost its sensitive-kind pull request with V x U under 3")
    with tempfile.TemporaryDirectory() as scratch:
        page, data = fill(raw, Path(scratch))
        check_filled(page, data, original)
        check_rendered(page, Path(scratch), original)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("reviewing-prs page template: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
