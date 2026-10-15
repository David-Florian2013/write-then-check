# Security

`skills/checker/scripts/check.py` looks for a few secret shapes and filenames in a unified diff. A miss is a bug.

Open an issue with the shape of the line (lengths and prefixes), not a live key, password, or token. If you already committed a real secret, revoke it first. This skill does not rotate credentials and it does not scan history beyond the diff you pass in.
