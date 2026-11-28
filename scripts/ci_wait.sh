#!/usr/bin/env bash
# ci_wait.sh WORKFLOW_FILE [EVENT]
# Wait for the run of WORKFLOW_FILE for the current commit, print its summary,
# and exit 0 only if it succeeded.
set -euo pipefail
id=$("$(dirname "$0")/ci_run_id.sh" "$@")
gh run watch "$id" --interval 10 > /dev/null 2>&1 || true
gh run view "$id" 2>/dev/null
[[ $(gh run view "$id" --json conclusion --jq .conclusion) == success ]]
