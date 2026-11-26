// Offline checks for checks.mjs; no model is called.
import assert from 'node:assert/strict';
import check, { loadedSkill, onlyReadTools } from './checks.mjs';

assert.equal(onlyReadTools([{ name: 'Read' }, { name: 'Grep' }, { name: 'WebFetch' }]), true);
assert.equal(onlyReadTools([]), true);
assert.equal(onlyReadTools([{ name: 'Read' }, { name: 'Write', input: { file_path: '/tmp/x' } }]), false);
assert.equal(onlyReadTools([{ name: 'Edit' }]), false);
assert.equal(onlyReadTools([{ name: 'Bash', input: { command: 'ls' } }]), false);
assert.equal(onlyReadTools(undefined), false);
assert.equal(loadedSkill([{ name: 'Skill', input: { skill: 'active-learning' } }]), true);
assert.equal(loadedSkill([{ name: 'Skill', input: { skill: 'plugin:active-learning' } }]), true);
assert.equal(loadedSkill([{ name: 'Skill', input: { skill: 'atomic-note' } }]), false);
assert.equal(loadedSkill([{ name: 'Read' }]), false);

const response = (calls) => ({ providerResponse: { metadata: { toolCalls: calls } } });
assert.equal(check('', response([{ name: 'Read' }])), true);
assert.equal(check('', response([{ name: 'Write' }])), false);
const arm = (dir, calls) => ({ ...response(calls), config: { check: 'skill' }, provider: { config: { working_dir: dir } } });
assert.equal(check('', arm('./workspaces/x/claude-skill', [{ name: 'Read' }])), false);
assert.equal(check('', arm('./workspaces/x/claude-skill', [{ name: 'Skill', input: { skill: 'active-learning' } }])), true);
assert.equal(check('', arm('./workspaces/x/claude-baseline', [{ name: 'Read' }])), true);
console.log('active-learning eval checks: all passed');
