# Relationship Contract

Read this reference before interpreting a Person note, direct contact, cadence,
or durable relationship meaning.

## Use the target Person contract

The operational metadata is identity plus:

- `status`: `active`, `dormant`, `reference`, or `ended`;
- `tier`: `5-inner-circle`, `15-close`, `50-regular`, `150-meaningful`, or
  `500-weak-tie`; and
- `date_last_contacted`: the best reliable local date of substantive direct
  contact.

Active and dormant relationships require a tier. Reference relationships may
omit it. Ended relationships may preserve a known tier but do not require one.
An unknown reliable contact date may remain empty.

Use stable prose anchors for what the person cares about, their expertise,
their current focus, and ways the user and person may help each other. Preserve
ordinary project links and wikilinks as context, not CRM classification. Keep
dated Comments concise, specific, and forward chronological.

Completion: every target-form note has valid conditional fields and exposes
durable meaning without copying raw interaction history.

## Distinguish contact from ambient activity

A substantive direct contact is an exchange or directed attempt that could
reasonably maintain the relationship: an in-person conversation, direct
message, email, targeted group exchange, or unanswered outgoing direct
message. Passive likes, reactions, broadcasts, merely sharing a room, bulk
announcements, and observing someone else's update do not count.

Advance `date_last_contacted` monotonically. If the canonical date is newer
than or equal to the observed local date, report **Already satisfied** and do
not rewrite the note. Multiple sources describing the same interaction support
one contact observation, not several touches.

Completion: every contact proposal represents one safely identified direct
interaction and never moves the canonical date backward.

## Store only relationship-load-bearing meaning

Information is relationship-load-bearing when it is likely to change a future
interaction: a stable preference, meaningful life or work change, commitment,
sensitivity, shared context, current focus, or fact that improves how the user
can prepare, help, or avoid harm. Propose the smallest prose or Comment change
that preserves that meaning.

Small talk, raw transcripts, touch-by-touch history, passive activity, facts
already present, and short-lived details with no plausible future use stay in
their source. A promise with a specific follow-up date creates a separate Task
effect; the date does not go into Person metadata or prose.

Completion: each proposed prose change has a named future relationship use and
contains no source archive or duplicate commitment.

## Derive cadence only for active relationships

Maximum silence is derived from tier:

| Tier | Maximum silence |
| --- | --- |
| `5-inner-circle` | 7 days |
| `15-close` | 30 days |
| `50-regular` | 90 days |
| `150-meaningful` | 180 days |
| `500-weak-tie` | No fixed cadence |

Only `active` people appear in routine overdue review. `dormant`, `reference`,
and `ended` do not. Any status, including reference, may still surface when a
strong contextual reason and plausible useful action make the person relevant
now. Most deliberate cadence scans belong in configured morning or weekly
reviews; another workflow surfaces an overdue person only when that person is
already relevant to its current context.

Crossing a threshold is evidence to assess, not an outreach requirement. A
plausible useful action names what the user could do, why now, and how it might
benefit the relationship or current work; "check in because overdue" alone is
not enough.

Completion: cadence produces only justified active exceptions, while strong
contextual relevance remains available across statuses.

## Read mixed schemas without writing legacy fields

During transition, map numeric tiers `5`, `15`, `50`, `150`, and `500` to their
labeled equivalents for reads. Keep legacy `sphere`, `next_touch`, tier `0`,
tier `1500`, and Non-Contact values visible so records are not silently lost,
but do not write them into a converted or new note.

Convert a retained note only through person-level reviewed effects. Preserve
unrelated metadata, aliases, manual prose, links, embeds, and Comments. Before
removing a populated future `next_touch`, find or propose its equivalent
canonical Task. Remove the field only after that Task is **Applied** or
**Already satisfied**, or after the user explicitly rejects the commitment.

A partial or indeterminate conversion is not converted. Keep dependent cleanup
blocked until a reviewed repair and full CLI readback establish the complete
target contract. Legacy compatibility may be removed only after an
authoritative CLI query returns zero legacy Person notes.

Completion: legacy and target notes remain discoverable, and every converted
note preserves meaning and any unresolved commitment.
