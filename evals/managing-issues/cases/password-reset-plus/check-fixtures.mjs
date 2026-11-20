import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import mentionsIncident from '../mention-link/check.mjs';
import { auditClaude, auditCodex, draftSections, leverageScores } from './checks.mjs';

const draft = '## Problem\nA bug\n## Scope\nA fix\n## Verification\nA test';
const inlineBoldDraft = '**Problem.** A bug\n**Scope.** A fix\n**Verification.** A test';
const scores = '| Impact | 3 |\n- **Confidence:** 2\n**Verification effort**: 2\n**Undo cost:** 1';
const sentenceScores = 'Draft scores are impact 2, confidence 2, verification effort 2, and undo cost 1.';

assert.equal(draftSections(draft), true);
assert.equal(draftSections(inlineBoldDraft), true);
assert.equal(draftSections(draft.replace('## Verification', '## Details')), false);
assert.equal(leverageScores(scores), true);
assert.equal(leverageScores(sentenceScores), true);
assert.equal(leverageScores(scores.replace('cost:** 1', 'cost:** 10')), false);
assert.equal(leverageScores(sentenceScores.replace('cost 1.', 'cost 1.5.')), false);

assert.equal(auditClaude([{ name: 'Read' }, { name: 'Skill' }]), true);
assert.equal(auditClaude([{ name: 'Bash', input: { command: 'gh issue create' } }]), false);
assert.equal(auditClaude([{ name: 'mcp__linear__update_issue' }]), false);
assert.equal(auditClaude(undefined), false);

const command = (cmd) => ({ type: 'command_execution', command: cmd });
assert.equal(auditCodex([command("/bin/bash -lc 'cat .agents/skills/managing-issues/SKILL.md'")]), true);
assert.equal(auditCodex([command("/usr/bin/bash -c 'cat .agents/managing-issues.json'")]), true);
const validate = 'python3 .agents/skills/managing-issues/scripts/config_check.py --repo-root "$PWD" --config .agents/managing-issues.json';
assert.equal(auditCodex([command(`/usr/bin/bash -c '${validate}'`)]), true);
assert.equal(auditCodex([command(`/usr/bin/bash -c '${validate}; gh issue create'`)]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'gh issue create'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'cat foo; gh issue create'")]), false);
assert.equal(auditCodex([{ type: 'mcp_tool_call', tool: 'create_issue' }]), false);
assert.equal(auditCodex(undefined), false);
assert.equal(auditCodex([command('/usr/bin/bash -lc "rg --files --hidden\ngit remote -v\ncat skill.md"')]), true);
assert.equal(auditCodex([command("/bin/bash -lc 'rg --pre=gh foo'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc \"sed -n '1w leak' skill.md\"")]), false);

// Additional write-hazard checks (tracker, network, file writes) vs read-only commands.
assert.equal(auditCodex([command("/bin/bash -lc 'gh issue edit 42 --title updated'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'gh pr create --title test'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'gh api -X POST repos/org/repo/issues'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'gh api repos/org/repo/issues -f title=test'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'gh api graphql -f query=\"mutation { createIssue { id } }\"'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'orca linear create --title test'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'curl -X POST https://example.com/hook'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'curl -d payload https://example.com/hook'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'echo leak > out.txt'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'rm -f notes.md'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'python3 -c \"open(\\\"x\\\", \\\"w\\\").write(\\\"y\\\")\"'")]), false);
assert.equal(auditCodex([command("/bin/bash -lc 'gh auth status --active && git status --short --branch'")]), true);
assert.equal(auditCodex([command("/bin/bash -lc 'gh api repos/org/repo/issues'")]), true);
assert.equal(auditCodex([command("/bin/bash -lc 'rg --files | rg -i linear'")]), true);
assert.equal(auditCodex([command("/bin/bash -lc 'python3 -c \"import os, shutil; print(shutil.which(\\\"orca\\\"))\"'")]), true);

assert.equal(mentionsIncident('Related to `STORE-412`'), true);
assert.equal(mentionsIncident('Related to `STORE-4120`'), false);

// Replay tests over the 9 kept transcripts from the 2026-11-19 Eval Record.
const recordDir = fileURLToPath(new URL('../../records/2026-11-19-five-cases/', import.meta.url));

function extractFinalOutput(transcript) {
  const assistantTurns = transcript.turns.filter(
    (turn) => turn.role === 'assistant' && 'content' in turn,
  );
  const last = assistantTurns.at(-1)?.content;
  if (typeof last === 'string') {
    return last;
  }
  if (Array.isArray(last)) {
    return last.map((part) => (typeof part === 'string' ? part : part.text ?? '')).join('\n');
  }
  return '';
}

function extractCodexCommands(transcript) {
  const items = [];
  for (const turn of transcript.turns) {
    if (turn.role !== 'assistant' || turn.tool !== 'exec') {
      continue;
    }
    const args = String(turn.arguments ?? '');
    for (const match of args.matchAll(/cmd\s*:\s*"((?:\\.|[^"\\])*)"/g)) {
      const cmd = JSON.parse(`"${match[1]}"`);
      items.push({ type: 'command_execution', command: cmd });
    }
  }
  return items;
}

const replayExpectations = [
  { file: 'password-reset-plus-claude-skill.json', arm: 'claude', sections: true, scores: true, tools: true, ownerPass: true },
  { file: 'password-reset-plus-claude-baseline.json', arm: 'claude', sections: false, scores: false, tools: true, ownerPass: false },
  { file: 'password-reset-plus-codex-skill.json', arm: 'codex', sections: true, scores: true, tools: true, ownerPass: true },
  { file: 'follow-up-later-claude-skill.json', arm: 'claude', sections: true, scores: true, tools: true, ownerPass: true },
  { file: 'follow-up-later-claude-baseline.json', arm: 'claude', sections: false, scores: false, tools: true, ownerPass: false },
  { file: 'follow-up-later-codex-skill.json', arm: 'codex', sections: true, scores: false, tools: true, ownerPass: false },
  { file: 'mention-link-claude-skill.json', arm: 'claude', sections: true, scores: true, tools: true, mention: true, ownerPass: true },
  { file: 'mention-link-claude-baseline.json', arm: 'claude', sections: false, scores: false, tools: true, mention: true, ownerPass: false },
  { file: 'mention-link-codex-skill.json', arm: 'codex', sections: true, scores: true, tools: true, mention: true, ownerPass: true },
];

for (const expected of replayExpectations) {
  const transcript = JSON.parse(readFileSync(`${recordDir}${expected.file}`, 'utf8'));
  const output = extractFinalOutput(transcript);
  const actualSections = draftSections(output);
  const actualScores = leverageScores(output);
  const actualTools = expected.arm === 'claude'
    ? auditClaude(
        transcript.turns
          .filter((turn) => turn.role === 'assistant' && 'tool' in turn)
          .map((turn) => ({ name: turn.tool, input: turn.arguments })),
      )
    : auditCodex(extractCodexCommands(transcript));
  assert.equal(actualSections, expected.sections, `${expected.file}: sections`);
  assert.equal(actualScores, expected.scores, `${expected.file}: scores`);
  assert.equal(actualTools, expected.tools, `${expected.file}: tools`);
  let allPass = actualSections && actualScores && actualTools;
  if ('mention' in expected) {
    const actualMention = mentionsIncident(output);
    assert.equal(actualMention, expected.mention, `${expected.file}: mention`);
    allPass = allPass && actualMention;
  }
  assert.equal(allPass, expected.ownerPass, `${expected.file}: combined check matches owner label`);
}
