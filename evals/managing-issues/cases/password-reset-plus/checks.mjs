const headings = ['Problem', 'Scope', 'Verification'];
const factors = ['Impact', 'Confidence', 'Verification effort', 'Undo cost'];
const allowedCodexItems = ['agent_message', 'reasoning', 'todo_list', 'command_execution'];

export function draftSections(output) {
  return headings.every((name) => {
    const heading = new RegExp(
      `^[ \\t]*(?:#{1,6} +${name}[:# \\t]*$|\\*\\*${name}[.:]?\\*\\*[.:]?(?=[ \\t]|$))`,
      'im',
    );
    return heading.test(output);
  });
}

export function leverageScores(output) {
  return factors.every((factor) => {
    const score = new RegExp(
      `\\b${factor}[*\\s:|=—–]+(?:score[*\\s:|=—–]+)?[* ]*[1-3](?!\\d|\\.\\d)`,
      'i',
    );
    return score.test(output);
  });
}

export function auditClaude(calls) {
  return Array.isArray(calls) && calls.every(
    (call) => ['Read', 'Glob', 'Grep', 'Skill'].includes(call.name),
  );
}

function isReadOnlySandbox(settings) {
  if (settings.sandbox_mode === 'read-only') {
    return true;
  }
  const fs = settings.permissions?.file_system;
  return fs?.type === 'restricted'
    && Array.isArray(fs.entries)
    && fs.entries.length > 0
    && fs.entries.every((entry) => entry?.access === 'read' || entry?.access === 'deny');
}

function isNetworkDisabled(settings) {
  return settings.network_access_enabled === false
    || settings.permissions?.network === 'restricted'
    || settings.permissions?.network === 'disabled';
}

export function auditCodex(settings, items) {
  if (!settings || typeof settings !== 'object') {
    return false;
  }
  if (settings.approval_policy !== 'never') {
    return false;
  }
  if (!isReadOnlySandbox(settings) || !isNetworkDisabled(settings)) {
    return false;
  }
  if (items === undefined) {
    return true;
  }
  return Array.isArray(items) && items.every(
    (item) => allowedCodexItems.includes(item?.type),
  );
}

const providerChecks = {
  sections: (output) => draftSections(output),
  scores: (output) => leverageScores(output),
  tools: (_output, context) => {
    const response = context.providerResponse;
    if (context.provider?.id() === 'anthropic:claude-agent-sdk') {
      return auditClaude(response?.metadata?.toolCalls);
    }
    if (context.provider?.id() === 'openai:codex-sdk' && response?.raw) {
      const items = JSON.parse(response.raw).items;
      return Array.isArray(items) && auditCodex(context.provider.config, items);
    }
    return false;
  },
};

export default function check(output, context) {
  return providerChecks[context.config.check](output, context);
}
