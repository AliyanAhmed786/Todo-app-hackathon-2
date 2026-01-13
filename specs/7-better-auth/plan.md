# Implementation Plan: Better Auth Integration for Todo App

**Feature**: 7-better-auth
**Created**: 2026-01-08
**Status**: Draft
**Input**: User description: "i want you create specs for better auth based on the report in specs folder "7-betterauth" and this spec.md is based to proper implement the betterauth in the project and work fully depend on the project"

## Technical Context

### Current State
- Frontend application exists with React/Next.js components that currently use a custom JWT authentication system
- Backend has custom authentication implementation instead of Better Auth
- Database is configured with Neon PostgreSQL
- Current auth system stores user data in local database tables
- Better Auth client library is installed in frontend (better-auth@0.0.1)
- Custom JWT middleware exists in backend using python-jose
- No Better Auth server components are installed in backend

### Architecture
- Frontend: Next.js with Better Auth client integration
- Backend: FastAPI with Better Auth server integration
- Database: Neon Serverless PostgreSQL (for user data if needed)
- Authentication: Better Auth managed authentication service with shared database session validation

### Dependencies
- better-auth package for Next.js integration
- Official Better Auth server library
- Neon PostgreSQL database
- Next.js 16+ for frontend
- FastAPI for backend integration
- SQLModel for database modeling

### Integration Points
- Frontend API calls to Better Auth endpoints
- Backend integration with Better Auth server
- Database for user sessions and accounts with shared validation
- Existing task management API endpoints that need authentication updates

## Constitution Check

### Spec-First Workflow (NON-NEGOTIABLE)
✅ Plan follows spec-first approach - all requirements defined in spec.md before implementation

### Clean Code Standards
✅ Plan adheres to clean code standards - proper separation of concerns between auth and business logic

### Technology Stack Adherence
✅ Plan uses Better Auth as specified in constitution Phase II stack (Section 47)

### Code Traceability
✅ Plan will use Task IDs to link implementations to specifications

### Open Source Transparency
✅ All code will be in public GitHub repository with proper documentation

### Gate Evaluation
✅ All constitution checks pass - ready to proceed with implementation plan

## Phase 0: Research

### Research Findings

**Decision**: Use Better Auth library for authentication with database session validation
**Rationale**: Better Auth provides enterprise-grade authentication with email/password, social logins, and session management. It aligns with the project constitution requirement and provides security best practices out-of-the-box. The shared database validation approach ensures consistency between frontend and backend authentication.

**Decision**: Integrate Better Auth with existing task management system using database cascade deletion
**Rationale**: Better Auth can be integrated with existing database and API structures while providing enhanced authentication capabilities. The cascade deletion approach ensures data integrity when accounts are removed.

**Decision**: Store session tokens in HTTP-only cookies for security
**Rationale**: HTTP-only cookies provide better security than localStorage for session tokens, preventing XSS attacks from accessing authentication tokens.

## Phase 1: Design & Contracts

### Data Model: data-model.md

#### User Entity (Managed by Better Auth)
- Better Auth manages core user authentication data
- User ID, email, password hash, verification status
- Social provider data if social login is enabled later

#### Session Entity (Managed by Better Auth in Neon DB)
- **id**: String (Primary Key, Unique session identifier)
- **token**: String (Session token value)
- **user_id**: String (Reference to Better Auth user ID)
- **expires_at**: DateTime (Expiration timestamp)
- **created_at**: DateTime (Creation timestamp)
- **updated_at**: DateTime (Last updated timestamp)

#### Account Entity (Managed by Better Auth in Neon DB)
- **id**: String (Primary Key, Unique account identifier)
- **user_id**: String (Reference to Better Auth user ID)
- **provider_id**: String (Provider identifier, e.g., "email", "google")
- **provider_account_id**: String (Account identifier from provider)
- **created_at**: DateTime (Creation timestamp)
- **updated_at**: DateTime (Last updated timestamp)

#### Task Entity (Existing - Updated for Better Auth)
- **id**: Integer (Primary Key, Auto-increment)
- **title**: String (1-200 characters, required)
- **description**: String (max 1000 characters, optional)
- **status**: Boolean (default: false)
- **category**: String (max 100 characters, optional)
- **priority**: Integer (1-3, default: 1)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated, updates on modification)
- **user_id**: String (Better Auth user ID with CASCADE DELETE)

### API Contracts

#### Better Auth Endpoints (to be implemented)
```
POST /api/auth/register
- Request: {email: string, password: string, name?: string}
- Response: {user: User, session: Session}
- Status: 201 Created

POST /api/auth/login
- Request: {email: string, password: string}
- Response: {user: User, session: Session}
- Status: 200 OK

GET /api/auth/session
- Headers: Cookie: better-auth.session_token=xxx (HTTP-only cookie)
- Response: {user: User, session?: Session}
- Status: 200 OK

POST /api/auth/logout
- Headers: Cookie: better-auth.session_token=xxx (HTTP-only cookie)
- Response: {}
- Status: 200 OK

POST /api/auth/forgot-password
- Request: {email: string}
- Response: {}
- Status: 200 OK

POST /api/auth/reset-password
- Request: {token: string, newPassword: string}
- Response: {user: User}
- Status: 200 OK
```

#### Updated Task Endpoints (using Better Auth with database session validation)
```
GET /api/tasks
- Headers: Cookie: better-auth.session_token=xxx (HTTP-only cookie)
- Response: {tasks: Task[]}
- Status: 200 OK

POST /api/tasks
- Headers: Cookie: better-auth.session_token=xxx (HTTP-only cookie)
- Request: {title: string, description?: string, category?: string, priority?: number}
- Response: {task: Task}
- Status: 201 Created

GET /api/tasks/{taskId}
- Headers: Cookie: better-auth.session_token=xxx (HTTP-only cookie)
- Response: {task: Task}
- Status: 200 OK

PUT /api/tasks/{taskId}
- Headers: Cookie: better-auth.session_token=xxx (HTTP-only cookie)
- Request: {title?: string, description?: string, status?: boolean, category?: string, priority?: number}
- Response: {task: Task}
- Status: 200 OK

DELETE /api/tasks/{taskId}
- Headers: Cookie: better-auth.session_token=xxx (HTTP-only cookie)
- Response: {}
- Status: 204 No Content
```

### Quickstart Guide

1. Install Better Auth: `npm install better-auth`
2. Configure Better Auth server in backend with Neon DB integration
3. Set up Better Auth client in frontend
4. Update existing API endpoints to use Better Auth database session validation
5. Remove custom JWT logic and python-jose dependencies
6. Test authentication flow end-to-end

### Agent Context Update

The agent context has been updated to include:
- Better Auth server integration with database session validation
- Better Auth client implementation with HTTP-only cookies
- Session management with Better Auth database queries
- Updated API authentication using Better Auth database validation
- Removal of custom JWT authentication system
- Migration plan from custom auth to Better Auth

## Phase 2: Implementation Approach

### Implementation Order
1. Set up Better Auth server configuration with Neon DB
2. Implement Better Auth client in frontend with HTTP-only cookie support
3. Remove existing custom JWT authentication middleware
4. Update backend authentication to use database session validation
5. Modify existing API endpoints to use Better Auth authentication
6. Test authentication flows
7. Update documentation and deployment configs

### Key Components
- Better Auth server configuration with database adapter
- Better Auth client setup with HTTP-only cookie handling
- Authentication middleware using Better Auth database validation
- Updated API routers with Better Auth validation
- Session management with database queries
- Migration scripts for existing users (if needed)

## Re-evaluation of Constitution Check

All constitution requirements continue to be met:
✅ Spec-first workflow maintained
✅ Clean code standards upheld
✅ Technology stack adherence confirmed (Better Auth as required)
✅ Code traceability planned
✅ Open source transparency maintained

The implementation plan is ready for development phase.