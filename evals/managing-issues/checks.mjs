const headings = ['Problem', 'Scope', 'Verification'];
const factors = ['Impact', 'Confidence', 'Verification effort', 'Undo cost'];

export function draftSections(output) {
  return typeof output === 'string' && headings.every((name) => {
    const heading = new RegExp(
      `^[ \\t]*(?:#{1,6} +${name}[:# \\t]*$|\\*\\*${name}[.:]?\\*\\*[.:]?(?=[ \\t]|$))`,
      'im',
    );
    return heading.test(output);
  });
}

export function leverageScores(output) {
  return typeof output === 'string' && factors.every((factor) => {
    const score = new RegExp(
      `\\b${factor}[*\\s:|=—–]+(?:score[*\\s:|=—–]+)?[* ]*[1-3](?!\\d|\\.\\d)`,
      'i',
    );
    return score.test(output);
  });
}

export function mentionsIncident(output) {
  return typeof output === 'string' && /\bSTORE-412\b/.test(output);
}

export function onlyAllowedTools(_output, context) {
  const allowed = context?.provider?.config?.custom_allowed_tools;
  const calls = context?.providerResponse?.metadata?.toolCalls;
  return Array.isArray(allowed) && Array.isArray(calls)
    && calls.every((call) => typeof call?.name === 'string' && allowed.includes(call.name));
}

const checks = {
  tools: onlyAllowedTools,
  sections: (output) => draftSections(output),
  scores: (output) => leverageScores(output),
  mention: (output) => mentionsIncident(output),
};

export default function check(output, context) {
  const name = context?.config?.check ?? 'tools';
  if (!Object.hasOwn(checks, name)) {
    throw new Error(`Unknown managing-issues check: ${String(name)}`);
  }
  return checks[name](output, context);
}
