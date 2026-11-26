// The tools a run may use. Write and Edit are offered but denied, so a call to
// any tool outside this list is an attempt to change something.
export const readTools = ['Read', 'Glob', 'Grep', 'Skill', 'WebSearch', 'WebFetch'];

export function onlyReadTools(calls) {
  return Array.isArray(calls) && calls.every((call) => readTools.includes(call?.name));
}

export function loadedSkill(calls) {
  return Array.isArray(calls) && calls.some(
    (call) => call?.name === 'Skill' && /(^|:)active-learning$/.test(call?.input?.skill ?? ''),
  );
}

// The baseline arm has no skill to load, so only the skill arm is held to it.
export default function check(_output, context) {
  const calls = context.providerResponse?.metadata?.toolCalls;
  if (context.config?.check === 'skill') {
    const skillArm = String(context.provider?.config?.working_dir ?? '').endsWith('/claude-skill');
    return !skillArm || loadedSkill(calls);
  }
  return onlyReadTools(calls);
}
