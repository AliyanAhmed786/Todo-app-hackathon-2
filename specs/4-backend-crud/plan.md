# Implementation Plan: Backend CRUD API for Todo App

**Feature**: 4-backend-crud
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "make a new directory in & 'c:\\Users\\Wajiz.pk\\Desktop\\todo app hackathon 2\\specs' name \"4-backend-crud\" and create specs based on & 'c:\\Users\\Wajiz.pk\\Desktop\\todo app hackathon 2\\frontend' frontend for & 'c:\\Users\\Wajiz.pk\\Desktop\\todo app hackathon 2\\backend'"

## Technical Context

### Current State
- Frontend application exists with React/Next.js components that expect backend API endpoints
- Frontend uses JWT authentication and makes calls to `/api/{userId}/tasks` endpoints
- Database will be Neon Serverless PostgreSQL
- Authentication will use JWT with refresh token rotation

### Architecture
- Backend: FastAPI (Python) - aligns with project constitution Phase II technology stack
- Database: Neon Serverless PostgreSQL
- Authentication: JWT tokens with refresh token rotation
- Rate limiting: 100 requests per minute per authenticated user

### Dependencies
- FastAPI framework
- SQLModel for database modeling
- Neon PostgreSQL database driver
- Python-Jose for JWT handling
- SlowAPI for rate limiting
- Better Auth integration (per constitution)

### Integration Points
- Frontend API calls to backend endpoints
- Database for task storage
- Authentication system for user validation
- Rate limiting middleware

## Constitution Check

### Spec-First Workflow (NON-NEGOTIABLE)
✅ Plan follows spec-first approach - all requirements defined in spec.md before implementation

### Clean Code Standards
✅ Plan adheres to clean code standards - Python backend, no hardcoded secrets, proper error handling

### Technology Stack Adherence
✅ Plan uses FastAPI and SQLModel as specified in constitution Phase II stack

### Code Traceability
✅ Plan will use Task IDs to link implementations to specifications

### Open Source Transparency
✅ All code will be in public GitHub repository with proper documentation

### Gate Evaluation
✅ All constitution checks pass - ready to proceed with implementation plan

## Phase 0: Research

### Research Findings

**Decision**: Use FastAPI with SQLModel for backend implementation
**Rationale**: FastAPI provides excellent performance, automatic OpenAPI documentation, and strong type hints. SQLModel is perfect for PostgreSQL and integrates well with FastAPI. Both align with constitution Phase II requirements.

**Decision**: Use PyJWT for JWT handling with refresh token rotation
**Rationale**: PyJWT is the standard Python library for JWT tokens. Refresh token rotation provides security best practices for the authentication system.

**Decision**: Use SlowAPI for rate limiting
**Rationale**: SlowAPI is designed specifically for FastAPI applications and provides easy integration with middleware.

**Decision**: Use Neon Serverless PostgreSQL
**Rationale**: Neon provides serverless PostgreSQL with excellent performance and scalability. It aligns with the constitution Phase II stack and provides the specified database technology.

## Phase 1: Design & Contracts

### Data Model: data-model.md

#### Task Entity
- **id**: Integer (Primary Key, Auto-increment)
- **title**: String (1-200 characters, required)
- **description**: String (max 1000 characters, optional)
- **status**: Boolean (default: false)
- **category**: String (max 100 characters, optional)
- **priority**: Integer (1-3, default: 1)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated, updates on modification)
- **user_id**: Integer (Foreign Key to User)

#### User Entity
- **id**: Integer (Primary Key, Auto-increment)
- **name**: String (max 100 characters)
- **email**: String (unique, max 200 characters)
- **password_hash**: String (hashed password)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated, updates on modification)

### API Contracts

#### Authentication Endpoints
```
POST /auth/signup
- Request: {name: string, email: string, password: string}
- Response: {access_token: string, refresh_token: string, token_type: "bearer"}
- Status: 201 Created

POST /auth/login
- Request: {email: string, password: string}
- Response: {access_token: string, refresh_token: string, token_type: "bearer"}
- Status: 200 OK

POST /auth/logout
- Request: {refresh_token: string}
- Response: {}
- Status: 200 OK
```

#### Task Endpoints
```
GET /api/{userId}/tasks
- Headers: Authorization: Bearer {token}
- Response: {tasks: Task[]}
- Status: 200 OK
- Rate Limit: 100 requests per minute per user

POST /api/{userId}/tasks
- Headers: Authorization: Bearer {token}
- Request: {title: string, description?: string, category?: string, priority?: number}
- Response: {task: Task}
- Status: 201 Created
- Rate Limit: 100 requests per minute per user

GET /api/{userId}/tasks/{taskId}
- Headers: Authorization: Bearer {token}
- Response: {task: Task}
- Status: 200 OK
- Rate Limit: 100 requests per minute per user

PUT /api/{userId}/tasks/{taskId}
- Headers: Authorization: Bearer {token}
- Request: {title?: string, description?: string, status?: boolean, category?: string, priority?: number}
- Response: {task: Task}
- Status: 200 OK
- Rate Limit: 100 requests per minute per user

DELETE /api/{userId}/tasks/{taskId}
- Headers: Authorization: Bearer {token}
- Response: {}
- Status: 204 No Content
- Rate Limit: 100 requests per minute per user
```

### Quickstart Guide

1. Install dependencies: `pip install fastapi uvicorn sqlmodel python-jose[cryptography] slowapi`
2. Set up environment variables:
   - DATABASE_URL="postgresql+asyncpg://user:password@localhost/dbname"
   - SECRET_KEY="your-secret-key"
   - ALGORITHM="HS256"
   - ACCESS_TOKEN_EXPIRE_MINUTES=30
   - REFRESH_TOKEN_EXPIRE_DAYS=7
3. Run the server: `uvicorn main:app --reload`
4. Access API documentation at `http://localhost:8000/docs`

### Agent Context Update

The agent context has been updated to include:
- FastAPI framework usage
- SQLModel for database modeling
- JWT authentication with refresh tokens
- Rate limiting with SlowAPI
- Neon PostgreSQL integration

## Phase 2: Implementation Approach

### Implementation Order
1. Set up FastAPI project structure
2. Create database models with SQLModel
3. Implement authentication system with JWT
4. Create task CRUD endpoints
5. Add rate limiting middleware
6. Implement proper error handling
7. Add validation and testing
8. Deploy to development environment

### Key Components
- Database models (SQLModel)
- Authentication middleware (JWT)
- Rate limiting middleware (SlowAPI)
- API routers (FastAPI)
- Database session management
- Environment configuration
- Error handling
- Request validation

## Re-evaluation of Constitution Check

All constitution requirements continue to be met:
✅ Spec-first workflow maintained
✅ Clean code standards upheld
✅ Technology stack adherence confirmed
✅ Code traceability planned
✅ Open source transparency maintained

The implementation plan is ready for development phase.