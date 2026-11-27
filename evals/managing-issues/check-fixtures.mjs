import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import {
  chmodSync,
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  realpathSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import check, {
  draftSections,
  leverageScores,
  mentionsIncident,
  onlyAllowedTools,
} from './checks.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const ALLOWED_READ_TOOLS = new Set(['Read', 'Glob', 'Grep', 'Skill', 'WebSearch', 'WebFetch']);

function isInsideDir(parentDir, childPath) {
  const rel = relative(realpathSync(parentDir), realpathSync(childPath));
  return rel !== '' && !rel.startsWith('..') && !rel.startsWith('/');
}

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

// 1. Exercise write-tool denial in checks.mjs.
const sampleAllowed = ['Read', 'Glob', 'Grep', 'Skill'];
const makeContext = (calls, custom_allowed_tools = sampleAllowed, config) => ({
  ...(config ? { config } : {}),
  provider: { config: { custom_allowed_tools } },
  providerResponse: { metadata: { toolCalls: calls } },
});

assert.equal(onlyAllowedTools('', makeContext([{ name: 'Read' }, { name: 'Grep' }, { name: 'Skill' }])), true);
assert.equal(onlyAllowedTools('', makeContext([])), true);
assert.equal(onlyAllowedTools('', makeContext([{ name: 'Read' }, { name: 'Write', input: { file_path: 'note.md' } }])), false);
assert.equal(onlyAllowedTools('', makeContext([{ name: 'Edit' }])), false);
assert.equal(onlyAllowedTools('', makeContext([{ name: 'NotebookEdit' }])), false);
assert.equal(onlyAllowedTools('', makeContext([{ name: 'Bash', input: { command: 'gh issue create' } }])), false);
assert.equal(onlyAllowedTools('', makeContext([{ name: 'mcp__linear__update_issue' }])), false);
assert.equal(onlyAllowedTools('', makeContext(undefined)), false);
assert.equal(onlyAllowedTools('', makeContext([null])), false);
assert.equal(onlyAllowedTools('', makeContext([{}])), false);
assert.equal(onlyAllowedTools('', makeContext([{ name: 'Read' }], null)), false);
assert.equal(onlyAllowedTools('', {}), false);

// Default export dispatches write-tool denial when config.check is omitted.
assert.equal(check('', makeContext([{ name: 'Read' }, { name: 'Skill' }])), true);
assert.equal(check('', makeContext([{ name: 'Write' }])), false);
assert.equal(check('', makeContext([{ name: 'Read' }], sampleAllowed, { check: 'tools' })), true);

// 2. Exercise managing-issues deterministic structural checks in checks.mjs.
const draft = '## Problem\nA bug\n## Scope\nA fix\n## Verification\nA test';
const inlineBoldDraft = '**Problem.** A bug\n**Scope.** A fix\n**Verification.** A test';
const scores = '| Impact | 3 |\n- **Confidence:** 2\n**Verification effort**: 2\n**Undo cost:** 1';
const sentenceScores = 'Draft scores are impact 2, confidence 2, verification effort 2, and undo cost 1.';

assert.equal(draftSections(draft), true);
assert.equal(draftSections(inlineBoldDraft), true);
assert.equal(draftSections(draft.replace('## Verification', '## Details')), false);
assert.equal(draftSections(null), false);

assert.equal(leverageScores(scores), true);
assert.equal(leverageScores(sentenceScores), true);
assert.equal(leverageScores(scores.replace('cost:** 1', 'cost:** 10')), false);
assert.equal(leverageScores(sentenceScores.replace('cost 1.', 'cost 1.5.')), false);
assert.equal(leverageScores(undefined), false);

assert.equal(mentionsIncident('Related to `STORE-412`'), true);
assert.equal(mentionsIncident('Related to `STORE-4120`'), false);
assert.equal(mentionsIncident(null), false);

assert.equal(check(draft, { config: { check: 'sections' } }), true);
assert.equal(check(scores, { config: { check: 'scores' } }), true);
assert.equal(check('Mentions STORE-412 here.', { config: { check: 'mention' } }), true);
assert.throws(() => check(draft, { config: { check: 'nonexistent' } }), /Unknown managing-issues check/);
assert.throws(() => check(draft, { config: { check: 'toString' } }), /Unknown managing-issues check/);

// 3. Replay deterministic checks over the 6 historical Claude transcripts.
const recordDir = join(here, 'records', '2026-11-19-five-cases');
const replayExpectations = [
  { file: 'password-reset-plus-claude-skill.json', sections: true, scores: true, tools: true, ownerPass: true },
  { file: 'password-reset-plus-claude-baseline.json', sections: false, scores: false, tools: true, ownerPass: false },
  { file: 'follow-up-later-claude-skill.json', sections: true, scores: true, tools: true, ownerPass: true },
  { file: 'follow-up-later-claude-baseline.json', sections: false, scores: false, tools: true, ownerPass: false },
  { file: 'mention-link-claude-skill.json', sections: true, scores: true, tools: true, mention: true, ownerPass: true },
  { file: 'mention-link-claude-baseline.json', sections: false, scores: false, tools: true, mention: true, ownerPass: false },
];

for (const expected of replayExpectations) {
  const transcript = JSON.parse(readFileSync(join(recordDir, expected.file), 'utf8'));
  const output = extractFinalOutput(transcript);
  const calls = transcript.turns
    .filter((turn) => turn.role === 'assistant' && 'tool' in turn)
    .map((turn) => ({ name: turn.tool, input: turn.arguments }));
  const actualSections = draftSections(output);
  const actualScores = leverageScores(output);
  const actualTools = onlyAllowedTools(output, makeContext(calls));
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

// 4. Verify committed lockfile and pinned Claude-only dependencies.
const pkgPath = join(here, 'package.json');
const lockPath = join(here, 'package-lock.json');
assert.equal(existsSync(lockPath), true, 'package-lock.json must be committed');
const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
const lock = JSON.parse(readFileSync(lockPath, 'utf8'));
assert.equal(typeof lock.lockfileVersion, 'number', 'package-lock.json must declare lockfileVersion');
assert.equal(lock.packages?.['']?.dependencies?.promptfoo, pkg.dependencies?.promptfoo);
assert.equal(
  lock.packages?.['']?.dependencies?.['@anthropic-ai/claude-agent-sdk'],
  pkg.dependencies?.['@anthropic-ai/claude-agent-sdk'],
);
assert.deepEqual(
  Object.keys(pkg.dependencies ?? {}).sort(),
  ['@anthropic-ai/claude-agent-sdk', 'promptfoo'],
  'package.json must depend only on Claude Agent SDK and Promptfoo',
);

// 5. Verify all three cases and promptfooconfig.cjs invariants.
const caseIds = readdirSync(join(here, 'cases'), { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort();
assert.deepEqual(
  caseIds,
  ['follow-up-later', 'mention-link', 'password-reset-plus'],
  'expected the three managing-issues Eval Cases',
);

const configPath = join(here, 'promptfooconfig.cjs');
const previousCase = process.env.ROOKERY_EVAL_CASE;
try {
  delete process.env.ROOKERY_EVAL_CASE;
  delete require.cache[require.resolve(configPath)];
  assert.throws(() => require(configPath), /ROOKERY_EVAL_CASE/);

  process.env.ROOKERY_EVAL_CASE = '../escape';
  delete require.cache[require.resolve(configPath)];
  assert.throws(() => require(configPath), /ROOKERY_EVAL_CASE/);

  for (const caseId of caseIds) {
    assert.equal(existsSync(join(here, 'cases', caseId, 'prompt.md')), true, `missing prompt.md for ${caseId}`);
    assert.equal(existsSync(join(here, 'cases', caseId, 'README.md')), true, `missing README.md for ${caseId}`);

    process.env.ROOKERY_EVAL_CASE = caseId;
    delete require.cache[require.resolve(configPath)];
    const config = require(configPath);

    assert.equal(config.sharing, false, 'Promptfoo sharing must be disabled');
    const timeoutMs = config.evaluateOptions?.timeoutMs;
    assert.equal(
      Number.isSafeInteger(timeoutMs) && timeoutMs > 0 && timeoutMs <= 600000,
      true,
      'evaluateOptions.timeoutMs must be a positive bounded integer (<= 600000 ms)',
    );

    assert.ok(Array.isArray(config.providers) && config.providers.length === 2, 'expected skill and baseline providers');
    for (const provider of config.providers) {
      assert.equal(provider.id, 'anthropic:claude-agent-sdk', 'only anthropic:claude-agent-sdk is allowed');
      const cfg = provider.config ?? {};
      assert.equal(cfg.apiKeyRequired, false, 'apiKeyRequired must be false for subscription auth');
      assert.equal(cfg.permission_mode, 'dontAsk', 'permission_mode must be dontAsk');
      assert.equal(cfg.strict_mcp_config, true, 'strict_mcp_config must be true');
      assert.equal(cfg.exclude_dynamic_sections, true, 'exclude_dynamic_sections must be true');
      assert.deepEqual(cfg.setting_sources, ['project'], 'setting_sources must be ["project"]');
      assert.equal(cfg.settings?.autoMemoryEnabled, false, 'settings.autoMemoryEnabled must be false');
      assert.equal(cfg.env?.CLAUDE_CODE_DISABLE_AUTO_MEMORY, '1', 'env.CLAUDE_CODE_DISABLE_AUTO_MEMORY must be "1"');
      assert.equal(cfg.settings?.syncClaudeAiSkills, false, 'settings.syncClaudeAiSkills must be false');
      assert.equal(cfg.settings?.syncClaudeAiPlugins, false, 'settings.syncClaudeAiPlugins must be false');
      assert.equal(
        cfg.settings?.permissions?.blockReadsOutsideWorkingDirectories,
        true,
        'settings.permissions.blockReadsOutsideWorkingDirectories must be true',
      );

      assert.ok(Array.isArray(cfg.tools), 'tools must be an array');
      assert.ok(Array.isArray(cfg.custom_allowed_tools) && cfg.custom_allowed_tools.length > 0, 'custom_allowed_tools must be non-empty');
      assert.equal(cfg.tools.includes('Bash'), false, 'Bash must not be offered in tools');
      assert.equal(cfg.tools.includes('Write'), true, 'Write must be offered so attempts are recorded');
      assert.equal(cfg.tools.includes('Edit'), true, 'Edit must be offered so attempts are recorded');
      for (const tool of cfg.custom_allowed_tools) {
        assert.equal(
          ALLOWED_READ_TOOLS.has(tool),
          true,
          `custom_allowed_tools may contain only approved read-only tools; got ${tool}`,
        );
        assert.equal(cfg.tools.includes(tool), true, `allowed tool ${tool} must be in tools`);
      }

      // Exercise checks.mjs against the loaded provider config.
      assert.equal(onlyAllowedTools('', makeContext([{ name: 'Read' }, { name: 'Skill' }], cfg.custom_allowed_tools)), true);
      assert.equal(onlyAllowedTools('', makeContext([{ name: 'Write' }], cfg.custom_allowed_tools)), false);
      assert.equal(onlyAllowedTools('', makeContext([{ name: 'Edit' }], cfg.custom_allowed_tools)), false);
      assert.equal(onlyAllowedTools('', makeContext([{ name: 'NotebookEdit' }], cfg.custom_allowed_tools)), false);
      assert.equal(onlyAllowedTools('', makeContext([{ name: 'Bash' }], cfg.custom_allowed_tools)), false);
    }

    assert.ok(Array.isArray(config.tests) && config.tests.length === 1, 'expected one test entry per case');
    const assertions = config.tests[0].assert ?? [];
    assert.ok(
      assertions.some((item) => item.type === 'javascript' && item.value === 'file://./checks.mjs' && item.config === undefined),
      'expected default file://./checks.mjs write-denial assertion',
    );
    assert.ok(
      assertions.some((item) => item.type === 'skill-used' && item.value === 'managing-issues'),
      'expected skill-used assertion for managing-issues',
    );
    assert.ok(
      assertions.some((item) => item.type === 'javascript' && item.value === 'file://./checks.mjs' && item.config?.check === 'sections'),
      'expected Draft sections assertion',
    );
    assert.ok(
      assertions.some((item) => item.type === 'javascript' && item.value === 'file://./checks.mjs' && item.config?.check === 'scores'),
      'expected Leverage scores assertion',
    );
    const hasMention = assertions.some(
      (item) => item.type === 'javascript' && item.value === 'file://./checks.mjs' && item.config?.check === 'mention',
    );
    assert.equal(hasMention, caseId === 'mention-link', `mention assertion mismatch for ${caseId}`);
  }
} finally {
  if (previousCase === undefined) delete process.env.ROOKERY_EVAL_CASE;
  else process.env.ROOKERY_EVAL_CASE = previousCase;
}

// 6. Verify prepare.sh hardening contract.
const prepareSh = readFileSync(join(here, 'prepare.sh'), 'utf8');
assert.match(prepareSh, /package-lock\.json/, 'prepare.sh must copy package-lock.json');
assert.match(prepareSh, /\bnpm\b[^\n]*\bci\b/, 'prepare.sh must install via npm ci');
assert.doesNotMatch(prepareSh, /\bnpm\b[^\n]*\binstall\b/, 'prepare.sh must not use npm install');

// 7. Exercise run.sh offline against a stub promptfoo binary and verify the
// actual child environment isolates HOME and CLAUDE_CONFIG_DIR inside $work.
const scratch = mkdtempSync(join(tmpdir(), 'rookery-eval-run-test-'));
try {
  const workDir = join(scratch, 'work');
  const fakeCallerHome = join(scratch, 'caller-home');
  const fakeClaudeDir = join(fakeCallerHome, '.claude');
  const envOut = join(scratch, 'captured-env.json');
  const firstCase = caseIds[0];

  mkdirSync(join(workDir, 'cases', firstCase), { recursive: true });
  mkdirSync(join(workDir, 'node_modules', '.bin'), { recursive: true });
  mkdirSync(fakeClaudeDir, { recursive: true });
  writeFileSync(join(workDir, 'cases', firstCase, 'prompt.md'), 'synthetic prompt\n');
  writeFileSync(join(fakeClaudeDir, '.credentials.json'), '{"synthetic":true}\n');

  const stubPromptfoo = join(workDir, 'node_modules', '.bin', 'promptfoo');
  writeFileSync(
    stubPromptfoo,
    `#!/usr/bin/env bash
set -euo pipefail
node -e '
const fs = require("node:fs");
fs.writeFileSync(${JSON.stringify(envOut)}, JSON.stringify({
  HOME: process.env.HOME,
  CLAUDE_CONFIG_DIR: process.env.CLAUDE_CONFIG_DIR,
  CLAUDE_SECURESTORAGE_CONFIG_DIR: process.env.CLAUDE_SECURESTORAGE_CONFIG_DIR,
  CLAUDE_CODE_DISABLE_AUTO_MEMORY: process.env.CLAUDE_CODE_DISABLE_AUTO_MEMORY,
  PROMPTFOO_EVAL_TIMEOUT_MS: process.env.PROMPTFOO_EVAL_TIMEOUT_MS,
  PROMPTFOO_DISABLE_TELEMETRY: process.env.PROMPTFOO_DISABLE_TELEMETRY,
  ROOKERY_EVAL_CASE: process.env.ROOKERY_EVAL_CASE,
}));
'
`,
  );
  chmodSync(stubPromptfoo, 0o700);

  execFileSync('bash', [join(here, 'run.sh'), workDir, 'claude-skill', firstCase], {
    env: {
      PATH: process.env.PATH ?? '/usr/bin:/bin',
      HOME: fakeCallerHome,
      USER: 'synthetic-user',
      TMPDIR: scratch,
    },
    stdio: 'pipe',
  });

  const captured = JSON.parse(readFileSync(envOut, 'utf8'));
  assert.equal(isInsideDir(workDir, captured.HOME), true, `HOME must be inside work dir, got ${captured.HOME}`);
  assert.notEqual(realpathSync(captured.HOME), realpathSync(fakeCallerHome), 'HOME must not be the caller HOME');
  assert.equal(
    isInsideDir(workDir, captured.CLAUDE_CONFIG_DIR),
    true,
    `CLAUDE_CONFIG_DIR must be inside work dir, got ${captured.CLAUDE_CONFIG_DIR}`,
  );
  assert.equal(
    lstatSync(join(captured.CLAUDE_CONFIG_DIR, '.credentials.json')).isSymbolicLink(),
    true,
    'file-backed credentials should be linked into the isolated CLAUDE_CONFIG_DIR',
  );
  assert.equal(captured.CLAUDE_SECURESTORAGE_CONFIG_DIR, '', 'default macOS Keychain scope must remain empty string');
  assert.equal(captured.CLAUDE_CODE_DISABLE_AUTO_MEMORY, '1');
  assert.equal(captured.PROMPTFOO_DISABLE_TELEMETRY, '1');
  assert.equal(captured.ROOKERY_EVAL_CASE, firstCase);
  const envTimeoutMs = Number(captured.PROMPTFOO_EVAL_TIMEOUT_MS);
  assert.equal(Number.isSafeInteger(envTimeoutMs) && envTimeoutMs > 0 && envTimeoutMs <= 600000, true);
} finally {
  rmSync(scratch, { recursive: true, force: true });
}

console.log('managing-issues eval checks: all passed');
