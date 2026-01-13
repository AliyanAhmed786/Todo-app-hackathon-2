# Backend Details - Todo App

## Overview
The Todo App backend is a comprehensive REST API built with FastAPI and SQLModel, featuring authentication with Better Auth database session validation, task management, and real-time updates via WebSockets. The system follows modern security practices with HTTP-only cookies for session management and input sanitization.

## Architecture

### Tech Stack
- **Framework**: FastAPI (v0.115.0)
- **Database ORM**: SQLModel with async support
- **Database**: PostgreSQL with asyncpg driver
- **Authentication**: Custom Better Auth implementation with database session validation
- **Real-time Updates**: Socket.IO for WebSocket connections
- **Rate Limiting**: slowapi for request throttling
- **Password Hashing**: passlib with bcrypt

### Core Components

#### 1. Main Application (`main.py`)
- FastAPI application with lifespan events for startup/shutdown
- CORS middleware configured for development origins
- Logging setup with rotating file handler
- Health check endpoint with database connectivity verification
- Routes mounted for tasks, auth, and dashboard APIs

#### 2. Configuration (`config.py`)
- Environment-based settings using Pydantic Settings
- Database URL, JWT configuration, and rate limiting parameters
- Secret key management with production safety checks
- Better Auth secret handling

#### 3. Database Layer (`database/`)
- **Connection**: Async database engine with optimized settings for Neon PostgreSQL
- **Models**: SQLModel-based entities with relationships
- **Sessions**: Async context managers for transaction handling
- **Migrations**: Schema creation and update utilities

#### 4. Data Models (`models/`)
- **User**: User accounts with Better Auth-compatible string IDs
- **Task**: Todo items with priority, status, category, and timestamps
- **Session**: Database session records for Better Auth validation
- **Account**: Third-party authentication providers
- **Verification**: Email/phone verification tokens

#### 5. API Routers (`api/`)
- **Task Router**: Full CRUD operations for tasks with user isolation
- **Auth Router**: Registration, login, logout, and session management
- **Dashboard Router**: Statistics and analytics endpoints

#### 6. Services (`services/`)
- **Task Service**: Business logic for task operations with user validation
- **User Service**: User account management
- **Login Service**: Authentication logic
- **Session Service**: Database session validation
- **Registration Service**: User creation with validation

#### 7. Middleware (`middleware/`)
- **Auth Middleware**: Current user extraction from database sessions
- **Better Auth**: Database session validation implementation
- **Rate Limiter**: Request throttling per authenticated user

#### 8. Security Features
- **Input Sanitization**: XSS and SQL injection prevention
- **HTTP-only Cookies**: Secure session management
- **JWT Tokens**: Signed with shared secrets
- **User Isolation**: All queries filtered by authenticated user ID
- **Password Hashing**: bcrypt with salt

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration with database session
- `POST /api/auth/login` - User authentication
- `POST /api/auth/logout` - Session termination
- `GET /api/auth/session` - Current session validation
- `POST /api/auth/refresh` - Session renewal

### Tasks
- `GET /api/tasks` - Retrieve user's tasks with pagination
- `POST /api/tasks` - Create new task for user
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/complete` - Mark task as complete
- `DELETE /api/tasks/{id}` - Delete task

### Dashboard
- `GET /api/dashboard/stats` - User statistics
- `GET /api/dashboard/overview` - Comprehensive overview

### Health
- `GET /health` - System health check with database connectivity

## Database Schema

### Task Model
- `id`: Primary key (int, auto-increment)
- `title`: Required string (1-200 chars)
- `description`: Optional string (0-1000 chars)
- `status`: Boolean (default: false)
- `category`: Optional string (0-100 chars)
- `priority`: Integer enum (1=Low, 2=Medium, 3=High)
- `created_at`: Timestamp (auto-generated)
- `updated_at`: Timestamp (auto-updated)
- `user_id`: Foreign key to User

### User Model
- `id`: Primary key (string, UUID-based)
- `name`: String (max 100 chars)
- `email`: Unique string (max 200 chars)
- `password_hash`: Hashed password
- `email_verified`: Boolean (default: false)
- `image`: Optional string (max 500 chars)
- `created_at`: Timestamp (auto-generated)
- `updated_at`: Timestamp (auto-updated)

### Session Model
- `id`: Primary key (string, hex)
- `token`: Unique session token
- `user_id`: Foreign key to User
- `expires_at`: Expiration timestamp
- `created_at`: Creation timestamp

## Security Measures

### Authentication Flow
1. User registers/logs in via auth endpoints
2. Session created in database with HTTP-only cookie
3. Subsequent requests validated against database sessions
4. No JWT token decoding - pure database validation

### Input Validation
- Sanitization of all user inputs
- Regex patterns to remove dangerous characters
- Character length limits
- Type validation using Pydantic models

### Rate Limiting
- 100 requests per minute per authenticated user
- 429 response for exceeding limits
- Configurable through environment variables

## Real-time Features

### WebSocket Integration
- Socket.IO server with CORS configuration
- User-isolated rooms based on authentication
- Dashboard updates broadcast to connected clients
- Task change notifications

## Error Handling

### Custom Exceptions
- `TaskNotFoundError`: When requested task doesn't exist
- `UserNotFoundError`: When requested user doesn't exist
- `UnauthorizedAccessError`: When user accesses unauthorized resources
- `ValidationError`: For input validation failures
- `DatabaseError`: For database-related issues

### Global Handlers
- HTTP exceptions with proper status codes
- Database integrity error handling
- General exception fallback with logging

## Deployment Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key
- `BETTER_AUTH_SECRET`: Shared secret for auth
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token lifetime
- `DEBUG`: Development mode flag

### Production Settings
- Secure cookie settings
- Enhanced logging
- Strict rate limiting
- Database connection pooling

## Testing

### Test Suite
- Comprehensive test coverage for auth flows
- Task CRUD operation tests
- Session management tests
- Dashboard functionality tests

### Test Files
- `test_main.py`: Basic API tests
- `test_better_auth_*.py`: Authentication-specific tests
- `test_comprehensive_better_auth.py`: End-to-end tests
- `test_dashboard.py`: Dashboard functionality tests

## Key Features

### Multi-user Support
- Complete user isolation
- Individual task ownership
- Personalized dashboards
- User-specific statistics

### Task Management
- Priority levels (Low, Medium, High)
- Status tracking (completed/pending)
- Categorization
- Rich descriptions

### Dashboard Analytics
- Total task count
- Completed vs pending breakdown
- Progress tracking
- Real-time updates

### Scalability Features
- Async database operations
- Connection pooling
- Rate limiting
- Efficient query patterns