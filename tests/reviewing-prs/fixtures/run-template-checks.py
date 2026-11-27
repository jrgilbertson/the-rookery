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
drawer, the filters, the copy controls, the verdict notes, the keyboard
shortcuts and their switch, the active card, the collapsed routine cards, and
what the browser keeps. Smaller rounds check a page with unreadable data, one
with no pull requests, and one with no dependency bot. It cannot tell whether
the page looks right; that takes a browser.
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
const seeded = JSON.parse(process.argv[4] || "{}");
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
      const kids = n && n.isFragment ? n.children.splice(0) : [typeof n === "string" ? text(n) : n];
      for (const kid of kids) { kid.parentNode = this; this.children.push(kid); }
    }
  }
  replaceChildren(...nodes) { this._text = null; this.children = []; this.append(...nodes); }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  getAttribute(k) { return k in this.attributes ? this.attributes[k] : null; }
  removeAttribute(k) { delete this.attributes[k]; }
  addEventListener(type, handler) { ((this.listeners ||= {})[type] ||= []).push(handler); }
  fire(type, event = {}) { return Promise.all(((this.listeners || {})[type] || []).map((handler) => handler(event))); }
  contains(other) { return walk(this).includes(other); }
  // Focus moves the way a browser moves it: the document hears focusin with the node as its target.
  focus() { focusedNode = this; for (const handler of document.listeners?.focusin ?? []) handler({ target: this }); }
  select() {} replaceWith() {}
  scrollIntoView() { scrolled = this.id; }
  // Enough of matches() and closest() for the page's guards: a list of tag names, each with an
  // optional class, the checkbox exclusion, or a bare [contenteditable].
  matches(selector) {
    return selector.split(",").some((raw) => {
      const [, tag, rest] = /^([a-z0-9]*)(.*)$/.exec(raw.trim());
      if (tag && tag !== this.tagName) return false;
      if (rest === "[contenteditable]") return "contenteditable" in this.attributes;
      if (rest === ':not([type="checkbox"])') return this.type !== "checkbox";
      if (rest.startsWith(".")) return this.classList.contains(rest.slice(1));
      return rest === "";
    });
  }
  closest(selector) {
    for (let node = this; node; node = node.parentNode) if (node.matches(selector)) return node;
    return null;
  }
  querySelector() { return null; } querySelectorAll() { return []; }
  getBoundingClientRect() { return this.rect || { top: 0, bottom: 0 }; }
  get offsetHeight() { return 56; }
}
const fixed = { "round-data": Object.assign(new Node("script"), { _text: data }) };
for (const [id, tag] of [["page", "main"], ["rail", "nav"], ["theme", "button"], ["bar", "header"], ["bar-note", "span"],
  ["bar-progress", "a"], ["bar-copy", "button"], ["bar-cue", "span"], ["shortcuts", "button"], ["shortcut-help-toggle", "button"],
  ["shortcut-help", "div"], ["announcer", "div"]]) fixed[id] = Object.assign(new Node(tag), { id });
// The template ships the help panel closed.
fixed["shortcut-help"].hidden = true;
const store = new Map(Object.entries(seeded));
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
const window = { matchMedia: () => ({ matches: false, addEventListener() {} }), localStorage, innerHeight: 800, location: { hash: "" },
  requestAnimationFrame: (callback) => callback() };
window.addEventListener = heard(window);
let clipboard = null, scrolled = null, focusedNode = null, clipboardFails = false;
const writeText = async (value) => { if (clipboardFails) throw new Error("denied"); clipboard = value; };
vm.runInNewContext(code, { window, document, navigator: { clipboard: { writeText } },
  URL, console, Element: Node, setTimeout: () => 0, clearTimeout() {} });

const has = (n, cls) => (n.className || "").split(" ").includes(cls);
const within = (root, cls) => walk(root).filter((n) => has(n, cls));
const one = (root, cls) => within(root, cls)[0] || null;
// What a sighted reader sees: text outside the visually hidden labels.
const seen = (n) => n.isText ? n.textContent : has(n, "vh") ? "" : n._text !== null ? n._text : n.children.map(seen).join("");
const chips = (root) => within(root, "chip").filter((n) => !n.hidden).map(seen);
const hiddenIds = () => Object.keys(fixed).filter((id) => fixed[id].hidden);
const snap = () => {
  const all = walk(fixed.page);
  const merged = all.find((n) => n.id === "merged");
  const drawer = all.find((n) => n.tagName === "details");
  const verdicts = all.find((n) => n.id === "verdicts");
  const empty = all.find((n) => n.id === "filter-empty");
  const marks = all.concat(walk(fixed.rail)).filter((n) => has(n, "seal") || has(n, "ring") || has(n, "route-dot"));
  return {
    order: fixed.page.children.filter((n) => !n.isText).map((n) => n.id || n.className || n.tagName),
    headings: all.filter((n) => n.tagName === "h1").map((n) => n.textContent),
    alerts: all.filter((n) => n.attributes.role === "alert").map((n) => n.textContent),
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
        vuAttributes: { ...(one(row, "vu")?.attributes ?? {}) }, vuLabel: one(one(row, "vu")?.parentNode ?? row, "vh")?.textContent ?? null,
        chips: chips(row), size: one(row, "size")?.textContent ?? null,
      })),
    })),
    blocks: all.filter((n) => n.tagName === "article").map((a) => ({
      id: a.id, cls: a.className, hidden: a.hidden, hold: has(a, "hold"),
      title: walk(a).find((n) => n.tagName === "h2")?.textContent ?? "",
      driver: one(a, "driver")?.textContent ?? "",
      chips: chips(one(a, "block-meta") || new Node("x")), xnotes: within(a, "xnote").map((n) => n.textContent),
      sysnotes: within(a, "sysnote").map((n) => n.textContent), sections: within(a, "sec-title").map((n) => n.textContent),
      vuChip: { attributes: { ...(one(a, "vu-chip")?.attributes ?? {}) }, label: one(one(a, "vu-chip") || new Node("x"), "vh")?.textContent ?? null },
      active: has(a, "active"), collapsed: one(a, "block-body")?.hidden ?? null, controlsHidden: one(a, "verdict")?.hidden ?? null,
      toggle: one(a, "card-toggle") ? { ...one(a, "card-toggle").attributes } : null,
      badge: { text: one(a, "verdict-badge")?.textContent ?? null, hidden: one(a, "verdict-badge")?.hidden ?? null },
      // The parts a collapsed card must keep in view sit outside the two parts its toggle hides.
      keptOutside: ["rank", "block-meta", "card-factors", "verdict-badge"].every((cls) => one(a, cls)
        && !within(one(a, "block-body"), cls).length && !within(one(a, "verdict"), cls).length)
        && !walk(one(a, "block-body")).some((n) => n.tagName === "h2"),
      factors: within(a, "pill").map((p) => ({ three: has(p, "three"), shown: seen(p), label: one(p, "vh")?.textContent ?? null })),
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
    bar: { copy: fixed["bar-copy"].textContent, cue: fixed["bar-cue"].textContent, copyDisabled: fixed["bar-copy"].attributes["aria-disabled"] ?? null,
      progress: fixed["bar-progress"].textContent, href: fixed["bar-progress"].href ?? null,
      shortcuts: fixed.shortcuts.attributes["aria-pressed"], hidden: hiddenIds(),
      help: { hidden: fixed["shortcut-help"].hidden, expanded: fixed["shortcut-help-toggle"].attributes["aria-expanded"] ?? null } },
    box: !verdicts ? null : { copy: one(verdicts, "copy")?.textContent ?? null, value: walk(verdicts).find((n) => n.tagName === "textarea")?.value ?? null,
      copyDisabled: one(verdicts, "copy")?.attributes["aria-disabled"] ?? null, placeholder: walk(verdicts).find((n) => n.tagName === "textarea")?.placeholder ?? null,
      label: walk(verdicts).find((n) => n.tagName === "textarea")?.attributes["aria-label"] ?? null,
      status: one(verdicts, "copy-status")?.textContent ?? null },
    announced: fixed.announcer.textContent, focus: focusedNode ? focusedNode.id || focusedNode.tagName : null,
    theme: document.documentElement.dataset.theme ?? null, storage: Object.fromEntries(store),
    live: all.concat(walk(fixed.rail), Object.values(fixed)).filter((n) => n.attributes["aria-live"]).length,
    rail: { hidden: fixed.rail.hidden, links: within(fixed.rail, "r-links").flatMap((n) => n.children.map((a) => a.textContent)),
      current: walk(fixed.rail).filter((n) => n.attributes["aria-current"] === "true").map((n) => one(n, "r-title")?.textContent ?? ""),
      tags: [...new Set(walk(fixed.rail).map((n) => n.tagName))],
      lists: walk(fixed.rail).filter((n) => n.tagName === "ol").map((ol) => ({
        labelled: Boolean(ol.attributes["aria-labelledby"] && document.getElementById(ol.attributes["aria-labelledby"])),
        items: ol.children.map((li) => ({ hidden: li.hidden, text: li.textContent })) })) },
    filters: { tabs: all.filter((n) => n.tagName === "button" && n.dataset.filter).map((b) => ({
        key: b.dataset.filter, text: b.textContent, pressed: b.attributes["aria-pressed"] })),
      broken: all.find((n) => n.id === "filter-broken") ? { checked: all.find((n) => n.id === "filter-broken").checked } : null,
      status: all.find((n) => n.id === "filter-status") ? { text: all.find((n) => n.id === "filter-status").textContent } : null,
      empty: empty ? { hidden: empty.hidden, text: empty.textContent } : null },
    marksHidden: marks.every((n) => n.attributes["aria-hidden"] === "true"), markCount: marks.length,
    clipboard, scrolled, stored: store.size,
  };
};
const article = (title) => walk(fixed.page).find((n) => n.tagName === "article" && walk(n).find((h) => h.tagName === "h2")?.textContent.endsWith(title));
const titled = (root, cls, title) => walk(root).find((n) => n.tagName === "a" && one(n, cls)?.textContent === title || (has(n, cls) && n.tagName === "a" && n.textContent === title));
// A key lands on the notes field of a card, on the broken-only checkbox, on a bare element of a given tag, or on nothing.
const keyTarget = (where) => !where ? null : where === "toggle" ? walk(fixed.page).find((n) => n.id === "filter-broken")
  : where.startsWith("tag:") ? new Node(where.slice(4)) : one(article(where), "notes");
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
    if (what === "rect") article(a).rect = { top: b, bottom: c };
    if (what === "scroll") for (const handler of window.listeners?.scroll ?? []) handler({});
    if (what === "focus") walk(article(a)).find((n) => n.tagName === "h2").focus();
    if (what === "fold") await one(article(a), "card-toggle").fire("click");
    if (what === "rail") await titled(fixed.rail, "r-title", a).fire("click");
    if (what === "overview") await titled(fixed.page, "title", a).fire("click");
    if (what === "press") await fixed[a].fire("click");
    if (what === "clipboard") clipboardFails = a === "fail";
    if (what === "hash") { window.location.hash = "#" + a; for (const handler of window.listeners?.hashchange ?? []) handler({}); }
    if (what === "key") {
      for (const handler of document.listeners?.keydown ?? []) handler({ key: a, target: keyTarget(c), repeat: Boolean(b), preventDefault() {} });
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
    check(set(addresses) <= {"data:,", "#verdicts", "#page"}, f"the template loads or links something external: {addresses}")
    policy = re.search(r'Content-Security-Policy" content="([^"]*)"', text)
    check(policy is not None and "default-src 'none'" in policy.group(1) and "connect-src 'none'" in policy.group(1)
          and "script-src 'nonce-{{NONCE}}'" in policy.group(1), "the policy lost default-src 'none', connect-src 'none', or its nonce")
    for kept, why in (
        ('STORE = "reviewing-prs:"', "the browser-storage key prefix"),
        ('PREFS = "reviewing-prs-prefs:"', "the separate prefix that keeps the theme and the shortcuts switch from expiring"),
        ("30 * 24 * 60 * 60 * 1000", "the 30-day expiry of stored verdicts"),
        ("verdictBox.value && verdictBox.value !== lastCopied", "the guard against leaving with uncopied verdicts"),
        ('url.protocol === "https:"', "the https-only check on links"),
        ('anchor.rel = "noopener noreferrer"', "noopener noreferrer on outside links"),
        ("JSON.parse(document.getElementById(\"round-data\").textContent)", "the guarded read of the round's data"),
        ('event.repeat && ["m", "c", "d", "x"].includes(event.key)', "the held-key guard on verdict keys"),
        ("return spansLine(here) ? here : null;", "the reading-line guard on the active card"),
        ('window.addEventListener("scroll"', "the scroll listener that keeps the active card current"),
        ("@media (prefers-reduced-motion: reduce)", "a reduced-motion rule"),
        ("[hidden] { display: none !important; }", "the rule that lets a filter hide rows and cards that set their own display"),
        ('<div class="vh" id="announcer" role="status" aria-live="polite"></div>', "the one visually hidden, polite announcer"),
        ('id="bar-copy"', "the sticky bar's Copy verdicts button"),
        ('<button type="button" class="ctl" id="shortcuts" aria-pressed="true">', "the keyboard shortcuts switch, a pressed button that starts on"),
        ('id="shortcut-help-toggle" aria-expanded="false" aria-controls="shortcut-help"', "the ? button that discloses the shortcut help"),
        ('<main id="page" tabindex="-1">', "a main region the skip link can move focus to"),
        ("--control-border: light-dark(#7C87A0, #686E7A);", "the Control Border token for both papers"),
        ("@media (min-width: 1320px)", "the rail's breakpoint, wide enough to keep laptop titles readable"),
    ):
        check(kept in text, f"the template lost {why}")
    check("box-shadow" not in text, "the template casts a shadow, which working pages forbid")
    check(text.count("aria-live") == 1, f"the page must have exactly one live region: {text.count('aria-live')}")
    check(0 <= text.find('<a class="skip" href="#page">') < text.find('class="rail"'), "the skip link to #page must come before the rail")
    help_panel = re.search(r'<div class="help" id="shortcut-help"[^>]*\bhidden>(.*?)</div>', text, re.S)
    check(help_panel is not None and all(f"<kbd>{key}</kbd>" in help_panel.group(1) for key in "jknmcdx")
          and all(f"<dt>{word}</dt><dd>" in help_panel.group(1) for word in ("Merge", "Request changes", "Defer", "Not applicable")),
          "the shortcut help must start hidden, list every key, and explain every verdict")
    check_help_key(text, help_panel.group(1) if help_panel else "")
    check('role="dialog"' not in text and "showModal" not in text and "<dialog" not in text, "the shortcut help must stay non-modal")
    # Every control the page draws takes the Control Border; the hairline is for sheets and dividers.
    for selector in (".ctl", ".flt", ".seg", ".notes", ".card-toggle", ".drawer summary", ".verdicts textarea", ".skip"):
        rule = re.search(r"(?m)^" + re.escape(selector) + r" \{[^}]*\}", text)
        check(rule is not None and "solid var(--control-border)" in rule.group(0), f"{selector} must be edged in the Control Border")
    check(text.count("--paper:") == 1 and text.count("#14161B") == 1, "Night Paper must be stated once, not once per way of asking for it")
    check(0 <= text.find("@media (max-width: 560px)") < text.find("@media (max-width: 320px)"), "the 560px rules must come before the 320px ones they are narrowed by")
    check(not re.search(r"\.vu-chip \{[^}]*999px", text), "the V x U chip takes the 2px corner, not a pill")
    check(re.search(r"(?m)^  \.rail a \{[^}]*min-height: 36px", text) is not None, "a rail link must be at least 36px tall")
    check(re.search(r"(?m)^\.ctl \{[^}]*min-height: 36px", text) is not None
          and re.search(r"\.ctl, [^{]*\{ min-height: 44px; \}", text) is not None, "bar controls must be 36px tall, and 44px on a narrow screen")
    shouted = re.findall(r"[a-z,:] Verdicts?\b", text)
    check(not shouted, f"the interface writes verdict in lower case inside a sentence: {shouted[:3]}")
    check(not re.search(r"\[tabindex=\"-1\"\]:focus\s*\{\s*outline:\s*none", text),
          "a heading focused from the keyboard must keep its focus ring")
    for selector in (".rank", ".vu", ".bar strong", "h1"):
        rule = re.search(r"(?m)^" + re.escape(selector) + r" \{[^}]*font: [^;]*? ([0-9.]+)rem[^;]*var\(--display\)", text)
        check(rule is not None and float(rule.group(1)) >= 1, f"{selector} must set Didot at 1rem or larger")
    for rule in re.findall(r"[^{}]*\{[^}]*var\(--display\)[^}]*\}", text):
        size = re.search(r"font: [^;]*? ([0-9.]+)rem", rule)
        check(size is None or float(size.group(1)) >= 1, f"Didot is set under 1rem: {rule.strip()[:60]}")


def check_help_key(text: str, panel: str) -> None:
    """The ? panel also explains the page's own marks: the Described? column, the scores, orange, and the groups."""
    terms = {term: (cls, mark) for cls, mark, term in re.findall(r'<dt(?: class="([a-z]+)")?>(?:<span class="([a-z-]+)" aria-hidden="true"></span>)?([^<]+)</dt><dd>[^<]+</dd>', panel)}
    wanted = {
        "Yes": ("", ""), "No": ("flag", "seal"), "Unclear": ("flag", "seal"), "unchanged": ("quiet", ""),
        "I · impact": ("", ""), "C · confidence": ("", ""), "V · verify": ("", ""), "U · undo": ("", ""), "V × U": ("", ""), "Leverage": ("", ""),
        "U = 3": ("", ""), "Hold violation": ("", ""), "Sensitive kind": ("", ""), "Changed after your verdict": ("", ""),
        "Held for review": ("", "seal"), "Under the hold line": ("", "ring"), "Dependency bots": ("", "ring"), "In flight": ("", "route-dot"),
    }
    for term, drawn in wanted.items():
        check(terms.get(term) == drawn, f"the help must explain {term!r} and draw it as the page does, {drawn}: {terms.get(term)}")
    for heading in ("The Described? column", "Scores", "Orange marks what needs you", "Groups"):
        check(re.search(r'<h2 class="sec-title[a-z ]*">(?:<span class="seal" aria-hidden="true"></span>)?' + re.escape(heading) + "</h2>", panel) is not None,
              f"the help must head a part of its key {heading!r}")
    check('<h2 class="sec-title flag"><span class="seal" aria-hidden="true"></span>Orange marks' in panel
          and re.search(r"(?m)^\.help \.flag \{ color: var\(--signal-ink\); \}", text) is not None,
          "the help must set the words beside its orange seals in Signal Ink")
    check(len(re.findall(r'class="seal"', panel)) == 4, f"the help keeps orange scarce, one seal for each thing the page seals: {len(re.findall(r'class=.seal.', panel))}")
    check("3 or more" in panel and "(I × C) ÷ (V × U)" in panel, "the help must state the hold line and the leverage formula")
    # The key names what the script draws, so a renamed group, chip, or cell cannot leave the key behind.
    script = text.split('<script nonce="{{NONCE}}">', 1)[-1]
    for drawn in ('name: "Held for review"', 'name: "Under the hold line"', 'name: "Dependency bots"', '"In flight"', '"Hold violation: "',
                  '"Sensitive kind: "', '"Changed after your verdict"', '"Merged without you"', 'unchanged: "unchanged"', '"Unclear"', 'yes: "Yes", no: "No"',
                  '"Described?"', '"V × U"', '"leverage"', '["impact", true], ["confidence", false], ["verify", true], ["undo", true]', "product >= 3",
                  '"If it is wrong · a revert does not undo it"'):
        check(drawn in script, f"the help explains a mark the script no longer draws this way: {drawn}")
    check('aria-label="Help: keyboard shortcuts, verdicts, and what the marks on this page mean">?</button>' in text
          and '<div class="help" id="shortcut-help" role="region" aria-label="Help: keyboard shortcuts, verdicts, and page marks" tabindex="0" hidden>' in text,
          "the ? button and its region must say the help covers shortcuts, verdicts, and the page's marks, and the region must take focus so the keyboard can scroll it")
    check(panel.count("<section>") == 3 and panel.count("</section>") == 3 and "<div" not in panel,
          "the help is three sections, and holds no div that would end the panel early for these checks")
    check(re.search(r"@media \(min-width: 1200px\) \{\s*\.help \{ display: grid; grid-template-columns: repeat\(3, minmax\(0, 1fr\)\);", text) is not None,
          "the help must set its three parts side by side on a wide screen")
    check(re.search(r"(?m)^\.help \{[^}]*max-height: calc\(100vh - var\(--bar-h, 60px\) - 16px\); overflow-y: auto;", text) is not None,
          "the help must scroll inside itself when it is taller than the window")


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


def render(page: str, scratch: Path, actions: list | None = None, stored: dict | None = None) -> list | None:
    node = shutil.which("node")
    if node is None:
        failures.append("node is required to run the page's script")
        return None
    (scratch / "render.js").write_text(RENDER)
    (scratch / "page.html").write_text(page)
    result = subprocess.run([node, str(scratch / "render.js"), str(scratch / "page.html"), json.dumps(actions or []), json.dumps(stored or {})],
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
    bots = [number.get(r["title"]) for r in group(rendered, "bots")["rows"]]
    check(held == [418, 421, 131, 436, 432],
          f"held group order, highest V x U first, ties by leverage (#436 at 2.00 before #432 at 1.33): {held}")
    check(under == [134, 409], f"under-the-line group order: {under}")
    check(bots == [405], f"the dependency bot must have its own group: {bots}")
    check("sensitive kind" in group(rendered, "hold")["subtitle"], "the held group's subtitle does not mention sensitive kinds")
    check([g["cls"] for g in rendered["groups"]] == ["over hold", "over under", "over bots"],
          f"a round with a dependency bot and no in-flight pull request must draw three groups: {[g['cls'] for g in rendered['groups']]}")
    # The sample exercises the filters: a bot splits the tabs and a conflict brings the broken-only toggle.
    check([t["key"] for t in rendered["filters"]["tabs"]] == ["all", "ready", "bots", "flight"] and rendered["filters"]["broken"] == {"checked": False},
          f"the sample must draw the filter tabs and the broken-only toggle: {rendered['filters']}")
    kinds = {number.get(r["title"]): r["kind"] for g in rendered["groups"] for r in g["rows"]}
    check("dependency lockfile" in (kinds.get(405) or ""), f"#405's overview row does not name its sensitive kind: {kinds.get(405)}")
    check("money" in (kinds.get(421) or ""), f"#421's overview row does not name its sensitive kind: {kinds.get(421)}")
    check(kinds.get(418) is None, "a pull request with no sensitive kind shows one")
    blocks = {number.get(next((t for t in number if b["title"].endswith(t)), None)): b for b in rendered["blocks"]}
    lockfile = blocks.get(405, {})
    check(lockfile.get("driver", "").startswith("Meets a hold test: sensitive kind dependency lockfile."),
          f"#405's block does not name the hold test it meets: {lockfile.get('driver')}")
    check(lockfile.get("collapsed") is False and lockfile.get("toggle") is None, "a dependency bot that meets a hold test must not be collapsible")
    check(blocks.get(134, {}).get("collapsed") is True and blocks.get(409, {}).get("collapsed") is True, "routine cards under the hold line must start collapsed")
    check(all(blocks.get(n, {}).get("collapsed") is False for n in held), "a held card must never start collapsed")
    check("Over the hold line, V × U 6, and it touches a sensitive kind: money." in blocks.get(421, {}).get("driver", ""),
          f"#421's block does not name its sensitive kind: {blocks.get(421, {}).get('driver')}")
    check(blocks.get(134, {}).get("driver", "").startswith("Under the hold line, V × U 1."), "#134's block is not under the hold line")
    first = next(pr for pr in original["prs"] if pr["number"] == 418)
    check(chosen["box"]["value"] == f"{first.get('repo')}#{first.get('number')} @ {first.get('head')} | not applicable | ",
          f"choosing Not applicable must build its verdict line: {chosen['box']['value']!r}")
    # A round with pull requests and no verdict yet says so, and stops saying so once one is chosen.
    check(rendered["bar"]["copyDisabled"] == "true" and rendered["box"]["copyDisabled"] == "true" and "No verdicts chosen yet" in rendered["box"]["placeholder"],
          f"with no verdict chosen the copy buttons must read as unavailable and the box must say why: {rendered['bar']['copyDisabled']}, {rendered['box']['placeholder']!r}")
    check(chosen["bar"]["copyDisabled"] == "false" and chosen["box"]["copyDisabled"] == "false", "a chosen verdict must make the copy buttons available")
    check(rendered["bar"]["hidden"] == ["shortcut-help"], f"a round with pull requests shows every bar control, with the help closed: {rendered['bar']['hidden']}")
    # A small round stays legible: each merge has its own notice and the merged lists are open.
    notices = [n["text"] for n in rendered["notices"]]
    check(any("#412 merged without you" in n for n in notices) and any("#129 changed after your verdict" in n for n in notices),
          f"a small round must keep one notice per merged pull request: {notices}")
    drawer = (rendered["merged"] or {}).get("drawer") or {}
    check(drawer.get("open") is True, "a small round must show its merged lists open")
    check(rendered["stored"] == 0 and chosen["stored"] == 1, "a chosen verdict must be kept in browser storage, keyed to the reviewed head")
    for b in rendered["blocks"]:
        check(b["github"] is not None and b["github"]["href"].startswith("https://github.com/") and b["github"]["rel"] == "noopener noreferrer",
              f"{b['title']!r} lost its safe Open on GitHub link: {b['github']}")
        check(b["seg"].get("role") == "group" and b["seg"].get("aria-label", "").startswith("Verdict for "), f"{b['title']!r} lost its verdict group label")
        check(b["notes"].get("aria-label", "").startswith("Notes for "), f"{b['title']!r} lost its notes label")
        # The V x U figure is drawn for the eye and named in words beside it, never with a label on an element that has no role.
        check("aria-label" not in b["vuChip"]["attributes"] and (b["vuChip"]["label"] or "").startswith("Verification effort times undo cost: "),
              f"{b['title']!r}: the V x U chip must carry a visually hidden label, not aria-label: {b['vuChip']}")
        check(len(b["factors"]) == 5 and all(f["label"] for f in b["factors"]), f"{b['title']!r} must show five labelled factor pills: {b['factors']}")
        check(b["keptOutside"], f"{b['title']!r}: the title, rank, chips, factors, and verdict badge must stay outside what the toggle hides")
    for g in rendered["groups"]:
        for r in g["rows"]:
            check(r["vuAttributes"].get("aria-hidden") == "true" and "aria-label" not in r["vuAttributes"]
                  and (r["vuLabel"] or "").startswith("Verification effort times undo cost: "), f"{r['title']!r}: the Overview's V x U figure must be hidden and named beside it")
    money = blocks.get(421, {}).get("factors", [])
    check([f["shown"] for f in money] == ["impact 2", "confidence 2", "verify 2", "undo 3", "leverage 0.67"] and [f["three"] for f in money] == [False, False, False, True, False],
          f"#421's factor pills must show each factor and highlight the three: {money}")
    check(money and money[3]["label"].startswith("Undo cost 3 of 3"), f"a factor pill's hidden label must name its factor: {money[3:4]}")
    check(rendered["box"]["label"] == "Chosen verdicts, one line per pull request", "the verdicts box lost its label")
    check(rendered["live"] == 0 and rendered["announced"] == "", "the page's script must add no live region of its own and say nothing on load")


def check_two_group_round(raw: str, scratch: Path) -> None:
    """Without a dependency bot the Overview draws two groups and no bucket tabs."""
    variant = json.loads(raw)
    for pr in variant["prs"]:
        pr.pop("bucket", None)
    page, _ = fill(json.dumps(variant, indent=2, ensure_ascii=False) + "\n", scratch)
    steps = render(page, scratch)
    if steps is None:
        return
    rendered = steps[0]
    number = {pr["title"]: pr["number"] for pr in variant["prs"]}
    check([g["cls"] for g in rendered["groups"]] == ["over hold", "over under"],
          f"a round with no dependency bot and no in-flight pull request must draw only two groups: {[g['cls'] for g in rendered['groups']]}")
    held = [number.get(r["title"]) for r in group(rendered, "hold")["rows"]]
    check(held == [418, 421, 131, 436, 432, 405], f"#405 must fall to Held for its lockfile, last at V x U 1: {held}")
    lockfile = next((b for b in rendered["blocks"] if b["title"].endswith("Bump vite from 6.3.1 to 6.3.2")), {})
    check(lockfile.get("hold") is True and lockfile.get("driver", "").startswith("Held for a sensitive kind, dependency lockfile, though V × U is 1."),
          f"#405's block must say why it is held: {lockfile.get('driver')}")
    check(rendered["filters"]["tabs"] == [] and rendered["filters"]["broken"] == {"checked": False},
          f"with one bucket there are no tabs to choose between, and the conflict still brings the broken-only toggle: {rendered['filters']}")


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
    prs[-6]["holdViolation"] = "merged past a hold last week"  # Routine change 2: under the line, but not routine
    add(300, "Held by its label alone", 1, 1, bucket="held", owner="owned by repo-captain", audience="operator")
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
                            "without": rows(2000, without, "reason", "Merged with no verdict and no label."),
                            "autoMerged": rows(3000, auto_merged, "reason", "Routine, V=1 U=1."),
                            "changedAfter": rows(4000, 2, "summary", "One commit after your merge verdict.")}
    return round_data


def check_large_round(original: dict, scratch: Path) -> None:
    variant = large_round(original)
    quoted = 'say "done" when\nfixed | then run a | b'
    page, _ = fill(json.dumps(variant, indent=2, ensure_ascii=False) + "\n", scratch)
    actions = [
        ["jump", 2],                                    # 1 the summary notice's link
        ["notes", "Risky change 1", quoted],            # 2 a note with no verdict
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
        ["hash", "pr-1"],                               # 26 Back to a card the filter hides
    ]
    # Later steps are named, so a check reads at[...] instead of counting.
    at: dict[str, int] = {}

    def then(name: str, *action) -> None:
        actions.append(list(action))
        at[name] = len(actions)

    quiet = "Routine change 6"   # collapsed, and last under the Ready tab, so it is the card on the reading line
    then("ready", "tab", "ready")
    then("span quiet", "span", quiet)
    then("m on collapsed", "key", "m")
    then("j opens", "key", "j")
    then("m on open", "key", "m")
    then("fold", "fold", quiet)
    then("m on folded", "key", "c")
    then("unfold", "fold", quiet)
    then("rail opens", "rail", "Routine change 4")
    then("overview opens", "overview", "Routine change 0")
    then("address opens", "hash", "pr-13")             # Routine change 1, first under the hold line
    then("j while choosing", "key", "j", False, "tag:select")
    then("c in a textarea", "key", "c", False, "tag:textarea")
    then("c on a button", "key", "c", False, "tag:button")
    then("c on a link", "key", "c", False, "tag:a")
    then("c on a summary", "key", "c", False, "tag:summary")
    then("j on a button", "key", "j", False, "tag:button")
    then("switch off", "press", "shortcuts")
    then("c while off", "key", "c")
    then("j while off", "key", "k")
    then("switch on", "press", "shortcuts")
    then("c while on", "key", "c")
    then("held d", "key", "d", True)
    then("place focused", "rect", "Routine change 0", 60, 200)
    then("focus", "focus", "Routine change 0")
    then("d on focused", "key", "d")
    then("scroll away", "rect", "Routine change 0", -500, -10)
    then("scrolled", "scroll")
    then("d on the line", "key", "d")
    then("help", "press", "shortcut-help-toggle")
    then("escape", "key", "Escape")
    then("theme", "press", "theme")
    then("bots", "tab", "bots")
    then("broken bots", "broken", True)
    then("decide one", "verdict", "Bump failing package", "defer")
    then("progress opens", "press", "bar-progress")    # Next now points at the conflicting bot, still collapsed
    then("decide both", "verdict", "Bump conflicting package", "defer")
    then("n when done", "key", "n")
    then("back up", "key", "k")
    then("clipboard off", "clipboard", "fail")
    then("copy fails", "copy", "bar")
    steps = render(page, scratch, actions)
    if steps is None:
        return
    first = steps[0]
    step = lambda name: steps[at[name]]  # noqa: E731
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
    check("by a review:held label or a Fleet: hold receipt" in next((b["driver"] for b in first["blocks"] if b["title"].endswith("Held by its label alone")), ""),
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
    check(any("worker may still be updating" in x for x in flight["sysnotes"]) and not flight["xnotes"],
          f"an in-flight card must explain itself in the page's own voice, not on Dispatch Paper: {flight['sysnotes']}, {flight['xnotes']}")
    check("V × U 9" in flight["chips"], f"a card must carry its V x U beside the verdict controls: {flight['chips']}")
    check(any(c.startswith("Sensitive kind") for c in cards["Bump passing package 3"]["chips"]), "a card must carry its sensitive kind beside the verdict controls")
    check(cards["Held by its label alone"]["sections"][:1] == ["What is different for an operator"] and cards["Fleet change 0"]["sections"][:1] == ["What is different for a customer"],
          f"the audience takes a or an by its first sound: {cards['Held by its label alone']['sections'][:1]}, {cards['Fleet change 0']['sections'][:1]}")
    check(not any("flight" in b["cls"].split() for t, b in cards.items() if not t.startswith("Fleet")), "only in-flight cards take the in-flight class")
    check(first["order"].index("key") < first["order"].index("over hold"), f"the V x U key must sit above the Overview rows: {first['order'][:6]}")

    # Bounded notices, the drawer, and the three merged lists.
    check(len(first["notices"]) == 3, f"52 merges without the operator must collapse to one notice beside the two changed ones: {len(first['notices'])}")
    summary = first["notices"][-1]
    check(summary["text"].startswith("52 pull requests merged without you") and summary["href"] == "#merged" and summary["sealed"],
          f"the summary notice must count the merges and link to #merged: {summary}")
    check(all(n["href"].startswith("#changed-") for n in first["notices"][:2]), "each changed-after-verdict pull request keeps its own notice")
    check(first["order"].index("verdicts") < first["order"].index("merged") < first["order"].index("in-progress"),
          f"Your verdicts must come before Merged recently: {first['order'][-4:]}")
    merged = first["merged"]
    check(merged["drawer"] is not None and merged["drawer"]["inside"] and merged["drawer"]["open"] is False, "a large merged section must start collapsed")
    check(merged["drawer"]["summaryHeadings"] == 0 and merged["headings"][:1] == ["h2"], "the drawer's summary must not hold a heading")
    check("114" in merged["drawer"]["summary"], f"the drawer's summary must say how many it holds: {merged['drawer']['summary']}")
    lists = {l["title"]: l for l in merged["lists"]}
    check([l["rows"] for l in merged["lists"]] == [2, 52, 60], f"merged lists: changed, without, auto-merged: {[(l['title'], l['rows']) for l in merged['lists']]}")
    check(lists.get("Auto-merged as routine", {}).get("sealed") == 0, "routine auto-merges must not carry the orange seal")
    check(lists.get("Merged without you", {}).get("sealed") == 52 and lists.get("Changed after your verdict", {}).get("sealed") == 2,
          "unapproved merges and changes after a verdict keep the orange seal")
    check(lists.get("Changed after your verdict", {}).get("ids") == ["changed-1", "changed-2"] and lists.get("Merged without you", {}).get("ids", [])[:1] == ["merged-1"],
          "merged rows must keep their ids for the notice links")
    check(steps[1]["merged"]["drawer"]["open"] is True, "following a notice to #merged must open the drawer first")

    # Notes: the hint, the normalization, and a line that still splits.
    card = lambda step: next(b for b in step["blocks"] if b["title"].endswith("Risky change 1"))  # noqa: E731
    check(card(first)["hint"] == {"text": "Pick a verdict to include this note", "hidden": True}, f"the note hint must exist and start hidden: {card(first)['hint']}")
    check(card(steps[2])["hint"]["hidden"] is False and steps[2]["box"]["value"] == "", "a note with no verdict must show the hint and stay out of the verdicts")
    check(card(steps[3])["hint"]["hidden"] is True, "choosing a verdict must clear the note hint")
    check("aria-describedby" in card(steps[2])["notes"] and "aria-describedby" not in card(steps[3])["notes"] and "aria-describedby" not in card(first)["notes"],
          "the notes field must be described by the hint only while the hint shows")
    line = steps[3]["box"]["value"]
    check('"' not in line and "\n" not in line, f"a copied verdict line must hold no double quote and no newline: {line!r}")
    check(line.split(" | ", 2) == [f"acme/ledger-app#101 @ {101:040x}", "request changes", "say 'done' when fixed | then run a | b"],
          f"a note must survive splitting the line on its first two separators: {line.split(' | ', 2)}")

    # The copy controls.
    check(first["bar"]["copy"] == "Copy verdicts (0)" and first["box"]["copy"] == "Copy verdicts (0)", f"both copy buttons must show the count: {first['bar']['copy']!r}, {first['box']['copy']!r}")
    check(steps[3]["bar"]["copy"] == "Copy verdicts (1)" and steps[3]["box"]["copy"] == "Copy verdicts (1)", "the copy count must follow the verdicts")
    check("this browser" in first["bar"]["cue"], f"the bar must say where choices are kept: {first['bar']['cue']!r}")
    check(steps[4]["clipboard"] == line and steps[4]["bar"]["cue"].startswith("Copied"), f"the bar's button must copy the verdicts: {steps[4]['bar']['cue']!r}")
    check(steps[4]["bar"]["copy"] == "Copied" and steps[4]["box"]["copy"] == "Copied", f"both copy buttons must flash Copied: {steps[4]['bar']['copy']!r}, {steps[4]['box']['copy']!r}")
    check(steps[4]["announced"].startswith("Copied."), f"copying must be announced: {steps[4]['announced']!r}")
    check(not any(line in value for value in steps[4]["storage"].values()), "what was last copied must stay in memory, never in browser storage")
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
    check(first["filters"]["broken"] == {"checked": False} and first["filters"]["status"] == {"text": ""}, "the broken toggle and a filter status must exist")
    check(steps[6]["announced"].startswith("Showing 6 of 31 pull requests.") and steps[14]["announced"].startswith("Showing all 31 pull requests."),
          f"a filter must announce what it leaves showing: {steps[6]['announced']!r}, {steps[14]['announced']!r}")
    check(all(s["live"] == 0 for s in steps), "the page's script must add no live region beside the announcer")
    check(first["bar"]["href"] == "#pr-1" and "Next ↓" in first["bar"]["progress"], f"the bar must point at the first undecided pull request: {first['bar']}")
    bots = steps[6]
    shown = lambda step: [b["title"].lstrip("0123456789") for b in step["blocks"] if not b["hidden"]]  # noqa: E731
    check(len(shown(bots)) == 6 and all(t.startswith("Bump") for t in shown(bots)), f"the Bots tab must show only dependency bots: {shown(bots)}")
    check([g["hidden"] for g in bots["groups"]] == [True, True, False, True], "groups with nothing showing must hide")
    check(sum(not i["hidden"] for l in bots["rail"]["lists"] for i in l["items"]) == 6, "the rail must follow the filter")
    check(bots["bar"]["href"] == "#pr-21", f"Next must point at the first visible undecided pull request: {bots['bar']['href']}")
    check(bots["box"]["value"] != "", "a filter must not drop verdicts already chosen on hidden pull requests")
    broken = steps[7]
    check(shown(broken) == ["Bump failing package", "Bump conflicting package"], f"Bots with the broken toggle: {shown(broken)}")
    check(group(broken, "bots")["heading"] == "Dependency bots (2 of 6)", f"a filtered group must count what shows: {group(broken, 'bots')['heading']}")
    check("2 of 31" in broken["filters"]["status"]["text"], f"the filter status must say how many show: {broken['filters']['status']['text']!r}")
    none = steps[8]
    check(shown(none) == [] and none["filters"]["empty"]["hidden"] is False and none["bar"]["href"] == "#verdicts",
          f"an empty filter must say so and point Next at the verdicts: {none['filters']['empty']}, {none['bar']['href']}")
    check(first["filters"]["empty"]["hidden"] is True, "the empty-filter message must start hidden")

    # Keys act on visible cards only, and a verdict key needs a card on the reading line.
    check(steps[10]["box"]["value"] == steps[9]["box"]["value"], "m must set nothing when no card spans the reading line")
    check(steps[12]["box"]["value"] == steps[9]["box"]["value"], "a held-down m must set nothing")
    check(f"acme/ledger-app#904 @ {904:040x} | merge | " in steps[13]["box"]["value"], f"m must merge the visible card on the reading line: {steps[13]['box']['value']!r}")
    check(steps[13]["bar"]["copy"] == "Copy verdicts (2)", "a key-set verdict must count")
    check(steps[13]["announced"].startswith("Merge set for ledger-app #904."), f"a verdict set by key must be announced: {steps[13]['announced']!r}")
    # The stand-in does not scroll, so the mark is read after the next thing that redraws it, the All tab.
    active = [b["title"].lstrip("0123456789") for b in steps[14]["blocks"] if b["active"]]
    check(active == ["Fleet change 4"] and steps[14]["rail"]["current"] == ["Fleet change 4"],
          f"the card on the reading line must be the one active card, in the page and in the rail: {active}, {steps[14]['rail']['current']}")
    check(not any(b["active"] for b in steps[9]["blocks"]) and steps[9]["rail"]["current"] == [], "with no card on the reading line, none is active")
    check(len(shown(steps[14])) == 31, "the All tab must bring every pull request back")
    check(len(shown(steps[26])) == 31 and steps[26]["scrolled"] == "pr-1" and steps[26]["filters"]["broken"] == {"checked": False},
          f"an address that names a hidden card must clear the filter and go to it: {len(shown(steps[26]))}, {steps[26]['scrolled']}")
    check(steps[19]["box"]["value"] == steps[18]["box"]["value"], "a key typed into a note must set no verdict")
    check(f"#703 @ {703:040x} | not applicable | " in steps[20]["box"]["value"], f"keys must still work with focus on the broken-only checkbox: {steps[20]['box']['value']!r}")
    check(steps[21]["scrolled"] == "pr-25" and steps[22]["scrolled"] == "pr-21",
          f"k and n must move among visible cards only: {steps[21]['scrolled']}, {steps[22]['scrolled']}")
    check(shown(steps[24]) == ["Risky change 9", "Routine change 7"] and steps[25]["scrolled"] == cards["Risky change 9"]["id"],
          f"k must skip the cards the filter hides: {shown(steps[24])}, {steps[25]['scrolled']}")
    check(f"acme/ledger-app#703 @ {703:040x} | defer | " in steps[18]["box"]["value"] and f"#904 @ {904:040x} | merge | " in steps[18]["box"]["value"],
          f"a verdict key must act on a visible card, never on one the filter hides: {steps[18]['box']['value']!r}")

    # Routine cards start collapsed, and every way to one opens it.
    folded = sorted(t for t, b in cards.items() if b["collapsed"])
    routine = sorted([f"Routine change {i}" for i in range(8) if i != 2] + [f"Bump passing package {i}" for i in range(3)]
                     + ["Bump failing package", "Bump conflicting package"])
    check(folded == routine, f"only cards under the hold line or from a dependency bot, with no hold and no violation, start collapsed: {folded}")
    check(all(b["controlsHidden"] and b["toggle"].get("aria-expanded") == "false" and b["toggle"].get("aria-controls") == f"{b['id']}-verdict {b['id']}-body"
              for b in cards.values() if b["collapsed"]), "a collapsed card hides its verdict controls behind a toggle that names what it opens")
    check(all(b["toggle"] is None for t, b in cards.items() if t not in routine), "a card that is held, in flight, or carries a violation has no toggle")
    card_at = lambda name, title=quiet: next(b for b in step(name)["blocks"] if b["title"].endswith(title))  # noqa: E731
    chosen_at = lambda name: step(name)["box"]["value"]  # noqa: E731
    check(chosen_at("m on collapsed") == chosen_at("span quiet") and card_at("m on collapsed")["collapsed"] is True, "m must set nothing on a collapsed card")
    check(card_at("j opens")["collapsed"] is False and step("j opens")["scrolled"] == cards[quiet]["id"], "j onto a collapsed card must open it")
    check(f"#506 @ {506:040x} | merge | " in chosen_at("m on open"), f"m must act once the card is open: {chosen_at('m on open')!r}")
    check(card_at("fold")["collapsed"] is True and card_at("fold")["badge"] == {"text": "Your verdict: Merge", "hidden": False},
          f"a collapsed card must show the verdict it holds: {card_at('fold')['badge']}")
    check(chosen_at("m on folded") == chosen_at("fold"), "a verdict key must do nothing on a card folded again")
    check(card_at("unfold")["collapsed"] is False and card_at("unfold")["badge"]["hidden"] is True, "an open card shows its pressed button, not the badge")
    check(card_at("rail opens", "Routine change 4")["collapsed"] is False, "a rail link must open a collapsed card")
    check(card_at("overview opens", "Routine change 0")["collapsed"] is False, "an Overview title must open a collapsed card")
    check(cards["Routine change 1"]["id"] == "pr-13" and card_at("address opens", "Routine change 1")["collapsed"] is False
          and step("address opens")["scrolled"] == "pr-13", "an address that names a collapsed card must open it and go to it")
    check(step("decide one")["bar"]["href"] == "#" + cards["Bump conflicting package"]["id"] and card_at("decide one", "Bump conflicting package")["collapsed"] is True
          and card_at("progress opens", "Bump conflicting package")["collapsed"] is False, "the bar's Next link must open the collapsed card it points at")

    # Where a key lands decides what it may do.
    check(step("j while choosing")["scrolled"] == "pr-13", "no key may act while a list has the focus")
    for name in ("c in a textarea", "c on a button", "c on a link", "c on a summary"):
        check(chosen_at(name) == chosen_at("address opens"), f"a verdict key must do nothing: {name}")
    check(step("j on a button")["scrolled"] == cards[quiet]["id"], "j must still move with the focus on a button")

    # The switch turns every shortcut off, and the browser remembers it.
    off = step("switch off")
    check(first["bar"]["shortcuts"] == "true" and off["bar"]["shortcuts"] == "false" and off["storage"].get("reviewing-prs-prefs:shortcuts") == "off",
          f"the shortcuts switch must start on, turn off, and be remembered: {first['bar']['shortcuts']}, {off['bar']['shortcuts']}")
    check(chosen_at("c while off") == chosen_at("switch off") and step("j while off")["scrolled"] == step("switch off")["scrolled"],
          "with the switch off no shortcut may act")
    check(step("switch on")["bar"]["shortcuts"] == "true" and f"#506 @ {506:040x} | request changes | " in chosen_at("c while on"),
          f"turning the switch back on must restore the keys: {chosen_at('c while on')!r}")

    check(chosen_at("held d") == chosen_at("c while on"), "a held-down verdict key must set nothing")

    # A focused card in view is the active card; scrolling it away hands the keys back to the reading line.
    held_focus = step("d on focused")
    check(f"#500 @ {500:040x} | defer | " in held_focus["box"]["value"] and f"#506 @ {506:040x} | request changes | " in held_focus["box"]["value"],
          f"a verdict key must act on the focused card in view, not the one on the reading line: {held_focus['box']['value']!r}")
    check([b["title"].lstrip("0123456789") for b in step("focus")["blocks"] if b["active"]] == ["Routine change 0"]
          and step("focus")["rail"]["current"] == ["Routine change 0"], "the focused card in view must be the one active card")
    check([b["title"].lstrip("0123456789") for b in step("scrolled")["blocks"] if b["active"]] == [quiet],
          "scrolling the focused card out of view must hand the active card back to the reading line")
    check(f"#506 @ {506:040x} | defer | " in chosen_at("d on the line") and f"#500 @ {500:040x} | defer | " in chosen_at("d on the line"),
          f"after the focused card scrolls away, a verdict key acts on the reading line: {chosen_at('d on the line')!r}")

    # The help panel, the theme, and what the browser keeps.
    check(first["bar"]["help"] == {"hidden": True, "expanded": None} and step("help")["bar"]["help"] == {"hidden": False, "expanded": "true"},
          f"the ? button must open the help: {step('help')['bar']['help']}")
    check(step("escape")["bar"]["help"] == {"hidden": True, "expanded": "false"} and step("escape")["focus"] == "shortcut-help-toggle",
          f"Escape must close the help and return focus to the ? button: {step('escape')['bar']['help']}, {step('escape')['focus']}")
    check(first["theme"] is None and step("theme")["theme"] == "dark" and step("theme")["storage"].get("reviewing-prs-prefs:theme") == "dark",
          f"the theme must be remembered: {step('theme')['theme']}, {step('theme')['storage'].get('reviewing-prs-prefs:theme')}")
    kept = set(steps[-1]["storage"]) - {"reviewing-prs-prefs:theme", "reviewing-prs-prefs:shortcuts"}
    check(kept and all(key.startswith("reviewing-prs:acme/ledger-app#") for key in kept), f"the browser keeps verdicts and two preferences, nothing else: {sorted(kept)[:3]}")

    # n goes on to the verdicts when nothing showing is left to decide, and a refused copy brings the text to the operator.
    check(step("n when done")["scrolled"] == "verdicts", f"n with nothing left to decide must go to the verdicts: {step('n when done')['scrolled']}")
    failed = step("copy fails")
    check(step("back up")["scrolled"] != "verdicts" and failed["scrolled"] == "verdicts" and failed["focus"] == "textarea" and "copy it by hand" in failed["box"]["status"]
          and failed["announced"].startswith("Copy did not work here."), f"a refused copy must scroll to the verdicts and say what to do: {failed['box']['status']!r}")

    # A second visit starts from what the first one stored.
    again = render(page, scratch, [["key", "m"]], steps[-1]["storage"])
    if again is None:
        return
    check(again[0]["theme"] == "dark" and again[0]["bar"]["shortcuts"] == "true", f"a reload must keep the theme and the switch: {again[0]['theme']}, {again[0]['bar']['shortcuts']}")
    recalled = next(b for b in again[0]["blocks"] if b["title"].endswith(quiet))
    check(recalled["collapsed"] is True and recalled["badge"] == {"text": "Your verdict: Defer", "hidden": False},
          f"a routine card with a recalled verdict stays collapsed and shows it: {recalled['badge']}")
    silenced = render(page, scratch, [["span", "Fleet change 4"], ["key", "m"]], {**steps[-1]["storage"], "reviewing-prs-prefs:shortcuts": "off"})
    if silenced is None:
        return
    check(silenced[0]["bar"]["shortcuts"] == "false" and silenced[2]["box"]["value"] == silenced[0]["box"]["value"],
          "a reload must keep the shortcuts switched off")

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


def check_audience_articles(original: dict, scratch: Path) -> None:
    """The heading takes a or an by the audience's first sound, not its first letter."""
    expected = {"user": "a user", None: "a user", "operator": "an operator", "unit": "a unit", "utility": "a utility",
                "underwriter": "an underwriter", "editor": "an editor"}
    variant = copy.deepcopy(original)
    variant["prs"] = []
    for number, audience in enumerate(expected, start=1):
        pr = copy.deepcopy(original["prs"][0])
        pr.update(number=number, title=f"Audience {audience}", head=f"{number:040x}", audience=audience)
        if audience is None:
            del pr["audience"]
        variant["prs"].append(pr)
    page, _ = fill(json.dumps(variant, indent=2, ensure_ascii=False) + "\n", scratch)
    steps = render(page, scratch)
    if steps is None:
        return
    shown = {block["title"].lstrip("0123456789"): block["sections"][:1] for block in steps[0]["blocks"]}
    for audience, phrase in expected.items():
        check(shown.get(f"Audience {audience}") == [f"What is different for {phrase}"],
              f"an audience of {audience!r} must read 'What is different for {phrase}': {shown.get(f'Audience {audience}')}")


def check_chrome_states(original: dict, scratch: Path) -> None:
    """A page with unreadable data or no pull requests shows no control that would do nothing."""
    round_controls = {"bar-progress", "bar-copy", "shortcuts", "shortcut-help-toggle", "shortcut-help"}
    page, _ = fill(json.dumps(original, indent=2, ensure_ascii=False) + "\n", scratch)
    broken = DATA_BLOCK.sub(lambda match: match.group(0).replace(match.group(1), '{"prs": ['), page)
    steps = render(broken, scratch)
    if steps is not None:
        shown = steps[0]
        check(shown["headings"] == ["This round could not be read"] and len(shown["alerts"]) == 1 and "not valid" in shown["alerts"][0],
              f"unreadable data must show a heading and one alert: {shown['headings']}, {shown['alerts']}")
        check(shown["order"] == ["block frame"], f"unreadable data must show the framed message and nothing else: {shown['order']}")
        check(round_controls <= set(shown["bar"]["hidden"]) and "theme" not in shown["bar"]["hidden"] and shown["rail"]["hidden"] is True,
              f"unreadable data must hide the bar's round controls and the rail, and keep the theme button: {shown['bar']['hidden']}")

    empty = copy.deepcopy(original)
    empty["prs"] = []
    empty["across"] = []
    page, _ = fill(json.dumps(empty, indent=2, ensure_ascii=False) + "\n", scratch)
    steps = render(page, scratch, [["key", "n"]])
    if steps is not None:
        shown = steps[0]
        check("No open pull requests in this round." in shown["lede"], f"an empty round must say so: {shown['lede']!r}")
        check(round_controls <= set(shown["bar"]["hidden"]) and shown["box"] is None and "verdicts" not in shown["order"],
              f"an empty round must hide the bar's round controls and draw no verdicts box: {shown['bar']['hidden']}, {shown['order']}")
        check(shown["rail"]["links"] == ["Merged recently"] and shown["rail"]["hidden"] is False,
              f"an empty round's rail must not link to the verdicts: {shown['rail']['links']}")
        check((shown["merged"] or {}).get("lists"), "an empty round must still show what merged recently")
        check(steps[1]["scrolled"] is None, "a key must do nothing on an empty round")

    nothing = copy.deepcopy(empty)
    nothing["merged"] = {}
    page, _ = fill(json.dumps(nothing, indent=2, ensure_ascii=False) + "\n", scratch)
    steps = render(page, scratch)
    if steps is not None:
        check(steps[0]["rail"]["hidden"] is True, "a rail with nothing to link to must be hidden")


def check_storage_cleanup(page: str, scratch: Path) -> None:
    """One unreadable entry must not keep expired verdicts, and a preference never expires."""
    now = 1_900_000_000_000  # far enough ahead that "fresh" below is fresh whenever this runs
    seeded = {
        "reviewing-prs:acme/a#1@unreadable": "{not json",
        "reviewing-prs:acme/a#2@expired": json.dumps({"verdict": "merge", "notes": "", "saved": 1}),
        "reviewing-prs:acme/a#3@fresh": json.dumps({"verdict": "merge", "notes": "", "saved": now}),
        "reviewing-prs-prefs:theme": "dark",
        "someone-else:key": "{not json",
    }
    steps = render(page, scratch, [], seeded)
    if steps is None:
        return
    check(sorted(steps[0]["storage"]) == ["reviewing-prs-prefs:theme", "reviewing-prs:acme/a#3@fresh", "someone-else:key"],
          f"the clean-up must drop the unreadable and the expired entry and keep the rest: {sorted(steps[0]['storage'])}")


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
        check_storage_cleanup(page, Path(scratch))
    for extra in (lambda scratch: check_incomplete_scores(raw, scratch), lambda scratch: check_two_group_round(raw, scratch),
                  lambda scratch: check_large_round(original, scratch), lambda scratch: check_notice_threshold(original, scratch),
                  lambda scratch: check_chrome_states(original, scratch),
                  lambda scratch: check_audience_articles(original, scratch)):
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
