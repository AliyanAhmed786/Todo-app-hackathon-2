# Better Auth API Contracts

## Authentication Endpoints

### POST /api/auth/register
Registers a new user account

Request Body:
```
{
  "email": "string (user email address)",
  "password": "string (user password)",
  "name": "string (optional user name)"
}
```

Response (201 Created):
```
{
  "user": {
    "id": "string (user ID)",
    "email": "string (user email)",
    "name": "string (user name)"
  },
  "session": {
    "user": {
      "id": "string (user ID)",
      "email": "string (user email)",
      "name": "string (user name)"
    },
    "token": "string (session token)"
  }
}
```

### POST /api/auth/login
Logs in an existing user

Request Body:
```
{
  "email": "string (user email address)",
  "password": "string (user password)"
}
```

Response (200 OK):
```
{
  "user": {
    "id": "string (user ID)",
    "email": "string (user email)",
    "name": "string (user name)"
  },
  "session": {
    "user": {
      "id": "string (user ID)",
      "email": "string (user email)",
      "name": "string (user name)"
    },
    "token": "string (session token)"
  }
}
```

### GET /api/auth/session
Retrieves current user session

Headers:
- Cookie: better-auth.session_token=xxx (HTTP-only cookie)

Response (200 OK):
```
{
  "user": {
    "id": "string (user ID)",
    "email": "string (user email)",
    "name": "string (user name)"
  },
  "session": {
    "user": {
      "id": "string (user ID)",
      "email": "string (user email)",
      "name": "string (user name)"
    },
    "token": "string (session token)"
  }
}
```

### POST /api/auth/logout
Logs out the current user

Headers:
- Cookie: better-auth.session_token=xxx (HTTP-only cookie)

Response (200 OK):
```
{}
```

## Task Management Endpoints (Protected)

### GET /api/tasks
Retrieves all tasks for the authenticated user

Headers:
- Cookie: better-auth.session_token=xxx (HTTP-only cookie)

Response (200 OK):
```
{
  "tasks": [
    {
      "id": "integer (task ID)",
      "title": "string (task title)",
      "description": "string (task description)",
      "status": "boolean (task completion status)",
      "category": "string (task category)",
      "priority": "integer (task priority 1-3)",
      "created_at": "datetime (task creation time)",
      "updated_at": "datetime (task last update time)",
      "user_id": "string (user ID)"
    }
  ]
}
```

### POST /api/tasks
Creates a new task for the authenticated user

Headers:
- Cookie: better-auth.session_token=xxx (HTTP-only cookie)

Request Body:
```
{
  "title": "string (task title, 1-200 chars)",
  "description": "string (optional task description, max 1000 chars)",
  "category": "string (optional task category, max 100 chars)",
  "priority": "integer (optional task priority 1-3, default 1)"
}
```

Response (201 Created):
```
{
  "task": {
    "id": "integer (task ID)",
    "title": "string (task title)",
    "description": "string (task description)",
    "status": "boolean (task completion status)",
    "category": "string (task category)",
    "priority": "integer (task priority 1-3)",
    "created_at": "datetime (task creation time)",
    "updated_at": "datetime (task last update time)",
    "user_id": "string (user ID)"
  }
}
```

### GET /api/tasks/{taskId}
Retrieves a specific task for the authenticated user

Path Parameters:
- taskId: integer (ID of the task to retrieve)

Headers:
- Cookie: better-auth.session_token=xxx (HTTP-only cookie)

Response (200 OK):
```
{
  "task": {
    "id": "integer (task ID)",
    "title": "string (task title)",
    "description": "string (task description)",
    "status": "boolean (task completion status)",
    "category": "string (task category)",
    "priority": "integer (task priority 1-3)",
    "created_at": "datetime (task creation time)",
    "updated_at": "datetime (task last update time)",
    "user_id": "string (user ID)"
  }
}
```

### PUT /api/tasks/{taskId}
Updates a specific task for the authenticated user

Path Parameters:
- taskId: integer (ID of the task to update)

Headers:
- Cookie: better-auth.session_token=xxx (HTTP-only cookie)

Request Body:
```
{
  "title": "string (optional task title, 1-200 chars)",
  "description": "string (optional task description, max 1000 chars)",
  "status": "boolean (optional task completion status)",
  "category": "string (optional task category, max 100 chars)",
  "priority": "integer (optional task priority 1-3)"
}
```

Response (200 OK):
```
{
  "task": {
    "id": "integer (task ID)",
    "title": "string (task title)",
    "description": "string (task description)",
    "status": "boolean (task completion status)",
    "category": "string (task category)",
    "priority": "integer (task priority 1-3)",
    "created_at": "datetime (task creation time)",
    "updated_at": "datetime (task last update time)",
    "user_id": "string (user ID)"
  }
}
```

### DELETE /api/tasks/{taskId}
Deletes a specific task for the authenticated user

Path Parameters:
- taskId: integer (ID of the task to delete)

Headers:
- Cookie: better-auth.session_token=xxx (HTTP-only cookie)

Response (204 No Content):
```
{}
```