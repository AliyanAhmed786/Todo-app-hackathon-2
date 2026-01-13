# Data Model: Backend CRUD API for Todo App

## Entity: Task
- **id**: Integer (Primary Key, Auto-increment)
- **title**: String (1-200 characters, required)
- **description**: String (max 1000 characters, optional)
- **status**: Boolean (default: false)
- **category**: String (max 100 characters, optional)
- **priority**: Integer (1-3, default: 1)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated, updates on modification)
- **user_id**: Integer (Foreign Key to User)

## Entity: User
- **id**: Integer (Primary Key, Auto-increment)
- **name**: String (max 100 characters)
- **email**: String (unique, max 200 characters)
- **password_hash**: String (hashed password)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated, updates on modification)

## Relationships
- User (1) -> Task (Many): A user can have many tasks
- Task (Many) -> User (1): Each task belongs to one user

## Validation Rules
- Task title: 1-200 characters
- Task description: 0-1000 characters
- Task category: 0-100 characters
- Task priority: 1 (Low), 2 (Medium), 3 (High)
- Task status: Boolean (false = pending, true = completed)
- User email: Must be unique and valid email format
- User name: Max 100 characters

## State Transitions
- Task status: Can transition from false (pending) to true (completed) and back
- User account: Active by default, can be deactivated (future enhancement)

## Indexes
- Task.user_id: Foreign key index for performance
- User.email: Unique index for login performance
- Task.created_at: Index for chronological sorting