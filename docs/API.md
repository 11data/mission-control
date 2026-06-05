# Task API Contract

Base URL: http://guenther.tail360cf1.ts.net:8090

GET /tasks
Response 200
[
  {"id": "uuid","title":"...","assignee":"sophie","status":"todo","priority":"high","category":"marketing","due":"2026-06-10T08:00:00Z","notes":"..."},
  ...
]

GET /tasks/by-assignee/{name}

POST /tasks
Request
{ "title":"...","assignee":"sophie","status":"backlog","priority":"medium","category":"dev","due":"2026-06-10" }
Response 201 -> created task object

PATCH /tasks/{id}
Request body examples:
{ "status": "in-progress" }
{ "assignee": "felix" }
Response 200 -> updated task

Errors
400 — bad request
404 — not found
500 — server error

Notes
- All timestamps ISO8601 UTC
- Client must retry on 5xx with backoff