#!/usr/bin/env bash
set -euo pipefail

git log --date=short --pretty=format:'%ad%x09%s' --reverse
