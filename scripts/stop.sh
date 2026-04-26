#!/bin/bash

export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

docker stop claude-trigger 2>/dev/null || true
docker rm   claude-trigger 2>/dev/null || true