#!/usr/bin/env bash
set -euo pipefail
mkdir -p migrations/rollback
if [ ! -f VERSION ]; then
  echo "0.1.0" > VERSION
fi
echo "init migration applied"
