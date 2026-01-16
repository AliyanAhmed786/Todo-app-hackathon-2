# Todo App Hackathon - Complete Project Structure

**Project Type:** Multi-User Web Todo Application with Authentication, Task Management, Real-time Chat, and Dashboard
**Tech Stack:** Next.js (Frontend) + FastAPI (Backend) + PostgreSQL (Database) + Better Auth (Authentication)

---

## 📋 Root Directory Structure

```
todo app hackathon 2/
├── backend/                    # FastAPI backend server
├── frontend/                   # Next.js React frontend application
├── src/                        # Legacy source files (CLI/core logic)
├── tests/                      # Workspace-level tests
├── docs/                       # Documentation files
├── specs/                      # Project specifications by phase
├── history/                    # Prompt history records (AI development tracking)
├── pdf/                        # PDF resources
├── .claude/                    # Claude AI configuration
├── .git/                       # Git version control
├── .specify/                   # Specify framework config
├── .pytest_cache/              # Pytest cache
├── .gitignore                  # Git ignore rules
├── backend-details.md          # Backend architecture details
├── frontend-details.md         # Frontend architecture details
├── backend.env                 # Backend environment variables
├── chatbot-structure.md        # Chatbot integration structure
├── CLAUDE.md                   # Claude code rules and guidelines
├── README.md                   # Main project README
├── test_dashboard.py           # Dashboard testing script
└── test_enhanced_ui.py         # Enhanced UI testing script
```

---

## 🔧 BACKEND STRUCTURE (`backend/`)

FastAPI-based REST API with database models, authentication, and business logic.

### Core Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app entry point with CORS, middleware, lifespan management, and router registration |
| `config.py` | Application configuration (database URLs, secrets, environment settings) |
| `production_config.py` | Production-specific configuration settings |
| `.env` | Environment variables (database URL, API keys, secrets) |
| `requirements.txt` | Python dependencies (FastAPI, SQLModel, PostgreSQL, etc.) |
| `setup.py` | Package setup and installation configuration |
| `Dockerfile` | Docker container definition for backend deployment |
| `deploy.py` | Deployment scripts and configurations |
| `reset_database.py` | Utility to reset and reinitialize database |
| `todo_app.db` | SQLite database (fallback/development) |
| `app.log` | Application logs |
| `README.md` | Backend-specific documentation |

### API Layer (`backend/api/`)

Router modules that handle HTTP requests and responses.

| File | Purpose |
|------|---------|
| `auth_router.py` | Authentication endpoints (login, signup, logout, session validation) |
| `task_router.py` | Task CRUD endpoints (create, read, update, delete tasks) |
| `dashboard_router.py` | Dashboard endpoints (statistics, analytics, user data) |
| `chat_router.py` | Chat/real-time messaging endpoints |

### Database Layer (`backend/database/`)

Database connection, migrations, and session management.

| File | Purpose |
|------|---------|
| `connection.py` | Database connection setup and pooling configuration |
| `session.py` | SQLAlchemy session factory and dependency injection |
| `migrations.py` | Database schema initialization and migration runner |
| `add_due_date_migration.py` | Migration to add due_date field to tasks |
| `complete_schema_migration.py` | Comprehensive schema migration |
| `schema_updater.py` | Schema update utilities and helpers |
| `migrations/` | Migration files directory |

### Models Layer (`backend/models/`)

SQLModel database models with Pydantic validation.

| File | Purpose |
|------|---------|
| `user.py` | User model (id, email, password_hash, metadata) |
| `task.py` | Task model (id, title, description, status, due_date, user_id) |
| `session.py` | Session model (user sessions, tokens, expiry) |
| `account.py` | Account model (account details, profile info) |
| `verification.py` | Email/verification token model |
| `conversation.py` | Chat conversation model |
| `message.py` | Chat message model |

### Services Layer (`backend/services/`)

Business logic and data operations.

| File | Purpose |
|------|---------|
| `user_service.py` | User operations (create, update, delete, fetch) |
| `task_service.py` | Task operations (CRUD, filtering, sorting) |
| `registration_service.py` | User registration logic and validation |
| `login_service.py` | Login logic, authentication, JWT generation |
| `logout_service.py` | Logout logic, session invalidation |
| `session_service.py` | Session management and validation |

### Authentication (`backend/auth/`)

Authentication setup and integration.

| File | Purpose |
|------|---------|
| `auth_setup.py` | Better Auth initialization and configuration |

### Middleware (`backend/middleware/`)

Request/response processing and cross-cutting concerns.

| File | Purpose |
|------|---------|
| `auth.py` | Authentication middleware (token validation) |
| `better_auth.py` | Better Auth middleware integration |
| `rate_limiter.py` | Rate limiting to prevent API abuse |

### Dependencies (`backend/dependencies/`)

FastAPI dependency injection utilities.

| File | Purpose |
|------|---------|
| `auth.py` | Authentication dependencies (get_current_user) |
| `chat_auth.py` | Chat-specific authentication dependencies |

### Schemas (`backend/schemas/`)

Pydantic request/response schemas for validation.

| File | Purpose |
|------|---------|
| `auth.py` | Login/signup/token request/response schemas |
| `task.py` | Task creation/update/response schemas |
| `user.py` | User profile/update schemas |

### Exception Handling (`backend/exceptions/`)

Custom exceptions and error handlers.

| File | Purpose |
|------|---------|
| `chat_exceptions.py` | Chat-specific exceptions |
| `handlers.py` | Global exception handlers (404, 500, validation errors) |

### Agents (`backend/agents/`)

AI/chatbot agent implementations.

| File | Purpose |
|------|---------|
| `chat_agent.py` | Chat agent logic for AI-powered conversations |

### MCP Integration (`backend/mcp/`)

Model Context Protocol (MCP) server for AI integration.

| File | Purpose |
|------|---------|
| `config.py` | MCP server configuration |
| `server.py` | MCP server implementation |
| `tools.py` | MCP tool definitions and implementations |

### Test Files (in `backend/`)

| File | Purpose |
|------|---------|
| `test_main.py` | Tests for main app setup |
| `test_dashboard.py` | Dashboard endpoint tests |
| `test_comprehensive_better_auth.py` | Comprehensive authentication tests |
| `test_better_auth_registration.py` | Registration flow tests |
| `test_better_auth_login.py` | Login flow tests |
| `test_better_auth_logout.py` | Logout flow tests |
| `test_better_auth_task_crud.py` | Task CRUD with auth tests |
| `test_better_auth_session_persistence.py` | Session persistence tests |
| `test_account_deletion_cascade.py` | Account deletion cascade tests |

---

## 🎨 FRONTEND STRUCTURE (`frontend/`)

Next.js React application with TypeScript and Tailwind CSS.

### Root Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | NPM dependencies (React, Next.js, Tailwind, Axios, etc.) |
| `tsconfig.json` | TypeScript configuration |
| `tailwind.config.ts` | Tailwind CSS customization |
| `postcss.config.js` | PostCSS configuration for Tailwind |
| `next-env.d.ts` | Next.js TypeScript type definitions |

### Application Source (`frontend/src/`)

| Directory | Purpose |
|-----------|---------|
| `components/` | Reusable React components |
| `pages/` | Next.js page components (routes) |
| `services/` | API client and business logic |
| `lib/` | Utilities and helpers |
| `styles/` | Global CSS/Tailwind styles |
| `tests/` | Component and integration tests |
| `utils/` | Helper functions and utilities |
| `app/` | App shell and layout |

### Components (`frontend/src/components/`)

UI components used throughout the application.

| Component | Purpose |
|-----------|---------|
| `HomePage.tsx` | Landing/home page component |
| `LoginForm.tsx` | Login form (server-side) |
| `LoginFormClient.tsx` | Login form (client-side) |
| `SignupForm.tsx` | Signup form (server-side) |
| `SignupFormClient.tsx` | Signup form (client-side) |
| `TaskForm.tsx` | Create/edit task form |
| `TaskList.tsx` | Display list of tasks |
| `TaskEditModal.tsx` | Modal for editing tasks |
| `DashboardPageClient.tsx` | Dashboard page client component |
| `DashboardStats.tsx` | Dashboard statistics display |
| `Navbar.tsx` | Navigation bar component |
| `ProtectedRoute.tsx` | Route protection wrapper (auth check) |
| `Modal.tsx` | Reusable modal component |
| `DeleteConfirmationModal.tsx` | Confirmation modal for deletions |
| `ToastNotification.tsx` | Toast notification component |
| `LoadingSpinner.tsx` | Loading indicator component |
| `ErrorBoundary.tsx` | Error boundary component |
| `chatbot-ui/` | Chatbot UI components directory |
| `test.txt` | Test file (placeholder) |
| `__tests__/` | Component tests directory |

### Pages (`frontend/src/pages/`)

Next.js page routes.

| File | Purpose |
|------|---------|
| `homepage.tsx` | Homepage route |

### Services (`frontend/src/services/`)

API communication and data fetching.

| File | Purpose |
|------|---------|
| `api.ts` | Main API client (Axios configuration) |
| `api-client.ts` | Alternative/legacy API client |

### Utilities (`frontend/src/lib/`)

Helper functions and configurations.

| File | Purpose |
|------|---------|
| `config.ts` | Application configuration (API URLs, constants) |
| `auth.ts` | Authentication utilities |
| `authClient.ts` | Better Auth client setup |
| `authUtils.ts` | Authentication helper functions |
| `queryClient.ts` | React Query client configuration |
| `api.ts` | API utilities and helpers |

### Static Assets (`frontend/public/`)

Static files (images, fonts, etc.) served directly.

---

## 📁 PROJECT SPECIFICATIONS (`specs/`)

Archived specification documents by development phase.

| Phase | Directory | Purpose |
|-------|-----------|---------|
| Phase 1 | `1-todo-console-app/` | Console-based todo app specification |
| Phase 2 | `2-multi-user-todo-web-app/` | Multi-user web app specification |
| Phase 3 | `3-web-ui/` | Web UI specification |
| Phase 4 | `4-backend-crud/` | Backend CRUD operations spec |
| Phase 5 | `5-frontend-improved-ui/` | Frontend UI improvements spec |
| Phase 6 | `6-dashboard-improvement/` | Dashboard feature spec |
| Phase 7 | `7-better-auth/` | Better Auth implementation spec |
| Phase 9 | `9-chatbot-backend/` | Chatbot backend spec |

---

## 📚 DOCUMENTATION (`docs/`)

| File | Purpose |
|------|---------|
| `nextjs-task-deletion-fixes-summary.md` | Fixes summary for task deletion in Next.js |

---

## 🧪 TEST STRUCTURE

### Root Level Tests
- `test_dashboard.py` - Dashboard functionality testing
- `test_enhanced_ui.py` - Enhanced UI component testing

### Backend Tests (`backend/`)
- Unit and integration tests for API endpoints
- Authentication and session tests
- Task CRUD operation tests

### Frontend Tests (`frontend/src/tests/`)
- Component unit tests
- Integration tests
- UI interaction tests

### Main Test Directories
- `tests/` - Workspace-level tests
  - `unit/` - Unit tests
  - `integration/` - Integration tests
  - `conftest.py` - Pytest configuration

---

## 🔑 KEY DEPENDENCIES

### Backend (Python)
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlmodel** - ORM/SQL toolkit
- **psycopg2-binary** - PostgreSQL adapter
- **passlib[bcrypt]** - Password hashing
- **python-dotenv** - Environment variable management
- **python-socketio** - WebSocket support
- **openai** - OpenAI API integration
- **mcp-sdk** - Model Context Protocol
- **slowapi** - Rate limiting

### Frontend (JavaScript/TypeScript)
- **next** - React framework
- **react** - UI library
- **typescript** - Type safety
- **tailwindcss** - Utility-first CSS
- **axios** - HTTP client
- **better-auth** - Authentication
- **socket.io-client** - Real-time communication
- **framer-motion** - Animation library
- **lucide-react** - Icon library

---

## 🏗️ APPLICATION ARCHITECTURE

### Data Flow
1. **Frontend (Next.js)** → Makes HTTP requests to Backend API
2. **Backend (FastAPI)** → Validates requests, processes business logic
3. **Database (PostgreSQL)** → Stores persistent data
4. **Real-time** → WebSocket connections for chat/updates

### Authentication Flow
1. User signs up/logs in via frontend
2. Backend validates credentials and generates JWT
3. Frontend stores token (localStorage/cookies)
4. All subsequent requests include JWT in headers
5. Backend validates JWT for protected endpoints

### Key Features
- ✅ User Authentication (signup, login, logout)
- ✅ Task Management (CRUD operations)
- ✅ User Isolation (users only see their tasks)
- ✅ Dashboard (statistics and analytics)
- ✅ Real-time Chat (with AI agent)
- ✅ Rate Limiting (API protection)
- ✅ Error Handling (global exception handlers)
- ✅ Database Migrations (schema versioning)

---

## 🚀 DEPLOYMENT

### Docker Support
- `backend/Dockerfile` - Backend container definition
- Can be containerized and deployed to cloud platforms

### Configuration
- **Development** - Uses `.env` file
- **Production** - Uses `production_config.py`

---

## 📝 CONFIGURATION FILES

| File | Purpose |
|------|---------|
| `.env` | Environment variables (backend) |
| `.gitignore` | Git ignore rules |
| `CLAUDE.md` | AI coding guidelines |
| `chatbot-structure.md` | Chatbot integration details |
| `backend-details.md` | Backend documentation |
| `frontend-details.md` | Frontend documentation |
| `README.md` | Main project documentation |

---

## 🔄 Development Workflow

1. **Backend Development** - Edit files in `backend/` → Run tests → Test with API client
2. **Frontend Development** - Edit components in `frontend/src/` → Hot reload → Test in browser
3. **Database Changes** - Create migrations in `backend/database/migrations/` → Run migrations
4. **Testing** - Run pytest for backend tests, Jest/Vitest for frontend tests
5. **Deployment** - Build Docker image → Deploy to production

---

## 📊 Project Statistics

- **Backend Files**: ~50+ Python files (models, services, routers, tests)
- **Frontend Components**: ~18+ TypeScript React components
- **API Endpoints**: ~25+ endpoints (auth, tasks, dashboard, chat)
- **Database Models**: 7 main models (user, task, session, account, etc.)
- **Test Coverage**: Comprehensive unit and integration tests

---

## ✨ Notable Features

- **Better Auth Integration** - Modern authentication system
- **Real-time Chat** - WebSocket-based messaging with AI agent
- **MCP Server** - Model Context Protocol for AI integration
- **Dashboard Analytics** - User statistics and task insights
- **Rate Limiting** - API protection against abuse
- **Database Migrations** - Version-controlled schema changes
- **Responsive UI** - Mobile-friendly design with Tailwind CSS
- **Type Safety** - Full TypeScript implementation

---

## 🛠️ Quick Reference

| Task | Location |
|------|----------|
| Add new API endpoint | `backend/api/` + create router |
| Add new component | `backend/frontend/src/components/` |
| Update database model | `backend/models/` |
| Create migration | `backend/database/migrations/` |
| Add business logic | `backend/services/` |
| Configure settings | `backend/config.py` |
| Update dependencies | Update `requirements.txt` or `package.json` |
| Write tests | Create test file in `backend/` or `frontend/src/tests/` |

---

**Last Updated:** January 16, 2026
**Project Status:** Active Development
**Phase:** 9+ (Chatbot Backend Implemented)
