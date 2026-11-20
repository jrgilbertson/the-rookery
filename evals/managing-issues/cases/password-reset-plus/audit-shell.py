"""Fail only shell commands that could perform a tracker, network, or file write."""

import json
import re
import shlex
import sys


SHELL_WRAPPERS = {"/bin/bash", "/usr/bin/bash", "bash", "/bin/sh", "/usr/bin/sh", "sh"}

FILE_WRITE_COMMANDS = {
    "rm",
    "rmdir",
    "unlink",
    "shred",
    "mv",
    "cp",
    "install",
    "touch",
    "mkdir",
    "mktemp",
    "truncate",
    "dd",
    "tee",
    "ln",
    "chmod",
    "chown",
    "chgrp",
    "patch",
    "sponge",
    "ed",
    "ex",
    "eval",
}

NETWORK_WRITE_COMMANDS = {
    "nc",
    "ncat",
    "socat",
    "ssh",
    "scp",
    "rsync",
    "sftp",
    "ftp",
    "http",
    "httpie",
    "xh",
}

GH_WRITE_VERBS = {
    "create",
    "edit",
    "delete",
    "close",
    "reopen",
    "merge",
    "comment",
    "review",
    "ready",
    "update",
    "set",
    "add",
    "remove",
    "archive",
    "transfer",
    "upload",
    "rename",
    "clone",
    "link",
    "unlink",
    "pin",
    "unpin",
    "lock",
    "unlock",
    "develop",
    "item-add",
    "item-create",
    "item-edit",
    "item-delete",
    "item-archive",
    "field-create",
    "field-delete",
}

TRACKER_CLI_COMMANDS = {"orca", "orca-ide", "orca-dev", "linear"}
TRACKER_WRITE_VERBS = {
    "create",
    "update",
    "edit",
    "delete",
    "cancel",
    "close",
    "reopen",
    "comment",
    "link",
    "unlink",
    "add",
    "remove",
    "set",
    "archive",
    "move",
    "assign",
    "save",
    "send",
    "reply",
    "start",
    "stop",
    "kill",
    "dispatch",
    "merge",
    "push",
    "submit",
    "apply",
    "write",
}

GIT_WRITE_SUBCOMMANDS = {
    "add",
    "am",
    "apply",
    "checkout",
    "cherry-pick",
    "clean",
    "clone",
    "commit",
    "fetch",
    "init",
    "merge",
    "mv",
    "pull",
    "push",
    "rebase",
    "reset",
    "restore",
    "revert",
    "rm",
    "stash",
    "switch",
    "tag",
}

PKG_WRITE_SUBCOMMANDS = {
    "add",
    "install",
    "publish",
    "remove",
    "run",
    "uninstall",
    "update",
    "upgrade",
}

INLINE_CODE_WRITE_RE = re.compile(
    r"""
    \b(?:
        subprocess|
        child_process|
        urllib|
        requests|
        http\.client|
        httpx|
        aiohttp|
        socket
    )\b
    | \bos\.(?:system|popen|remove|unlink|rmdir|mkdir|makedirs|rename|replace|chmod|chown|truncate|write|open)\b
    | \bshutil\.(?:rmtree|copy|copy2|copyfile|copytree|move|make_archive)\b
    | \.(?:write_text|write_bytes|unlink|rmdir|mkdir|rename|replace|touch|chmod)\s*\(
    | \bopen\s*\([^)]*['"][^'"]*[wax+][^'"]*['"]
    | \bfs\.(?:writeFile|appendFile|rm|unlink|mkdir|rename|copyFile|chmod|chown)
    | \bfetch\s*\(
    """,
    re.VERBOSE,
)

SEPARATOR_TOKENS = {";", "&&", "||", "|", "&", "\n"}


def unwrap_shell(command):
    try:
        parts = shlex.split(command)
    except ValueError:
        return None
    if len(parts) == 3 and parts[0] in SHELL_WRAPPERS and parts[1] in {"-lc", "-c"}:
        return parts[2]
    return command


def extract_heredocs(script):
    """Strip heredoc bodies from script and return (cleaned_script, bodies)."""
    lines = script.splitlines()
    out_lines = []
    bodies = []
    i = 0
    heredoc_re = re.compile(r"<<-?\s*(?:'([^']+)'|\"([^\"]+)\"|([A-Za-z_][A-Za-z0-9_]*))")
    while i < len(lines):
        line = lines[i]
        delims = [m.group(1) or m.group(2) or m.group(3) for m in heredoc_re.finditer(line)]
        out_lines.append(line)
        i += 1
        for delim in delims:
            body_lines = []
            while i < len(lines) and lines[i].strip() != delim:
                body_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            bodies.append("\n".join(body_lines))
    return "\n".join(out_lines), bodies


def tokenize_script(script):
    # Normalize redacted transcript placeholders like <run> so '<' and '>' are not parsed as redirects.
    normalized = re.sub(r"<([a-z][a-z0-9-]*)>", r"__placeholder_\1__", script)
    lexer = shlex.shlex(normalized, posix=True, punctuation_chars=";&|<>")
    lexer.whitespace_split = True
    lexer.whitespace = " \t\r"
    return list(lexer)


def split_segments(tokens):
    segments = []
    current = []
    for tok in tokens:
        if tok in SEPARATOR_TOKENS:
            if current:
                segments.append(current)
                current = []
        else:
            current.append(tok)
    if current:
        segments.append(current)
    return segments


def has_unsafe_redirect(segment):
    """Return True if segment contains a file-writing redirection (ignoring /dev/null and fd dups)."""
    i = 0
    while i < len(segment):
        tok = segment[i]
        # Skip heredoc / herestring / input-only redirects.
        if tok in {"<", "<<", "<<<", "<<-"}:
            i += 2
            continue
        if re.fullmatch(r"(?:[0-9]+|&)?(?:>>|>\||<>|>)(?:&[0-9]+)?", tok):
            if tok.endswith("&1") or tok.endswith("&2"):
                i += 1
                continue
            target = segment[i + 1] if i + 1 < len(segment) else ""
            if target == "/dev/null":
                i += 2
                continue
            return True
        if re.fullmatch(r"(?:[0-9]+|&)?(?:>>|>\||<>|>)/dev/null", tok):
            i += 1
            continue
        if re.fullmatch(r"(?:[0-9]+|&)?(?:>>|>\||<>|>).+", tok):
            return True
        i += 1
    return False


def strip_redirections(segment):
    cleaned = []
    i = 0
    while i < len(segment):
        tok = segment[i]
        if tok in {"<", "<<", "<<<", "<<-"} or re.fullmatch(r"(?:[0-9]+|&)?(?:>>|>\||<>|>)", tok):
            i += 2
            continue
        if re.fullmatch(r"(?:[0-9]+|&)?(?:>>|>\||<>|>).*", tok):
            i += 1
            continue
        cleaned.append(tok)
        i += 1
    return cleaned


def is_write_gh(args):
    if not args:
        return False
    sub = args[0]
    rest = args[1:]
    if sub == "api":
        method = None
        has_body = False
        is_graphql = False
        i = 0
        while i < len(rest):
            a = rest[i]
            if a == "graphql" or a.endswith("/graphql"):
                is_graphql = True
            elif a in {"-X", "--method"} and i + 1 < len(rest):
                method = rest[i + 1].upper()
                i += 1
            elif a.startswith("--method="):
                method = a.split("=", 1)[1].upper()
            elif a in {"-f", "-F", "--field", "--raw-field", "--input"} or a.startswith(
                ("--field=", "--raw-field=", "--input=")
            ):
                has_body = True
            i += 1
        if method is not None and method != "GET":
            return True
        if is_graphql:
            return any(re.search(r"\bmutation\b", a) for a in rest)
        if has_body and method != "GET":
            return True
        return False
    if sub in {"issue", "pr", "label", "project", "release", "repo"}:
        return any(a in GH_WRITE_VERBS for a in rest)
    return any(a in GH_WRITE_VERBS for a in args)


def is_write_curl(args):
    i = 0
    while i < len(args):
        a = args[i]
        if a in {"-X", "--request"} and i + 1 < len(args):
            if args[i + 1].upper() not in {"GET", "HEAD"}:
                return True
            i += 1
        elif a.startswith("--request="):
            if a.split("=", 1)[1].upper() not in {"GET", "HEAD"}:
                return True
        elif a in {
            "-d",
            "--data",
            "--data-raw",
            "--data-binary",
            "--data-urlencode",
            "--json",
            "-F",
            "--form",
            "--form-string",
            "-T",
            "--upload-file",
            "-o",
            "--output",
            "-O",
            "--remote-name",
        } or a.startswith(
            ("--data", "--json=", "--form", "--upload-file=", "--output=")
        ):
            return True
        i += 1
    return False


def is_write_wget(args):
    stdout_only = False
    i = 0
    while i < len(args):
        a = args[i]
        if a in {"--post-data", "--post-file"} or a.startswith(("--post-data=", "--post-file=")):
            return True
        if a == "--method" and i + 1 < len(args):
            if args[i + 1].upper() not in {"GET", "HEAD"}:
                return True
            i += 1
        if a.startswith("--method="):
            if a.split("=", 1)[1].upper() not in {"GET", "HEAD"}:
                return True
        if a == "-O" and i + 1 < len(args) and args[i + 1] == "-":
            stdout_only = True
            i += 1
        if a in {"-O-", "--output-document=-"}:
            stdout_only = True
        i += 1
    return not stdout_only


def is_write_sed(args):
    scripts = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-i" or a.startswith("-i") or a == "--in-place" or a.startswith("--in-place="):
            return True
        if a in {"-e", "--expression"} and i + 1 < len(args):
            scripts.append(args[i + 1])
            i += 1
        elif a.startswith("--expression="):
            scripts.append(a.split("=", 1)[1])
        elif not a.startswith("-") and not scripts:
            scripts.append(a)
        i += 1
    for s in scripts:
        # Reject write ('w') or execute ('e') sed commands.
        if re.search(r"(?:^|[;\s0-9$,!])(?:w\s+\S|e(?:\s|$))", s):
            return True
    return False


def is_write_rg(args):
    return any(a == "--pre" or a.startswith("--pre=") for a in args)


def is_write_find(args):
    unsafe = {"-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint", "-fprintf", "-fls"}
    return any(a in unsafe for a in args)


def is_write_interpreter(cmd, args, heredoc_bodies):
    i = 0
    inline_code = []
    script_path = None
    while i < len(args):
        a = args[i]
        if a in {"-c", "-e"} and i + 1 < len(args):
            inline_code.append(args[i + 1])
            i += 1
        elif a == "-":
            inline_code.extend(heredoc_bodies)
        elif not a.startswith("-") and script_path is None:
            script_path = a
        i += 1
    if inline_code:
        return any(INLINE_CODE_WRITE_RE.search(code) for code in inline_code)
    if script_path is not None:
        # Allow the bundled read-only config validator.
        if script_path.endswith("config_check.py"):
            return False
        # Other arbitrary scripts could write.
        return True
    if heredoc_bodies:
        return any(INLINE_CODE_WRITE_RE.search(code) for code in heredoc_bodies)
    return False


def is_write_segment(segment, heredoc_bodies):
    if has_unsafe_redirect(segment):
        return True
    words = strip_redirections(segment)
    # Strip leading env var assignments like FOO=bar.
    while words and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[0]):
        words = words[1:]
    if not words:
        return False
    cmd, *args = words
    base = cmd.rsplit("/", 1)[-1]

    if base in {"env", "timeout", "nice", "nohup"}:
        # Inspect wrapped command if present.
        idx = 0
        while idx < len(args) and (args[idx].startswith("-") or "=" in args[idx] or args[idx].isdigit()):
            idx += 1
        return is_write_segment(args[idx:], heredoc_bodies) if idx < len(args) else False

    if base in FILE_WRITE_COMMANDS or base in NETWORK_WRITE_COMMANDS:
        return True
    if base == "gh":
        return is_write_gh(args)
    if base in TRACKER_CLI_COMMANDS:
        return any(a in TRACKER_WRITE_VERBS for a in args)
    if base == "git":
        sub = next((a for a in args if not a.startswith("-")), None)
        if sub in GIT_WRITE_SUBCOMMANDS:
            return True
        if sub == "branch" and any(a in {"-d", "-D", "-m", "-M", "-c", "-C"} for a in args):
            return True
        if sub == "config" and any(
            a in {"--unset", "--unset-all", "--add", "--replace-all"} for a in args
        ):
            return True
        return False
    if base == "curl":
        return is_write_curl(args)
    if base == "wget":
        return is_write_wget(args)
    if base == "sed":
        return is_write_sed(args)
    if base == "rg":
        return is_write_rg(args)
    if base == "find":
        return is_write_find(args)
    if base in {"python", "python3", "node", "ruby", "perl"}:
        return is_write_interpreter(base, args, heredoc_bodies)
    if base in {"npm", "npx", "pip", "pip3", "brew", "apt", "apt-get"}:
        return any(a in PKG_WRITE_SUBCOMMANDS for a in args)
    if base in {"sh", "bash", "zsh"}:
        # Nested shell invocation: unwrap and check recursively.
        for i, a in enumerate(args):
            if a in {"-c", "-lc"} and i + 1 < len(args):
                return not read_only_shell(args[i + 1])
        return True
    return False


def read_only_shell(command):
    script = unwrap_shell(command)
    if script is None:
        return False
    cleaned, heredoc_bodies = extract_heredocs(script)
    try:
        tokens = tokenize_script(cleaned)
    except ValueError:
        return False
    for segment in split_segments(tokens):
        if is_write_segment(segment, heredoc_bodies):
            return False
    return True


if __name__ == "__main__":
    commands = json.load(sys.stdin)
    sys.exit(0 if all(map(read_only_shell, commands)) else 1)
