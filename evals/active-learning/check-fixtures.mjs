import assert from 'node:assert/strict';
import onlyAllowedTools from './checks.mjs';

const allowed = ['Read', 'Glob', 'Grep', 'Skill', 'WebSearch', 'WebFetch'];
const run = (calls, custom_allowed_tools = allowed) => ({
  provider: { config: { custom_allowed_tools } },
  providerResponse: { metadata: { toolCalls: calls } },
});

assert.equal(onlyAllowedTools('', run([{ name: 'Read' }, { name: 'Grep' }, { name: 'WebFetch' }])), true);
assert.equal(onlyAllowedTools('', run([])), true);
assert.equal(onlyAllowedTools('', run([{ name: 'Read' }, { name: 'Write', input: { file_path: '/tmp/x' } }])), false);
assert.equal(onlyAllowedTools('', run([{ name: 'Edit' }])), false);
assert.equal(onlyAllowedTools('', run([{ name: 'Bash', input: { command: 'ls' } }])), false);
assert.equal(onlyAllowedTools('', run(undefined)), false);
assert.equal(onlyAllowedTools('', run([{ name: 'Read' }], null)), false);
console.log('active-learning eval checks: all passed');
