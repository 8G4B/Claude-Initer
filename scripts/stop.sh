#!/bin/bash
docker stop claude-trigger 2>/dev/null || true
docker rm   claude-trigger 2>/dev/null || true