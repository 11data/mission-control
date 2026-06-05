#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
# Ensure environment file exists
ENVFILE=/etc/mission-control/mission-control.env
if [ -f "$ENVFILE" ]; then
  # shellcheck source=/dev/null
  source "$ENVFILE"
fi
python3 integrations/hubspot/export_runner.py
