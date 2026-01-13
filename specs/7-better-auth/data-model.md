# Data Model: Better Auth Integration for Todo App

**Feature**: 7-better-auth
**Created**: 2026-01-08

## Better Auth Database Schema

### Session Table
- **id** (String, Primary Key): Unique session identifier
- **token** (String): Session token value
- **user_id** (String): Reference to user ID in users table
- **expires_at** (DateTime): Timestamp when session expires
- **created_at** (DateTime): Timestamp when session was created
- **updated_at** (DateTime): Timestamp when session was last updated

### Account Table
- **id** (String, Primary Key): Unique account identifier
- **user_id** (String): Reference to user ID in users table
- **provider_id** (String): Provider identifier (e.g., "email", "google")
- **provider_account_id** (String): Account identifier from the provider
- **created_at** (DateTime): Timestamp when account was created
- **updated_at** (DateTime): Timestamp when account was last updated

### User Table
- **id** (String, Primary Key): Unique user identifier
- **email** (String, Unique): User's email address
- **email_verified** (Boolean): Whether email has been verified
- **name** (String): User's display name
- **image** (String): URL to user's profile image
- **created_at** (DateTime): Timestamp when user was created
- **updated_at** (DateTime): Timestamp when user was last updated

### Verification Table
- **id** (String, Primary Key): Unique verification identifier
- **identifier** (String): Identifier for verification (email, phone, etc.)
- **value** (String): Verification value
- **expires_at** (DateTime): Timestamp when verification expires
- **created_at** (DateTime): Timestamp when verification was created

## Application Database Schema

### Task Table
- **id** (Integer, Primary Key): Unique task identifier
- **title** (String): Task title (1-200 characters)
- **description** (String): Task description (max 1000 characters)
- **status** (Boolean): Whether task is completed (default: false)
- **category** (String): Task category (max 100 characters)
- **priority** (Integer): Task priority (1-3, default: 1)
- **created_at** (DateTime): Timestamp when task was created
- **updated_at** (DateTime): Timestamp when task was last updated
- **user_id** (String): Reference to user who owns the task (CASCADE DELETE)

## Relationships

### User and Task
- One-to-Many relationship between User and Task
- Task.user_id references User.id
- CASCADE DELETE ensures tasks are removed when user is deleted

### User and Session
- One-to-Many relationship between User and Session
- Session.user_id references User.id
- Sessions are automatically invalidated when user is deleted

### User and Account
- One-to-Many relationship between User and Account
- Account.user_id references User.id
- Multiple accounts per user for different providers