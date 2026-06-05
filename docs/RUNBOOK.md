# Runbook

Common issues

Frontend 500 / blank
- Check static files present in /home/clawd/dev/mission-control/dashboard
- Check browser console for missing scripts

API 502 / unreachable
- Check backend: systemctl status mission-control-api
- Check network: curl -v http://guenther.tail360cf1.ts.net:8090/stats

Restart frontend
pkill -f "http.server 3030" || true
cd /home/clawd/dev/mission-control/dashboard
nohup python3 -m http.server 3030 > /dev/null 2>&1 &

Backup
- Dump DB nightly to /backups
- Keep 7-day retention

Contact
- Felix (tech) for infra issues
- Mira (ops) for permission issues