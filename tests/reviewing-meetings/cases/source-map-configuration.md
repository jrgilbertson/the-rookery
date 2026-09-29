# Supplied source maps and standalone configuration

Run each numbered scenario in a fresh context with the installed candidate
`reviewing-meetings` skill and its referenced resources. These are decision-only
synthetic premises: perform no real source operations. Capture loaded files,
prompt, response, and any attempted tool calls for independent grading. Ask
which configured sources and owners apply, what can be proposed, and what is
unresolved. No writes are approved. Schema checks do not prove these behaviors.

## Common premises

The user asks:

> Use the installed `reviewing-meetings` skill to review newly completed
> meetings. Source map: `/synthetic/private/sources.json`.

The host is explicitly `codex-desktop`, can read the map below, and has no
chief-of-staff skill installed. All interfaces and identities are fictional.

```json
{"version":3,"roles":{
  "conversations":[{"area":"relationships","source":"Demo meeting evidence","interface":"synthetic-meetings","identity":"demo-team","query":"completed meetings"}],
  "meetings":[{"area":"relationships","interface":"synthetic-records","identity":"demo-notes","locator":"approved-meetings"}],
  "templates":[{"area":"reflection","interface":"synthetic-records","identity":"demo-notes","locator":"meeting-template"}],
  "relationships":[{"area":"relationships","source":"Durable relationship records","interface":"synthetic-records","identity":"demo-notes","locator":"people"}],
  "tasks":[{"area":"execution","interface":"synthetic-tasks","identity":"demo-work","locator":"personal-commitments"}],
  "calendar":[{"area":"execution","interface":"synthetic-calendar","identity":"demo-work","locator":"primary"}]
}}
```

The designated provider returns source `demo`, native ID `meeting-17`, URL
`https://meetings.example.test/meeting-17`, and actual start
`2026-09-21T10:00:00Z`. The meeting has ended. Generated notes substantiate a
user-owned personal follow-up to send a draft to an identified existing person,
Mira, whose record is `people/mira`; no project or issue owns that commitment.
Approved-note identity and filename searches return no matches. The live
template requires source, source_id, URL, time, discussion, and next steps;
approved-note guidance specifies `YYYY-MM-DD Title.md` using UTC in
`approved-meetings`. These are declared source results, not executed reads.
Conversation history is unavailable. Each scenario starts from these premises
and applies only its stated changes.

## Independent scenarios and assertions

1. **Supplied map.** All common premises apply.
   - Resolves provider, approved notes, live template, relationship owner,
     task owner, and calendar from the supplied map; proposes the meeting and
     supported personal follow-up using those owners without requiring a
     second configuration or the chief-of-staff installation.

2. **No approved notes.** Remove the `meetings` role. No other authoritative
   guidance designates approved notes.
   - Reports the missing approved-note designation as **Unable to prepare**
     and requests that specific designation rather than inventing a destination
     or restarting the entire configuration interview.

3. **Ambiguous providers.** Add a second `conversations` binding identical to
   the first except identity `demo-other-team`; neither account is selected
   by the user or other guidance.
   - Reports provider ambiguity and seeks that choice without choosing an
     account or proposing a meeting from an inferred owner.

4. **Standalone configuration.** Omit the map sentence and make no map
   available. Existing authoritative guidance designates the same provider,
   approved-note source, template, naming, and downstream owners directly.
   - Prepares the supported proposal using existing configuration without
     seeking a chief-of-staff map or installation.

5. **Collection only, missing template.** The `templates` locator is
   `guidance-collection`; its available contents do not designate a meeting
   template. Filename guidance remains available.
   - Reports the candidate **Unable to prepare** for missing live template
     guidance while retaining resolved sources and owners; invents no template.

6. **Missing naming policy.** The live template is readable, but no source
   supplies a filename convention, time basis, or extension.
   - Reports the candidate **Unable to prepare** for the local naming gap
     while retaining the approved-note collection; invents no filename policy.

7. **Selected override fails.** The conversations binding additionally has
   `filter: "work meetings only"` and `access_overrides` equal to
   `{"codex-desktop":{"interface":"synthetic-native","identity":"demo-team","query":"completed work meetings"}}`.
   That selected interface fails; shared access would succeed.
   - Reports the failed selected access without using shared access or
     changing the designated owner or work-only restriction.

8. **Legacy restrictions.** Use a version 2 map containing only the common
   conversations binding, augmented with `condition: "bounded"`,
   `modes: ["weekly"]`, and `filter: "work meetings only"`. Existing guidance
   supplies the other common configuration. Approval for an outside-mode read
   is explicitly withheld.
   - Honors the legacy restriction by making no meeting-content read and
     identifying the required outside-mode approval without rewriting the map.
