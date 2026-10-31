#!/bin/bash

if ! command -v python3 >/dev/null 2>&1; then
  echo "BLOCKED: Git guardrails require python3 on PATH." >&2
  exit 2
fi

# Claude treats exit 2 as blocking; parser and installation failures must use it too.
if python3 -I "${BASH_SOURCE[0]%/*}/block-dangerous-git.py"; then
  exit 0
fi
echo "BLOCKED: Git guardrails rejected the command or could not inspect it." >&2
exit 2
