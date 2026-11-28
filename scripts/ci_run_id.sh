#!/usr/bin/env bash
# ci_run_id.sh WORKFLOW_FILE [EVENT]
# Print the ID of the run of .github/workflows/WORKFLOW_FILE triggered by EVENT
# (default: push) for the current commit; wait up to 5 minutes for it to appear.
set -euo pipefail
wf=${1:?usage: ci_run_id.sh WORKFLOW_FILE [EVENT]}
event=${2:-push}
sha=$(git rev-parse HEAD)
repo=$(git remote get-url origin | sed -E 's#.*github.com[:/]##; s#\.git$##')
for _ in $(seq 1 60); do
    id=$(gh api "repos/$repo/actions/runs?head_sha=$sha&event=$event&per_page=100" \
         --jq ".workflow_runs[] | select(.path == \".github/workflows/$wf\") | .id" | head -n 1)
    [[ -n $id ]] && { echo "$id"; exit 0; }
    sleep 5
done
echo "ci_run_id: no $event run of $wf for ${sha:0:7}" >&2
exit 1
