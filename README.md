# write-then-check

One agent writes. A second pass checks the diff. It stops on `PASS`, or after three rounds.

<p align="center">
  <img src="docs/banner.png" alt="One writes. The other checks. PASS, or three rounds." width="100%">
</p>

**Writer:** edits the files, then stops. It is not allowed to call the work done.

**Checker:** reads the diff. It prints `PASS` or `FAIL`. It does not edit.

```bash
npx skills add David-Florian2013/write-then-check -g -a '*' -y
```

## See it run

No model is called. Round 1 is a diff with a key and a `.env`. The checker fails it. Round 2 is the same change without them. The checker passes, and the loop stops. The key in round 1 is Amazon's documented example (`AKIAIOSFODNN7EXAMPLE`), not a live credential.

<p align="center">
  <img src="docs/demo-terminal.png" alt="Terminal: round 1 FAIL on .env and an AWS example key. Round 2 PASS and stop." width="100%">
</p>

```text
$ python3 scripts/demo.py
write-then-check
checker: skills/checker/scripts/check.py
model: none    network: none
cap: 3 rounds, or the same FAIL twice

1  writer adds app.py, a key, and .env
   FAIL
   file     .env
   secret   aws-access-key
   writer   may not say done

2  writer removes the key and .env
   PASS
   stop     round 2
```

[![CI](https://github.com/David-Florian2013/write-then-check/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/David-Florian2013/write-then-check/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/David-Florian2013/write-then-check)](LICENSE)
[![Release](https://img.shields.io/github/v/release/David-Florian2013/write-then-check)](https://github.com/David-Florian2013/write-then-check/releases)

## Install

Both skills, every agent the [skills CLI](https://github.com/vercel-labs/skills) knows:

```bash
npx skills add David-Florian2013/write-then-check -g -a '*' -y
```

One agent:

```bash
npx skills add David-Florian2013/write-then-check -g -a claude-code -y
npx skills add David-Florian2013/write-then-check -g -a codex -y
npx skills add David-Florian2013/write-then-check -g -a cursor -y
```

One skill:

```bash
npx skills add David-Florian2013/write-then-check -g -a claude-code -y -s checker
npx skills add David-Florian2013/write-then-check -g -a claude-code -y -s writer
```

The checker is the one with the script. The writer refuses to start the loop if the request is still vague. When [prompt-clarifier](https://github.com/David-Florian2013/prompt-clarifier) is installed, the writer hands that moment to it. This repo does not copy that skill.

`./install.sh` copies both folders into `~/.claude/skills`. CI runs that against an empty directory.

GitHub CLI 2.90.0 or newer can install a skill from the release:

```bash
gh skill install David-Florian2013/write-then-check checker --agent claude-code --scope user
gh skill install David-Florian2013/write-then-check writer --agent claude-code --scope user
```

Or download `checker.skill` and `writer.skill` from the [latest release](https://github.com/David-Florian2013/write-then-check/releases/latest). Each is a zip. Unzip it into the skills folder for the agent you use.

## The two skills

| Skill | Does | Does not |
|---|---|---|
| [`writer`](skills/writer/SKILL.md) | Edits, then stops | Say the task is done |
| [`checker`](skills/checker/SKILL.md) | Runs [`scripts/check.py`](skills/checker/scripts/check.py) on the diff | Edit anything |

A host that can start a second agent should run the checker there, with no write tool. Claude Code can. Codex and Cursor often cannot. The script's exit code counts on all of them. A `PASS` the script did not print does not count.

The loop ends on `PASS`, on round 3, or when the same `FAIL` comes back. Then a person decides.

## What the script flags

Added lines: an `AKIA…` access key, a `ghp_…` token, a private-key block, a Slack token (`xoxb-` and the same family).

Paths: `.env` (not `.env.example`), `.env.local`, `.env.production`, `.env.development`, `credentials.json`, `id_rsa`, `id_ed25519`, and files ending in `.pem`, `.p12`, or `.pfx`.

That list is the whole checker. Read it in [`check.py`](skills/checker/scripts/check.py). It makes no network call.

## Limits

- A `PASS` means this diff missed that list. It does not mean the code is right, or that tests passed.
- Nothing in this repo can force a host to spawn a second model. The instruction says to. The script is the part that actually runs.
- The writer will not invent a filename for a vague request. One question, then it waits.
- The demo diffs are fixtures. They are not a trace from Claude, Codex, or any other model.
- Round 3 and a repeated `FAIL` are stop rules in the writer skill. The demo shows the pass on round 2, which is the path those rules allow.

## Claude Code plugin

```text
/plugin marketplace add David-Florian2013/write-then-check
/plugin install write-then-check@write-then-check
```

`./install.sh` is the path CI checks.

## License

[MIT](LICENSE).
