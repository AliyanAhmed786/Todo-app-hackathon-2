# API Contracts: Dashboard Improvement

**Feature**: 6-dashboard-improvement | **Date**: 2026-01-03

## REST API Endpoints

### Dashboard Statistics Endpoints

#### GET /api/{userId}/dashboard/stats
- **Purpose**: Retrieve dashboard statistics for a specific user
- **Authentication**: JWT Bearer token required
- **Parameters**:
  - userId: Path parameter (integer) - ID of the user whose stats are requested
- **Request Headers**:
  - Authorization: Bearer {token}
- **Response**:
  - 200: OK - Dashboard statistics object
    ```json
    {
      "totalTasks": 15,
      "completedTasks": 8,
      "pendingTasks": 7,
      "updatedAt": "2026-01-03T10:30:00Z"
    }
    ```
  - 401: Unauthorized - Invalid or expired token
  - 403: Forbidden - User trying to access another user's data
  - 404: Not Found - User ID does not exist
  - 500: Internal Server Error - Server error

### Task Management Endpoints (Enhanced)

#### GET /api/{userId}/tasks
- **Purpose**: Retrieve all tasks for a specific user with dashboard statistics
- **Authentication**: JWT Bearer token required
- **Parameters**:
  - userId: Path parameter (integer) - ID of the user whose tasks are requested
- **Response**:
  - 200: OK - Array of tasks with dashboard statistics
    ```json
    {
      "tasks": [
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
      ],
      "dashboardStats": {
        "totalTasks": 15,
        "completedTasks": 8,
        "pendingTasks": 7
      }
    }
    ```

#### POST /api/{userId}/tasks
- **Purpose**: Create a new task for a specific user
- **Authentication**: JWT Bearer token required
- **Request Body**:
  ```json
  {
    "title": "New Task",
    "description": "Task description",
    "category": "Work",
    "priority": 2
  }
  ```
- **Response**:
  - 201: Created - Task created successfully
    ```json
    {
      "id": 1,
      "title": "New Task",
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

#### PUT /api/{userId}/tasks/{taskId}
- **Purpose**: Update an existing task for a specific user
- **Authentication**: JWT Bearer token required
- **Request Body** (partial updates allowed):
  ```json
  {
    "title": "Updated Task Title",
    "status": true,
    "priority": 3
  }
  ```
- **Response**:
  - 200: OK - Task updated successfully
    ```json
    {
      "id": 1,
      "title": "Updated Task Title",
      "description": "Task description",
      "status": true,
      "category": "Work",
      "priority": 3,
      "createdAt": "2026-01-03T10:00:00Z",
      "updatedAt": "2026-01-03T10:31:00Z",
      "userId": 1,
      "version": 2
    }
    ```

#### DELETE /api/{userId}/tasks/{taskId}
- **Purpose**: Delete a specific task for a user
- **Authentication**: JWT Bearer token required
- **Response**:
  - 204: No Content - Task deleted successfully

## WebSocket API for Real-Time Updates

### Connection
- **Endpoint**: `ws://localhost:8000/ws/dashboard/{userId}`
- **Authentication**: JWT token passed as query parameter `?token={jwt_token}`

### Message Types

#### Server to Client Messages

**dashboard_update**
- **Purpose**: Send updated dashboard statistics to client
- **Message Format**:
  ```json
  {
    "type": "dashboard_update",
    "payload": {
      "totalTasks": 16,
      "completedTasks": 9,
      "pendingTasks": 7,
      "updatedAt": "2026-01-03T10:30:00Z"
    },
    "timestamp": "2026-01-03T10:30:00Z"
  }
  ```

**task_update**
- **Purpose**: Notify client of a task change
- **Message Format**:
  ```json
  {
    "type": "task_update",
    "payload": {
      "taskId": 1,
      "action": "updated", // "created", "updated", "deleted"
      "task": {
        "id": 1,
        "title": "Updated Task",
        "status": true,
        "priority": 2
      }
    },
    "timestamp": "2026-01-03T10:30:00Z"
  }
  ```

#### Client to Server Messages

**subscribe_dashboard**
- **Purpose**: Request to subscribe to dashboard updates
- **Message Format**:
  ```json
  {
    "type": "subscribe_dashboard",
    "payload": {
      "userId": 1
    }
  }
  ```

**unsubscribe_dashboard**
- **Purpose**: Request to unsubscribe from dashboard updates
- **Message Format**:
  ```json
  {
    "type": "unsubscribe_dashboard",
    "payload": {
      "userId": 1
    }
  }
  ```

## Authentication Endpoints

### POST /auth/refresh
- **Purpose**: Refresh access token using refresh token
- **Request Body**:
  ```json
  {
    "refresh_token": "refresh_token_string"
  }
  ```
- **Response**:
  - 200: OK - New tokens provided
    ```json
    {
      "access_token": "new_access_token",
      "refresh_token": "new_refresh_token",
      "token_type": "bearer"
    }
    ```
  - 401: Unauthorized - Invalid refresh token

## Error Response Format

All error responses follow this format:
```json
{
  "detail": "Error message describing the issue"
}
```

## Validation Rules

### Request Validation
- All user IDs must be positive integers
- Task titles must be 1-200 characters
- Task descriptions must be 0-1000 characters
- Priority must be 1, 2, or 3
- Category must be 0-100 characters

### Response Validation
- All timestamps must be in ISO 8601 format
- Status fields must be boolean values
- Statistics counts must be non-negative integers