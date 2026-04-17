#!/bin/bash
set -e
cd "$(dirname "$0")/.."

docker build -t claude-trigger .

docker run -d \
  --name claude-trigger \
  --restart unless-stopped \
  -e TRIGGER_URL="${TRIGGER_URL}" \
  -e TRIGGER_TOKEN="${TRIGGER_TOKEN}" \
  claude-trigger