#!/usr/bin/env bash
# Restart (or start/stop/freeze/unfreeze) an instance. Scope: instances:write
# Usage: ./restart-instance.sh <name> [action=restart]
set -euo pipefail
: "${VELOXA_API_KEY:?export VELOXA_API_KEY first}"
API=${VELOXA_API:-https://console.veloxahost.com/api/v1}

name=${1:?name required}
action=${2:-restart}

curl -fsS -X POST "$API/instances/$name/state" \
  -H "Authorization: Bearer $VELOXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"action\": \"$action\"}"
echo
