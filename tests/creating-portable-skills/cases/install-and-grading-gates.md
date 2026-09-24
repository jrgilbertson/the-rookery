# Unrun install checks and the choice of grader

Provenance: regression control for the install-smoke completion gate and
independent cross-model grading contract. The 2026-09-23 final package review
originally added this case after finding both contracts untested.

## Prompt

> I revised the instructions in my `expense-notes` skill and changed its
> packaging.
> Two questions.
>
> 1. The install smoke check passed on one of my two roster harnesses. The
>    other harness isn't installed on this machine, so its check couldn't
>    run. Can I mark the packaging step complete?
> 2. Who should grade the with-and-without comparison, how should grading
>    of each pair be assigned, and what should the grader know about which
>    variant produced each output? I wrote the revision and generated both
>    variants' outputs with the same model I'd normally grade with, and I also
>    have access to a second vendor's model.

## Expected behavior

- [ ] (1) Says packaging cannot be marked complete yet: the second harness
      needs either a smoke pass or a logged "not run" together with the
      user's logged decision to ship without it.
- [ ] (2) Recommends that one grader score both outputs of each case's
      matched pair (baseline and revised, or without-skill and with-skill).
- [ ] (2) Says the grader sees the outputs labeled neutrally, without knowing
      which variant is which.
- [ ] (2) Recommends the second vendor's model as the grader because it is a
      different model from the one that wrote the revision or the outputs.
