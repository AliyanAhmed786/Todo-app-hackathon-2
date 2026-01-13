# Data Model: Multi-User Web Todo Application (Phase II)

**Feature**: 2-multi-user-todo-web-app
**Date**: 2025-12-23
**Modeler**: Claude Code Agent

## Entity: User

### Fields
- `id` (UUID, Primary Key)
  - Type: UUID string
  - Constraints: Unique, Required
  - Description: Unique identifier for each user

- `email` (String)
  - Type: String
  - Constraints: Unique, Required, Valid email format
  - Length: Max 255 characters
  - Description: User's email address for authentication

- `password_hash` (String)
  - Type: String (hashed)
  - Constraints: Required
  - Length: Variable (depends on hashing algorithm)
  - Description: Hashed password using secure algorithm

- `created_at` (Timestamp)
  - Type: DateTime (ISO 8601)
  - Constraints: Required, Auto-generated
  - Description: Timestamp when user account was created

- `updated_at` (Timestamp)
  - Type: DateTime (ISO 8601)
  - Constraints: Required, Auto-updated
  - Description: Timestamp when user record was last updated

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- Password must meet complexity requirements (min 8 chars, mixed case, number, special char)

### Relationships
- One-to-Many: User → Tasks (user has many tasks)

## Entity: Task

### Fields
- `id` (Integer, Primary Key)
  - Type: Integer (Auto-increment)
  - Constraints: Unique, Required, Auto-generated
  - Description: Unique identifier for each task (never recycled)

- `user_id` (UUID, Foreign Key)
  - Type: UUID string
  - Constraints: Required, References User.id
  - Description: Owner of the task

- `title` (String)
  - Type: String
  - Constraints: Required, No whitespace-only
  - Length: 1-200 characters
  - Description: Title of the task

- `description` (String)
  - Type: String
  - Constraints: Optional
  - Length: 0-1000 characters
  - Description: Optional detailed description of the task

- `status` (Boolean)
  - Type: Boolean
  - Constraints: Required
  - Values: false=incomplete, true=complete
  - Description: Completion status of the task

- `created_at` (Timestamp)
  - Type: DateTime (ISO 8601)
  - Constraints: Required, Auto-generated
  - Description: Timestamp when task was created

- `updated_at` (Timestamp)
  - Type: DateTime (ISO 8601)
  - Constraints: Required, Auto-updated
  - Description: Timestamp when task was last updated

### Validation Rules
- Title must be 1-200 characters
- Title cannot be whitespace-only
- Description must be 0-1000 characters
- Status must be boolean (true/false)
- user_id must reference an existing User

### Relationships
- Many-to-One: Task → User (task belongs to one user)

## Database Schema

### User Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Task Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    status BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes
```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_users_email ON users(email);
```

## State Transitions

### Task Status
- Initial State: `status = false` (incomplete)
- Transition 1: `false` → `true` (mark as complete)
- Transition 2: `true` → `false` (mark as incomplete)

## Constraints

1. **Referential Integrity**: Task.user_id must reference an existing User.id
2. **User Isolation**: Users can only access tasks with matching user_id
3. **Unique Email**: No two users can have the same email address
4. **Task ID Recycling**: Task IDs are auto-incrementing and never recycled
5. **Character Limits**: All text fields have defined character limits as specified