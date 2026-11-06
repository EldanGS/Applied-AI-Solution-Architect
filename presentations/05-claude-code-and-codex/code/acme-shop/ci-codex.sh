#!/bin/sh
set -eu
codex exec '$fix-tests' --json --ephemeral \
  --model gpt-6-luna --sandbox workspace-write \
  -o report.txt < /dev/null > agent.jsonl
cat report.txt; echo       # the agent's one-line report
python -m pytest -q        # the tests decide, not the agent
test -z "$(git status --porcelain tests/)"   # tests/ untouched
