#!/bin/bash
# Example: Check Mission Control in OpenClaw agent heartbeat

AGENT_NAME="mira"
API_URL="http://localhost:8090"

# Get count of pending tasks
PENDING_COUNT=$(curl -s "${API_URL}/tasks/by-assignee/${AGENT_NAME}" | \
                jq '[.[] | select(.status == "todo" or .status == "in-progress")] | length')

if [ "$PENDING_COUNT" -gt 0 ]; then
    echo "⚠️ ${PENDING_COUNT} task(s) need attention in Mission Control"
    
    # Get urgent tasks
    URGENT_TASKS=$(curl -s "${API_URL}/tasks/by-assignee/${AGENT_NAME}" | \
                   jq -r '.[] | select(.priority == "urgent" and (.status == "todo" or .status == "in-progress")) | .title')
    
    if [ -n "$URGENT_TASKS" ]; then
        echo "🔴 URGENT tasks:"
        echo "$URGENT_TASKS"
    fi
else
    echo "✅ No pending tasks in Mission Control"
fi
