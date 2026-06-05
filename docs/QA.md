# QA & Acceptance Tests

Smoke tests
- Load dashboard -> returns 200 and renders Kanban
- GET /stats shows total > 0

Drag/drop test
1. Move a card from `todo` to `in-progress`
2. Confirm PATCH /tasks/{id} called with {"status":"in-progress"}
3. Confirm UI updates and counts refresh

Create task
1. Open New Task modal, fill fields, submit
2. Confirm POST /tasks and new card appears

Manual checks
- Dark mode persists after refresh
- Avatars show initials and color
- Mobile: sidebar collapses

Automation suggestions
- Add Cypress integration tests for drag/drop and create task flows