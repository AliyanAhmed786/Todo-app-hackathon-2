# Chatbot Backend Implementation Specification

## 1. Overview

### 1.1 Context
The Todo App currently has a frontend chatbot UI but lacks the backend implementation. This specification outlines the implementation of Phase III AI Chatbot backend that enables users to interact with the Todo App through natural language using OpenAI Agents SDK and MCP (Model Context Protocol) tools.

### 1.2 Objective
To implement a complete backend system for the chatbot that allows users to perform all todo operations through natural language conversations, with proper authentication, conversation state management, and integration with existing task management services.

## 2. Functional Requirements

### 2.1 Conversation Management Requirements
- **REQ-CONV-001**: The system shall provide data models for conversations and messages in backend/models/
- **REQ-CONV-002**: The system shall store conversation state in the database for continuity
- **REQ-CONV-003**: The system shall fetch conversation history from DB before processing each request

### 2.2 API Endpoint Requirements
- **REQ-API-001**: The system shall provide a POST /api/{user_id}/chat endpoint in backend/api/chat_router.py
- **REQ-API-002**: The system shall require JWT authentication for the chat endpoint
- **REQ-API-003**: The system shall accept user_id as a path parameter for proper user isolation

### 2.3 MCP Server Requirements
- **REQ-MCP-001**: The system shall implement an MCP server in backend/mcp/ using the Official MCP SDK
- **REQ-MCP-002**: The system shall implement 5 MCP tools as specified: add_task, list_tasks, complete_task, delete_task, update_task
- **REQ-MCP-003**: The system shall ensure MCP tools are stateless and query DB directly

### 2.4 AI Agent Integration Requirements
- **REQ-AI-001**: The system shall integrate OpenAI Agents SDK with a single agent instance using GPT-4 Turbo (gpt-4-1106-preview) model
- **REQ-AI-002**: The system shall connect the agent to all 5 MCP tools for natural language processing
- **REQ-AI-003**: The system shall handle natural language → tool selection mapping

### 2.5 Task Operation Requirements
- **REQ-TASK-001**: The system shall implement add_task(user_id, title, description, priority, due_date) MCP tool where priority is one of "high", "medium", "low" and due_date is in ISO 8601 format (YYYY-MM-DD)
- **REQ-TASK-002**: The system shall implement list_tasks(user_id, status) MCP tool
- **REQ-TASK-003**: The system shall implement complete_task(user_id, task_id) MCP tool
- **REQ-TASK-004**: The system shall implement delete_task(user_id, task_id) MCP tool
- **REQ-TASK-005**: The system shall implement update_task(user_id, task_id, title, description, priority, due_date) MCP tool where priority is one of "high", "medium", "low" and due_date is in ISO 8601 format (YYYY-MM-DD)

### 2.6 Authentication Requirements
- **REQ-AUTH-001**: The system shall enforce JWT authentication for all chat endpoint requests with 1-hour expiry and automatic refresh for long conversations
- **REQ-AUTH-002**: The system shall restrict operations to user's own data only
- **REQ-AUTH-003**: The system shall validate user identity before processing requests

## 3. Non-Functional Requirements

### 3.1 Performance Requirements
- **REQ-PERF-001**: The system shall respond to chat requests within 3 seconds for 95% of requests under normal load
- **REQ-PERF-002**: The system shall maintain conversation state efficiently without impacting performance
- **REQ-PERF-003**: The system shall handle AI service latencies gracefully with 10-second timeout for AI operations
- **REQ-PERF-004**: The system shall support 100 concurrent users

### 3.2 Security Requirements
- **REQ-SEC-001**: The system shall validate JWT tokens for all chat endpoint requests
- **REQ-SEC-002**: The system shall prevent cross-user data access through proper user_id validation
- **REQ-SEC-003**: The system shall sanitize all user inputs before processing

### 3.3 Scalability Requirements
- **REQ-SCALE-001**: The system shall support stateless server architecture for horizontal scaling
- **REQ-SCALE-002**: The system shall efficiently handle increasing conversation volume

### 3.4 Availability Requirements
- **REQ-AVAIL-001**: The system shall provide graceful degradation when AI services are unavailable
- **REQ-AVAIL-002**: The system shall maintain 99% uptime for core functionality

## 4. User Scenarios & Testing

### 4.1 User Scenario 1: Creating a Task via Chat
**Actor**: Authenticated user
**Goal**: Create a new task using natural language
**Steps**:
1. User sends "Add a task to buy groceries" to POST /api/{user_id}/chat
2. System authenticates the user via JWT
3. OpenAI Agent processes the natural language and selects add_task tool
4. MCP server executes add_task(user_id, "buy groceries", null)
5. System returns confirmation response to user

**Acceptance Criteria**:
- Task is created in the database with correct user association
- User receives appropriate confirmation message
- Conversation history is updated

### 4.2 User Scenario 2: Listing Tasks via Chat
**Actor**: Authenticated user
**Goal**: Retrieve a list of tasks using natural language
**Steps**:
1. User sends "Show me my pending tasks" to POST /api/{user_id}/chat
2. System authenticates the user via JWT
3. OpenAI Agent processes the natural language and selects list_tasks tool
4. MCP server executes list_tasks(user_id, "pending")
5. System returns formatted task list to user

**Acceptance Criteria**:
- Correct tasks are retrieved based on user and status filters
- User receives properly formatted task list
- Conversation history is updated

### 4.3 User Scenario 3: Updating a Task via Chat
**Actor**: Authenticated user
**Goal**: Update an existing task using natural language
**Steps**:
1. User sends "Complete the meeting task" to POST /api/{user_id}/chat
2. System authenticates the user via JWT
3. OpenAI Agent processes the natural language and first calls list_tasks to identify the correct task
4. MCP server executes list_tasks(user_id, null) to retrieve user's tasks
5. OpenAI Agent analyzes the task list to identify the "meeting task"
6. OpenAI Agent selects complete_task tool with the correct task_id
7. MCP server executes complete_task(user_id, identified_task_id)
8. System returns confirmation response to user

**Acceptance Criteria**:
- Task is updated in the database with correct status
- User receives appropriate confirmation message
- Conversation history is updated

## 5. Key Entities & Data Model

### 5.1 Conversation Entity
- **Entity**: Conversation
- **Attributes**:
  - id (UUID, primary key)
  - user_id (foreign key to User)
  - created_at (timestamp)
  - updated_at (timestamp)
  - metadata (JSON for conversation context)

### 5.2 Message Entity
- **Entity**: Message
- **Attributes**:
  - id (UUID, primary key)
  - conversation_id (foreign key to Conversation)
  - sender (enum: 'user' | 'agent')
  - content (text)
  - timestamp (timestamp)
  - metadata (JSON for AI context)

### 5.3 Task Data Model Reference
- **Priority Values**: "high", "medium", "low"
- **Due Date Format**: ISO 8601 format (YYYY-MM-DD)

## 6. Technical Architecture

### 6.1 System Architecture
```
User → POST /api/{user_id}/chat → JWT Auth → OpenAI Agent → MCP Server (5 tools) → Database
```

### 6.2 Component Interactions
- Chat endpoint authenticates user and retrieves conversation history
- OpenAI Agent processes natural language and selects appropriate MCP tool
- MCP tools execute database operations using existing task_service.py logic
- Results are returned to user with updated conversation state

## 7. Request/Response Schemas

### 7.1 POST /api/{user_id}/chat Request Body
```
{
  "message": "Natural language command from user",
  "conversation_id": "UUID of existing conversation (optional)"
}
```

### 7.2 POST /api/{user_id}/chat Response Format
```
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

## 8. Error Handling

### 8.1 Invalid Task ID Scenarios
- **ERR-TASK-001**: When a user refers to a task that doesn't exist, the system shall return a helpful error message suggesting the user clarify or list their tasks
- **ERR-TASK-002**: When a user refers to a task they don't own, the system shall return an access denied message

### 8.2 Database Operation Failures
- **ERR-DB-001**: When database operations fail, the system shall return a user-friendly error message without exposing internal details
- **ERR-DB-002**: The system shall log detailed error information for debugging purposes

### 8.3 OpenAI API Failures
- **ERR-AI-001**: When OpenAI API is unavailable, the system shall provide graceful degradation with appropriate user notification
- **ERR-AI-002**: The system shall implement retry logic with exponential backoff (1s, 2s, 4s, 8s max) with 3 attempts before user notification for temporary API failures

### 8.4 Authentication Errors
- **ERR-AUTH-001**: When JWT tokens are invalid or expired, the system shall return appropriate HTTP 401 status with clear error message
- **ERR-AUTH-002**: When user_id in token doesn't match the path parameter, the system shall return HTTP 403 forbidden

## 9. Assumptions

- **ASSUMPTION-001**: OpenAI API access is properly configured with valid API keys
- **ASSUMPTION-002**: Existing task_service.py contains all necessary business logic for task operations
- **ASSUMPTION-003**: Database connection pool is properly configured for concurrent access
- **ASSUMPTION-004**: JWT authentication middleware is already available and functional
- **ASSUMPTION-005**: MCP SDK is compatible with current Python/FastAPI versions

## 10. Success Criteria

### 10.1 Functional Success Metrics
- [ ] 100% of specified MCP tools are implemented and functional
- [ ] Chat endpoint successfully processes natural language requests
- [ ] All task operations (create, read, update, delete) work via chat interface
- [ ] JWT authentication is enforced for all chat operations
- [ ] Conversation history is properly maintained and accessible

### 10.2 Performance Success Metrics
- [ ] 95% of chat requests respond within 5 seconds
- [ ] System handles at least 50 concurrent chat sessions
- [ ] Database queries maintain acceptable performance under load

### 10.3 User Experience Success Metrics
- [ ] Users can perform all basic task operations via natural language
- [ ] Error messages are clear and actionable
- [ ] Conversation context is maintained appropriately across exchanges
- [ ] Authentication failures are handled gracefully with clear feedback

### 10.4 Technical Success Metrics
- [ ] All components follow existing code patterns and conventions
- [ ] No direct imports exist between chat endpoint and task operations (per constraint)
- [ ] MCP tools properly utilize existing task_service.py logic
- [ ] System maintains backward compatibility with existing functionality

## 11. Dependencies

- **DEPENDENCY-001**: OpenAI Agents SDK
- **DEPENDENCY-002**: Official MCP SDK
- **DEPENDENCY-003**: Existing JWT authentication system
- **DEPENDENCY-004**: Existing task_service.py business logic
- **DEPENDENCY-005**: SQLModel ORM and database connection

## 12. Constraints

- MCP tools must be stateless and query DB directly
- Chat endpoint must fetch conversation history from DB before each request
- Chat endpoint CANNOT directly import task operations (decoupling achieved through MCP tools)
- MCP tools CAN import and use existing task_service.py logic
- JWT auth required for chat endpoint
- System must be stateless server architecture for scalability

## Clarifications

### Session 2026-01-15

- Q: What are the specific values for priority and due_date formats? → A: Priority: "high", "medium", "low"; Due Date: ISO 8601 format (YYYY-MM-DD)
- Q: What is the JWT token expiry and refresh strategy? → A: JWT tokens have 1-hour expiry with automatic refresh mechanism for long conversations
- Q: What are the specific performance targets? → A: Response time: 3 seconds for 95% of requests; Support 100 concurrent users; Allow 10-second timeout for AI operations
- Q: What is the retry strategy for AI service failures? → A: Exponential backoff: 1s, 2s, 4s, 8s max with 3 attempts before user notification
- Q: Which OpenAI model should be used? → A: Use GPT-4 Turbo (gpt-4-1106-preview) for optimal balance of capability and cost