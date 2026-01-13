# API Contracts: Frontend UI Improvements

## Authentication Endpoints

### POST /auth/login
**Description**: Authenticate user and return session token
**Request**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```
**Response**:
- 200: `{"token": "string", "user": {"id": "string", "email": "string"}}`
- 401: `{"error": "Invalid credentials"}`
- 422: `{"error": "Validation error", "details": "array"}`

### POST /auth/signup
**Description**: Register new user
**Request**:
```json
{
  "email": "string (required)",
  "password": "string (required, min 8 chars)",
  "name": "string (optional)"
}
```
**Response**:
- 201: `{"token": "string", "user": {"id": "string", "email": "string"}}`
- 409: `{"error": "User already exists"}`
- 422: `{"error": "Validation error", "details": "array"}`

## Task Management Endpoints

### GET /tasks
**Description**: Get user's tasks with pagination
**Query Parameters**:
- page: number (default: 1)
- limit: number (default: 10)
- status: "pending|completed|all" (default: "all")
- priority: "P1|P2|P3|all" (default: "all")
**Response**:
- 200: `{"tasks": [{"id": "string", "title": "string", "description": "string", "priority": "P1|P2|P3", "status": "pending|completed", "createdAt": "date", "updatedAt": "date"}], "total": number, "page": number, "limit": number}`
- 401: `{"error": "Unauthorized"}`

### POST /tasks
**Description**: Create a new task
**Request**:
```json
{
  "title": "string (required, max 255)",
  "description": "string (optional, max 1000)",
  "priority": "P1|P2|P3 (default: P3)"
}
```
**Response**:
- 201: `{"id": "string", "title": "string", "description": "string", "priority": "P1|P2|P3", "status": "pending", "createdAt": "date", "updatedAt": "date"}`
- 401: `{"error": "Unauthorized"}`
- 422: `{"error": "Validation error", "details": "array"}`

### PUT /tasks/{id}
**Description**: Update an existing task
**Path Parameters**:
- id: string (task ID)
**Request**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "priority": "P1|P2|P3 (optional)",
  "status": "pending|completed (optional)"
}
```
**Response**:
- 200: `{"id": "string", "title": "string", "description": "string", "priority": "P1|P2|P3", "status": "pending|completed", "createdAt": "date", "updatedAt": "date"}`
- 401: `{"error": "Unauthorized"}`
- 404: `{"error": "Task not found"}`
- 422: `{"error": "Validation error", "details": "array"}`

### DELETE /tasks/{id}
**Description**: Delete a task
**Path Parameters**:
- id: string (task ID)
**Response**:
- 204: No content
- 401: `{"error": "Unauthorized"}`
- 404: `{"error": "Task not found"}`

## Dashboard Statistics Endpoint

### GET /dashboard/stats
**Description**: Get user's dashboard statistics
**Response**:
- 200: `{"totalTasks": number, "completedTasks": number, "pendingTasks": number, "progressPercentage": number}`
- 401: `{"error": "Unauthorized"}`

## Error Handling

All API endpoints follow consistent error response format:
- 400: `{"error": "Bad Request", "message": "string"}`
- 401: `{"error": "Unauthorized", "message": "Authentication required"}`
- 404: `{"error": "Not Found", "message": "Resource not found"}`
- 422: `{"error": "Validation Error", "details": [{"field": "string", "message": "string"}]}`
- 500: `{"error": "Internal Server Error", "message": "An unexpected error occurred"}`

## Versioning

All API endpoints use the same version (v1) and are accessible at `/api/v1/{endpoint}`.