// Native Promptfoo lifecycle/assertion functions. No model transport or recorder.
const {spawnSync} = require('node:child_process');
const path = require('node:path');
function inspect(hook, test, response) {
  const call = spawnSync('python3', [path.join(__dirname, 'promptfoo_suite.py'), 'hook'], {
    input: JSON.stringify({hook, setup: test.metadata.setup, response}),
    encoding: 'utf8', env: {...process.env, PYTHONDONTWRITEBYTECODE: '1'},
    maxBuffer: 32 * 1024 * 1024,
  });
  if (call.status !== 0) throw new Error('Native capture inspection failed: ' + call.stderr);
  return JSON.parse(call.stdout);
}
exports.beforeEach = context => {
  inspect('beforeEach', context.test);
  return context;
};
exports.afterEach = context => {
  context.result.metadata.portableSkills = inspect('afterEach', context.test, context.result.response);
  return context;
};
exports.assertCapture = (output, context) => {
  try { return inspect('assertCapture', context.test, context.providerResponse); }
  catch (error) { return {pass: false, score: 0, reason: 'Unmeasured: ' + error.message}; }
};
