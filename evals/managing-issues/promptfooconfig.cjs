const { readFileSync } = require('node:fs');
const { join } = require('node:path');

const readTools = ['Read', 'Glob', 'Grep', 'Skill'];
const claude = {
  model: 'claude-opus-5-5',
  effort: 'medium',
  apiKeyRequired: false,
  max_turns: 8,
  max_budget_usd: 0.95,
  setting_sources: ['project'],
  tools: readTools,
  custom_allowed_tools: readTools,
  permission_mode: 'dontAsk',
  strict_mcp_config: true,
  exclude_dynamic_sections: true,
  settings: {
    syncClaudeAiSkills: false,
    syncClaudeAiPlugins: false,
    permissions: { blockReadsOutsideWorkingDirectories: true },
  },
};

const caseId = process.env.ROOKERY_EVAL_CASE;
const fixture = `cases/${caseId}`;
const workspace = `./workspaces/${caseId}`;
const checks = [
  ['sections', 'Draft sections'],
  ['scores', 'Leverage scores'],
  ['tools', 'Read-only tool calls'],
];
const caseChecks = {
  'mention-link': 'STORE-412 present',
};

module.exports = {
  description: 'Managing issues Skill Eval',
  sharing: false,
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
    {
      id: 'openai:codex-sdk',
      label: 'Codex with skill',
      config: {
        model: 'gpt-6.2-sol',
        model_reasoning_effort: 'high',
        working_dir: `${workspace}/codex-skill`,
        skip_git_repo_check: true,
        approval_policy: 'never',
        network_access_enabled: false,
        web_search_mode: 'disabled',
        cli_env: { CODEX_HOME: join(__dirname, 'codex-home') },
        cli_config: {
          cli_auth_credentials_store: 'file',
          allow_login_shell: false,
          analytics: { enabled: false },
          feedback: { enabled: false },
          features: { apps: false, multi_agent: false },
        },
      },
    },
  ],
  tests: [
    {
      description: caseId,
      vars: {
        request: readFileSync(join(__dirname, fixture, 'prompt.md'), 'utf8').trimEnd(),
      },
      assert: checks.map(([check, metric]) => ({
        type: 'javascript',
        value: 'file://./cases/password-reset-plus/checks.mjs',
        metric,
        config: { check },
      })).concat(caseChecks[caseId] ? [{
        type: 'javascript',
        value: `file://./${fixture}/check.mjs`,
        metric: caseChecks[caseId],
      }] : []),
    },
  ],
};
