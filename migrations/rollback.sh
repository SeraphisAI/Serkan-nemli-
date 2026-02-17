#!/usr/bin/env bash
set -euo pipefail
TARGET_FILE=$(ls -1t migrations/rollback/rollback_from_*.txt 2>/dev/null | head -n1 || true)
if [ -z "$TARGET_FILE" ]; then
  echo "no rollback snapshot found"
  exit 1
fi
cat "$TARGET_FILE" > VERSION
echo "rolled back to $(cat VERSION)"
