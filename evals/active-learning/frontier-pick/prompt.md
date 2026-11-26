---
tags: [active-learning]
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, WebSearch, WebFetch]
---

My vault is ./vault. Earlier you gave me this frontier for distributed systems, the things beyond my notes:

1. Fencing tokens: how a storage service rejects writes from a client whose lock has expired.
2. Leases and clock drift: why a lock with a timeout is only as safe as the clocks involved.
3. Consensus with Raft: how a group of nodes agrees on one log despite failures.
4. Vector clocks: tracking which events happened before which without a shared clock.
5. Exactly-once versus effectively-once processing.

For each one you asked: learn it now, add it to To Explore, or skip it.

Let's learn fencing tokens.
