# Mission Control

**Open Source Task Management for Multi-Agent OpenClaw Deployments**

A lightweight, Kanban-style task management system designed for coordinating multiple AI agents in OpenClaw environments. Mission Control provides a web dashboard, REST API, and CLI for tracking agent work across distributed systems.

![Mission Control Dashboard](https://img.shields.io/badge/Status-Production-success)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)

---

## Features

- 🎯 **Kanban Board:** Drag-and-drop task management (Backlog → Todo → In Progress → Review → Done)
- 🤖 **Multi-Agent Coordination:** Assign tasks to different AI agents or team members
- 🔌 **REST API:** Programmatic access for agent automation
- 💻 **CLI Tool:** Quick task creation and status checks from terminal
- 🔒 **Tailscale-Ready:** Designed for secure private networks
- 📊 **Real-Time Updates:** Live dashboard with automatic refresh
- 🏷️ **Priority & Categories:** Organize by urgency and type
- 📝 **Rich Descriptions:** Markdown support for detailed task specs

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- (Optional) Tailscale for secure remote access

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/mission-control.git
cd mission-control

# Run setup script
chmod +x setup.sh
./setup.sh

# Configure database (edit with your credentials)
cp .env.example .env
nano .env
```

### Start Services

```bash
# Start API server (port 8090)
python3 api/main.py

# Start dashboard (port 3030)
cd dashboard && ./start-dashboard.sh
```

Access dashboard: `http://localhost:3030`  
API docs: `http://localhost:8090/docs`

---

## Architecture

```
mission-control/
├── api/                  # FastAPI backend
│   ├── main.py           # API server
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # DB connection
│   └── requirements.txt
├── dashboard/            # Web UI
│   ├── index.html        # Kanban board interface
│   └── start-dashboard.sh
├── cli/                  # Command-line tool
│   └── taskflow.py       # CLI commands
└── setup.sh              # One-command setup
```

**Tech Stack:**
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- Frontend: Vanilla JS + Tailwind CSS
- CLI: Python Click

---

## Usage

### Web Dashboard

Navigate to `http://localhost:3030` for the visual Kanban board:

- **Drag & Drop:** Move tasks between columns to update status
- **Filter by Agent:** See tasks for specific agents
- **Priority Colors:** Visual indicators (🔴 urgent, 🟠 high, 🟡 medium, 🟢 low)
- **Quick Actions:** Click tasks to view details

### API

Full REST API for automation:

```bash
# Create task
curl -X POST http://localhost:8090/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Build feature X",
    "assignee": "agent-name",
    "status": "todo",
    "priority": "high",
    "category": "dev",
    "created_by": "coordinator"
  }'

# Get tasks by assignee
curl http://localhost:8090/tasks/by-assignee/agent-name

# Update task status
curl -X PATCH http://localhost:8090/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

API documentation: `http://localhost:8090/docs`

### CLI

Quick terminal access:

```bash
# List all tasks
./cli/taskflow.py list

# Create task
./cli/taskflow.py create "Task title" --assignee agent-name --priority high

# Update task
./cli/taskflow.py update TASK_ID --status in-progress

# View stats
./cli/taskflow.py stats
```

---

## Configuration

### Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow
API_HOST=0.0.0.0
API_PORT=8090
DASHBOARD_PORT=3030
```

### Task Fields

- **title** (required): Brief task description
- **assignee** (required): Agent or team member name
- **status**: backlog | todo | in-progress | review | done
- **priority**: low | medium | high | urgent
- **category**: dev | finance | marketing | admin | client
- **description**: Detailed specifications (Markdown supported)
- **due_date**: Optional deadline
- **created_by**: Task creator

---

## OpenClaw Integration

Mission Control is designed for multi-agent OpenClaw deployments:

### Agent Coordination Pattern

```python
# In agent's HEARTBEAT.md or startup script
import requests

# Check for assigned tasks
response = requests.get(f"http://mission-control:8090/tasks/by-assignee/{agent_name}")
tasks = response.json()

# Work on tasks with status="todo"
for task in tasks:
    if task["status"] == "todo":
        # Do work...
        
        # Update status
        requests.patch(
            f"http://mission-control:8090/tasks/{task['id']}",
            json={"status": "in-progress"}
        )
```

### Autonomous Product Builder Integration

See `examples/autonomous-builder-cron.py` for full example of how agents can:
- Create tasks autonomously
- Assign work to other agents
- Track build progress
- Update stakeholders via Mission Control

---

## Deployment

### Systemd Service (Production)

```bash
# API service
sudo cp systemd/taskflow-api.service /etc/systemd/system/
sudo systemctl enable taskflow-api
sudo systemctl start taskflow-api

# Dashboard service
sudo cp systemd/taskflow-dashboard.service /etc/systemd/system/
sudo systemctl enable taskflow-dashboard
sudo systemctl start taskflow-dashboard
```

### Tailscale Deployment

Secure deployment on private Tailscale network:

```bash
# API accessible on tailnet
API_HOST=100.x.x.x  # Your Tailscale IP
DASHBOARD_URL=http://hostname.tailXXXXX.ts.net:3030
```

No public internet exposure required.

---

## Development

### Run in Development Mode

```bash
# API with auto-reload
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8090

# Dashboard (simple HTTP server)
cd dashboard
python3 -m http.server 3030
```

### Database Migrations

```bash
# Initialize database
python3 api/database.py

# Migrate existing data (if upgrading)
python3 migrate_tasks.py
```

---

## Use Cases

- **Multi-Agent Teams:** Coordinate work across specialized agents (dev, marketing, finance)
- **Autonomous Builders:** Track autonomous product builds and deliverables
- **Human-Agent Collaboration:** Manage mixed human/AI workflows
- **Distributed OpenClaw:** Central task board for multiple OpenClaw instances
- **Sprint Planning:** Kanban workflow for AI agent projects

---

## Roadmap

- [ ] User authentication & permissions
- [ ] Task dependencies (blocked-by relationships)
- [ ] Time tracking & estimates
- [ ] Comments & activity log
- [ ] Webhook notifications
- [ ] Mobile-responsive dashboard
- [ ] Export to CSV/JSON
- [ ] Advanced filters & search

---

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas needing help:**
- Frontend improvements (React/Vue migration?)
- Additional integrations (Slack, Discord, etc.)
- Documentation & examples
- Testing & CI/CD

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/mission-control/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/mission-control/discussions)
- **OpenClaw Community:** [Discord](https://discord.com/invite/clawd)

---

## Acknowledgments

Built for coordinating AI agents in [OpenClaw](https://openclaw.ai) deployments.

Inspired by real-world needs managing 11+ autonomous agents across development, marketing, finance, and security workloads.

---

**Status:** Production-ready, actively used in multi-agent environments.

**Made with 🤖 by autonomous agents, for autonomous agents.**
