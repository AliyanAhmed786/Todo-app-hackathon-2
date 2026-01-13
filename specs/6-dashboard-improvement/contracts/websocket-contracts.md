# WebSocket Contracts: Dashboard Improvement

**Feature**: 6-dashboard-improvement | **Date**: 2026-01-03

## WebSocket Connection Protocol

### Connection Endpoint
- **URL**: `ws://localhost:8000/ws/dashboard/{userId}`
- **Authentication**: JWT token passed as query parameter `?token={jwt_token}`
- **Protocol Version**: 1.0

### Connection Process
1. Client establishes WebSocket connection to the endpoint
2. Server validates JWT token from query parameter
3. If valid, server accepts connection and adds client to user's subscription list
4. Server sends confirmation message to client

### Connection Confirmation Message
```json
{
  "type": "connection_success",
  "payload": {
    "userId": 1,
    "message": "Successfully connected to dashboard updates"
  },
  "timestamp": "2026-01-03T10:30:00Z"
}
```

## Message Format

All WebSocket messages follow this structure:
```json
{
  "type": "message_type",
  "payload": { /* message-specific data */ },
  "timestamp": "2026-01-03T10:30:00Z"
}
```

## Server-to-Client Messages

### 1. Dashboard Statistics Update
- **Type**: `dashboard_update`
- **Purpose**: Notify client of updated dashboard statistics
- **Payload**:
  ```json
  {
    "totalTasks": 15,
    "completedTasks": 8,
    "pendingTasks": 7,
    "updatedAt": "2026-01-03T10:30:00Z"
  }
  ```
- **Trigger**: When any task is created, updated, or deleted for the user

### 2. Task Update Notification
- **Type**: `task_update`
- **Purpose**: Notify client of a specific task change
- **Payload**:
  ```json
  {
    "taskId": 1,
    "action": "created", // "created", "updated", "deleted"
    "task": {
      "id": 1,
      "title": "Updated Task",
      "description": "Task description",
      "status": true,
      "category": "Work",
      "priority": 2,
      "updatedAt": "2026-01-03T10:30:00Z"
    }
  }
  ```
- **Trigger**: When a task is modified by the user or another user with access

### 3. Error Message
- **Type**: `error`
- **Purpose**: Notify client of an error condition
- **Payload**:
  ```json
  {
    "code": "AUTH_EXPIRED",
    "message": "Authentication token has expired. Please reconnect with a new token."
  }
  ```
- **Trigger**: When authentication becomes invalid during connection

### 4. Connection Status
- **Type**: `connection_status`
- **Purpose**: Inform client of connection status changes
- **Payload**:
  ```json
  {
    "status": "connected", // "connected", "reconnecting", "disconnected"
    "message": "Connection established successfully"
  }
  ```
- **Trigger**: When connection state changes

## Client-to-Server Messages

### 1. Subscribe to Dashboard Updates
- **Type**: `subscribe_dashboard`
- **Purpose**: Request to receive dashboard updates
- **Payload**:
  ```json
  {
    "userId": 1
  }
  ```
- **Response**: Server confirms subscription and begins sending updates

### 2. Unsubscribe from Dashboard Updates
- **Type**: `unsubscribe_dashboard`
- **Purpose**: Request to stop receiving dashboard updates
- **Payload**:
  ```json
  {
    "userId": 1
  }
  ```
- **Response**: Server confirms unsubscription and stops sending updates

### 3. Ping/Pong for Connection Health
- **Type**: `ping`
- **Purpose**: Check connection health
- **Payload**: Empty object `{}` or timestamp
- **Response**: Server sends `pong` message

### 4. Pong Response
- **Type**: `pong`
- **Purpose**: Response to ping message
- **Payload**: Same timestamp as ping or empty object

## Error Codes

| Code | Description | Action Required |
|------|-------------|----------------|
| AUTH_EXPIRED | JWT token has expired | Re-authenticate and reconnect |
| AUTH_INVALID | Invalid JWT token provided | Re-authenticate and reconnect |
| USER_NOT_FOUND | User ID in token does not exist | Verify user account |
| SUBSCRIPTION_FAILED | Failed to establish subscription | Retry subscription |
| CONNECTION_LIMIT | Too many connections for user | Close other connections |

## Connection Management

### Reconnection Strategy
- Client should implement exponential backoff for reconnection attempts
- Initial delay: 1 second, max delay: 30 seconds
- Client should attempt to reconnect automatically when connection is lost

### Message Acknowledgment
- For critical messages, implement acknowledgment system
- Server sends message with unique ID
- Client responds with acknowledgment of the message ID

### Rate Limiting
- Server limits messages to 10 per second per connection
- Excessive messages result in temporary connection blocking

## Security Considerations

### Authentication
- JWT tokens must be validated on each connection
- Tokens should include user ID and expiration
- Refresh tokens should be used to obtain new JWTs before expiration

### Authorization
- Clients can only subscribe to their own dashboard updates
- Server validates that userId in subscription matches authenticated user
- Cross-user data access is prevented

### Message Validation
- All incoming messages are validated for proper structure
- Malformed messages result in connection termination
- Payload data is sanitized before processing

## Performance Guidelines

### Message Frequency
- Dashboard updates: Maximum 1 per second per user
- Task updates: Batched to avoid excessive messages
- Clients should debounce UI updates to prevent excessive re-rendering

### Connection Limits
- Maximum 5 concurrent connections per user
- Server maintains connection pool for efficient resource usage
- Inactive connections are closed after 10 minutes of inactivity

## Client Implementation Guidelines

### Connection Handling
```javascript
// Example WebSocket connection setup
const connectWebSocket = (userId, token) => {
  const ws = new WebSocket(`ws://localhost:8000/ws/dashboard/${userId}?token=${token}`);

  ws.onopen = () => {
    // Send subscription request
    ws.send(JSON.stringify({
      type: 'subscribe_dashboard',
      payload: { userId },
      timestamp: new Date().toISOString()
    }));
  };

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    handleWebSocketMessage(message);
  };

  ws.onclose = () => {
    // Implement reconnection logic
    setTimeout(connectWebSocket, 1000, userId, token);
  };

  return ws;
};
```

### Message Handling
- Process messages on a separate thread to avoid blocking UI
- Implement message queuing for handling bursts of messages
- Update UI efficiently using virtual DOM or similar techniques