#!/usr/bin/env bash
# Create an Ubuntu 24.04 container. Scope: instances:write
# Usage: ./create-instance.sh <name> [cpu=1] [memory_mb=1024] [disk_gb=20]
set -euo pipefail
: "${VELOXA_API_KEY:?export VELOXA_API_KEY first}"
API=${VELOXA_API:-https://console.veloxahost.com/api/v1}

name=${1:?name required}
cpu=${2:-1}; mem=${3:-1024}; disk=${4:-20}

curl -fsS -X POST "$API/instances" \
  -H "Authorization: Bearer $VELOXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg n "$name" --argjson c "$cpu" --argjson m "$mem" --argjson d "$disk" \
        '{name:$n, type:"container", image:"ubuntu/24.04", cpu_limit:$c, memory_limit_mb:$m, disk_size_gb:$d}')"
echo
echo "Created $name. Check status: ./list-instances.sh"
