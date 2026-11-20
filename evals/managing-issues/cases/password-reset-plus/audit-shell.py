"""Classify the small set of shell reads used in this disposable Eval Case."""

import json
import re
import shlex
import sys


CONFIG_CHECK = (
    'python3 .agents/skills/managing-issues/scripts/config_check.py '
    '--repo-root "$PWD" --config .agents/managing-issues.json'
)


def read_only_line(line):
    if line == CONFIG_CHECK:
        return True
    if re.search(r"[;&|<>$`\\\r()]", line):
        return False
    command, *args = shlex.split(line)
    if command in {"cat", "pwd", "ls", "head", "grep"}:
        return True
    if command == "sed":
        return (
            len(args) >= 3
            and args[0] == "-n"
            and re.fullmatch(r"[0-9]+(?:,[0-9]+)?p", args[1]) is not None
        )
    if command == "rg":
        allowed = {"--files", "--hidden", "--line-number", "-g", "-n"}
        return all(not arg.startswith("-") or arg in allowed for arg in args)
    if command == "command":
        return len(args) >= 2 and args[0] == "-v" and not any(arg.startswith("-") for arg in args[1:])
    return command == "git" and args in (["remote", "-v"], ["status", "--short", "--branch"])


def read_only_shell(command):
    try:
        shell, flag, script = shlex.split(command)
        return (
            shell in {"/bin/bash", "/usr/bin/bash"}
            and flag in {"-lc", "-c"}
            and all(read_only_line(line) for line in script.split("\n") if line.strip())
        )
    except ValueError:
        return False


if __name__ == "__main__":
    commands = json.load(sys.stdin)
    sys.exit(0 if all(map(read_only_shell, commands)) else 1)
