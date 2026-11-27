#!/usr/bin/env python3
"""Check the reviewing-prs page template and the shell steps that fill it.

The page shows text that strangers wrote, so its safety rests on two things:
the template's own rules (one policy, one nonce'd script, no HTML built from
strings) and the shell steps that put the round's data into it without
decoding or stripping the escapes. This runner fills the template with the
sample round the way the skill prescribes and checks the result as text.

It then runs the page's own script in Node against a minimal stand-in for the
browser's DOM, and checks where each pull request lands: which side of the
hold line, in what order, and whether a sensitive kind is named. A large
round built here then checks the four groups, the bounded notices, the merged
drawer, the filters, the copy controls, and the Verdict notes. It cannot tell
whether the page looks right; that takes a browser.
"""

from __future__ import annotations

import copy
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
    text = REFERENCE.read_text()
    section = text.split("## Build the page", 1)[1]
    match = re.search(r"```sh\n(.*?)```", section, re.S)
    if not match:
        raise SystemExit("FAIL references/review-page.md has no shell block under 'Build the page'")
    return "set -eu\n" + match.group(1).replace("<skill-dir>", '"$skill_dir"')

BANNED = re.compile(r"innerHTML|outerHTML|insertAdjacentHTML|document\.write|\son[a-z]+\s*=|<form\b|<iframe\b|<object\b|<embed\b|eval\(|new Function")
DATA_BLOCK = re.compile(r'<script type="application/json" id="round-data">\n(.*?)\n</script>', re.S)

failures: list[str] = []

RENDER = r"""
const fs = require("fs"), vm = require("vm");
const html = fs.readFileSync(process.argv[2], "utf8");
const actions = JSON.parse(process.argv[3] || "[]");
const data = /<script type="application\/json" id="round-data">\n([\s\S]*?)\n<\/script>/.exec(html)[1];
const code = /<script nonce="[0-9a-f]+">([\s\S]*?)<\/script>/.exec(html)[1];
const text = (value) => ({ isText: true, textContent: String(value), children: [] });
const walk = (node, out = []) => { if (node && !node.isText) { out.push(node); for (const c of node.children) walk(c, out); } return out; };
class Node {
  constructor(tag) {
    this.tagName = tag; this.children = []; this._text = null; this.attributes = {}; this.dataset = {}; this.style = {};
    this.className = ""; this.id = ""; this.hidden = false; this.open = false; this.checked = false; this.value = "";
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
  removeAttribute(k) { delete this.attributes[k]; }
  addEventListener(type, handler) { ((this.listeners ||= {})[type] ||= []).push(handler); }
  fire(type, event = {}) { return Promise.all(((this.listeners || {})[type] || []).map((handler) => handler(event))); }
  contains(other) { return walk(this).includes(other); }
  focus() {} select() {} replaceWith() {}
  scrollIntoView() { scrolled = this.id; }
  // Enough of closest() for the page's typing guard: a text field matches, a checkbox only when the selector does not rule it out.
  closest(selector) {
    if (!selector.includes(this.tagName)) return null;
    return this.type === "checkbox" && selector.includes(':not([type="checkbox"])') ? null : this;
  }
  querySelector() { return null; } querySelectorAll() { return []; }
  getBoundingClientRect() { return this.rect || { top: 0, bottom: 0 }; }
  get offsetHeight() { return 56; }
}
const fixed = { "round-data": Object.assign(new Node("script"), { _text: data }) };
for (const [id, tag] of [["page", "main"], ["rail", "nav"], ["theme", "button"], ["bar", "header"], ["bar-note", "span"],
  ["bar-progress", "a"], ["bar-copy", "button"], ["bar-cue", "span"]]) fixed[id] = Object.assign(new Node(tag), { id });
const store = new Map();
const localStorage = { getItem: (k) => (store.has(k) ? store.get(k) : null), setItem: (k, v) => store.set(k, String(v)), removeItem: (k) => store.delete(k),
  key: (i) => [...store.keys()][i] ?? null, get length() { return store.size; } };
const heard = (target) => (type, handler) => { ((target.listeners ||= {})[type] ||= []).push(handler); };
const document = {
  documentElement: { dataset: {}, style: { setProperty() {} } },
  createElement: (tag) => new Node(tag), createTextNode: text,
  createDocumentFragment: () => Object.assign(new Node("#fragment"), { isFragment: true }),
  getElementById: (id) => fixed[id] || walk(fixed.page).concat(walk(fixed.rail)).find((n) => n.id === id) || null,
  querySelector: () => null,
};
document.addEventListener = heard(document);
const window = { matchMedia: () => ({ matches: false, addEventListener() {} }), localStorage, innerHeight: 800, location: { hash: "" } };
window.addEventListener = heard(window);
let clipboard = null, scrolled = null;
vm.runInNewContext(code, { window, document, navigator: { clipboard: { writeText: async (value) => { clipboard = value; } } },
  URL, console, Element: Node, setTimeout: () => 0, clearTimeout() {} });

const has = (n, cls) => (n.className || "").split(" ").includes(cls);
const within = (root, cls) => walk(root).filter((n) => has(n, cls));
const one = (root, cls) => within(root, cls)[0] || null;
const chips = (root) => within(root, "chip").map((n) => n.textContent);
const snap = () => {
  const all = walk(fixed.page);
  const merged = all.find((n) => n.id === "merged");
  const drawer = all.find((n) => n.tagName === "details");
  const verdicts = all.find((n) => n.id === "verdicts");
  const empty = all.find((n) => n.id === "filter-empty");
  const marks = all.concat(walk(fixed.rail)).filter((n) => has(n, "seal") || has(n, "ring") || has(n, "route-dot"));
  return {
    order: fixed.page.children.filter((n) => !n.isText).map((n) => n.id || n.className || n.tagName),
    lede: one(fixed.page, "lede")?.textContent ?? "",
    notices: (one(fixed.page, "notices")?.children ?? []).map((li) => ({
      text: li.textContent, sealed: within(li, "seal").length > 0, href: walk(li).find((n) => n.tagName === "a")?.href ?? null })),
    groups: all.filter((n) => n.tagName === "section" && has(n, "over")).map((section) => ({
      cls: section.className, hold: has(section, "hold"), hidden: section.hidden,
      heading: walk(section).find((n) => n.tagName === "h2")?.textContent ?? "",
      subtitle: walk(section).find((n) => n.tagName === "small")?.textContent ?? "",
      rows: within(section, "orow").map((row) => ({
        title: one(row, "title")?.textContent ?? "", hidden: row.hidden,
        kind: one(row, "kind")?.textContent ?? null,
        vu: one(row, "vu")?.children[0]?.textContent ?? null,
        chips: chips(row), size: one(row, "size")?.textContent ?? null,
      })),
    })),
    blocks: all.filter((n) => n.tagName === "article").map((a) => ({
      id: a.id, cls: a.className, hidden: a.hidden, hold: has(a, "hold"),
      title: walk(a).find((n) => n.tagName === "h2")?.textContent ?? "",
      driver: one(a, "driver")?.textContent ?? "",
      chips: chips(one(a, "block-meta") || new Node("x")), xnotes: within(a, "xnote").map((n) => n.textContent),
      hint: one(a, "hint") ? { text: one(a, "hint").textContent, hidden: one(a, "hint").hidden } : null,
      seg: one(a, "seg")?.attributes ?? {}, notes: { ...(one(a, "notes")?.attributes ?? {}) },
      github: walk(a).filter((n) => n.tagName === "a" && n.textContent === "Open on GitHub").map((n) => ({ href: n.href, rel: n.rel }))[0] ?? null,
    })),
    merged: merged && {
      headings: walk(merged).filter((n) => /^h[1-6]$/.test(n.tagName)).map((n) => n.tagName),
      drawer: drawer ? { open: drawer.open, inside: merged.contains(drawer),
        summary: walk(drawer).find((n) => n.tagName === "summary")?.textContent ?? "",
        summaryHeadings: walk(walk(drawer).find((n) => n.tagName === "summary")).filter((n) => /^h[1-6]$/.test(n.tagName)).length } : null,
      lists: within(merged, "mlist").map((box) => ({
        title: walk(box).find((n) => n.tagName === "h3")?.textContent ?? "",
        rows: within(box, "crow").length, sealed: within(box, "seal").length,
        ids: within(box, "crow").map((n) => n.id),
      })),
    },
    bar: { copy: fixed["bar-copy"].textContent, cue: fixed["bar-cue"].textContent,
      progress: fixed["bar-progress"].textContent, href: fixed["bar-progress"].href ?? null },
    box: verdicts && { copy: one(verdicts, "copy")?.textContent ?? null, value: walk(verdicts).find((n) => n.tagName === "textarea")?.value ?? null,
      label: walk(verdicts).find((n) => n.tagName === "textarea")?.attributes["aria-label"] ?? null,
      status: walk(verdicts).find((n) => n.attributes["aria-live"])?.textContent ?? null },
    rail: { tags: [...new Set(walk(fixed.rail).map((n) => n.tagName))],
      lists: walk(fixed.rail).filter((n) => n.tagName === "ol").map((ol) => ({
        labelled: Boolean(ol.attributes["aria-labelledby"] && document.getElementById(ol.attributes["aria-labelledby"])),
        items: ol.children.map((li) => ({ hidden: li.hidden, text: li.textContent })) })) },
    filters: { tabs: all.filter((n) => n.tagName === "button" && n.dataset.filter).map((b) => ({
        key: b.dataset.filter, text: b.textContent, pressed: b.attributes["aria-pressed"] })),
      broken: all.find((n) => n.id === "filter-broken") ? { checked: all.find((n) => n.id === "filter-broken").checked } : null,
      status: all.find((n) => n.id === "filter-status") ? { text: all.find((n) => n.id === "filter-status").textContent,
        live: all.find((n) => n.id === "filter-status").attributes["aria-live"] } : null,
      empty: empty ? { hidden: empty.hidden, text: empty.textContent } : null },
    marksHidden: marks.every((n) => n.attributes["aria-hidden"] === "true"), markCount: marks.length,
    clipboard, scrolled, stored: store.size,
  };
};
const article = (title) => walk(fixed.page).find((n) => n.tagName === "article" && walk(n).find((h) => h.tagName === "h2")?.textContent.endsWith(title));
const run = async () => {
  const steps = [snap()];
  for (const [what, a, b, c] of actions) {
    if (what === "verdict") await walk(article(a)).find((n) => n.tagName === "button" && n.dataset.verdict === b).fire("click");
    if (what === "notes") { const input = one(article(a), "notes"); input.value = b; await input.fire("input"); }
    if (what === "copy") await (a === "bar" ? fixed["bar-copy"] : one(walk(fixed.page).find((n) => n.id === "verdicts"), "copy")).fire("click");
    if (what === "tab") await walk(fixed.page).find((n) => n.tagName === "button" && n.dataset.filter === a).fire("click");
    if (what === "broken") { const boxNode = walk(fixed.page).find((n) => n.id === "filter-broken"); boxNode.checked = a; await boxNode.fire("change"); }
    if (what === "jump") await walk(one(fixed.page, "notices")).filter((n) => n.tagName === "a")[a].fire("click");
    if (what === "span") article(a).rect = { top: 0, bottom: 500 };
    if (what === "key") {
      const target = c === "toggle" ? walk(fixed.page).find((n) => n.id === "filter-broken") : c ? one(article(c), "notes") : null;
      for (const handler of document.listeners?.keydown ?? []) handler({ key: a, target, repeat: Boolean(b), preventDefault() {} });
    }
    steps.push(snap());
  }
  process.stdout.write(JSON.stringify(steps));
};
run();
"""


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def check_template(text: str) -> None:
    head = text.split("<head>", 1)[1].lstrip() if "<head>" in text else ""
    check(head.startswith('<meta http-equiv="Content-Security-Policy"'), "the policy is not the first element in <head>")
    check(text.count("{{ROUND_DATA}}") == 1 and re.search(r"^\{\{ROUND_DATA\}\}$", text, re.M) is not None,
          "{{ROUND_DATA}} must appear once, alone on its own line")
    check(text.count("{{NONCE}}") == 2, "{{NONCE}} must appear twice: in the policy and on the script")
    check(len(re.findall(r"<script\b", text)) == 2, "the template must hold exactly the data block and one script")
    check(not BANNED.search(text), "the template uses a banned call, handler attribute, or element: " + str(BANNED.findall(text)[:3]))
    addresses = re.findall(r'(?:src|href)="([^"]*)"', text) + re.findall(r"url\(([^)]*)\)", text) + re.findall(r"@import", text)
    check(set(addresses) <= {"data:,", "#verdicts"}, f"the template loads or links something external: {addresses}")
    policy = re.search(r'Content-Security-Policy" content="([^"]*)"', text)
    check(policy is not None and "default-src 'none'" in policy.group(1) and "connect-src 'none'" in policy.group(1)
          and "script-src 'nonce-{{NONCE}}'" in policy.group(1), "the policy lost default-src 'none', connect-src 'none', or its nonce")
    for kept, why in (
        ('STORE = "reviewing-prs:"', "the browser-storage key prefix"),
        ("30 * 24 * 60 * 60 * 1000", "the 30-day expiry of stored Verdicts"),
        ("verdictBox.value && verdictBox.value !== lastCopied", "the guard against leaving with uncopied Verdicts"),
        ('url.protocol === "https:"', "the https-only check on links"),
        ('anchor.rel = "noopener noreferrer"', "noopener noreferrer on outside links"),
        ("JSON.parse(document.getElementById(\"round-data\").textContent)", "the guarded read of the round's data"),
        ('event.repeat && ["m", "c", "d", "x"].includes(event.key)', "the held-key guard on Verdict keys"),
        ("spansLine(here) && choose(here, key)", "the reading-line guard on Verdict keys"),
        ("IntersectionObserver", "the rail's scroll-spy"),
        ("@media (prefers-reduced-motion: reduce)", "a reduced-motion rule"),
        ("[hidden] { display: none !important; }", "the rule that lets a filter hide rows and cards that set their own display"),
        ('id="bar-cue" role="status" aria-live="polite"', "a polite live region for the bar's cue"),
        ('id="bar-copy"', "the sticky bar's Copy Verdicts button"),
    ):
        check(kept in text, f"the template lost {why}")
    check("box-shadow" not in text, "the template casts a shadow, which Working Pages forbid")
    check(not re.search(r"\[tabindex=\"-1\"\]:focus\s*\{\s*outline:\s*none", text),
          "a heading focused from the keyboard must keep its focus ring")
    for selector in (".rank", ".vu", ".bar strong", "h1"):
        rule = re.search(r"(?m)^" + re.escape(selector) + r" \{[^}]*font: [^;]*? ([0-9.]+)rem[^;]*var\(--display\)", text)
        check(rule is not None and float(rule.group(1)) >= 1, f"{selector} must set Didot at 1rem or larger")
    for rule in re.findall(r"[^{}]*\{[^}]*var\(--display\)[^}]*\}", text):
        size = re.search(r"font: [^;]*? ([0-9.]+)rem", rule)
        check(size is None or float(size.group(1)) >= 1, f"Didot is set under 1rem: {rule.strip()[:60]}")


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


def render(page: str, scratch: Path, actions: list | None = None) -> list | None:
    node = shutil.which("node")
    if node is None:
        failures.append("node is required to run the page's script")
        return None
    (scratch / "render.js").write_text(RENDER)
    (scratch / "page.html").write_text(page)
    result = subprocess.run([node, str(scratch / "render.js"), str(scratch / "page.html"), json.dumps(actions or [])],
                            capture_output=True, text=True, check=False)
    if result.returncode != 0:
        failures.append(f"the page's script failed to run: {result.stderr.strip()[:400]}")
        return None
    return json.loads(result.stdout)


def group(snapshot: dict, cls: str) -> dict:
    return next((g for g in snapshot["groups"] if cls in g["cls"].split()), {"rows": [], "heading": "", "subtitle": "", "hidden": True})


def check_rendered(page: str, scratch: Path, original: dict) -> None:
    steps = render(page, scratch, [["verdict", "Refactor: rename formatCents to formatMinorUnits", "na"]])
    if steps is None:
        return
    rendered, chosen = steps
    number = {pr["title"]: pr["number"] for pr in original["prs"]}
    held = [number.get(r["title"]) for r in group(rendered, "hold")["rows"]]
    under = [number.get(r["title"]) for r in group(rendered, "under")["rows"]]
    check(held == [418, 421, 131, 436, 432, 405],
          f"held group order, highest V x U first, ties by leverage (#436 at 2.00 before #432 at 1.33), then #405 held for its lockfile at V x U 1: {held}")
    check(under == [134, 409], f"under-the-line group order: {under}")
    check("sensitive kind" in group(rendered, "hold")["subtitle"], "the held group's subtitle does not mention sensitive kinds")
    check([g["cls"] for g in rendered["groups"]] == ["over hold", "over under"],
          f"a round with no dependency bot and no in-flight pull request must draw only two groups: {[g['cls'] for g in rendered['groups']]}")
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
    first = next(pr for pr in original["prs"] if pr["number"] == 418)
    check(chosen["box"]["value"] == f"{first.get('repo')}#{first.get('number')} @ {first.get('head')} | not applicable | ",
          f"choosing Not applicable must build its Verdict line: {chosen['box']['value']!r}")
    # A small round stays legible: each merge has its own notice and the merged lists are open.
    notices = [n["text"] for n in rendered["notices"]]
    check(any("#412 merged without you" in n for n in notices) and any("#129 changed after your Verdict" in n for n in notices),
          f"a small round must keep one notice per merged pull request: {notices}")
    drawer = (rendered["merged"] or {}).get("drawer") or {}
    check(drawer.get("open") is True, "a small round must show its merged lists open")
    check(rendered["stored"] == 0 and chosen["stored"] == 1, "a chosen Verdict must be kept in browser storage, keyed to the reviewed head")
    for b in rendered["blocks"]:
        check(b["github"] is not None and b["github"]["href"].startswith("https://github.com/") and b["github"]["rel"] == "noopener noreferrer",
              f"{b['title']!r} lost its safe Open on GitHub link: {b['github']}")
        check(b["seg"].get("role") == "group" and b["seg"].get("aria-label", "").startswith("Verdict for "), f"{b['title']!r} lost its Verdict group label")
        check(b["notes"].get("aria-label", "").startswith("Notes for "), f"{b['title']!r} lost its notes label")
    check(rendered["box"]["label"] == "Chosen Verdicts, one line per pull request", "the Verdicts box lost its label")


def check_incomplete_scores(raw: str, scratch: Path) -> None:
    variant = json.loads(raw)
    for pr in variant["prs"]:
        if pr["number"] == 134:
            pr["scores"].pop("confidence")
        if pr["number"] == 409:
            pr["scores"].pop("undo")
    page, _ = fill(json.dumps(variant, indent=2, ensure_ascii=False) + "\n", scratch)
    steps = render(page, scratch)
    if steps is None:
        return
    rendered = steps[0]
    number = {pr["title"]: pr["number"] for pr in variant["prs"]}
    rows = {number.get(row["title"]): row for row in group(rendered, "hold")["rows"]}
    held = list(rows)
    check(set(held[:2]) == {134, 409}, f"a pull request missing any score must sort to the top of the held group: {held}")
    drivers = {n: next((b["driver"] for b in rendered["blocks"] if b["title"].endswith(t)), "") for t, n in number.items()}
    for pr, badge, placement in ((134, "1", "Held because a score is missing. V × U is 1."), (409, "?", "Held because a score is missing.")):
        check(rows.get(pr, {}).get("vu") == badge, f"#{pr}'s V x U badge must read {badge}: {rows.get(pr, {}).get('vu')}")
        expected = placement + " " + next(p["driver"] for p in variant["prs"] if p["number"] == pr)
        check(drivers.get(pr) == expected, f"#{pr}'s block must say it is held for a missing score: {drivers.get(pr)}")


def large_round(original: dict, without: int = 52, auto_merged: int = 60) -> dict:
    """A fleet-sized round: 31 open pull requests in four groups and over 100 merged ones."""
    base = next(pr for pr in original["prs"] if pr["number"] == 409)
    prs = []

    def add(number: int, title: str, verify: int, undo: int, **fields) -> None:
        pr = copy.deepcopy(base)
        pr.update(number=number, title=title, head=f"{number:040x}", url=f"https://github.com/acme/ledger-app/pull/{number}",
                  scores={"impact": 2, "confidence": 2, "verify": verify, "undo": undo},
                  size={"additions": number % 90 + 1, "deletions": number % 7, "files": number % 4 + 1}, checks="pass", conflict=False)
        pr.pop("sensitiveKind", None)
        pr.update(fields)
        prs.append(pr)

    # Written out of order on purpose: the page, not the round, decides the groups.
    for i in range(5):
        add(900 + i, f"Fleet change {i}", 3, 3, bucket="in-flight", owner="owned by repo-captain")
    prs[-1]["holdViolation"] = "ready with checks passing, no review:held"
    for i in range(4):
        add(700 + i, f"Bump passing package {i}", 1, 1, bucket="bot", owner="Dependabot")
    prs[-1]["sensitiveKind"] = "dependency lockfile"
    add(710, "Bump failing package", 1, 1, bucket="bot", owner="Dependabot", checks="fail")
    add(711, "Bump conflicting package", 1, 1, bucket="bot", owner="Renovate", conflict="true")
    for i in range(8):
        add(500 + i, f"Routine change {i}", 1, 1 + i % 2)
    prs[-1]["checks"] = "FAILURE"  # not the contract's word: the page must still count it as broken
    add(300, "Held by its label alone", 1, 1, bucket="held", owner="owned by repo-captain")
    for i in range(10):
        add(100 + i, f"Risky change {i}", 2 + i % 2, 3, bucket="held" if i % 2 else "unclassified")
    prs[-1]["conflict"] = True
    add(200, "Score missing", 1, 1)
    prs[-1]["scores"].pop("undo")

    def rows(start: int, count: int, key: str, text: str) -> list:
        return [{"repo": "acme/cli-kit", "number": start + i, "url": f"https://github.com/acme/cli-kit/pull/{start + i}",
                 "title": f"Merged change {start + i}", key: text} for i in range(count)]

    round_data = copy.deepcopy(original)
    round_data["prs"] = prs
    round_data["across"] = []
    round_data["scope"] = f"{len(prs)} open pull requests across acme"
    round_data["merged"] = {"window": "The last 7 days.",
                            "without": rows(2000, without, "reason", "Merged with no Verdict and no label."),
                            "autoMerged": rows(3000, auto_merged, "reason", "Routine, V=1 U=1."),
                            "changedAfter": rows(4000, 2, "summary", "One commit after your merge Verdict.")}
    return round_data


def check_large_round(original: dict, scratch: Path) -> None:
    variant = large_round(original)
    quoted = 'say "done" when\nfixed | then run a | b'
    page, _ = fill(json.dumps(variant, indent=2, ensure_ascii=False) + "\n", scratch)
    actions = [
        ["jump", 2],                                    # 1 the summary notice's link
        ["notes", "Risky change 1", quoted],            # 2 a note with no Verdict
        ["verdict", "Risky change 1", "changes"],       # 3
        ["copy", "bar"],                                # 4
        ["notes", "Risky change 1", "plain"],           # 5 an edit after copying
        ["tab", "bots"],                                # 6
        ["broken", True],                               # 7
        ["tab", "flight"],                              # 8 nothing in flight is broken
        ["broken", False],                              # 9
        ["key", "m"],                                   # 10 no card spans the reading line
        ["span", "Fleet change 4"],                     # 11
        ["key", "m", True],                             # 12 a held-down key
        ["key", "m"],                                   # 13
        ["tab", "all"],                                 # 14
        ["copy", "box"],                                # 15
        ["tab", "bots"],                                # 16 the in-flight card that spans the line is now hidden
        ["span", "Bump passing package 3"],             # 17
        ["key", "d"],                                   # 18
        ["key", "x", False, "Bump passing package 3"],  # 19 typed into a note
        ["key", "x", False, "toggle"],                  # 20 focus left on the broken-only checkbox
        ["key", "k"],                                   # 21 from the last bot to the one before it
        ["key", "n"],                                   # 22 the next undecided bot, wrapping past the decided one
        ["tab", "ready"],                               # 23
        ["broken", True],                               # 24 two broken cards, eight ranks apart
        ["key", "k"],                                   # 25
    ]
    steps = render(page, scratch, actions)
    if steps is None:
        return
    first = steps[0]
    titles = lambda cls, step=first: [r["title"] for r in group(step, cls)["rows"]]  # noqa: E731
    total = len(variant["prs"])

    # Four groups, in order, each pull request in exactly one.
    check([g["cls"] for g in first["groups"]] == ["over hold", "over under", "over bots", "over flight"],
          f"the Overview must draw Held, Under, Dependency bots, and In-flight in that order: {[g['cls'] for g in first['groups']]}")
    check(sum(len(g["rows"]) for g in first["groups"]) == total, "every open pull request must appear in exactly one group")
    held = titles("hold")
    check(held[:1] == ["Score missing"], f"a missing score must stay at the top of Held: {held[:2]}")
    check("Held by its label alone" in held, "a pull request in the held bucket must sit in Held whatever its scores")
    check(len(held) == 12 and len(titles("under")) == 8, f"Held and Under sizes: {len(held)}, {len(titles('under'))}")
    check(titles("bots")[:2] == ["Bump failing package", "Bump conflicting package"],
          f"broken and conflicting dependency bots must come before passing ones: {titles('bots')}")
    check(len(titles("flight")) == 5 and all(t.startswith("Fleet change") for t in titles("flight")),
          f"in-flight fleet pull requests must have their own group: {titles('flight')}")
    order = [b["title"].lstrip("0123456789") for b in first["blocks"]]
    check(order.index("Held by its label alone") < order.index("Fleet change 0"),
          "a review:held pull request at V x U 1 must come before an in-flight one at V x U 9")
    check([g["heading"] for g in first["groups"]] == ["Held for review (12)", "Under the hold line (8)", "Dependency bots (6)", "In-flight fleet pull requests (5)"],
          f"group headings with counts: {[g['heading'] for g in first['groups']]}")
    missing = next((r for r in group(first, "hold")["rows"] if r["title"] == "Score missing"), {})
    check(missing.get("vu") == "?", f"a missing factor keeps the ? badge: {missing.get('vu')}")
    check(next((b["driver"] for b in first["blocks"] if b["title"].endswith("Score missing")), "").startswith("Held because a score is missing."),
          "a missing score keeps its placement line")
    check("it carries review:held" in next((b["driver"] for b in first["blocks"] if b["title"].endswith("Held by its label alone")), ""),
          "a pull request held by its label alone must say so")
    drivers = {b["title"].lstrip("0123456789"): b["driver"] for b in first["blocks"]}
    check(drivers["Fleet change 0"].startswith("Meets a hold test: V × U 9."), f"an in-flight card must not claim a place on the hold line: {drivers['Fleet change 0']}")
    check(drivers["Bump passing package 3"].startswith("Meets a hold test: sensitive kind dependency lockfile."), f"a bot's card must name the hold test it meets: {drivers['Bump passing package 3']}")
    check(drivers["Bump passing package 0"].startswith("Meets no hold test, V × U 1."), f"a routine bot's card: {drivers['Bump passing package 0']}")
    check(all(("hold" in b["cls"].split()) == (b["title"].lstrip("0123456789") in held) for b in first["blocks"]), "only cards in the Held group take the held style")

    # Readiness, size, and the in-flight treatment, on the row and on the card.
    rows = {r["title"]: r for g in first["groups"] for r in g["rows"]}
    cards = {b["title"].lstrip("0123456789"): b for b in first["blocks"]}
    for name, where in (("row", rows), ("card", cards)):
        check("checks fail" in where["Bump failing package"]["chips"], f"a failing pull request's {name} must say checks fail")
        check("conflict" in where["Bump conflicting package"]["chips"], f"a conflicting pull request's {name} must say conflict")
        check(where["Bump passing package 0"]["chips"] in ([], ["V × U 1"]), f"a passing pull request's {name} shows no readiness chip: {where['Bump passing package 0']['chips']}")
        check("In flight · moving target" in where["Fleet change 0"]["chips"], f"an in-flight pull request's {name} must carry the badge")
        check(any(c.startswith("Hold violation") for c in where["Fleet change 4"]["chips"]), f"a hold violation must show on the {name}")
    check(rows["Routine change 7"]["chips"] == ["checks failure"], f"an unknown word for the checks must show and count as failing: {rows['Routine change 7']['chips']}")
    check(rows["Bump failing package"]["size"] == "+81 −3 · 3 files", f"an Overview row must show the diff's size: {rows['Bump failing package']['size']}")
    check(rows["Bump passing package 3"]["kind"] == "Sensitive kind: dependency lockfile", "a dependency bot keeps its sensitive-kind marker")
    flight = cards["Fleet change 0"]
    check("flight" in flight["cls"].split(), "an in-flight card must take the dashed in-flight border class")
    check(any("worker may still be updating" in x for x in flight["xnotes"]), f"an in-flight card must explain itself: {flight['xnotes']}")
    check("V × U 9" in flight["chips"], f"a card must carry its V x U beside the Verdict controls: {flight['chips']}")
    check(any(c.startswith("Sensitive kind") for c in cards["Bump passing package 3"]["chips"]), "a card must carry its sensitive kind beside the Verdict controls")
    check(not any("flight" in b["cls"].split() for t, b in cards.items() if not t.startswith("Fleet")), "only in-flight cards take the in-flight class")
    check(first["order"].index("key") < first["order"].index("over hold"), f"the V x U key must sit above the Overview rows: {first['order'][:6]}")

    # Bounded notices, the drawer, and the three merged lists.
    check(len(first["notices"]) == 3, f"52 merges without the operator must collapse to one notice beside the two changed ones: {len(first['notices'])}")
    summary = first["notices"][-1]
    check(summary["text"].startswith("52 pull requests merged without you") and summary["href"] == "#merged" and summary["sealed"],
          f"the summary notice must count the merges and link to #merged: {summary}")
    check(all(n["href"].startswith("#changed-") for n in first["notices"][:2]), "each changed-after-Verdict pull request keeps its own notice")
    check(first["order"].index("verdicts") < first["order"].index("merged") < first["order"].index("in-progress"),
          f"Your Verdicts must come before Merged recently: {first['order'][-4:]}")
    merged = first["merged"]
    check(merged["drawer"] is not None and merged["drawer"]["inside"] and merged["drawer"]["open"] is False, "a large merged section must start collapsed")
    check(merged["drawer"]["summaryHeadings"] == 0 and merged["headings"][:1] == ["h2"], "the drawer's summary must not hold a heading")
    check("114" in merged["drawer"]["summary"], f"the drawer's summary must say how many it holds: {merged['drawer']['summary']}")
    lists = {l["title"]: l for l in merged["lists"]}
    check([l["rows"] for l in merged["lists"]] == [2, 52, 60], f"merged lists: changed, without, auto-merged: {[(l['title'], l['rows']) for l in merged['lists']]}")
    check(lists.get("Auto-merged as routine", {}).get("sealed") == 0, "routine auto-merges must not carry the orange seal")
    check(lists.get("Merged without you", {}).get("sealed") == 52 and lists.get("Changed after your Verdict", {}).get("sealed") == 2,
          "unapproved merges and changes after a Verdict keep the orange seal")
    check(lists.get("Changed after your Verdict", {}).get("ids") == ["changed-1", "changed-2"] and lists.get("Merged without you", {}).get("ids", [])[:1] == ["merged-1"],
          "merged rows must keep their ids for the notice links")
    check(steps[1]["merged"]["drawer"]["open"] is True, "following a notice to #merged must open the drawer first")

    # Notes: the hint, the normalization, and a line that still splits.
    card = lambda step: next(b for b in step["blocks"] if b["title"].endswith("Risky change 1"))  # noqa: E731
    check(card(first)["hint"] == {"text": "Pick a verdict to include this note", "hidden": True}, f"the note hint must exist and start hidden: {card(first)['hint']}")
    check(card(steps[2])["hint"]["hidden"] is False and steps[2]["box"]["value"] == "", "a note with no Verdict must show the hint and stay out of the Verdicts")
    check(card(steps[3])["hint"]["hidden"] is True, "choosing a Verdict must clear the note hint")
    check("aria-describedby" in card(steps[2])["notes"] and "aria-describedby" not in card(steps[3])["notes"] and "aria-describedby" not in card(first)["notes"],
          "the notes field must be described by the hint only while the hint shows")
    line = steps[3]["box"]["value"]
    check('"' not in line and "\n" not in line, f"a copied Verdict line must hold no double quote and no newline: {line!r}")
    check(line.split(" | ", 2) == [f"acme/ledger-app#101 @ {101:040x}", "request changes", "say 'done' when fixed | then run a | b"],
          f"a note must survive splitting the line on its first two separators: {line.split(' | ', 2)}")

    # The copy controls.
    check(first["bar"]["copy"] == "Copy Verdicts (0)" and first["box"]["copy"] == "Copy Verdicts (0)", f"both copy buttons must show the count: {first['bar']['copy']!r}, {first['box']['copy']!r}")
    check(steps[3]["bar"]["copy"] == "Copy Verdicts (1)" and steps[3]["box"]["copy"] == "Copy Verdicts (1)", "the copy count must follow the Verdicts")
    check("this browser" in first["bar"]["cue"], f"the bar must say where choices are kept: {first['bar']['cue']!r}")
    check(steps[4]["clipboard"] == line and steps[4]["bar"]["cue"].startswith("Copied"), f"the bar's button must copy the Verdicts: {steps[4]['bar']['cue']!r}")
    check("single quotes" in steps[4]["box"]["status"], f"copying must say when quotes were changed: {steps[4]['box']['status']!r}")
    check("Copied" not in steps[5]["bar"]["cue"] and "Copied" not in steps[5]["box"]["status"], "an edit after copying must clear the stale Copied cue")
    check(steps[15]["clipboard"].count("\n") == 1 and "single quotes" not in steps[15]["box"]["status"],
          f"copying plain notes must not mention quotes: {steps[15]['box']['status']!r}")

    # Filters.
    tabs = {t["key"]: t for t in first["filters"]["tabs"]}
    check(list(tabs) == ["all", "ready", "bots", "flight"], f"filter tabs: {list(tabs)}")
    counts = {key: int(re.search(r"(\d+)\s*$", t["text"]).group(1)) for key, t in tabs.items() if re.search(r"\d+\s*$", t["text"])}
    check(counts == {"all": 31, "ready": 20, "bots": 6, "flight": 5} and counts.get("ready", 0) + counts.get("bots", 0) + counts.get("flight", 0) == counts.get("all"),
          f"the bucket tabs must be exclusive and sum to the total: {counts}")
    check(first["filters"]["broken"] == {"checked": False} and (first["filters"]["status"] or {}).get("live") == "polite", "the broken toggle and a polite filter status must exist")
    check(first["bar"]["href"] == "#pr-1" and "Next ↓" in first["bar"]["progress"], f"the bar must point at the first undecided pull request: {first['bar']}")
    bots = steps[6]
    shown = lambda step: [b["title"].lstrip("0123456789") for b in step["blocks"] if not b["hidden"]]  # noqa: E731
    check(len(shown(bots)) == 6 and all(t.startswith("Bump") for t in shown(bots)), f"the Bots tab must show only dependency bots: {shown(bots)}")
    check([g["hidden"] for g in bots["groups"]] == [True, True, False, True], "groups with nothing showing must hide")
    check(sum(not i["hidden"] for l in bots["rail"]["lists"] for i in l["items"]) == 6, "the rail must follow the filter")
    check(bots["bar"]["href"] == "#pr-21", f"Next must point at the first visible undecided pull request: {bots['bar']['href']}")
    check(bots["box"]["value"] != "", "a filter must not drop Verdicts already chosen on hidden pull requests")
    broken = steps[7]
    check(shown(broken) == ["Bump failing package", "Bump conflicting package"], f"Bots with the broken toggle: {shown(broken)}")
    check(group(broken, "bots")["heading"] == "Dependency bots (2 of 6)", f"a filtered group must count what shows: {group(broken, 'bots')['heading']}")
    check("2 of 31" in broken["filters"]["status"]["text"], f"the filter status must say how many show: {broken['filters']['status']['text']!r}")
    none = steps[8]
    check(shown(none) == [] and none["filters"]["empty"]["hidden"] is False and none["bar"]["href"] == "#verdicts",
          f"an empty filter must say so and point Next at the Verdicts: {none['filters']['empty']}, {none['bar']['href']}")
    check(first["filters"]["empty"]["hidden"] is True, "the empty-filter message must start hidden")

    # Keys act on visible cards only, and a Verdict key needs a card on the reading line.
    check(steps[10]["box"]["value"] == steps[9]["box"]["value"], "m must set nothing when no card spans the reading line")
    check(steps[12]["box"]["value"] == steps[9]["box"]["value"], "a held-down m must set nothing")
    check(f"acme/ledger-app#904 @ {904:040x} | merge | " in steps[13]["box"]["value"], f"m must merge the visible card on the reading line: {steps[13]['box']['value']!r}")
    check(steps[13]["bar"]["copy"] == "Copy Verdicts (2)", "a key-set Verdict must count")
    check(len(shown(steps[14])) == 31, "the All tab must bring every pull request back")
    check(steps[19]["box"]["value"] == steps[18]["box"]["value"], "a key typed into a note must set no Verdict")
    check(f"#703 @ {703:040x} | not applicable | " in steps[20]["box"]["value"], f"keys must still work with focus on the broken-only checkbox: {steps[20]['box']['value']!r}")
    check(steps[21]["scrolled"] == "pr-25" and steps[22]["scrolled"] == "pr-21",
          f"k and n must move among visible cards only: {steps[21]['scrolled']}, {steps[22]['scrolled']}")
    check(shown(steps[24]) == ["Risky change 9", "Routine change 7"] and steps[25]["scrolled"] == cards["Risky change 9"]["id"],
          f"k must skip the cards the filter hides: {shown(steps[24])}, {steps[25]['scrolled']}")
    check(f"acme/ledger-app#703 @ {703:040x} | defer | " in steps[18]["box"]["value"] and f"#904 @ {904:040x} | merge | " in steps[18]["box"]["value"],
          f"a Verdict key must act on a visible card, never on one the filter hides: {steps[18]['box']['value']!r}")

    # Semantics.
    check(first["marksHidden"] and first["markCount"] > 0, "decorative seals, rings, and route dots must be hidden from assistive technology")
    check("h2" not in first["rail"]["tags"] and "h1" not in first["rail"]["tags"], f"the rail must not hold headings above the page's h1: {first['rail']['tags']}")
    check(len(first["rail"]["lists"]) == 4 and all(l["labelled"] for l in first["rail"]["lists"]), "each rail list must be labelled by its group name")


def check_notice_threshold(original: dict, scratch: Path) -> None:
    variant = large_round(original, without=5, auto_merged=0)
    page, _ = fill(json.dumps(variant, indent=2, ensure_ascii=False) + "\n", scratch)
    steps = render(page, scratch, [["jump", 6]])
    if steps is None:
        return
    first, jumped = steps
    check(len(first["notices"]) == 7 and all(n["href"].startswith(("#changed-", "#merged-")) for n in first["notices"]),
          f"five merges without the operator must each keep a notice: {len(first['notices'])}")
    drawer = (first["merged"] or {}).get("drawer") or {}
    check(drawer.get("open") is False, "seven merged pull requests must start collapsed")
    check(((jumped["merged"] or {}).get("drawer") or {}).get("open") is True, "following a notice to a merged row must open the drawer first")
    check(len((first["merged"] or {}).get("lists", [])) == 2, "an empty auto-merged list must not be drawn")


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
    for extra in (lambda scratch: check_incomplete_scores(raw, scratch), lambda scratch: check_large_round(original, scratch),
                  lambda scratch: check_notice_threshold(original, scratch)):
        with tempfile.TemporaryDirectory() as scratch:
            try:
                extra(Path(scratch))
            except (KeyError, IndexError, TypeError, StopIteration, AttributeError, ValueError) as error:
                failures.append(f"a rendered round is missing what a check reads: {type(error).__name__}: {error}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("reviewing-prs page template: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
