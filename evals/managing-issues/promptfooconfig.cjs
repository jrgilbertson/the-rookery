const { readFileSync } = require('node:fs');
const { join } = require('node:path');

// Offer Write and Edit so any attempt to change a file is recorded, while
// allowing only read-only tools; dontAsk denies everything not allowed.
// Bash is omitted: telling a read-only command from a writing one would mean
// parsing shell text.
const readTools = ['Read', 'Glob', 'Grep', 'Skill'];
const claude = {
  model: 'claude-opus-5-5',
  effort: 'high',
  apiKeyRequired: false,
  max_turns: 40,
  max_budget_usd: 0.95,
  setting_sources: ['project'],
  tools: [...readTools, 'Write', 'Edit'],
  custom_allowed_tools: readTools,
  permission_mode: 'dontAsk',
  strict_mcp_config: true,
  exclude_dynamic_sections: true,
  env: {
    CLAUDE_CODE_DISABLE_AUTO_MEMORY: '1',
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: '1',
  },
  settings: {
    autoMemoryEnabled: false,
    syncClaudeAiSkills: false,
    syncClaudeAiPlugins: false,
    permissions: { blockReadsOutsideWorkingDirectories: true },
  },
};

const caseId = process.env.ROOKERY_EVAL_CASE;
if (!caseId || caseId.includes('/') || caseId.includes('\\') || caseId === '.' || caseId === '..') {
  throw new Error('Set ROOKERY_EVAL_CASE to a case directory name under cases/.');
}
const workspace = `./workspaces/${caseId}`;

const assertions = [
  { type: 'javascript', value: 'file://./checks.mjs', metric: 'Changes nothing' },
  { type: 'skill-used', value: 'managing-issues', metric: 'Loaded the skill' },
  { type: 'javascript', value: 'file://./checks.mjs', metric: 'Draft sections', config: { check: 'sections' } },
  { type: 'javascript', value: 'file://./checks.mjs', metric: 'Leverage scores', config: { check: 'scores' } },
];
if (caseId === 'mention-link') {
  assertions.push({
    type: 'javascript',
    value: 'file://./checks.mjs',
    metric: 'STORE-412 present',
    config: { check: 'mention' },
  });
}

module.exports = {
  description: 'Managing issues Skill Eval',
  sharing: false,
  evaluateOptions: {
    timeoutMs: 300000,
  },
  prompts: ['{{request}}'],
  providers: [
    {
      id: 'anthropic:claude-agent-sdk',
      label: 'Claude with skill',
      config: { ...claude, working_dir: `${workspace}/claude-skill` },
    },
    {
      id: 'anthropic:claude-agent-sdk',
      label: 'Claude baseline',
      config: { ...claude, working_dir: `${workspace}/claude-baseline` },
    },
  ],
  tests: [
    {
      description: caseId,
      vars: {
        request: readFileSync(join(__dirname, 'cases', caseId, 'prompt.md'), 'utf8').trimEnd(),
      },
      assert: assertions,
    },
  ],
};
