# Wake Timer

Load this reference whenever checking, deduplicating, arming, or stopping the
Captain's wake timer, including when a duplicate Captain stands down in Step 1
of `SKILL.md` before stopping any timer.

## Idle-safe timer rule

The timer belongs to the Captain's own session. A scheduler that starts a new
session would be a second Captain. The wake prompt never names a pull request
number or dispatch ID; each wake rediscovers them.

Between wakes the Captain ends its turn, and Orca must show it `done`. While
a session shows `working`, Orca holds the operator's messages, and the Steer
that forces one through can cancel the timer. Keep exactly one recurring
timer that the harness does not report to Orca as unfinished work, and always
inspect and deduplicate live timers before arming a new one.

Never use Antigravity's `DurationSeconds` or a cron without `IsDaemon`,
Codex's `clock.sleep`, or Claude Code's `CronCreate`, `/loop`, `Monitor`, or
background shells. Each keeps the session `working` while it runs.

## Per-harness scheduling and PID ownership

- **Antigravity:** Always inspect active tasks with `manage_task` list before
  calling `schedule`. If `manage_task` list omits a candidate scheduled task's
  prompt or `IsDaemon` metadata, inspect that candidate with `manage_task`
  status. Filter strictly to tasks carrying the Captain's wake prompt and
  leave unrelated background tasks untouched:
  - **Normal wake (sole Captain confirmed, nonzero active counts):** stop any
    non-daemon or one-shot task carrying the wake prompt with `manage_task`
    kill. If one or more valid daemon (`IsDaemon: true`) wake timers are
    running, keep one (preferring the TaskId recorded in `state.md` — and
    retaining that active recorded TaskId rather than killing and re-arming it
    if list/status does not surface `IsDaemon`), kill any duplicate wake
    timers, and update `state.md` only if the retained TaskId changed. Only
    when zero valid wake timers exist, arm one with `schedule`
    (`CronExpression: "*/30 * * * *"`, `IsDaemon: true`) and record its task
    ID in `state.md`.
  - **Stop at zero (sole Captain confirmed, all counts zero):** stop every
    Captain wake timer in `manage_task` list with `manage_task` kill and clear
    the timer ID from `state.md`.
  - **Stand-down (Step 1 duplicate Captain):** stop only Captain wake timers
    in this conversation's own `manage_task` list and write nothing to
    `state.md`.
- **Claude Code and Codex:** the detached wake loop below. Always verify
  `[ -n "$state" ] && [ -n "$ORCA_TERMINAL_HANDLE" ]` before scanning or
  stopping any process. Do not rely on `cat "$state/wake.pid"` alone, because
  a race or interrupted restart can leave an earlier duplicate loop running.
  Instead scan the current user's processes with
  `ps -ww -u "$(id -u)" -o pid=,args=` (excluding both `$$` and `$PPID`) for
  `sh -c` wake loops whose command line carries the wake prompt and whose
  trailing arguments (after stripping trailing whitespace) end with the exact
  `wake "$state" <handle>` token pair, comparing `<handle>` by exact string
  equality against `$ORCA_TERMINAL_HANDLE` (never a substring glob that could
  confuse `term-1` with `term-10`, and never an un-delimited `$state` match
  that could collide with a sibling repository):
  - **Normal wake (sole Captain confirmed, nonzero active counts):** `kill`
    any matching wake loop whose exact trailing handle differs from
    `$ORCA_TERMINAL_HANDLE` (left by an earlier replaced Captain). Among
    matching loops carrying this session's exact `$ORCA_TERMINAL_HANDLE`, if
    one or more exist, keep one (preferring the PID in `$state/wake.pid`),
    `kill` any extras, and atomically sync `$state/wake.pid` without launching
    another loop. Launch the detached loop below only when zero valid loops
    match this session's exact handle.
  - **Stop at zero (sole Captain confirmed, all counts zero):** `kill` every
    matching wake loop for `$state` (this session's handle and any orphaned
    stale handles) and `rm -f "$state/wake.pid"`.
  - **Stand-down (Step 1 duplicate Captain):** `kill` only matching wake loops
    whose exact trailing handle equals this session's own
    `$ORCA_TERMINAL_HANDLE`. Never `kill` a loop carrying another handle and
    never modify or delete `$state/wake.pid`, because both belong to the live
    Captain.
  - **Never `kill` a PID whose command line is not a wake loop's**, because
    the PID may now belong to another process.
  - Because `setsid -f` returns before the child writes `wake.pid`, verify
    startup through the bounded wait in the launch snippet below; if that
    check fails, no timer is running.
- **Other harnesses (non-Antigravity, non-Claude Code, non-Codex):**
  - First prefer a native recurring daemon timer owned by this session that
    returns the session to idle (`done` in Orca) between wakes without
    spawning a new session. Always inspect and deduplicate live timers before
    arming, record the retained timer ID in `state.md`, and clear it when
    stopped (never editing `state.md` on stand-down).
  - If the harness has no native idle-safe recurring timer and runs in a POSIX
    shell with `$ORCA_TERMINAL_HANDLE`, use the detached wake loop and
    current-user `ps` deduplication rules above (`setsid` on Linux, or another
    new-session detacher on systems without `setsid`), enforcing the same
    non-empty variable guards, exact trailing token matching, atomic
    `wake.pid` write, and bounded startup verification.
  - If neither a native idle-safe daemon timer nor a detached external wake
    loop is available, do not fall back to an in-turn sleep or polling loop
    that holds the session `working`. Record the limitation as a `Decision`
    entry in `Open decisions` in `state.md` and report to the operator that
    manual wakes or an external session-targeted trigger are needed.

## Detached wake loop

The wake loop runs outside the harness and types the wake prompt into the
Captain's own terminal; the Orca guide allows `orca terminal send` into your
own pane. Start it in a new session, because Codex ends a plain background
job when the command that started it returns. `setsid` comes with Linux; on a
system without it, start the loop in a new session another way. With `$state`
set to the state folder and after the live `ps` scan confirms zero loops are
running for `"$state"` and `"$ORCA_TERMINAL_HANDLE"`:

```sh
[ -n "$state" ] && [ -n "$ORCA_TERMINAL_HANDLE" ] &&
rm -f "$state/wake.pid" &&
setsid -f sh -c 'tmp="$1/wake.pid.$$"
  printf "%s\n" "$$" > "$tmp" && mv -f "$tmp" "$1/wake.pid" || { rm -f "$tmp"; exit 1; }
  while sleep 1800; do
    out=$(orca terminal send --terminal "$2" --enter --json \
      --text "Wake: run the repo-captain wake routine." 2>&1) && continue
    case $out in
      *terminal_not_writable*|*terminal_handle_stale*) exit 0 ;;
    esac
  done' wake "$state" "$ORCA_TERMINAL_HANDLE" </dev/null >/dev/null 2>&1 &&
{
  i=0
  while [ "$i" -lt 20 ]; do
    if [ -s "$state/wake.pid" ]; then
      pid=$(cat "$state/wake.pid")
      uid=$(ps -o uid= -p "$pid" 2>/dev/null | tr -d '[:space:]')
      if [ "$uid" = "$(id -u)" ]; then
        args=$(ps -ww -o args= -p "$pid" 2>/dev/null | sed 's/[[:space:]]*$//')
        case $args in
          *"Wake: run the repo-captain wake routine."*" wake $state $ORCA_TERMINAL_HANDLE") break ;;
        esac
      fi
    fi
    i=$((i + 1))
    sleep 0.1
  done
  [ "$i" -lt 20 ]
}
```

The child writes `wake.pid` atomically before entering the loop, and the
bounded wait confirms that the new process is running for this exact state
folder and terminal handle before returning success. The loop exits on its own
once Orca reports the Captain's terminal closed or unknown. Any other failed
send, such as Orca restarting, is retried at the next interval.
