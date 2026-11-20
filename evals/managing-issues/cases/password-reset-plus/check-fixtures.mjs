import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import mentionsIncident from '../mention-link/check.mjs';
import check, { auditClaude, auditCodex, draftSections, leverageScores } from './checks.mjs';

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

const codexProviderConfig = {
  sandbox_mode: 'read-only',
  network_access_enabled: false,
  approval_policy: 'never',
};
const codexRecordedContext = {
  approval_policy: 'never',
  permissions: {
    type: 'managed',
    file_system: {
      type: 'restricted',
      entries: [
        { path: { type: 'path', path: '/usr/bin/gh' }, access: 'deny' },
        { path: { type: 'special', value: { kind: 'minimal' } }, access: 'read' },
      ],
    },
    network: 'restricted',
  },
};
const command = (cmd) => ({ type: 'command_execution', command: cmd });

assert.equal(auditCodex(codexProviderConfig, [command("/bin/bash -lc 'cat .agents/skills/managing-issues/SKILL.md'")]), true);
assert.equal(auditCodex(codexRecordedContext, [command("/usr/bin/bash -c 'cat .agents/managing-issues.json'")]), true);
assert.equal(auditCodex({ ...codexProviderConfig, sandbox_mode: 'workspace-write' }), false);
assert.equal(auditCodex({ ...codexProviderConfig, network_access_enabled: true }), false);
assert.equal(auditCodex({ ...codexProviderConfig, approval_policy: 'on-request' }), false);
assert.equal(auditCodex({
  ...codexRecordedContext,
  permissions: {
    ...codexRecordedContext.permissions,
    file_system: {
      type: 'restricted',
      entries: [{ path: { type: 'path', path: '/tmp/out' }, access: 'write' }],
    },
  },
}), false);
assert.equal(auditCodex({
  ...codexRecordedContext,
  permissions: { ...codexRecordedContext.permissions, network: 'enabled' },
}), false);
assert.equal(auditCodex(codexProviderConfig, [{ type: 'mcp_tool_call', tool: 'create_issue' }]), false);
assert.equal(auditCodex(undefined), false);
assert.equal(
  check('', {
    config: { check: 'tools' },
    provider: { id: () => 'openai:codex-sdk', config: codexProviderConfig },
    providerResponse: { raw: JSON.stringify({ items: [command('cat skill.md')] }) },
  }),
  true,
);
assert.equal(
  check('', {
    config: { check: 'tools' },
    provider: { id: () => 'openai:codex-sdk', config: { ...codexProviderConfig, network_access_enabled: true } },
    providerResponse: { raw: JSON.stringify({ items: [command('cat skill.md')] }) },
  }),
  false,
);

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

function extractCodexItems(transcript) {
  return transcript.turns
    .filter((turn) => turn.role === 'assistant' && 'tool' in turn)
    .map((turn) => (turn.tool === 'exec'
      ? { type: 'command_execution', command: String(turn.arguments ?? '') }
      : { type: turn.tool }));
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
    : auditCodex(transcript.context, extractCodexItems(transcript));
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
