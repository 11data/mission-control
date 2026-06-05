# Components & Acceptance

Sidebar
- Items: Dashboard, Team, Calendar, Analytics, Settings
- Accept: collapses on mobile, dark mode toggle works

Header
- Search, refresh, new task modal
- Accept: refresh updates timestamp and reloads tasks

Stats cards
- Total, Backlog, In Progress, Done, Urgent
- Accept: numbers match GET /stats

Kanban
- Columns: backlog, todo, in-progress, review, done
- Task card: title, tags, assignee initials, priority badge
- Accept: dragging a card triggers PATCH /tasks/{id} and UI updates

Modals
- New task modal creates via POST /tasks
- Accept: new card appears in selected column