# Architecture

Components
- Frontend: single-file TailAdmin Pro-derived HTML served from /dev/mission-control/dashboard/index.html
- API: Mission Control backend at http://guenther.tail360cf1.ts.net:8090
- Storage: PostgreSQL (backend)
- Static assets: stored in repo under /images /photos

Data flow
1. Frontend GET /tasks -> API
2. User drag/drop -> frontend PATCH /tasks/{id} {status}
3. API persists, emits events (future)

Security
- Internal network only (private IPs)
- SSH key-based deploys

Observability
- Healthcheck endpoint: GET /health
- Metrics: GET /stats