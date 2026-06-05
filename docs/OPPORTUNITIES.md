# Opportunities (CRM) — Docs & API

Purpose
- Track sales opportunities separately from tasks. Link opportunities to tasks and contacts. Support pipeline stages, deal value, owner, and key dates.

Data model (proposal)

Table: opportunities
- id: uuid (PK)
- title: text
- company: text
- contact_id: uuid (nullable)
- owner: text (assignee username)
- value: numeric
- currency: text (e.g. EUR)
- stage: text (lead|qualification|proposal|negotiation|closed_won|closed_lost)
- status: text (open|archived)
- close_date: date (nullable)
- source: text (referral|inbound|outbound|partner|other)
- notes: text
- created_at: timestamptz
- updated_at: timestamptz

Table: opportunity_tasks
- id: uuid
- opportunity_id: uuid (FK -> opportunities.id)
- task_id: uuid (FK -> tasks.id)
- role: text (implementation|followup|proposal|other)

API contract (proposal)

GET /opportunities
Response 200
[
 {"id":"...","title":"Pilot for X","company":"ACME","owner":"jon","value":12000,"currency":"EUR","stage":"qualification","status":"open","close_date":"2026-07-01","source":"inbound","notes":"..."}
]

GET /opportunities/{id}
Response 200 -> opportunity object with list of linked tasks

POST /opportunities
Request 201
{ "title":"...","company":"...","owner":"jon","value":10000,"currency":"EUR","stage":"lead","close_date":"2026-08-01","source":"inbound","notes":"..." }

PATCH /opportunities/{id}
{ "stage":"proposal" }

GET /opportunities/{id}/tasks
Response 200 -> [{task objects}]

Integration: link tasks to opportunity
POST /opportunities/{id}/tasks
{ "task_id": "uuid", "role":"followup" }

Acceptance tests
- Create opportunity -> appears in GET /opportunities
- Update stage via PATCH -> reflected in GET
- Link a task -> task listed under opportunity tasks

Frontend notes
- New "Opportunities" nav item in sidebar
- Pipeline view: columns are pipeline stages, drag card between stages updates stage (PATCH)
- Opportunity card shows value, owner, stage, and quick-create-task button
- Opportunity detail modal lists linked tasks with quick link to open task

Next steps
1. Add DB migrations and API endpoints on backend (if missing)
2. Add frontend mock (pipeline view) in dashboard
3. Add acceptance tests and docs-driven QA for Opportunities

Questions:
- Confirm pipeline stages or adjust (current: lead, qualification, proposal, negotiation, closed_won, closed_lost)
- HubSpot sync needed? (yes/no)
