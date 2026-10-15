#!/usr/bin/env python3
"""Show the checker script failing a bad diff and passing the next one.

This does not call a model and it does not use the network. The key in the
first diff is the public AWS documentation example, not a live credential.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "skills" / "checker" / "scripts" / "check.py"

BAD = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1 +1,2 @@
+value = "AKIAIOSFODNN7EXAMPLE"
diff --git a/.env b/.env
--- /dev/null
+++ b/.env
@@ -0,0 +1 @@
+TOKEN=example
"""

GOOD = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1 +1,2 @@
+value = "loaded-from-env"
"""


def run(diff):
    proc = subprocess.run(
        [sys.executable, str(CHECK)],
        input=diff,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout


def main():
    lines = [
        "write-then-check",
        "checker: skills/checker/scripts/check.py",
        "model: none    network: none",
        "cap: 3 rounds, or the same FAIL twice",
        "",
    ]
    rounds = (
        ("writer adds app.py, a key, and .env", BAD, 1),
        ("writer removes the key and .env", GOOD, 0),
    )
    failed = False
    for number, (title, diff, expect) in enumerate(rounds, 1):
        code, out = run(diff)
        lines.append(f"{number}  {title}")
        for raw in out.rstrip("\n").splitlines():
            lines.append(f"   {raw}")
        if number == 1:
            lines.append("   writer   may not say done")
        if code != expect:
            failed = True
        if code == 0:
            lines.append(f"   stop     round {number}")
            lines.append("")
            break
        lines.append("")
    else:
        failed = True
    text = "\n".join(lines).rstrip() + "\n"
    sys.stdout.write(text)
    if failed or "PASS" not in text or "FAIL" not in text or "aws-access-key" not in text:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
