"""
Example: OpenClaw Agent Integration with Mission Control

Shows how an agent can:
1. Check for assigned tasks on startup
2. Update task status during work
3. Create new tasks for other agents
"""

import requests
from typing import List, Dict

MISSION_CONTROL_API = "http://localhost:8090"
AGENT_NAME = "mira"  # Change to your agent name


def get_my_tasks(status: str = None) -> List[Dict]:
    """Get tasks assigned to this agent."""
    url = f"{MISSION_CONTROL_API}/tasks/by-assignee/{AGENT_NAME}"
    response = requests.get(url)
    tasks = response.json()
    
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    
    return tasks


def update_task_status(task_id: str, status: str, description: str = None):
    """Update a task's status and optionally add notes."""
    url = f"{MISSION_CONTROL_API}/tasks/{task_id}"
    payload = {"status": status}
    
    if description:
        payload["description"] = description
    
    requests.patch(url, json=payload)
    print(f"✅ Task {task_id} → {status}")


def create_task(title: str, assignee: str, priority: str = "medium", **kwargs):
    """Create a new task for another agent."""
    url = f"{MISSION_CONTROL_API}/tasks"
    payload = {
        "title": title,
        "assignee": assignee,
        "status": "todo",
        "priority": priority,
        "created_by": AGENT_NAME,
        **kwargs
    }
    
    response = requests.post(url, json=payload)
    task = response.json()
    print(f"🆕 Created task {task['id']} for {assignee}")
    return task


def agent_startup_check():
    """Run this on agent startup to check for work."""
    print(f"🔍 Checking Mission Control for {AGENT_NAME}...")
    
    # Get tasks waiting to be done
    todo_tasks = get_my_tasks(status="todo")
    in_progress_tasks = get_my_tasks(status="in-progress")
    
    print(f"📋 Found {len(todo_tasks)} todo, {len(in_progress_tasks)} in-progress")
    
    # Process each todo task
    for task in todo_tasks:
        print(f"\n📌 Task: {task['title']}")
        print(f"   Priority: {task['priority']}")
        print(f"   Description: {task.get('description', 'No description')}")
        
        # Mark as in-progress
        update_task_status(task["id"], "in-progress")
        
        # Do the work...
        # (Your agent logic here)
        
        # Mark as done
        update_task_status(
            task["id"], 
            "done",
            description=f"{task.get('description', '')}\n\n✅ Completed by {AGENT_NAME}"
        )


def example_coordination():
    """Example: Create tasks for other agents."""
    
    # Autonomous product builder scenario
    create_task(
        title="BUILD: Email Intelligence Pipeline",
        assignee="werner",
        priority="high",
        category="dev",
        description="""
Full PRD: ~/clawd/prd/email-intelligence.md

Mission: Build automated email-to-proposal pipeline.

Deliverables:
1. Email monitor (Gmail API)
2. Lead extractor
3. Proposal generator (Claude API)
4. Mission Control integration

Target: 4 hours
"""
    )
    
    # Content deployment task
    create_task(
        title="Deploy Context Infrastructure content package",
        assignee="sophie",
        priority="high",
        category="marketing",
        description="""
Deploy all content from ~/clawd/content/context-infrastructure/

Actions:
- Schedule LinkedIn article (09:00 CET)
- Schedule Twitter thread (13:00 CET)
- Upload case study PDF
- Monitor engagement for 48h
"""
    )


if __name__ == "__main__":
    # Run on agent startup
    agent_startup_check()
    
    # Example: Coordinate other agents
    # example_coordination()
