#!/usr/bin/env bash
# List instances. Requires: curl, jq. Scope: instances:read
set -euo pipefail
: "${VELOXA_API_KEY:?export VELOXA_API_KEY first}"
API=${VELOXA_API:-https://console.veloxahost.com/api/v1}

curl -fsS "$API/instances" -H "Authorization: Bearer $VELOXA_API_KEY" \
  | jq -r '(if type=="array" then . else (.instances // .data // []) end)[] | [.name, .status, .type] | @tsv' \
  | column -t
