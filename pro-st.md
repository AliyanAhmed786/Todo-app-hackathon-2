# Project Structure

```
.
├── backend.env
├── CLAUDE.md
├── ID-issue
├── project-structure.md
├── README.md
├── test_dashboard.py
├── test_enhanced_ui.py
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── production_config.py
│   ├── setup.py
│   ├── deploy.py
│   ├── reset_database.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── app.log.1
│   │
│   ├── api/
│   │   ├── auth_router.py
│   │   ├── task_router.py
│   │   ├── chat_router.py
│   │   └── dashboard_router.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── message.py
│   │   ├── conversation.py
│   │   ├── account.py
│   │   ├── session.py
│   │   └── verification.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── login_service.py
│   │   ├── logout_service.py
│   │   ├── registration_service.py
│   │   └── ... (additional services)
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── session.py
│   │   ├── migrations.py
│   │   ├── schema_updater.py
│   │   ├── add_due_date_migration.py
│   │   ├── complete_schema_migration.py
│   │   └── migrations/
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth_setup.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── better_auth.py
│   │   └── rate_limiter.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── chat_auth.py
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── chat_exceptions.py
│   │   └── handlers.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   └── chat_agent.py
│   │
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── server.py
│   │   └── tools.py
│   │
│   ├── utils/
│   │   └── ... (utility modules)
│   │
│   ├── test/
│   │   └── ... (backend tests)
│   │
│   └── __pycache__/
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.mjs
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── next-env.d.ts
│   │
│   ├── public/
│   │   └── ... (static assets)
│   │
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── utils/
│       ├── hooks/
│       └── styles/
│
├── src/
│   ├── main.py
│   ├── cli/
│   ├── models/
│   ├── services/
│   └── __pycache__/
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── __pycache__/
│
├── docs/
│   └── nextjs-task-deletion-fixes-summary.md
│
├── specs/
│   ├── 1-todo-console-app/
│   ├── 2-multi-user-todo-web-app/
│   ├── 3-web-ui/
│   ├── 4-backend-crud/
│   ├── 5-frontend-improved-ui/
│   ├── 6-dashboard-improvement/
│   ├── 7-better-auth/
│   ├── 9-chatbot-backend/
│   └── 10-docker-k8s-deployment/
│
├── history/
│   └── prompts/
│
└── pdf/
    └── ... (project PDFs)
```

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (TypeScript, React, Tailwind CSS)
- **Database**: SQLAlchemy ORM
- **Authentication**: Better Auth with JWT
- **AI/Chat**: Chat agents with MCP support
- **Containerization**: Docker

## Key Features

- User authentication (signup, login, logout, session management)
- Task CRUD operations with due dates
- Dashboard with statistics and task overview
- AI chat agent integration
- Multi-user support
- Database migrations and schema updates
- Rate limiting middleware
- Model Context Protocol (MCP) support
