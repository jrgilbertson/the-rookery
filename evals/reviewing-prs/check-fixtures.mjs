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
import onlyAllowedTools from './checks.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const ALLOWED_READ_TOOLS = new Set(['Read', 'Glob', 'Grep', 'Skill', 'WebSearch', 'WebFetch']);
const EXPECTED_CASES = [
  'conflicts-impact-digest-html',
  'owner-routing-and-scrubbing',
  'risk-overview-and-situations',
  'verdict-at-reviewed-head',
];

function isInsideDir(parentDir, childPath) {
  const rel = relative(realpathSync(parentDir), realpathSync(childPath));
  return rel !== '' && !rel.startsWith('..') && !rel.startsWith('/');
}

function walkTree(dir, onEntry) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const fullPath = join(dir, entry.name);
    onEntry(fullPath, entry);
    if (entry.isDirectory()) {
      walkTree(fullPath, onEntry);
    }
  }
}

// 1. Exercise write-tool denial in checks.mjs.
const allowed = ['Read', 'Glob', 'Grep', 'Skill'];
const run = (calls, custom_allowed_tools = allowed) => ({
  provider: { config: { custom_allowed_tools } },
  providerResponse: { metadata: { toolCalls: calls } },
});

assert.equal(onlyAllowedTools('', run([{ name: 'Read' }, { name: 'Grep' }, { name: 'Skill' }])), true);
assert.equal(onlyAllowedTools('', run([])), true);
assert.equal(onlyAllowedTools('', run([{ name: 'Read' }, { name: 'Write', input: { file_path: 'round.json' } }])), false);
assert.equal(onlyAllowedTools('', run([{ name: 'Edit' }])), false);
assert.equal(onlyAllowedTools('', run([{ name: 'NotebookEdit' }])), false);
assert.equal(onlyAllowedTools('', run([{ name: 'Bash', input: { command: 'gh pr list' } }])), false);
assert.equal(onlyAllowedTools('', run(undefined)), false);
assert.equal(onlyAllowedTools('', run([null])), false);
assert.equal(onlyAllowedTools('', run([{}])), false);
assert.equal(onlyAllowedTools('', run([{ name: 'Read' }], null)), false);
assert.equal(onlyAllowedTools('', {}), false);

// 2. Verify committed lockfile and pinned dependencies.
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

// 3. Verify all four cases and promptfooconfig.cjs invariants.
const caseIds = readdirSync(join(here, 'cases'), { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort();
assert.deepEqual(caseIds, EXPECTED_CASES, 'expected the four reviewing-prs Eval Cases');

const configPath = join(here, 'promptfooconfig.cjs');
const previousCase = process.env.ROOKERY_EVAL_CASE;
try {
  for (const caseId of caseIds) {
    const caseDir = join(here, 'cases', caseId);
    const promptPath = join(caseDir, 'prompt.md');
    assert.equal(existsSync(promptPath), true, `missing prompt.md for ${caseId}`);
    assert.equal(existsSync(join(caseDir, 'README.md')), true, `missing README.md for ${caseId}`);
    assert.equal(existsSync(join(caseDir, 'case.yaml')), false, `${caseId}: retired case.yaml must not exist`);
    assert.equal(existsSync(join(caseDir, 'turns.json')), false, `${caseId}: retired turns.json must not exist`);
    assert.equal(existsSync(join(caseDir, 'graders')), false, `${caseId}: retired graders/ must not exist`);
    assert.equal(
      readFileSync(promptPath, 'utf8').startsWith('---\n'),
      false,
      `${caseId}: prompt.md must not carry YAML frontmatter`,
    );

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
    assert.deepEqual(
      config.providers.map((provider) => provider.label),
      ['Claude with skill', 'Claude baseline'],
      'expected Claude with skill and Claude baseline arms',
    );
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
      assert.equal(onlyAllowedTools('', run([{ name: 'Read' }, { name: 'Glob' }], cfg.custom_allowed_tools)), true);
      assert.equal(onlyAllowedTools('', run([{ name: 'Write' }], cfg.custom_allowed_tools)), false);
      assert.equal(onlyAllowedTools('', run([{ name: 'Edit' }], cfg.custom_allowed_tools)), false);
      assert.equal(onlyAllowedTools('', run([{ name: 'NotebookEdit' }], cfg.custom_allowed_tools)), false);
      assert.equal(onlyAllowedTools('', run([{ name: 'Bash' }], cfg.custom_allowed_tools)), false);
    }

    assert.ok(Array.isArray(config.tests) && config.tests.length === 1, 'expected one test entry per case');
    const assertions = config.tests[0].assert ?? [];
    assert.ok(
      assertions.some((item) => item.type === 'javascript' && item.value === 'file://./checks.mjs'),
      'expected file://./checks.mjs assertion',
    );
    assert.ok(
      assertions.some((item) => item.type === 'skill-used' && item.value === 'reviewing-prs'),
      'expected skill-used assertion for reviewing-prs',
    );
  }
} finally {
  if (previousCase === undefined) delete process.env.ROOKERY_EVAL_CASE;
  else process.env.ROOKERY_EVAL_CASE = previousCase;
}

// 4. Verify every case fixture builds cleanly as plain files with no .git dir
// and no leaked grading conclusions.
const fixtureScratch = mkdtempSync(join(tmpdir(), 'rookery-reviewing-prs-fixture-test-'));
try {
  const fixtureScript = join(here, 'fixture.py');
  for (const caseId of caseIds) {
    const dest = join(fixtureScratch, caseId);
    execFileSync('python3', ['-I', fixtureScript, dest, caseId], { stdio: 'pipe' });

    assert.equal(existsSync(join(dest, 'github', 'viewer.json')), true, `${caseId}: missing github/viewer.json`);
    assert.equal(
      existsSync(join(dest, 'github', 'repos', 'acme', 'ledger-app', 'repo.json')),
      true,
      `${caseId}: missing acme/ledger-app repo.json`,
    );
    assert.equal(
      existsSync(join(dest, 'github', 'repos', 'acme', 'ledger-app', 'default-branch', 'AGENTS.md')),
      true,
      `${caseId}: missing default-branch AGENTS.md`,
    );

    let fileCount = 0;
    walkTree(dest, (fullPath, entry) => {
      assert.notEqual(entry.name, '.git', `${caseId}: fixture must not contain .git directory`);
      assert.equal(entry.isSymbolicLink(), false, `${caseId}: fixture must not contain symlinks`);
      if (entry.isFile()) {
        fileCount += 1;
        const text = readFileSync(fullPath, 'utf8');
        assert.equal(text.includes('<<'), false, `${caseId}: unreplaced template token in ${fullPath}`);
        assert.equal(text.includes('conflictsWith'), false, `${caseId}: fixture must not leak conflictsWith answer in ${fullPath}`);
        if (entry.name.endsWith('.json')) {
          JSON.parse(text);
        }
      }
    });
    assert.ok(fileCount >= 9, `${caseId}: expected populated synthetic workspace, got ${fileCount} files`);
  }

  assert.throws(
    () => execFileSync('python3', ['-I', fixtureScript, join(fixtureScratch, 'bad'), 'no-such-case'], { stdio: 'pipe' }),
    'fixture.py must reject unknown case IDs',
  );

  // Case-specific structural invariants.
  const ownerPr134 = JSON.parse(
    readFileSync(join(fixtureScratch, 'owner-routing-and-scrubbing', 'github', 'repos', 'acme', 'cli-kit', 'pulls', 'pr-134.json'), 'utf8'),
  );
  assert.equal(ownerPr134.isCrossRepository, true, 'owner-routing #134 must be a cross-repo fork');
  const payrollRepo = JSON.parse(
    readFileSync(join(fixtureScratch, 'owner-routing-and-scrubbing', 'github', 'repos', 'acme', 'payroll-internal', 'repo.json'), 'utf8'),
  );
  assert.equal(payrollRepo.visibility, 'PRIVATE', 'acme/payroll-internal must be PRIVATE');

  const pr426 = JSON.parse(
    readFileSync(join(fixtureScratch, 'conflicts-impact-digest-html', 'github', 'repos', 'acme', 'ledger-app', 'pulls', 'pr-426.json'), 'utf8'),
  );
  const pr427 = JSON.parse(
    readFileSync(join(fixtureScratch, 'conflicts-impact-digest-html', 'github', 'repos', 'acme', 'ledger-app', 'pulls', 'pr-427.json'), 'utf8'),
  );
  assert.ok(pr426.files.some((f) => f.path === 'app/routes.ts'), 'conflicts #426 must touch app/routes.ts');
  assert.ok(pr427.files.some((f) => f.path === 'app/routes.ts'), 'conflicts #427 must touch app/routes.ts');
  const pr139 = JSON.parse(
    readFileSync(join(fixtureScratch, 'conflicts-impact-digest-html', 'github', 'repos', 'acme', 'cli-kit', 'pulls', 'pr-139.json'), 'utf8'),
  );
  assert.match(pr139.title, /<script>/, 'conflicts #139 must carry hostile script tag in title');

  const pr440Diff = readFileSync(
    join(fixtureScratch, 'risk-overview-and-situations', 'github', 'repos', 'acme', 'ledger-app', 'pulls', 'pr-440.diff'),
    'utf8',
  );
  assert.match(pr440Diff, /currency_exponent/, 'risk-overview #440 diff must add currency_exponent column');
  const pr441Diff = readFileSync(
    join(fixtureScratch, 'risk-overview-and-situations', 'github', 'repos', 'acme', 'ledger-app', 'pulls', 'pr-441.diff'),
    'utf8',
  );
  assert.match(pr441Diff, /Math\.floor/, 'risk-overview #441 diff must show Math.floor rounding');
  assert.match(pr441Diff, /Math\.ceil/, 'risk-overview #441 diff must show Math.ceil rounding');

  const pr470Initial = JSON.parse(
    readFileSync(join(fixtureScratch, 'verdict-at-reviewed-head', 'github', 'repos', 'acme', 'ledger-app', 'pulls', 'pr-470.json'), 'utf8'),
  );
  const pr470Reread = JSON.parse(
    readFileSync(join(fixtureScratch, 'verdict-at-reviewed-head', 'github', 'reread-at-confirmation', 'acme', 'ledger-app', 'pr-470.json'), 'utf8'),
  );
  assert.equal(pr470Initial.headRefOid, '3e46a8ef0b842b34b1c0e6a92155922dcc8c771e');
  assert.equal(pr470Reread.headRefOid, 'b254a51b18a65ce4fa14062aae84be82ed3604a8');
  assert.equal(pr470Reread.baseRefName, pr470Initial.baseRefName);
} finally {
  rmSync(fixtureScratch, { recursive: true, force: true });
}

// 5. Verify prepare.sh hardening and no-skill baseline contract.
const prepareSh = readFileSync(join(here, 'prepare.sh'), 'utf8');
assert.match(prepareSh, /package-lock\.json/, 'prepare.sh must copy package-lock.json');
assert.match(prepareSh, /\bnpm\b[^\n]*\bci\b/, 'prepare.sh must install via npm ci');
assert.doesNotMatch(prepareSh, /\bnpm\b[^\n]*\binstall\b/, 'prepare.sh must not use npm install');
assert.match(prepareSh, /skills\/reviewing-prs/, 'prepare.sh must stage skills/reviewing-prs');
assert.doesNotMatch(prepareSh, /claude-baseline\/\.claude\/skills/, 'prepare.sh must stage no skill in baseline');
const stagedSkills = [...prepareSh.matchAll(/skills\/([a-z0-9-]+)/g)].map((match) => match[1]);
assert.equal(
  stagedSkills.length > 0 && stagedSkills.every((name) => name === 'reviewing-prs'),
  true,
  `prepare.sh must stage only reviewing-prs, got ${stagedSkills.join(', ')}`,
);

// 6. Exercise run.sh offline against a stub promptfoo binary and verify the
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

console.log('reviewing-prs eval checks: all passed');
