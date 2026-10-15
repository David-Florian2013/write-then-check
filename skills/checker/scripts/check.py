#!/usr/bin/env python3
"""Read a unified diff on stdin. Print PASS or FAIL. Exit 0 only on PASS.

No network. It looks at added lines and diff paths. It does not decide
whether the code is correct.
"""
import re
import sys

FORBIDDEN_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "credentials.json",
    "id_rsa",
    "id_ed25519",
}
FORBIDDEN_SUFFIXES = (".pem", ".p12", ".pfx")
SECRETS = (
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github-token", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
)
PATH_RE = re.compile(r"^\+\+\+ b/(.+)$|^diff --git a/.+ b/(.+)$")


def basename(path):
    name = path.strip().replace("\\", "/").split("/")[-1]
    if name.endswith('"'):
        name = name[:-1]
    return name


def forbidden_file(path):
    name = basename(path)
    if name == ".env.example":
        return False
    if name in FORBIDDEN_NAMES:
        return True
    return name.endswith(FORBIDDEN_SUFFIXES)


def judge(diff):
    files = []
    secrets = []
    seen_files = set()
    seen_secrets = set()
    for line in diff.splitlines():
        match = PATH_RE.match(line)
        if match:
            path = match.group(1) or match.group(2)
            if forbidden_file(path) and path not in seen_files:
                seen_files.add(path)
                files.append(basename(path))
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for label, pattern in SECRETS:
            if pattern.search(line) and label not in seen_secrets:
                seen_secrets.add(label)
                secrets.append(label)
    return files, secrets


def report(diff):
    files, secrets = judge(diff)
    if not files and not secrets:
        return 0, "PASS\n"
    lines = ["FAIL"]
    for name in files:
        lines.append(f"file     {name}")
    for label in secrets:
        lines.append(f"secret   {label}")
    return 1, "\n".join(lines) + "\n"


def main():
    diff = sys.stdin.read()
    code, text = report(diff)
    sys.stdout.write(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
