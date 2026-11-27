import assert from 'node:assert/strict';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import onlyAllowedTools from './checks.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);

// 1. Exercise write-tool denial in checks.mjs.
const allowed = ['Read', 'Glob', 'Grep', 'Skill', 'WebSearch', 'WebFetch'];
const run = (calls, custom_allowed_tools = allowed) => ({
  provider: { config: { custom_allowed_tools } },
  providerResponse: { metadata: { toolCalls: calls } },
});

assert.equal(onlyAllowedTools('', run([{ name: 'Read' }, { name: 'Grep' }, { name: 'WebFetch' }])), true);
assert.equal(onlyAllowedTools('', run([])), true);
assert.equal(onlyAllowedTools('', run([{ name: 'Read' }, { name: 'Write', input: { file_path: 'note.md' } }])), false);
assert.equal(onlyAllowedTools('', run([{ name: 'Edit' }])), false);
assert.equal(onlyAllowedTools('', run([{ name: 'Bash', input: { command: 'ls' } }])), false);
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

// 3. Verify all five cases and promptfooconfig.cjs invariants.
const caseIds = readdirSync(join(here, 'cases'), { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort();
assert.deepEqual(
  caseIds,
  ['daily-pass', 'digest-reply', 'failing-card', 'source-stop', 'source-terms'],
  'expected the five active-learning Eval Cases',
);

const configPath = join(here, 'promptfooconfig.cjs');
const previousCase = process.env.ROOKERY_EVAL_CASE;
try {
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
      assert.ok(Array.isArray(cfg.custom_allowed_tools), 'custom_allowed_tools must be an array');
      assert.equal(cfg.tools.includes('Bash'), false, 'Bash must not be offered in tools');
      assert.equal(cfg.custom_allowed_tools.includes('Bash'), false, 'Bash must not be allowed');
      assert.equal(cfg.tools.includes('Write'), true, 'Write must be offered so attempts are recorded');
      assert.equal(cfg.tools.includes('Edit'), true, 'Edit must be offered so attempts are recorded');
      assert.equal(cfg.custom_allowed_tools.includes('Write'), false, 'Write must not be allowed');
      assert.equal(cfg.custom_allowed_tools.includes('Edit'), false, 'Edit must not be allowed');
      for (const tool of cfg.custom_allowed_tools) {
        assert.equal(cfg.tools.includes(tool), true, `allowed tool ${tool} must be in tools`);
      }

      // Exercise checks.mjs against the loaded provider config.
      assert.equal(onlyAllowedTools('', run([{ name: 'Read' }, { name: 'WebFetch' }], cfg.custom_allowed_tools)), true);
      assert.equal(onlyAllowedTools('', run([{ name: 'Write' }], cfg.custom_allowed_tools)), false);
      assert.equal(onlyAllowedTools('', run([{ name: 'Edit' }], cfg.custom_allowed_tools)), false);
      assert.equal(onlyAllowedTools('', run([{ name: 'Bash' }], cfg.custom_allowed_tools)), false);
    }

    assert.ok(Array.isArray(config.tests) && config.tests.length === 1, 'expected one test entry per case');
    const assertions = config.tests[0].assert ?? [];
    assert.ok(
      assertions.some((item) => item.type === 'javascript' && item.value === 'file://./checks.mjs'),
      'expected file://./checks.mjs assertion',
    );
    assert.ok(
      assertions.some((item) => item.type === 'skill-used' && item.value === 'active-learning'),
      'expected skill-used assertion for active-learning',
    );
  }
} finally {
  if (previousCase === undefined) delete process.env.ROOKERY_EVAL_CASE;
  else process.env.ROOKERY_EVAL_CASE = previousCase;
}

// 4. Verify prepare.sh and run.sh hardening contracts.
const prepareSh = readFileSync(join(here, 'prepare.sh'), 'utf8');
assert.match(prepareSh, /package-lock\.json/, 'prepare.sh must copy package-lock.json');
assert.match(prepareSh, /\bnpm\b[^\n]*\bci\b/, 'prepare.sh must install via npm ci');
assert.doesNotMatch(prepareSh, /\bnpm\b[^\n]*\binstall\b/, 'prepare.sh must not use npm install');

const runSh = readFileSync(join(here, 'run.sh'), 'utf8');
assert.doesNotMatch(runSh, /HOME="\$HOME"/, 'run.sh must not pass the real HOME directly');
assert.match(runSh, /HOME="(?:\$run_home|\$work\/[^"]+)"/, 'run.sh must isolate HOME inside the run directory');
assert.match(runSh, /CLAUDE_CONFIG_DIR="(?:\$claude_home|\$work\/[^"]+)"/, 'run.sh must isolate CLAUDE_CONFIG_DIR inside the run directory');
assert.match(runSh, /CLAUDE_CODE_DISABLE_AUTO_MEMORY=1/, 'run.sh must set CLAUDE_CODE_DISABLE_AUTO_MEMORY=1');
assert.match(runSh, /PROMPTFOO_EVAL_TIMEOUT_MS=/, 'run.sh must enforce PROMPTFOO_EVAL_TIMEOUT_MS');

console.log('active-learning eval checks: all passed');
