#!/bin/bash
# Dashboard web server keeper

cd /home/clawd/clawd/dashboard

# Kill any existing server
pkill -f "http.server 3030" 2>/dev/null

# Start new server
nohup python3 -m http.server 3030 > dashboard.log 2>&1 &

echo "Dashboard server started on port 3030"
echo "PID: $!"
echo "Access: http://guenther.tail360cf1.ts.net:3030"
