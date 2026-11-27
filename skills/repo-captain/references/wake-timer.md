# Wake Timer

Load this reference whenever checking, arming, or stopping the Captain's wake
timer, including when a duplicate Captain stands down in Step 1 of `SKILL.md`
before stopping any timer.

## Idle-safe timer rule

The timer belongs to the Captain's own session. A scheduler that starts a new
session would be a second Captain. The wake prompt never names a pull request
number or dispatch ID; each wake rediscovers them.

Between wakes the Captain ends its turn, and Orca must show it `done`. While
a session shows `working`, Orca holds the operator's messages, and the Steer
that forces one through can cancel the timer. Keep exactly one recurring
timer that the harness does not report to Orca as unfinished work.

Never use Antigravity's `DurationSeconds` or a cron without `IsDaemon`,
Codex's `clock.sleep`, or Claude Code's `CronCreate`, `/loop`, `Monitor`, or
background shells. Each keeps the session `working` while it runs.

## Per-harness scheduling and PID ownership

- **Antigravity:** `schedule` with `CronExpression: "*/30 * * * *"` and
  `IsDaemon: true`. Record the task ID in `state.md`. Check it with
  `manage_task` list and stop it with `manage_task` kill.
- **Claude Code and Codex:** the detached wake loop below. Read its command
  line with `ps -ww -o args= -p "$(cat "$state/wake.pid")"`. A wake loop's
  line shows the wake prompt and the state folder. It is this session's timer
  only when it also shows this session's `$ORCA_TERMINAL_HANDLE`:
  - **When a live Captain replaces an earlier one:** a wake loop whose command
    line shows the wake prompt, the state folder, and another handle was left
    by an earlier Captain session; `kill` it before starting a new one.
  - **When a duplicate Captain stands down in Step 1:** stop a wake loop only
    when its command line shows this session's own `$ORCA_TERMINAL_HANDLE`.
    Never stop a wake loop carrying another handle, because that loop belongs
    to the live Captain.
  - **Never `kill` a PID whose command line is not a wake loop's**, because
    the PID may now belong to another process.
  - Because `setsid -f` returns before the child writes `wake.pid`, verify
    startup through the bounded wait in the launch snippet below; if that
    check fails, no timer is running.
- **Other harnesses (non-Antigravity, non-Claude Code, non-Codex):**
  - First prefer a native recurring daemon timer owned by this session that
    returns the session to idle (`done` in Orca) between wakes without
    spawning a new session, and record its timer ID in `state.md`.
  - If the harness has no native idle-safe recurring timer and runs in a POSIX
    shell with `$ORCA_TERMINAL_HANDLE`, use the detached wake loop below
    (`setsid` on Linux, or another new-session detacher on systems without
    `setsid`), enforcing the same atomic `wake.pid` write, handle-matching
    command-line ownership check, and bounded startup verification.
  - If neither a native idle-safe daemon timer nor a detached external wake
    loop is available, do not fall back to an in-turn sleep or polling loop
    that holds the session `working`. Record the limitation as an open
    decision in `state.md` and report to the operator that manual wakes or an
    external session-targeted trigger are needed.

## Detached wake loop

The wake loop runs outside the harness and types the wake prompt into the
Captain's own terminal; the Orca guide allows `orca terminal send` into your
own pane. Start it in a new session, because Codex ends a plain background
job when the command that started it returns. `setsid` comes with Linux; on a
system without it, start the loop in a new session another way. With `$state`
set to the state folder:

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
      args=$(ps -ww -o args= -p "$pid" 2>/dev/null)
      case $args in
        *"Wake: run the repo-captain wake routine."*"$state"*"$ORCA_TERMINAL_HANDLE"*) break ;;
      esac
    fi
    i=$((i + 1))
    sleep 0.1
  done
  [ "$i" -lt 20 ]
}
```

The child writes `wake.pid` atomically before entering the loop, and the
bounded wait confirms that the new process is running for this session before
returning success. The loop exits on its own once Orca reports the Captain's
terminal closed or unknown. Any other failed send, such as Orca restarting,
is retried at the next interval.
