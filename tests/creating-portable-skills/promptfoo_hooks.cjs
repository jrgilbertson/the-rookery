// Promptfoo hooks for the deterministic audit-file preservation check.
const {spawnSync} = require('node:child_process');
const path = require('node:path');
function inspect(hook, test) {
  const call = spawnSync('python3', [path.join(__dirname, 'promptfoo_suite.py'), 'hook'], {
    input: JSON.stringify({hook, setup: test.metadata.setup}),
    encoding: 'utf8', env: {...process.env, PYTHONDONTWRITEBYTECODE: '1'},
    maxBuffer: 32 * 1024 * 1024,
  });
  if (call.status !== 0) throw new Error('Audit file check failed: ' + call.stderr);
  return JSON.parse(call.stdout);
}
exports.beforeEach = context => {
  inspect('beforeEach', context.test);
  return context;
};
exports.afterEach = context => {
  context.result.metadata.portableSkills = inspect('afterEach', context.test);
  return context;
};
exports.assertPreservation = (output, context) => {
  try { return inspect('assertPreservation', context.test); }
  catch (error) { return {pass: false, score: 0, reason: 'Unmeasured: ' + error.message}; }
};
