# Deployment

Run locally (dev)
```
cd /home/clawd/dev/mission-control/dashboard
python3 -m http.server 3030
# Frontend served at http://localhost:3030
```

Production (recommended)
- Serve static files via nginx or Vercel
- Keep API on internal host: guenther.tail360cf1.ts.net:8090

SSH upload (example)
scp -i ~/.ssh/sophie_11data_deploy -r /path/to/tailadmin-html-pro clawd@100.119.145.16:/tmp/tailadmin-html-pro

Rollback
- Keep previous release copy under /var/www/mission-control/releases
- Symlink current -> release-YYYYMMDD

Cron
- Reminder job already created for post 006 (Typefully attach) via OpenClaw cron