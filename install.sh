#!/usr/bin/env bash
# Copy writer and checker into ~/.claude/skills (override with CLAUDE_SKILLS_DIR).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
for name in writer checker; do
  if [ ! -f "$ROOT/skills/$name/SKILL.md" ]; then
    echo "missing skills/$name/SKILL.md" >&2
    exit 1
  fi
done
mkdir -p "$DEST"
for name in writer checker; do
  rm -rf "$DEST/$name"
  cp -R "$ROOT/skills/$name" "$DEST/$name"
  echo "installed $name -> $DEST/$name"
done
