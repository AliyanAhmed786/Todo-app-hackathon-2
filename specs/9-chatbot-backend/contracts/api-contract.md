# Chatbot Backend API Contract

## 1. Authentication Contract

### 1.1 JWT Token Requirements
- **Header**: `Authorization: Bearer {token}`
- **Expiry**: 1 hour
- **Algorithm**: RS256
- **Claims Required**:
  - `sub`: User ID (UUID)
  - `exp`: Expiration timestamp
  - `iat`: Issued at timestamp
  - `jti`: JWT ID for revocation (optional)

### 1.2 User ID Validation
- Path parameter `{user_id}` must match JWT `sub` claim
- Return 403 Forbidden if mismatch
- Validate user exists in database

## 2. Endpoint Specifications

### 2.1 POST /api/{user_id}/chat

#### Request
**Path Parameters**:
- `user_id` (string, required): UUID of the authenticated user

**Headers**:
- `Authorization` (string, required): Bearer token with valid JWT
- `Content-Type` (string, required): application/json

**Body** (application/json):
```json
{
  "message": {
    "type": "string",
    "description": "Natural language command from user",
    "example": "Add a task to buy groceries",
    "minLength": 1,
    "maxLength": 1000
  },
  "conversation_id": {
    "type": "string",
    "description": "UUID of existing conversation (optional)",
    "format": "uuid",
    "nullable": true,
    "example": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

#### Response
**Success Response (200 OK)**:
```json
{
  "response": {
    "type": "string",
    "description": "Natural language response to user",
    "example": "I've created a task 'buy groceries' for you."
  },
  "conversation_id": {
    "type": "string",
    "description": "UUID of the conversation thread",
    "format": "uuid",
    "example": "550e8400-e29b-41d4-a716-446655440000"
  },
  "tool_calls": {
    "type": "array",
    "description": "List of tools called during processing",
    "items": {
      "type": "object",
      "properties": {
        "tool_name": {
          "type": "string",
          "description": "Name of the MCP tool called",
          "example": "add_task"
        },
        "parameters": {
          "type": "object",
          "description": "Parameters passed to the tool",
          "example": {
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "buy groceries",
            "priority": "medium"
          }
        },
        "result": {
          "type": "object",
          "description": "Result of the tool execution",
          "example": {
            "success": true,
            "task": {
              "id": "650e8400-e29b-41d4-a716-446655440001",
              "title": "buy groceries",
              "priority": "medium",
              "status": "pending"
            }
          }
        }
      }
    }
  },
  "action": {
    "type": "object",
    "description": "Information about the action taken",
    "properties": {
      "type": {
        "type": "string",
        "description": "Type of action taken",
        "enum": ["task_created", "task_updated", "task_deleted", "task_listed", "error"],
        "example": "task_created"
      },
      "data": {
        "type": "object",
        "description": "Additional data about the action",
        "example": {
          "task_id": "650e8400-e29b-41d4-a716-446655440001",
          "task_title": "buy groceries"
        }
      }
    }
  }
}
```

**Error Responses**:

**400 Bad Request**:
```json
{
  "error": {
    "type": "string",
    "description": "Error message",
    "example": "Invalid request body format"
  },
  "details": {
    "type": "object",
    "description": "Additional error details",
    "nullable": true
  }
}
```

**401 Unauthorized**:
```json
{
  "error": {
    "type": "string",
    "description": "Authentication error message",
    "example": "Invalid or expired token"
  }
}
```

**403 Forbidden**:
```json
{
  "error": {
    "type": "string",
    "description": "Authorization error message",
    "example": "Access denied: user_id mismatch"
  }
}
```

**429 Too Many Requests**:
```json
{
  "error": {
    "type": "string",
    "description": "Rate limit error message",
    "example": "Rate limit exceeded"
  },
  "retry_after": {
    "type": "integer",
    "description": "Seconds to wait before retrying",
    "example": 60
  }
}
```

**500 Internal Server Error**:
```json
{
  "error": {
    "type": "string",
    "description": "Generic error message",
    "example": "An unexpected error occurred"
  }
}
```

### 2.2 GET /api/{user_id}/chat/conversations (Future Enhancement)

#### Response
**Success Response (200 OK)**:
```json
{
  "conversations": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid",
          "description": "Conversation ID"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Creation timestamp"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Last update timestamp"
        },
        "preview": {
          "type": "string",
          "description": "Preview of last message"
        }
      }
    }
  }
}
```

## 3. Data Validation

### 3.1 Request Validation
- Message length: 1-1000 characters
- Conversation ID: Valid UUID format if provided
- User ID: Valid UUID format
- User must exist in database

### 3.2 Response Validation
- Response message: Non-empty string
- Conversation ID: Valid UUID
- Tool calls: Valid structure with required fields
- Action: Valid type and data

## 4. Rate Limiting

### 4.1 Limits
- Per user: 100 requests per minute
- Per IP: 1000 requests per minute
- Per conversation: 50 messages per minute

### 4.2 Enforcement
- Token bucket algorithm
- Sliding window counter for precise rate calculation
- 429 response with `Retry-After` header

## 5. Error Handling

### 5.1 Client Errors (4xx)
- Invalid input: 400 with validation details
- Authentication failure: 401 with token error
- Authorization failure: 403 with access error
- Rate limiting: 429 with retry information

### 5.2 Server Errors (5xx)
- Internal processing errors: 500 with generic message
- External API failures: 500 with service unavailable message
- Database errors: 500 with generic message

## 6. Security Headers

### 6.1 Required Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

## 7. Performance Requirements

### 7.1 Response Times
- 95th percentile: < 3 seconds
- 99th percentile: < 5 seconds
- Average: < 1.5 seconds

### 7.2 Concurrency
- Support 100 concurrent connections
- Handle 1000 requests per minute sustained load
- Graceful degradation under higher loads

## 8. API Versioning

### 8.1 Version Strategy
- URI versioning: `/api/v1/{user_id}/chat`
- Backward compatibility maintained for 6 months after deprecation
- Deprecation headers in responses

### 8.2 Compatibility
- Breaking changes require new version
- Non-breaking additions allowed in current version
- Field additions should be optional