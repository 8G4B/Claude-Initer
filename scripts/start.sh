#!/bin/bash
set -e

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

cd "$(dirname "$0")/.."

/usr/local/bin/docker build -t claude-trigger .

/usr/local/bin/docker run -d \
  --name claude-trigger \
  --restart unless-stopped \
  --env-file "$(dirname "$0")/../trigger.env" \
  claude-trigger