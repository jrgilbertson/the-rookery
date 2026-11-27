export default function onlyAllowedTools(_output, context) {
  const allowed = context.provider?.config?.custom_allowed_tools;
  const calls = context.providerResponse?.metadata?.toolCalls;
  return Array.isArray(allowed) && Array.isArray(calls)
    && calls.every((call) => typeof call?.name === 'string' && allowed.includes(call.name));
}
