---
id: 001
title: Todo App Backend Fixes for Connection Leaks and Priority Handling
stage: general
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Wajiz.pk
command: /sp.phr
labels: ["backend", "database", "cors", "priority", "connection-leak"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/database/connection.py
 - backend/api/task_router.py
 - backend/schemas/task.py
 - frontend/src/components/TaskList.tsx
 - backend/main.py
tests:
 - none
---

## Prompt

--title "Todo App Backend Fixes for Connection Leaks and Priority Handling" --stage general

## Response snapshot

Fixed multiple critical issues in the Todo app backend: 1) Fixed database connection leaks by implementing proper try/finally blocks with session.close() in the connection generator, 2) Fixed priority handling by updating schemas to accept string values and properly convert them to integers, 3) Fixed CORS configuration to allow all origins for development, 4) Verified TaskList component properly triggers parent refresh callbacks, 5) Fixed priority mapping in frontend component. All fixes address the reported 10s timeouts, 500 errors, and frontend state issues.

## Outcome

- ✅ Impact: Resolved database connection leaks, priority handling issues, and CORS problems in Todo app backend
- 🧪 Tests: none
- 📁 Files: backend/database/connection.py, backend/api/task_router.py, backend/schemas/task.py, frontend/src/components/TaskList.tsx, backend/main.py
- 🔁 Next prompts: none
- 🧠 Reflection: Proper error handling and resource management are critical for backend stability

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none