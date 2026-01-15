# Chatbot Backend Implementation Plan

## 1. Technical Context

### 1.1 Architecture Overview
- **Backend Framework**: FastAPI with SQLAlchemy async
- **Database**: Neon PostgreSQL (SQLModel ORM)
- **Existing Models**: User, Task, Session
- **Existing Services**: task_service.py
- **Authentication**: Better Auth JWT system

### 1.2 Target Architecture
- **Phase III**: AI Integration with OpenAI Agents SDK, MCP SDK, OpenAI ChatKit
- **Components**:
  - Conversation/Message models in backend/models/
  - MCP server in backend/mcp/ with 5 tools
  - POST /api/{user_id}/chat endpoint in backend/api/chat_router.py
  - OpenAI Agent integration with MCP tools
  - Database storage for conversation state

### 1.3 Technology Stack
- **Primary**: Python 3.13+, FastAPI, SQLModel
- **AI**: OpenAI Agents SDK, GPT-4 Turbo model
- **Protocol**: MCP SDK for tool communication
- **Authentication**: JWT tokens with 1-hour expiry and auto-refresh
- **Data Format**: ISO 8601 for dates, priority values: "high", "medium", "low"

### 1.4 Known Constraints
- MCP tools must be stateless and query DB directly
- Chat endpoint must fetch conversation history from DB before each request
- Chat endpoint CANNOT directly import task operations (decoupling achieved through MCP tools)
- MCP tools CAN import and use existing task_service.py logic
- JWT auth required for chat endpoint
- System must be stateless server architecture for scalability

## 2. Research & Unknowns

### 2.1 Resolved Requirements (from spec clarifications)
- Priority values: "high", "medium", "low"
- Due date format: ISO 8601 (YYYY-MM-DD)
- JWT token expiry: 1-hour with automatic refresh
- Performance targets: 3s response for 95% of requests, 100 concurrent users
- Retry strategy: Exponential backoff (1s, 2s, 4s, 8s max) with 3 attempts
- OpenAI model: GPT-4 Turbo (gpt-4-1106-preview)

### 2.2 Dependencies to Research
- OpenAI Agents SDK integration patterns
- MCP SDK implementation best practices
- SQLModel async operations with conversation history
- JWT token refresh mechanisms in FastAPI
- Rate limiting strategies for AI endpoints

## 3. Phase 0: Research & Resolution

### 3.1 Research Tasks Completed
- OpenAI Agents SDK integration with MCP tools
- MCP SDK setup and tool registration patterns
- Conversation history management in stateless systems
- JWT token refresh strategies for long-running conversations
- SQLModel relationship patterns for conversation/message entities

### 3.2 Technology Decisions
- Using OpenAI's Assistants API for chat management
- MCP tools as separate modules with direct database access
- Conversation state stored in database with periodic retrieval
- Token refresh handled by frontend with automatic renewal

## 4. Phase 1: Data Model Design

### 4.1 Entity Relationships
```
User (1) -> (Many) Conversation
Conversation (1) -> (Many) Message
Conversation (1) -> (Many) Task (via MCP tools)
```

### 4.2 Conversation Entity
- id: UUID (primary key)
- user_id: UUID (foreign key to User)
- created_at: DateTime
- updated_at: DateTime
- metadata: JSON (conversation context)

### 4.3 Message Entity
- id: UUID (primary key)
- conversation_id: UUID (foreign key to Conversation)
- sender: String enum ("user", "agent")
- content: Text
- timestamp: DateTime
- metadata: JSON (AI context)

## 5. Phase 2: API Contract Design

### 5.1 Authentication Contract
- JWT token in Authorization header
- 1-hour expiry with refresh mechanism
- User ID validation against path parameter

### 5.2 Endpoint Contract: POST /api/{user_id}/chat
**Request**:
```json
{
  "message": "Natural language command from user",
  "conversation_id": "UUID of existing conversation (optional)"
}
```

**Response**:
```json
{
  "response": "Natural language response to user",
  "conversation_id": "UUID of the conversation thread",
  "tool_calls": [
    {
      "tool_name": "Name of the MCP tool called",
      "parameters": "Parameters passed to the tool",
      "result": "Result of the tool execution"
    }
  ],
  "action": {
    "type": "Type of action taken (e.g., 'task_created', 'task_updated')",
    "data": "Additional data about the action"
  }
}
```

**Error Responses**:
- 401: Invalid/expired JWT token
- 403: User ID mismatch
- 429: Rate limit exceeded
- 500: Internal server error

## 6. Phase 3: Component Architecture

### 6.1 MCP Tool Layer
- add_task(user_id, title, description, priority, due_date)
- list_tasks(user_id, status)
- complete_task(user_id, task_id)
- delete_task(user_id, task_id)
- update_task(user_id, task_id, title, description, priority, due_date)

### 6.2 Service Layer Integration
- MCP tools call existing task_service.py methods
- Proper validation of user ownership before operations
- Error handling and response formatting

### 6.3 Agent Integration
- OpenAI Agent configured with MCP tools
- Natural language processing and tool selection
- Response generation with action context

## 7. Implementation Phases

### Phase 1: Infrastructure Setup
- Create conversation/message models
- Set up database migrations
- Implement MCP server skeleton

### Phase 2: Core MCP Tools
- Implement all 5 MCP tools
- Connect to existing task_service.py
- Add authentication and validation

### Phase 3: API Endpoint
- Create chat router and endpoint
- Implement JWT authentication
- Add conversation history management

### Phase 4: AI Integration
- Connect OpenAI Agent to MCP tools
- Implement natural language processing
- Add response formatting

### Phase 5: Testing & Integration
- End-to-end testing
- Performance optimization
- Error handling refinement

## 8. Risk Assessment

### 8.1 High-Risk Areas
- API costs: OpenAI usage could become expensive with high usage
- Security: JWT validation and user data isolation
- Performance: AI processing latency could impact user experience
- Reliability: External API dependencies

### 8.2 Mitigation Strategies
- Rate limiting and usage monitoring for API costs
- Thorough input validation and user isolation for security
- Caching and connection pooling for performance
- Retry mechanisms and graceful degradation for reliability

## 9. Constitution Check

This plan adheres to the project constitution:

- **Spec-First Workflow**: Following validated spec from `/specs/9-chatbot-backend/spec.md`
- **Incremental Complexity**: Building on existing foundation (Phase III: AI Integration)
- **Clean Code Standards**: Using existing patterns and conventions
- **Technology Stack Adherence**: Using specified OpenAI Agents SDK, MCP SDK per Phase III
- **Code Traceability**: Will reference Task IDs in implementation
- **Open Source Transparency**: All code in public repository

## 10. Success Criteria

- [ ] All 5 MCP tools implemented and functional
- [ ] Chat endpoint processes natural language requests successfully
- [ ] Conversation state properly maintained across exchanges
- [ ] JWT authentication enforced with proper validation
- [ ] Performance targets met (3s response time, 100 concurrent users)
- [ ] Error handling comprehensive and user-friendly
- [ ] Integration with existing task management seamless