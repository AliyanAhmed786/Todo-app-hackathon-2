# Todo App Hackathon - Complete Project Structure & File Analysis

**Project Type:** Full-Stack Multi-User Todo Application with Real-time Chat & Dashboard
**Architecture:** Next.js Frontend + FastAPI Backend + PostgreSQL Database
**Authentication:** Better Auth (Database Session Validation)
**Date Generated:** January 16, 2026

---

## 📑 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Backend Architecture & Files](#backend-architecture--files)
3. [Frontend Architecture & Files](#frontend-architecture--files)
4. [Database & Models](#database--models)
5. [API Endpoints](#api-endpoints)
6. [Authentication Flow](#authentication-flow)
7. [File Purpose Reference](#file-purpose-reference)
8. [Data Flow Diagrams](#data-flow-diagrams)

---

## 🎯 PROJECT OVERVIEW

### Key Statistics
- **Backend Files:** ~50+ Python files
- **Frontend Components:** ~18+ TypeScript React components
- **API Endpoints:** ~25+ endpoints
- **Database Models:** 7 core models
- **Services:** 6 business logic services
- **Test Files:** 9+ comprehensive test files

### Tech Stack Details
```
Frontend:
  - Next.js 16.1.1 (React 19)
  - TypeScript 5
  - Tailwind CSS 4
  - Axios for HTTP client
  - Socket.IO for real-time communication
  - Framer Motion for animations

Backend:
  - FastAPI 0.115.0
  - SQLModel 0.0.22 (ORM)
  - PostgreSQL (Neon)
  - Better Auth (custom session validation)
  - Python 3.11+

Database:
  - Neon PostgreSQL (managed)
  - Async connection pooling
  - SQLAlchemy async engine
```

---

## 🔧 BACKEND ARCHITECTURE & FILES

### Root Backend Files

#### `backend/main.py` - Application Entry Point
**Purpose:** FastAPI application initialization and setup
**Key Functions:**
- Sets up logging (console + rotating file handler)
- Configures CORS middleware for frontend communication
- Defines lifespan events (startup/shutdown)
- Registers all API routers
- Mounts WebSocket/Socket.IO server
- Health check endpoint for monitoring
- Root welcome endpoint

**Code Example:**
```python
# Creates FastAPI app with:
app = FastAPI(
    title="Todo App Backend API",
    description="Backend CRUD API for Todo App",
    version="1.0.0",
    lifespan=lifespan  # Handles startup/shutdown
)

# Includes routers:
app.include_router(task_router, prefix="/api/tasks")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(dashboard_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
```

#### `backend/config.py` - Application Configuration
**Purpose:** Centralized configuration management using Pydantic Settings
**Key Settings:**
- `database_url` - PostgreSQL connection string
- `secret_key` - JWT secret key
- `algorithm` - JWT algorithm (HS256)
- `access_token_expire_minutes` - Token lifetime (30 min)
- `refresh_token_expire_days` - Refresh token lifetime (7 days)
- `debug` - Debug mode toggle
- `rate_limit_requests` - Rate limiting configuration
- `better_auth_secret` - Better Auth secret key

**Code Example:**
```python
class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY", "dev-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
```

#### `backend/production_config.py` - Production Settings
**Purpose:** Production-specific configuration overrides
**Used For:** Environment-specific settings when deploying to production

#### `backend/requirements.txt` - Python Dependencies
**Core Dependencies:**
- `fastapi==0.115.0` - Web framework
- `uvicorn[standard]==0.32.0` - ASGI server
- `sqlmodel==0.0.22` - ORM & database models
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `passlib[bcrypt]==1.7.4` - Password hashing
- `python-socketio==5.11.4` - WebSocket support
- `openai==1.52.2` - OpenAI API integration
- `pytest==8.3.3` - Testing framework

#### `backend/.env` - Environment Variables
**Contains:**
- DATABASE_URL - Neon PostgreSQL connection
- SECRET_KEY - JWT signing key
- ALGORITHM - JWT algorithm
- DEBUG - Debug mode flag
- BETTER_AUTH_SECRET - Authentication secret

#### `backend/Dockerfile` - Docker Container Definition
**Purpose:** Container configuration for deployment
**Builds:** Python environment with all dependencies

#### `backend/deploy.py` - Deployment Configuration
**Purpose:** Deployment scripts and settings for production deployment

#### `backend/reset_database.py` - Database Reset Utility
**Purpose:** Clear and reinitialize database (development only)

#### `backend/setup.py` - Package Installation
**Purpose:** Python package setup and installation configuration

#### `backend/todo_app.db` - Fallback SQLite Database
**Purpose:** Local SQLite database for development when PostgreSQL unavailable

#### `backend/app.log` - Application Log File
**Purpose:** Rolling log file with application events and errors (10MB max, 5 backups)

#### `backend/README.md` - Backend Documentation
**Purpose:** Backend-specific setup and usage documentation

---

### API Layer (`backend/api/`)

All routers handle HTTP requests and return JSON responses. They use Better Auth for authentication.

#### `backend/api/auth_router.py` - Authentication Endpoints
**Purpose:** Handle user registration, login, logout, and session management
**Endpoints:**
```
POST /api/auth/signup        - Register new user
POST /api/auth/login         - Login user (returns JWT + session)
POST /api/auth/logout        - Logout user
GET  /api/auth/me            - Get current user profile
POST /api/auth/refresh       - Refresh JWT token
GET  /api/auth/verify-session - Verify session validity
```

**Key Features:**
- Password validation and hashing with bcrypt
- JWT token generation and validation
- Database session creation for Better Auth
- HTTP-only cookies for session tokens
- Input sanitization and validation
- Rate limiting applied

**Code Example:**
```python
@router.post("/signup", status_code=201)
async def register_user(user_in: UserCreateRequest, db: AsyncSession):
    # Validate input, create user, generate session & JWT tokens
    # Return user data with access_token and refresh_token
    # Set HTTP-only cookie with session token
```

#### `backend/api/task_router.py` - Task Management Endpoints
**Purpose:** Handle CRUD operations for tasks
**Endpoints:**
```
GET    /api/tasks              - Get all user's tasks
POST   /api/tasks              - Create new task
GET    /api/tasks/{id}         - Get single task
PUT    /api/tasks/{id}         - Update task
DELETE /api/tasks/{id}         - Delete task
GET    /api/tasks/stats        - Get task statistics (internal)
```

**Features:**
- User isolation (users only see their own tasks)
- Pagination support (skip, limit)
- Filtering by status
- Search by title/description
- Task priority levels (Low, Medium, High)
- Due date tracking
- Timestamps (created_at, updated_at)

**Task Properties:**
- `id` - Unique identifier
- `title` - Task title (required)
- `description` - Detailed description
- `status` - Completion flag (true/false)
- `priority` - 1=Low, 2=Medium, 3=High
- `category` - Optional category
- `due_date` - Optional deadline
- `user_id` - Foreign key to user
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

#### `backend/api/dashboard_router.py` - Dashboard Statistics
**Purpose:** Provide dashboard analytics and statistics
**Endpoints:**
```
GET /api/dashboard/stats      - Get user's dashboard statistics
```

**Returns:**
```json
{
  "total_tasks": 25,
  "completed_tasks": 15,
  "pending_tasks": 10,
  "completion_rate": 60.0
}
```

#### `backend/api/chat_router.py` - Chat Functionality
**Purpose:** Handle real-time chat and AI chatbot integration
**Uses:** WebSocket connection via Socket.IO
**Features:**
- Real-time message delivery
- AI agent for task assistance
- Message history
- User presence tracking

---

### Database Layer (`backend/database/`)

#### `backend/database/connection.py` - Database Connection
**Purpose:** Establish and manage PostgreSQL connection pool
**Key Features:**
- Async SQLAlchemy engine with asyncpg driver
- Connection pooling (20 base + 10 overflow)
- Connection recycling every 4.5 minutes (Neon timeout is 5 min)
- Pre-ping verification before using connections
- Connection timeout: 10 seconds
- Query timeout: 30 seconds

**Code Example:**
```python
engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,      # Verify connections
    pool_recycle=280,        # Recycle every 4.5 min
    pool_size=20,            # Base pool size
    max_overflow=10,         # Additional connections
    pool_timeout=30          # Wait time for connection
)
```

#### `backend/database/session.py` - Session Management
**Purpose:** Database session factory and dependency injection
**Provides:**
- `get_async_db_session()` - Async context manager
- `get_db_session_generator()` - FastAPI dependency

**Features:**
- Automatic commit on success
- Rollback on exceptions
- Proper connection cleanup
- No connection leaks

#### `backend/database/migrations.py` - Schema Creation
**Purpose:** Initialize database tables from SQLModel models
**Function:**
```python
async def create_db_and_tables():
    # Creates all tables defined in models
    # Called during application startup
```

**Tables Created:**
- `user` - User accounts
- `task` - Todo tasks
- `session` - Authentication sessions
- `account` - Account details
- `verification` - Email verification tokens
- `conversation` - Chat conversations
- `message` - Chat messages

#### `backend/database/add_due_date_migration.py`
**Purpose:** Migration to add due_date field to tasks table

#### `backend/database/complete_schema_migration.py`
**Purpose:** Comprehensive schema migration

#### `backend/database/schema_updater.py`
**Purpose:** Schema update utilities and helpers

#### `backend/database/migrations/` - Migration Files Directory
**Purpose:** Store migration scripts for version control

---

### Models Layer (`backend/models/`)

SQLModel models = SQLAlchemy ORM + Pydantic validation

#### `backend/models/user.py` - User Model
**Purpose:** Define User database table structure
**Fields:**
- `id` (UUID) - Unique identifier
- `email` (EmailStr) - Unique email address
- `name` (str) - User's full name
- `password_hash` (str) - Hashed password
- `is_active` (bool) - Account active flag
- `created_at` (datetime) - Registration timestamp
- `updated_at` (datetime) - Last update timestamp

**Validation:**
- Input sanitization (remove SQL injection patterns, XSS attempts)
- Email format validation
- Name length limits (1-100 characters)
- Password strength requirements
- Unique email constraint

**Code Example:**
```python
class User(UserBase, table=True):
    __tablename__ = "user"
    
    id: str = Field(default_factory=uuid4, primary_key=True)
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship()
```

#### `backend/models/task.py` - Task Model
**Purpose:** Define Task database table structure
**Fields:**
- `id` (int) - Auto-incrementing ID
- `title` (str) - Task title (1-200 chars)
- `description` (str) - Detailed description (0-1000 chars)
- `status` (bool) - Completion status
- `priority` (enum) - 1=Low, 2=Medium, 3=High
- `category` (str) - Optional category
- `due_date` (datetime) - Optional deadline
- `user_id` (str) - FK to User
- `created_at` (datetime) - Creation time
- `updated_at` (datetime) - Last update time

**Validation:**
- Title length (1-200 chars)
- Description length (0-1000 chars)
- Valid priority values
- Input sanitization
- User isolation (tasks belong to users)

#### `backend/models/session.py` - Session Model
**Purpose:** Store Better Auth sessions in database
**Fields:**
- `id` (str) - Session UUID
- `token` (str) - Session token (urlsafe)
- `user_id` (str) - FK to User
- `expires_at` (datetime) - Expiration time
- `created_at` (datetime) - Creation time

**Purpose:** Database-backed session validation instead of stateless JWT

#### `backend/models/account.py` - Account Model
**Purpose:** Extended account information
**Fields:** Account profile and metadata

#### `backend/models/verification.py` - Verification Model
**Purpose:** Email verification and password reset tokens
**Fields:** Token, user_id, expiration, type

#### `backend/models/conversation.py` - Conversation Model
**Purpose:** Chat conversation thread
**Fields:** ID, participants, creation time, last activity

#### `backend/models/message.py` - Message Model
**Purpose:** Individual chat messages
**Fields:** ID, conversation_id, sender_id, content, timestamp

---

### Services Layer (`backend/services/`)

Business logic tier - handles all data operations and rules.

#### `backend/services/user_service.py` - User Operations
**Functions:**
```python
create_user()           - Register new user
authenticate_user()     - Verify email & password
get_user()              - Fetch user by ID
update_user()           - Update user profile
delete_user()           - Delete user account (cascades)
get_user_by_email()     - Find user by email
```

**Example:**
```python
async def create_user(*, db_session, email, password, name):
    # Hash password with bcrypt
    # Create User model instance
    # Add to database
    # Return created user
```

#### `backend/services/task_service.py` - Task Operations
**Functions:**
```python
create_task()           - Create new task
get_task_by_id()        - Get single task (with ownership check)
get_tasks_by_user()     - Get all user's tasks
update_task()           - Update task fields
delete_task()           - Delete task
get_dashboard_stats_for_user() - Aggregate statistics
```

**Code Example:**
```python
async def create_task(*, db_session, task_in, user_id):
    task = Task.model_validate(task_in, update={"user_id": user_id})
    db_session.add(task)
    await db_session.commit()
    return task

async def delete_task(*, db_session, task_id, user_id):
    task = await get_task_by_id(db_session, task_id, user_id)
    await db_session.delete(task)
    await db_session.commit()
```

#### `backend/services/registration_service.py` - Registration Logic
**Purpose:** Handle user registration workflow
**Functions:**
- Validate email doesn't exist
- Hash password securely
- Create user and initial session
- Send verification email (optional)
- Return user object with session

#### `backend/services/login_service.py` - Login Logic
**Purpose:** Handle user login workflow
**Functions:**
```python
async def login_user(*, db_session, email, password):
    # Authenticate user
    # Create database session
    # Generate JWT tokens
    # Return user + session
```

**Returns:** Tuple[User, Session]

#### `backend/services/logout_service.py` - Logout Logic
**Purpose:** Handle user logout
**Functions:**
- Invalidate session token
- Clear database session record
- Optional JWT token blacklist

#### `backend/services/session_service.py` - Session Management
**Purpose:** Manage user sessions
**Functions:**
- Create session
- Validate session token
- Refresh session expiration
- Destroy session

---

### Middleware (`backend/middleware/`)

Request/response processing and cross-cutting concerns.

#### `backend/middleware/auth.py` - Authentication Middleware
**Purpose:** Validate JWT tokens and extract user information
**Functions:**
```python
async def get_current_user(request: Request) -> dict:
    # Extract session token from cookies
    # Validate against database
    # Return user dictionary
```

**Used in:** Dependency injection for protected routes

**Example:**
```python
@router.get("/tasks")
async def get_tasks(current_user: dict = Depends(get_current_user)):
    # current_user is already authenticated
    user_id = current_user.get("id")
```

#### `backend/middleware/better_auth.py` - Better Auth Integration
**Purpose:** Better Auth specific session validation
**Functions:**
```python
async def get_current_user_from_session(request):
    # Extract session token from better-auth cookie
    # Query database for valid session
    # Return authenticated user
```

#### `backend/middleware/rate_limiter.py` - Rate Limiting
**Purpose:** Prevent API abuse
**Implementation:** Uses slowapi library
**Limits:**
- General endpoints: 100 requests per 60 seconds
- Dashboard endpoints: 50 requests per 60 seconds
- Chat endpoints: configurable limits

**Code Pattern:**
```python
@router.get("/tasks")
@limiter.limit("100/minute")
async def get_tasks(request: Request):
    # Limited to 100 requests per minute
```

---

### Dependencies (`backend/dependencies/`)

FastAPI dependency injection functions.

#### `backend/dependencies/auth.py` - Auth Dependencies
**Functions:**
```python
async def get_current_user(request, db) -> dict:
    # Dependency for protected endpoints
    # Returns authenticated user dictionary

def verify_user_owns_resource(user_id, resource_user_id) -> bool:
    # Verify user owns the resource
```

**Usage:**
```python
@router.get("/tasks")
async def get_tasks(current_user: dict = Depends(get_current_user)):
    # Automatically validated
```

#### `backend/dependencies/chat_auth.py` - Chat Authentication
**Purpose:** Chat-specific authentication dependencies

---

### Schemas (`backend/schemas/`)

Pydantic request/response validation schemas.

#### `backend/schemas/auth.py` - Authentication Schemas
**Schemas:**
```python
class UserCreateRequest:
    name: str
    email: EmailStr
    password: str

class UserLoginRequest:
    email: EmailStr
    password: str

class AuthResponse:
    user: dict
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
```

#### `backend/schemas/task.py` - Task Schemas
**Schemas:**
```python
class TaskCreateRequest:
    title: str              # Required
    description: Optional[str] = None
    priority: int = 2       # Default Medium
    category: Optional[str] = None

class TaskUpdateRequest:
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    priority: Optional[int] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskResponse:
    id: int
    title: str
    description: Optional[str]
    status: bool
    priority: int
    category: Optional[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

#### `backend/schemas/user.py` - User Schemas
**Schemas:** User profile and update schemas

---

### Exception Handling (`backend/exceptions/`)

#### `backend/exceptions/handlers.py` - Exception Handlers
**Custom Exceptions:**
```python
class TaskNotFoundError(HTTPException):
    # 404 - Task doesn't exist

class UserNotFoundError(HTTPException):
    # 404 - User doesn't exist

class UnauthorizedAccessError(HTTPException):
    # 403 - User lacks permission

class ValidationError(HTTPException):
    # 422 - Invalid input

class DatabaseError(HTTPException):
    # 500 - Database operation failed
```

**Global Exception Handlers:**
```python
async def http_exception_handler()
async def validation_exception_handler()
async def database_exception_handler()
async def general_exception_handler()
```

#### `backend/exceptions/chat_exceptions.py`
**Purpose:** Chat-specific exceptions

---

### Agents (`backend/agents/`)

#### `backend/agents/chat_agent.py` - AI Chat Agent
**Purpose:** Handle AI-powered chat responses
**Features:**
- Task creation from natural language
- Task completion assistance
- Dashboard queries
- OpenAI API integration

---

### MCP Integration (`backend/mcp/`)

Model Context Protocol for AI integration.

#### `backend/mcp/server.py` - MCP Server
**Purpose:** Host MCP tools for AI agent
**Tools Provided:**
- `add_task` - Create task from AI
- `list_tasks` - Fetch user's tasks
- `complete_task` - Mark task done
- `delete_task` - Remove task
- `update_task` - Modify task

**Code Example:**
```python
class MCPServer:
    async def initialize_tools(self):
        self.tools = {
            "add_task": tools_instance.add_task,
            "list_tasks": tools_instance.list_tasks,
            # ... more tools
        }
```

#### `backend/mcp/config.py` - MCP Configuration

#### `backend/mcp/tools.py` - MCP Tool Implementations

---

### Test Files (`backend/`)

#### `backend/test_main.py`
**Tests:** Main application setup

#### `backend/test_dashboard.py`
**Tests:** Dashboard endpoint functionality

#### `backend/test_comprehensive_better_auth.py`
**Tests:** Complete authentication flow (signup, login, logout, session)

#### `backend/test_better_auth_registration.py`
**Tests:** User registration and validation

#### `backend/test_better_auth_login.py`
**Tests:** Login flow and JWT generation

#### `backend/test_better_auth_logout.py`
**Tests:** Logout and session invalidation

#### `backend/test_better_auth_task_crud.py`
**Tests:** Task CRUD with authentication

#### `backend/test_better_auth_session_persistence.py`
**Tests:** Session persistence across requests

#### `backend/test_account_deletion_cascade.py`
**Tests:** User deletion and cascade delete of related tasks

---

## 🎨 FRONTEND ARCHITECTURE & FILES

### Root Configuration

#### `frontend/package.json` - Dependencies & Scripts
**Scripts:**
```json
"dev": "next dev"           - Start dev server (port 3000)
"build": "next build"       - Production build
"start": "next start"       - Run production build
"lint": "next lint"         - Run ESLint
```

**Key Dependencies:**
- `next@16.1.1` - React framework
- `react@19.0.0` - UI library
- `typescript@5` - Type safety
- `tailwindcss@4` - Styling
- `axios@1.6.0` - HTTP client
- `better-auth@0.0.1-beta.9` - Auth client
- `socket.io-client@4.8.3` - Real-time chat
- `framer-motion@11.18.2` - Animations
- `lucide-react@0.562.0` - Icons

#### `frontend/tsconfig.json` - TypeScript Configuration
**Settings:** Strict mode, target ES2020, module resolution

#### `frontend/tailwind.config.ts` - Tailwind Customization
**Customizations:** Theme colors, spacing, breakpoints

#### `frontend/postcss.config.js` - PostCSS Config
**Plugins:** Tailwind CSS, Autoprefixer

#### `frontend/next-env.d.ts` - Next.js Types
**Purpose:** TypeScript type definitions for Next.js

#### `frontend/next.config.js` (if exists)
**Purpose:** Next.js configuration

---

### Source Files (`frontend/src/`)

#### `frontend/src/app/` - App Shell
**Purpose:** App layout and global setup
**Contains:** Root layout, providers, global styles

#### `frontend/src/pages/homepage.tsx` - Home Page
**Purpose:** Landing/home page
**Route:** `/`
**Features:** Welcome message, quick links, featured info

---

### Components (`frontend/src/components/`)

Reusable React UI components with TypeScript interfaces.

#### `frontend/src/components/HomePage.tsx`
**Purpose:** Home page component
**Features:** Hero section, quick actions, intro content

#### `frontend/src/components/LoginForm.tsx`
**Purpose:** Login form (server-side)
**Type:** Form component using React hook form
**Fields:** Email, Password
**Features:** Input validation, error display, submit button

#### `frontend/src/components/LoginFormClient.tsx`
**Purpose:** Login form (client-side with hooks)
**Type:** Client component for interactivity
**Features:** Real-time validation, error handling, redirect on success

#### `frontend/src/components/SignupForm.tsx`
**Purpose:** Registration form (server-side)
**Fields:** Name, Email, Password, Confirm Password
**Features:** Password strength meter, email validation

#### `frontend/src/components/SignupFormClient.tsx`
**Purpose:** Registration form (client-side)
**Type:** Client component
**Features:** Real-time validation, success toast

#### `frontend/src/components/TaskForm.tsx`
**Purpose:** Create/edit task form
**Fields:**
- Title (required)
- Description (optional)
- Priority (Low/Medium/High)
- Category (optional)
- Due Date (optional)

**Features:**
- Form validation
- Autocomplete for categories
- Date picker for due date
- Submit and cancel buttons

#### `frontend/src/components/TaskList.tsx`
**Purpose:** Display and manage tasks
**Features:**
```tsx
- Display all user tasks
- Filter by status (All/Pending/Completed)
- Search by title
- Mark complete/incomplete
- Edit task (modal)
- Delete task (confirmation)
- Sort by priority/date
- Show task count
- Loading and error states
```

**Code Example:**
```tsx
interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: 'High' | 'Medium' | 'Low';
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
}

const TaskList: React.FC<TaskListProps> = ({ onTaskChange }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  
  useEffect(() => {
    fetchTasks();  // Load tasks on mount
  }, []);
  
  // Render tasks with interactive controls
};
```

#### `frontend/src/components/TaskEditModal.tsx`
**Purpose:** Modal for editing tasks
**Features:**
- Popup overlay
- Pre-filled form fields
- Save/Cancel buttons
- Real-time validation

#### `frontend/src/components/DashboardPageClient.tsx`
**Purpose:** Main dashboard page (client-side)
**Features:**
```tsx
- Display user name & email
- Dashboard statistics (Total, Completed, Pending tasks)
- Logout button
- TaskList component
- ChatBot component
- Error handling
- Loading states
- Real-time stats updates
```

**Code Example:**
```tsx
export const DashboardPageClient: React.FC = () => {
  const router = useRouter();
  const { data: session } = authClient.useSession();
  const [dashboardStats, setDashboardStats] = useState({
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0
  });
  
  const fetchDashboardStats = useCallback(async () => {
    const response = await dashboardAPI.getStats();
    setDashboardStats(response.data);
  }, []);
  
  // Render dashboard with stats and task list
};
```

#### `frontend/src/components/DashboardStats.tsx`
**Purpose:** Display dashboard statistics cards
**Shows:**
- Total tasks count
- Completed tasks count
- Pending tasks count
- Completion percentage
- Visual cards with icons

#### `frontend/src/components/Navbar.tsx`
**Purpose:** Navigation bar
**Features:**
- Logo/branding
- Links to main sections
- User dropdown (profile, logout)
- Mobile responsive menu
- Active route highlighting

#### `frontend/src/components/ProtectedRoute.tsx`
**Purpose:** Route protection wrapper
**Features:**
- Check authentication status
- Redirect unauthenticated users to login
- Display loading state while checking auth
- Works with Next.js navigation

#### `frontend/src/components/Modal.tsx`
**Purpose:** Reusable modal component
**Props:**
```tsx
isOpen: boolean
onClose: () => void
title: string
children: ReactNode
```

#### `frontend/src/components/DeleteConfirmationModal.tsx`
**Purpose:** Confirmation dialog for deletions
**Features:**
- Warning message
- Cancel/Confirm buttons
- Prevents accidental deletion

#### `frontend/src/components/ToastNotification.tsx`
**Purpose:** Toast notification component
**Types:** Success, Error, Warning, Info
**Features:**
- Auto-dismiss after delay
- Close button
- Animated entrance/exit

#### `frontend/src/components/LoadingSpinner.tsx`
**Purpose:** Loading indicator
**Displays:** Spinning animation with optional message

#### `frontend/src/components/ErrorBoundary.tsx`
**Purpose:** Error boundary for React components
**Features:**
- Catch errors in child components
- Display error UI
- Fallback content

#### `frontend/src/components/chatbot-ui/ChatBot.tsx`
**Purpose:** AI chatbot interface
**Features:**
- Chat message display
- Message input
- Real-time message updates via WebSocket
- Task creation from chat
- AI responses

---

### Services (`frontend/src/services/`)

API communication layer.

#### `frontend/src/services/api.ts` - API Client
**Purpose:** Axios instance and API functions
**Setup:**
```typescript
const api = axios.create({
  baseURL: API_BASE_URL,  // http://localhost:8000
  timeout: 30000,
  withCredentials: true   // For Better Auth cookies
});

// Request/response interceptors for auth error handling
```

**API Collections:**
```typescript
export const authAPI = {
  register(): Promise<AxiosResponse>
  login(): Promise<AxiosResponse>
  logout(): Promise<AxiosResponse>
  me(): Promise<AxiosResponse>
}

export const taskAPI = {
  getTasks(): Promise<AxiosResponse>
  createTask(): Promise<AxiosResponse>
  updateTask(): Promise<AxiosResponse>
  deleteTask(): Promise<AxiosResponse>
  getTask(): Promise<AxiosResponse>
}

export const dashboardAPI = {
  getStats(): Promise<AxiosResponse>
}

export const chatAPI = {
  sendMessage(): Promise<AxiosResponse>
  getMessages(): Promise<AxiosResponse>
}
```

---

### Libraries (`frontend/src/lib/`)

Utility functions and helper libraries.

#### `frontend/src/lib/api.ts` - Server Actions
**Purpose:** Server-side API functions using Next.js Server Actions
**Type:** `'use server'` directive
**Functions:**
```typescript
authServerActions = {
  register(name, email, password)
  login(email, password)
  logout()
}

taskServerActions = {
  getTasks()
  createTask(task)
  updateTask(id, task)
  deleteTask(id)
}
```

#### `frontend/src/lib/auth.ts` - Server-side Auth
**Purpose:** Authentication utilities for server components
**Functions:**
```typescript
getServerToken(): Promise<string | null>
isServerAuthenticated(): Promise<boolean>
getServerUserId(): Promise<string | null>
setServerToken(token: string): Promise<void>
removeServerToken(): Promise<void>
```

**Features:**
- JWT decoding
- Token management
- Cookie handling

#### `frontend/src/lib/authClient.ts` - Client-side Auth
**Purpose:** Better Auth client setup
**Features:**
- `useSession()` hook for session state
- `signIn()` function
- `signOut()` function
- `signUp()` function

#### `frontend/src/lib/authUtils.ts` - Auth Utilities
**Purpose:** Helper functions for authentication
**Functions:**
- Validate session
- Check authentication state
- Format auth errors

#### `frontend/src/lib/config.ts` - Configuration
**Purpose:** Application constants and config
**Contains:**
- API base URL
- Feature flags
- Timeouts
- Limits

#### `frontend/src/lib/queryClient.ts` - React Query Setup
**Purpose:** React Query client configuration
**Features:**
- Cache settings
- Retry logic
- Refetch behavior

---

### Utils (`frontend/src/utils/`)

Helper functions and utilities.

#### `frontend/src/utils/auth.ts` - Auth Helpers
**Functions:**
```typescript
redirectToLogin(): void
isAuthError(error): boolean
isValidSession(session): boolean
```

---

### Styles (`frontend/src/styles/`)

Global CSS and styling.

#### `frontend/src/styles/globals.css`
**Purpose:** Global styles and Tailwind imports

---

### Tests (`frontend/src/tests/`)

Component and integration tests.

---

### Public Assets (`frontend/public/`)

Static files served directly (images, fonts, etc.).

---

## 🗄️ DATABASE & MODELS

### Database Schema

```sql
-- Users Table
CREATE TABLE "user" (
  id UUID PRIMARY KEY,
  email VARCHAR(200) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  password_hash VARCHAR NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Tasks Table
CREATE TABLE task (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description VARCHAR(1000),
  status BOOLEAN DEFAULT FALSE,
  priority INTEGER DEFAULT 2,  -- 1=Low, 2=Medium, 3=High
  category VARCHAR(100),
  due_date TIMESTAMP,
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Sessions Table (Better Auth)
CREATE TABLE session (
  id VARCHAR PRIMARY KEY,
  token VARCHAR NOT NULL UNIQUE,
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Account Table
CREATE TABLE account (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  -- Additional account fields
);

-- Verification Table
CREATE TABLE verification (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES "user"(id),
  token VARCHAR NOT NULL UNIQUE,
  type VARCHAR NOT NULL,  -- 'email', 'password_reset'
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Conversations Table
CREATE TABLE conversation (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Messages Table
CREATE TABLE message (
  id UUID PRIMARY KEY,
  conversation_id UUID NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
  sender_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Relationships

```
User (1) ---> (Many) Task
User (1) ---> (Many) Session
User (1) ---> (Many) Account
User (1) ---> (Many) Verification
User (1) ---> (Many) Conversation
User (1) ---> (Many) Message (as sender)
Conversation (1) ---> (Many) Message
```

---

## 📡 API ENDPOINTS

### Authentication Endpoints

| Method | Endpoint | Description | Auth | Returns |
|--------|----------|-------------|------|---------|
| POST | `/api/auth/signup` | Register new user | ❌ | User + JWT tokens |
| POST | `/api/auth/login` | Login user | ❌ | User + JWT tokens |
| POST | `/api/auth/logout` | Logout user | ✅ | Success message |
| GET | `/api/auth/me` | Get current user | ✅ | User profile |
| POST | `/api/auth/refresh` | Refresh JWT | ✅ | New JWT token |
| GET | `/api/auth/verify-session` | Verify session | ✅ | Session validity |

### Task Endpoints

| Method | Endpoint | Description | Auth | Returns |
|--------|----------|-------------|------|---------|
| GET | `/api/tasks` | Get all user tasks | ✅ | Task[] |
| POST | `/api/tasks` | Create task | ✅ | Task |
| GET | `/api/tasks/{id}` | Get single task | ✅ | Task |
| PUT | `/api/tasks/{id}` | Update task | ✅ | Task |
| DELETE | `/api/tasks/{id}` | Delete task | ✅ | Success |

### Dashboard Endpoints

| Method | Endpoint | Description | Auth | Returns |
|--------|----------|-------------|------|---------|
| GET | `/api/dashboard/stats` | Get stats | ✅ | Stats JSON |

### Chat Endpoints

| Method | Endpoint | Description | Auth | Returns |
|--------|----------|-------------|------|---------|
| WS | `/ws` | WebSocket connection | ✅ | Real-time messages |
| GET | `/api/chat/messages` | Get message history | ✅ | Message[] |

### System Endpoints

| Method | Endpoint | Description | Auth | Returns |
|--------|----------|-------------|------|---------|
| GET | `/health` | Health check | ❌ | Health status |
| GET | `/` | Welcome message | ❌ | Welcome JSON |

---

## 🔐 AUTHENTICATION FLOW

### Signup Flow
```
1. User fills signup form (name, email, password)
2. Frontend POST /api/auth/signup
3. Backend validates input and checks email uniqueness
4. Backend creates User in database (password hashed)
5. Backend creates Session in database
6. Backend generates JWT tokens (access + refresh)
7. Backend sets HTTP-only cookie with session token
8. Frontend stores JWT in localStorage
9. Frontend redirects to dashboard
```

### Login Flow
```
1. User enters email & password
2. Frontend POST /api/auth/login
3. Backend queries user by email
4. Backend verifies password with bcrypt
5. Backend creates Session in database
6. Backend generates JWT tokens
7. Backend sets HTTP-only cookie
8. Frontend stores JWT
9. Frontend redirects to dashboard
```

### Protected Request Flow
```
1. Frontend makes request to /api/tasks
2. Frontend includes JWT in Authorization header (Bearer token)
3. Frontend includes HTTP-only cookie (browser auto-adds)
4. Backend receives request
5. Backend extracts session from cookie
6. Backend queries database for session validity
7. Backend gets user_id from session
8. Backend validates user is authenticated
9. Backend processes request
10. Backend returns data for authenticated user only
```

### Session Validation (Better Auth Approach)
```
Better Auth uses DATABASE session validation instead of JWT:

1. Session token stored in HTTP-only cookie (backend sets)
2. Browser automatically sends cookie with requests
3. Backend verifies session exists in database
4. Backend checks session expiration
5. Backend gets user associated with session
6. Session can be invalidated by deleting database record
7. No token signature verification needed
8. More secure: stolen token doesn't work without session record
```

---

## 📂 FILE PURPOSE REFERENCE

### By Functionality

#### Authentication Files
- `backend/services/registration_service.py` - User registration
- `backend/services/login_service.py` - User login
- `backend/services/logout_service.py` - User logout
- `backend/services/session_service.py` - Session management
- `backend/api/auth_router.py` - Auth endpoints
- `frontend/src/lib/auth.ts` - Server auth utilities
- `frontend/src/lib/authClient.ts` - Client auth
- `frontend/src/components/LoginFormClient.tsx` - Login UI
- `frontend/src/components/SignupFormClient.tsx` - Signup UI

#### Task Management Files
- `backend/models/task.py` - Task database model
- `backend/services/task_service.py` - Task operations
- `backend/api/task_router.py` - Task endpoints
- `backend/schemas/task.py` - Task validation
- `frontend/src/components/TaskList.tsx` - Task display
- `frontend/src/components/TaskForm.tsx` - Task creation
- `frontend/src/components/TaskEditModal.tsx` - Task editing
- `frontend/src/services/api.ts` - Task API calls

#### Dashboard Files
- `backend/api/dashboard_router.py` - Dashboard endpoints
- `backend/services/task_service.py` - Stats calculation
- `frontend/src/components/DashboardPageClient.tsx` - Dashboard UI
- `frontend/src/components/DashboardStats.tsx` - Stats display

#### Database Files
- `backend/database/connection.py` - DB connection
- `backend/database/session.py` - Session management
- `backend/database/migrations.py` - Schema creation
- `backend/config.py` - DB configuration

#### Error Handling Files
- `backend/exceptions/handlers.py` - Exception handlers
- `backend/exceptions/chat_exceptions.py` - Chat exceptions

#### Security Files
- `backend/middleware/auth.py` - Auth middleware
- `backend/middleware/better_auth.py` - Better Auth implementation
- `backend/middleware/rate_limiter.py` - Rate limiting
- `backend/dependencies/auth.py` - Auth dependencies

#### Chat/Real-time Files
- `backend/api/chat_router.py` - Chat endpoints
- `backend/agents/chat_agent.py` - AI agent logic
- `backend/mcp/server.py` - MCP server
- `frontend/src/components/chatbot-ui/ChatBot.tsx` - Chat UI

---

## 🔄 DATA FLOW DIAGRAMS

### Request/Response Flow

```
Frontend (Next.js) 
    ↓ (HTTP/HTTPS)
Browser (stores JWT in localStorage, cookie in storage)
    ↓ (Includes Authorization header + cookies)
FastAPI Backend
    ↓ (Validates JWT, checks session in DB)
Middleware (auth validation)
    ↓ (Extracts user_id from session)
API Router (task_router, auth_router, etc.)
    ↓ (Delegates to service layer)
Services (task_service, user_service, etc.)
    ↓ (Queries/updates database)
Database (PostgreSQL on Neon)
    ↓ (Returns data)
Services (formats response)
    ↓ (Returns response)
API Router (wraps in response)
    ↓ (HTTP response)
Frontend (updates state)
    ↓ (Re-renders UI)
User (sees updated task list/dashboard)
```

### Task Creation Flow

```
User fills task form → Click "Add Task"
    ↓
frontend/src/components/TaskForm.tsx
    ↓ (Collects: title, description, priority, category, due_date)
frontend/src/services/api.ts → taskAPI.createTask()
    ↓ (POST /api/tasks with task data)
backend/api/task_router.py → create_task_endpoint()
    ↓ (Extract user_id from current_user dependency)
backend/services/task_service.py → create_task()
    ↓ (Validate input, create Task model)
backend/database/connection.py (save to database)
    ↓ (INSERT into task table)
PostgreSQL (persists task)
    ↓ (Returns created task)
backend (returns task in response)
    ↓ (HTTP 201 Created)
frontend (adds task to state)
    ↓ (UI updates, shows new task in list)
User (sees new task)
```

### Authentication Flow

```
User submits login form (email + password)
    ↓
frontend/src/components/LoginFormClient.tsx
    ↓ (Calls authAPI.login())
frontend/src/services/api.ts
    ↓ (POST /api/auth/login)
backend/api/auth_router.py → login endpoint
    ↓ (Validates credentials)
backend/services/login_service.py
    ↓ (authenticate_user from user_service)
Database lookup for user by email
    ↓ (Hash comparison with bcrypt)
backend/services/login_service.py
    ↓ (Create session in database)
Database (INSERT into session table)
    ↓ (Generate JWT tokens)
backend (Return user + tokens)
    ↓ (Set HTTP-only cookie with session token)
frontend (Store JWT in localStorage)
    ↓ (Redirect to dashboard)
User (Sees dashboard)
```

---

## 🧪 TEST COVERAGE

### Backend Tests
- ✅ Authentication (signup, login, logout, session)
- ✅ Task CRUD operations
- ✅ User authorization (users only see their tasks)
- ✅ Dashboard statistics
- ✅ Account deletion cascade
- ✅ Database connectivity
- ✅ Input validation and sanitization

### Frontend Tests
- Component unit tests
- Integration tests
- API mocking
- User interaction testing

---

## 🚀 DEPLOYMENT STRUCTURE

### Docker Setup
```dockerfile
# backend/Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup
**Development (.env):**
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/todoapp
SECRET_KEY=dev-secret-key
DEBUG=True
```

**Production (.env.production):**
```
DATABASE_URL=postgresql+asyncpg://user:pass@neon.tech/prod_db
SECRET_KEY=<production-secret>
DEBUG=False
BETTER_AUTH_SECRET=<auth-secret>
```

---

## 📊 PROJECT STATISTICS

| Metric | Count |
|--------|-------|
| Backend Python files | ~50+ |
| Frontend TypeScript components | ~18+ |
| API endpoints | ~25+ |
| Database models | 7 |
| Services | 6 |
| Middleware | 3 |
| Tests | 9+ |
| Lines of backend code | 5000+ |
| Lines of frontend code | 3000+ |

---

## 🔍 KEY FILES TO MODIFY

### To Add New Feature
1. **Database**: `backend/models/` → Add new model
2. **Validation**: `backend/schemas/` → Add request schema
3. **Business Logic**: `backend/services/` → Add service function
4. **API**: `backend/api/` → Add endpoint
5. **UI**: `frontend/src/components/` → Add component
6. **API Client**: `frontend/src/services/api.ts` → Add API function

### To Fix Authentication Issues
1. Check: `backend/middleware/better_auth.py`
2. Check: `backend/services/login_service.py`
3. Check: `backend/dependencies/auth.py`
4. Check: `frontend/src/lib/authClient.ts`

### To Debug API Issues
1. Check: `backend/main.py` (app setup)
2. Check: `backend/config.py` (configuration)
3. Check: `backend/database/connection.py` (DB connection)
4. Check relevant router: `backend/api/`
5. Check service layer: `backend/services/`

---

**Documentation Generated:** January 16, 2026
**Version:** 1.0
**Status:** Production Ready

