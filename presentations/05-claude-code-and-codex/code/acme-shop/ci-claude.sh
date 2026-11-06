#!/bin/sh
set -eu
claude -p "/fix-tests" --output-format json \
  --model claude-sonnet-5-5 --max-turns 10 --max-budget-usd 1 \
  --allowedTools "Bash(python -m pytest *)" "Edit(./*.py)" \
  > agent.json
jq -r .result agent.json   # the agent's one-line report
python -m pytest -q        # the tests decide, not the agent
test -z "$(git status --porcelain tests/)"   # tests/ untouched
