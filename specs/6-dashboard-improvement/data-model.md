# Data Model: Dashboard Improvement

**Feature**: 6-dashboard-improvement | **Date**: 2026-01-03

## Entities

### Dashboard Statistics
- **Entity**: DashboardStatistics
- **Fields**:
  - id: string (unique identifier for the statistics record)
  - userId: integer (foreign key to User)
  - totalTasks: integer (count of all tasks for the user)
  - completedTasks: integer (count of completed tasks)
  - pendingTasks: integer (count of pending tasks)
  - createdAt: datetime (timestamp when statistics were calculated)
  - updatedAt: datetime (timestamp when statistics were last updated)
- **Relationships**:
  - Belongs to: User (one-to-one relationship)
- **Validation rules**:
  - totalTasks >= 0
  - completedTasks >= 0
  - pendingTasks >= 0
  - totalTasks = completedTasks + pendingTasks
- **State transitions**: Statistics are recalculated when tasks are created, updated, or deleted

### Task (Enhanced)
- **Entity**: Task
- **Fields**:
  - id: integer (primary key)
  - title: string (min 1, max 200 characters)
  - description: string (optional, max 1000 characters)
  - status: boolean (true for completed, false for pending)
  - category: string (optional, max 100 characters)
  - priority: integer (1 for Low, 2 for Medium, 3 for High)
  - created_at: datetime (timestamp when task was created)
  - updated_at: datetime (timestamp when task was last updated)
  - user_id: integer (foreign key to User)
  - version: integer (for optimistic locking)
- **Relationships**:
  - Belongs to: User (many-to-one relationship)
- **Validation rules**:
  - title length between 1-200 characters
  - description length max 1000 characters if provided
  - priority value in [1, 2, 3]
  - category length max 100 characters if provided
- **State transitions**: Status can transition between true (completed) and false (pending)

### User
- **Entity**: User
- **Fields**:
  - id: integer (primary key)
  - name: string (user's display name)
  - email: string (unique, valid email format)
  - hashed_password: string (password hash)
  - created_at: datetime
  - updated_at: datetime
- **Relationships**:
  - Has many: Tasks (one-to-many relationship)
- **Validation rules**:
  - email format validation
  - unique email constraint
- **State transitions**: N/A

### WebSocket Message
- **Entity**: WebSocketMessage (transient, for real-time communication)
- **Fields**:
  - type: string (message type: 'dashboard_update', 'task_update', etc.)
  - payload: object (data payload specific to message type)
  - timestamp: datetime (when message was sent)
  - userId: integer (user ID for targeted messages)
- **Validation rules**:
  - type must be one of predefined message types
  - payload structure depends on message type
- **State transitions**: Messages are ephemeral, sent and received in real-time

## Database Schema

### Tables

#### users
- id: INTEGER PRIMARY KEY
- name: VARCHAR(255) NOT NULL
- email: VARCHAR(255) UNIQUE NOT NULL
- hashed_password: VARCHAR(255) NOT NULL
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

#### tasks
- id: INTEGER PRIMARY KEY
- title: VARCHAR(200) NOT NULL
- description: TEXT
- status: BOOLEAN DEFAULT FALSE
- category: VARCHAR(100)
- priority: INTEGER CHECK (priority IN [1, 2, 3]) DEFAULT 2
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- user_id: INTEGER REFERENCES users(id)
- version: INTEGER DEFAULT 1

#### dashboard_statistics (view or calculated data)
- user_id: INTEGER REFERENCES users(id)
- total_tasks: INTEGER
- completed_tasks: INTEGER
- pending_tasks: INTEGER
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## API Data Structures

### Dashboard Statistics Response
```json
{
  "totalTasks": 15,
  "completedTasks": 8,
  "pendingTasks": 7,
  "updatedAt": "2026-01-03T10:30:00Z"
}
```

### Task Response
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "Task description",
  "status": false,
  "category": "Work",
  "priority": 2,
  "createdAt": "2026-01-03T10:00:00Z",
  "updatedAt": "2026-01-03T10:00:00Z",
  "userId": 1,
  "version": 1
}
```

### WebSocket Message Structure
```json
{
  "type": "dashboard_update",
  "payload": {
    "totalTasks": 15,
    "completedTasks": 8,
    "pendingTasks": 7
  },
  "timestamp": "2026-01-03T10:30:00Z"
}
```