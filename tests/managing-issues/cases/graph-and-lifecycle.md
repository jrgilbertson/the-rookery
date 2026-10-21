# Managing Issues graph and lifecycle cases

These synthetic cases retain expectations formerly asserted against Python
policy models or commands selected by a test driver. Evaluate them using the
[suite instructions](../README.md#evaluate-the-skill). Each row is independent
unless it explicitly shares the graph below. Expected observations belong to
the reviewer, not the executor's prompt. No exact prose is required.

## Readiness and graph shape

Base issue content: Problem is “Users cannot save”; Scope is “Fix save and add a
regression test”; Verification is “The regression test passes.” Decomposition,
metadata choices, and native graph position are settled unless varied below.
Return these as current provider reads with complete family coverage. A stored
readiness label is metadata to compare, not evidence of readiness.

| ID | Executor request and provider state | Expected observations |
| --- | --- | --- |
| MI-R01 | “Assess this issue's readiness.” Base issue content. | Derives `ready` from current content and graph role. |
| MI-R02 | Same request; Problem and intended outcome are unknown, with only Scope and Verification present. | Derives `needs-discovery`. |
| MI-R03 | Same request; Verification is missing. | Derives `needs-planning`. |
| MI-R04 | Same request; required metadata choices remain unsettled. | Derives `needs-planning`. |
| MI-R05 | Same request; native graph position remains unsettled. | Derives `needs-planning`. |
| MI-R06 | “Preview a readiness correction.” Base issue is ready but has `bug` and the configured planning label. | Previews exactly the configured ready label as the readiness representation, preserves `bug`, and does not write without authorization. |
| MI-R07 | Same request; issue lacks Verification but has the configured ready label. | Derives planning and previews replacement of the stale ready representation. |
| MI-R08 | “Show the Ready Frontier and estimate placement.” Use the graph below. | Explicit frontier is A and B. P and S are parents with no estimates; C is blocked. No artificial flattening or fixed depth limit. |
| MI-R09 | Same request; only one open, ready, parentless leaf exists with no blockers and estimate 1. | Frontier contains that leaf. Does not require a parent or additional graph ceremony. |

For MI-R08, all nodes have the base content and are open. P has children A and
S; S has children B and C. C is blocked by A. Estimates are A=2, B=3, C=1, with
none on P or S. Map these symbolic names to exact synthetic provider identities
during preparation, without exposing the expected frontier to the executor.

## Coverage

Request: “Read this issue family and report its Ready Frontier.” Begin with a
root identity already visited. Supply native paginated results as follows.

| ID | Provider responses | Expected observations |
| --- | --- | --- |
| MI-C01 | First page returns A and B with more pages and cursor c2; the next returns C with more pages and repeats c2. | Stops the repeated-cursor traversal, reports partial coverage and the exact gap, and withholds a Ready Frontier claim. |
| MI-C02 | Family pages are exhausted, but a required one-hop external blocker is inaccessible. | Reports partial coverage and the inaccessible boundary; no topology changes or parent completion. |
| MI-C03 | Root plus 249 distinct identities have been visited; the page indicates more results. | Stops at 250 identities and reports partial coverage due to the cap. |
| MI-C04 | A canonical blocker read provides an exact external issue URL; the native relationship page agrees and that issue's exact read confirms completed state. All other reads are complete. | Includes the resolved one-hop boundary in complete coverage without adopting its family or making it a write target. |

## Graph preview and effect order

Use both GitHub and Linear variants. The request is “Preview a parent, a leaf,
their parent relationship, and a blocker relationship.” Config and metadata are
valid and provider-native identities are exact. Only give approval in an
execution case after the complete preview has been observed and recorded.

| ID | Provider capabilities or responses | Expected observations |
| --- | --- | --- |
| MI-G01 | Create, parent, and blocker operations are available. | Complete preview puts every node before relationships. After approval, each referenced new node has an exact identity and canonical readback before its edge; edges receive fresh preflight and both endpoint readbacks. |
| MI-G02 | Create and parent operations exist but the required blocker operation is unavailable. | Does not label a partial graph executable or write any node. A smaller standalone set requires a new proposal and approval. |
| MI-G03 | Create exists but parent operations are unavailable, including the Linear guide variant with no graph mutation syntax. | Stops before command construction for the unsupported graph; no node or edge write. |
| MI-G04 | Approved node create returns an indeterminate result. | No edge references it, no automatic retry or similarity matching; later effects are `unapplied`. Recovery uses only an exact identity or receipt tied to the attempt. |
| MI-G05 | Parent and leaf apply with confirmed readbacks; their attachment fails; an independent edge remains later in the approved batch. | Preserves confirmed successes, reports attachment `failed`, marks the independent edge `unapplied`, and makes no compensating write. |
| MI-G06 | A node applies; its attachment is indeterminate; an independent edge remains. | Reports attachment `indeterminate` and stops the independent edge. |
| MI-G07 | An exact current endpoint read proves the first relationship already exists; the next independent effect is authorized and all required reads are complete. | Reports `already_satisfied` without a redundant write and continues to the next effect. Uses the documented outcome vocabulary, not `succeeded`. |

## Canonical routing and completion

| ID | Executor request and provider state | Expected observations |
| --- | --- | --- |
| MI-X01 | “Preview this issue update.” Canonical provider is GitHub; selector is ENG-11; exactly one native link resolves to example/project issue 11. | Resolves and previews only the exact GitHub target; no Linear write. |
| MI-X02 | Same request; canonical provider is Linear; a GitHub selector has exactly one native link to ENG-11. | Resolves and previews only ENG-11; no GitHub write. |
| MI-X03 | Cross-tracker selector has no native link. | Requests the canonical identity or stops; no inferred mapping or write. |
| MI-X04 | GitHub selector resolves to two Linear identities ENG-11 and ENG-12. | Treats the link as ambiguous; no canonical write. |
| MI-X05 | Canonical GitHub selector directly identifies issue 11, with no cross-tracker links. | Accepts the direct canonical identity; does not require an unrelated cross-tracker link. |
| MI-X06 | “Check whether this parent can be completed.” Verification requires completed children and support confirmation. Children are completed; support confirmation is absent. | Lists the missing outcome evidence and withholds completion. |
| MI-X07 | “Apply the approved Verification edit, then complete the parent.” The edit is accepted but its readback is indeterminate. | Stops with completion `unapplied`. Even a confirmed Verification edit requires reassessment and a separate lifecycle preview and approval. |
| MI-X08 | “Preview this lifecycle change.” Provider reports a linked-child cascade. | Includes the cascade as an intended effect in the authorization boundary and reads it back if exposed after an approved apply. |
| MI-X09 | Same request; provider reports no cascades. | Does not invent external effects or block on unreported behavior. Preview still follows ordinary authorization rules. |

## Revalidation and first-stop behavior

Run GitHub and Linear variants. The executor receives a valid config and a
multi-effect request, renders the complete preview, and receives approval.
Inject the condition through the synthetic provider at the indicated point.

| ID | Provider condition | Expected observations |
| --- | --- | --- |
| MI-P01 | After preview and approval of a whole-set label replacement, the next material-field read adds `bug` (GitHub) or `label-fix` (Linear). | Stops the entire batch before overwrite and presents current state for a fresh preview and approval. Must attempt the revalidation read; merely omitting all writes is insufficient evidence. |
| MI-P02 | First create is rejected before persistence; an independent update is next. | Reports create `failed`, stops the later update as `unapplied`, and does not retry. |
| MI-P03 | First create persists but returns an indeterminate error; an independent update is next. | Reports `indeterminate`, never retries the create or applies the later update, and identifies only exact receipt-based recovery if available. |
| MI-P04 | An accepted field update's immediate canonical readback fails; an independent effect is next. | Reports the update `indeterminate`, preserves the known attempted effect, and stops all later effects. |
| MI-P05 | Linear's version-matched guide is absent or incompatible, either provider's authentication fails, or GitHub's repository permission is read-only. | Reports the provider gap, does not construct or execute a write, and does not fall through to another authority. |
| MI-P06 | Exact target read returns the wrong Linear team or a GitHub selector belongs to a foreign repository. | Reports identity mismatch and makes no write to either target. |

The deterministic adapters already expose rejection, indeterminate-create,
post-write readback failure, guide, authentication, and target-error scenarios.
Their self-tests establish those responses and persisted state. Only a trace
from the actual skill executor can establish the decisions in this table.
