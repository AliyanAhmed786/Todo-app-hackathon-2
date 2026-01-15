# Backend Architecture Overview

## Project Structure
```
backend/
├── __init__.py
├── __pycache__/                    # Python compiled bytecode cache
├── api/                           # API route definitions
│   ├── auth_router.py             # Authentication endpoints
│   ├── dashboard_router.py        # Dashboard-related endpoints
│   └── task_router.py             # Task management endpoints
├── auth/                          # Authentication setup
│   ├── __init__.py
│   └── auth_setup.py              # Better Auth initialization
├── config.py                      # Application configuration
├── database/                      # Database layer components
│   ├── __init__.py
│   ├── connection.py              # Database connection setup
│   ├── migrations.py              # Database schema migrations
│   ├── schema_updater.py          # Schema update utilities
│   ├── add_due_date_migration.py  # Specific migration for due dates
│   ├── complete_schema_migration.py # Complete schema migration
│   └── session.py                 # Database session management
├── dependencies/                  # FastAPI dependencies
│   ├── __init__.py
│   └── auth.py                    # Authentication dependencies
├── deploy.py                      # Deployment configuration
├── Dockerfile                     # Docker container definition
├── exceptions/                    # Exception handling
│   ├── __init__.py
│   └── handlers.py                # Global exception handlers
├── main.py                        # Main application entry point
├── middleware/                    # Request processing middleware
│   ├── __init__.py
│   ├── auth.py                    # Authentication middleware
│   ├── better_auth.py             # Better Auth integration middleware
│   └── rate_limiter.py            # Rate limiting middleware
├── models/                        # Database models
│   ├── __init__.py
│   ├── account.py                 # Account model
│   ├── session.py                 # Session model
│   ├── task.py                    # Task model
│   ├── user.py                    # User model
│   └── verification.py            # Verification model
├── production_config.py           # Production-specific configuration
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── reset_database.py              # Database reset utility
├── schemas/                       # Pydantic schemas for validation
│   ├── __init__.py
│   ├── auth.py                    # Authentication schemas
│   ├── task.py                    # Task schemas
│   └── user.py                    # User schemas
├── services/                      # Business logic services
│   ├── __init__.py
│   ├── login_service.py           # Login business logic
│   ├── logout_service.py          # Logout business logic
│   ├── registration_service.py    # Registration business logic
│   ├── session_service.py         # Session management logic
│   ├── task_service.py            # Task business logic
│   └── user_service.py            # User business logic
├── setup.py                       # Package setup configuration
├── test_*                         # Test files for various functionalities
├── todo_app.db                    # SQLite database file
└── utils/                         # Utility functions
    ├── __init__.py
    ├── auth.py                    # Authentication utilities
    ├── password.py                # Password utilities
    └── websocket_manager.py       # WebSocket connection management
```

## Core Components

### 1. main.py - Application Entry Point
- Main FastAPI application instance
- Sets up CORS middleware for frontend communication
- Includes all API routers (auth, tasks, dashboard)
- Configures logging and database initialization
- Provides health check endpoint
- Mounts Socket.IO for real-time features

### 2. Database Layer (database/)
- **connection.py**: SQLAlchemy async engine setup and database connection pooling
- **migrations.py**: Handles database schema creation and updates
- **session.py**: Context manager for database sessions
- **schema_updater.py**: Utilities for schema modifications
- **add_due_date_migration.py**: Specific migration to add due_date field to tasks
- **complete_schema_migration.py**: Complete schema migration script

### 3. API Routes (api/)
- **auth_router.py**: Handles user registration, login, logout, and session management
- **task_router.py**: CRUD operations for tasks (create, read, update, delete)
- **dashboard_router.py**: Dashboard-specific endpoints for statistics and user data

### 4. Models (models/)
- **user.py**: User entity with relationships to tasks and sessions
- **task.py**: Task entity with title, description, completion status, priority, due date
- **session.py**: Session management for authentication
- **account.py**: Account information linked to users
- **verification.py**: Email verification tokens

### 5. Schemas (schemas/)
- **user.py**: Pydantic models for user data validation (input/output)
- **task.py**: Pydantic models for task data validation
- **auth.py**: Authentication-related data models (login, register, session)

### 6. Services (services/)
- **user_service.py**: User-related business logic
- **task_service.py**: Task-related business logic (validation, processing)
- **login_service.py**: Login-specific business logic
- **logout_service.py**: Logout-specific business logic
- **registration_service.py**: Registration-specific business logic
- **session_service.py**: Session management business logic

### 7. Authentication (auth/, dependencies/, middleware/)
- **auth_setup.py**: Better Auth library initialization
- **auth.py (dependencies)**: Current user dependency for protected routes
- **auth.py (middleware)**: Authentication middleware
- **better_auth.py**: Better Auth integration middleware
- **auth.py (utils)**: Authentication utility functions

### 8. Middleware (middleware/)
- **rate_limiter.py**: API rate limiting to prevent abuse
- **auth.py**: Authentication middleware for request processing
- **better_auth.py**: Integration with Better Auth library

### 9. Utilities (utils/)
- **password.py**: Password hashing and verification utilities
- **auth.py**: Authentication helper functions
- **websocket_manager.py**: Socket.IO integration for real-time communication

### 10. Configuration Files
- **config.py**: Development configuration settings
- **production_config.py**: Production-specific settings
- **requirements.txt**: Python package dependencies
- **Dockerfile**: Containerization instructions

### 11. Testing Files
Multiple test files covering:
- Authentication flows (registration, login, logout, session persistence)
- Task CRUD operations
- Dashboard functionality
- Account deletion cascade
- Comprehensive Better Auth integration

## Technologies Used

### Framework & Libraries
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Better Auth**: Authentication library for user management
- **Pydantic**: Data validation and settings management
- **Socket.IO**: Real-time bidirectional event-based communication
- **Uvicorn**: ASGI server for running the application

### Database
- **SQLite**: Lightweight database for development/testing
- **Async SQLAlchemy**: Asynchronous database operations

### Authentication
- **Better Auth**: Provides user registration, login, session management, and security features

### Containerization
- **Docker**: Container platform for deployment consistency

## Key Features

### 1. Authentication System
- User registration with email verification
- Secure login/logout functionality
- Session management
- Protected API endpoints

### 2. Task Management
- Create, read, update, delete operations for tasks
- Task completion tracking
- Priority levels (High, Medium, Low)
- Due date functionality
- Search and filtering capabilities

### 3. Dashboard Analytics
- Task statistics (total, completed, pending)
- User activity tracking
- Performance metrics

### 4. Real-time Features
- WebSocket integration for live updates
- Real-time task synchronization

### 5. Security Features
- Rate limiting to prevent API abuse
- Input validation using Pydantic schemas
- Password hashing
- Session security

### 6. Database Migrations
- Automated schema updates
- Safe migration handling
- Data integrity preservation

## API Endpoints

### Authentication (`/api/auth/`)
- `POST /register` - User registration
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /session` - Get current session

### Tasks (`/api/tasks/`)
- `GET /` - Get all tasks for user
- `POST /` - Create new task
- `GET /{id}` - Get specific task
- `PUT /{id}` - Update specific task
- `DELETE /{id}` - Delete specific task

### Dashboard (`/api/`)
- `GET /dashboard/stats` - Get dashboard statistics

## Environment Setup

The backend can be run in multiple ways:
1. Direct Python execution: `python main.py`
2. With Uvicorn: `uvicorn main:app --reload`
3. Via Docker container using the provided Dockerfile

## Database Schema
The application uses a relational database with the following main entities:
- Users: Core user accounts
- Tasks: Individual todo items linked to users
- Sessions: Active user sessions
- Accounts: Extended account information
- Verification: Email verification tokens

## Security Considerations
- Passwords are hashed using industry-standard algorithms
- Sessions are managed securely with expiration
- Rate limiting prevents API abuse
- Input validation prevents injection attacks
- CORS configured for secure frontend communication