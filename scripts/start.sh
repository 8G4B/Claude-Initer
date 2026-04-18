#!/bin/bash
set -e
cd "$(dirname "$0")/.."

docker build -t claude-trigger .

docker run -d \
  --name claude-trigger \
  --restart unless-stopped \
  --env-file "$(dirname "$0")/../trigger.env" \
  claude-trigger