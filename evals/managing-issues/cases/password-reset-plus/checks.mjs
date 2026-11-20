import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const headings = ['Problem', 'Scope', 'Verification'];
const factors = ['Impact', 'Confidence', 'Verification effort', 'Undo cost'];

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

export function auditCodex(items) {
  if (!Array.isArray(items)) {
    return false;
  }
  const commands = [];
  for (const item of items) {
    switch (item.type) {
      case 'agent_message':
      case 'reasoning':
      case 'todo_list':
        break;
      case 'command_execution':
        commands.push(item.command);
        break;
      default:
        return false;
    }
  }
  const audit = fileURLToPath(new URL('./audit-shell.py', import.meta.url));
  return spawnSync('python3', ['-I', audit], {
    input: JSON.stringify(commands),
  }).status === 0;
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
      return auditCodex(JSON.parse(response.raw).items);
    }
    return false;
  },
};

export default function check(output, context) {
  return providerChecks[context.config.check](output, context);
}
