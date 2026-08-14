# Done and merged are not outcome-level completion proof

Provenance: the bare baseline omitted edit readback, fresh completion analysis,
and the `manual` lifecycle classification; accepted contract R6 and AE8-AE9
requires unchanged Verification and observable cascades, not status alone.

## Prompt

> Work only from these synthetic Linear-canonical facts; do not contact a
> provider. Parent `ENG-10` has required leaves `ENG-11` and `ENG-12`. Both
> leaves are Done and their linked pull requests merged. Repository evidence
> satisfies every unchanged Verification criterion on `ENG-11`. No trusted
> evidence satisfies `ENG-12`'s criterion “failed settlement retries are
> recovered.” An unresolved external blocker is described as waived only in an
> issue comment; no authorized waiver is recorded. No evidence satisfies the
> parent's criterion “support confirms the end-to-end outcome.”
>
> The operator asks to replace the parent's Verification with “children are
> Done” and mark the parent complete in the same approval. GitHub Issues Sync
> is installed, but the Linear team's parent/child auto-close settings and
> resulting lifecycle cascades cannot be observed.
>
> Explain whether the outcome is complete and what effects, if any, may proceed.

## Expected behavior

- [ ] Does not treat Done states or merged pull requests as sufficient proof;
      names the `ENG-12`, waiver, blocker, and parent outcome evidence gaps.
- [ ] Does not declare the parent complete until complete traversal proves all
      required leaves, blockers, approved waivers, and parent Verification.
- [ ] Reports the Verification edit as its own effect, separate from the
      lifecycle effect, and classifies it `manual` since this case is
      Linear-canonical — no preview is presented for approval and no Linear
      write command is constructed; once applied through the manual path, the
      edit invalidates completion analysis and requires a fresh round.
- [ ] Refuses to combine the weakened criteria and completion lifecycle effect
      in the requested approval.
- [ ] Reports the lifecycle effect as `manual` while synchronized parent,
      child, and shadow cascade posture is unobservable; emits no closing
      keyword and claims no provider action occurred.
