# Chatbot Architecture and Structure

## Overview
The chatbot system is designed to provide a conversational interface for all basic level features of the Todo App, enabling users to interact with the application through natural language. The system integrates both frontend and backend components with AI capabilities.

## Frontend Structure (from frontend-details.md)

### Chatbot UI Components (src/components/chatbot-ui/)
- **ChatBot.tsx**: Main chatbot component with open/close functionality and positioning controls
- **ChatWindow.tsx**: Chat interface window with message history, header, and input area
- **ChatInput.tsx**: Input field for sending messages with proper event handling
- **MessageBubble.tsx**: Individual message display component with sender differentiation
- **types.ts**: TypeScript interfaces for chat messages and chatbot props
- **index.ts**: Export file for easy imports

### Integration Points
- **DashboardPageClient.tsx**: Integrated into the dashboard with position="bottom-6 left-6" to avoid conflicts with New Task button
- **Glassmorphism Design**: Consistent frosted glass effect with coral accent colors matching the overall UI theme
- **Responsive Behavior**: Properly constrained height (max-h-[70vh]) to ensure header remains accessible when chat is long

### Frontend Features
- Fixed positioning with customizable placement
- Smooth animations and transitions
- Auto-scrolling to latest messages
- Typing indicators
- Message history display
- Proper error handling

## Backend Structure (from backend-details.md)

### API Endpoints for Chatbot Operations
- **Tasks (`/api/tasks/`)**:
  - `GET /` - Retrieve all tasks for user
  - `POST /` - Create new task
  - `PUT /{id}` - Update specific task
  - `DELETE /{id}` - Delete specific task

- **Authentication (`/api/auth/`)**:
  - `GET /session` - Verify user session
  - `POST /logout` - User logout

- **Dashboard (`/api/`)**:
  - `GET /dashboard/stats` - Get task statistics

### Backend Components Supporting Chatbot
- **api/task_router.py**: Task CRUD operations
- **services/task_service.py**: Business logic for task operations
- **models/task.py**: Task data model
- **schemas/task.py**: Task validation schemas
- **middleware/auth.py**: Authentication validation for protected operations

## Chatbot-Specific Backend Architecture

### 1. AI Integration Layer
- **OpenAI Agents SDK**: Powers the conversational AI logic
- **MCP (Model Context Protocol) Server**: Custom server using Official MCP SDK
- **Tool Definitions**: MCP tools that expose task operations as callable functions

### 2. State Management
- **Stateless Chat Endpoint**: RESTful endpoint that handles chat interactions
- **Conversation State Persistence**: Database storage for maintaining conversation context
- **Session Integration**: Links chat sessions to authenticated user sessions

### 3. MCP Server Architecture
```
MCP Server (using Official MCP SDK)
├── Tool Definitions
│   ├── create_task_tool(): Creates new tasks via API
│   ├── get_tasks_tool(): Retrieves user's tasks
│   ├── update_task_tool(): Updates existing tasks
│   ├── delete_task_tool(): Deletes tasks
│   ├── get_stats_tool(): Gets dashboard statistics
│   └── authenticate_user_tool(): Verifies user session
├── Context Management
│   ├── Conversation history storage
│   ├── User session linking
│   └── Intent recognition
└── Response Generation
    ├── Natural language processing
    ├── API call orchestration
    └── Formatted response generation
```

### 4. Database Schema for Chatbot
- **conversations** table: Stores conversation threads
  - conversation_id (UUID)
  - user_id (foreign key to users)
  - created_at
  - updated_at
  - context_data (JSONB for conversation state)

- **chat_messages** table: Stores individual messages
  - message_id (UUID)
  - conversation_id (foreign key)
  - sender ('user' or 'bot')
  - content (text)
  - timestamp
  - metadata (intents, entities)

## API Endpoints for Chatbot Operations

### Task Operations
```
POST /api/tasks
- Purpose: Create new tasks via chat commands
- Request: { title: string, description?: string, priority?: 'High'|'Medium'|'Low', dueDate?: string }
- Response: Created task object with ID

GET /api/tasks
- Purpose: Retrieve tasks for chat display
- Response: Array of task objects

PUT /api/tasks/{id}
- Purpose: Update tasks via chat commands
- Request: Partial task update object
- Response: Updated task object

DELETE /api/tasks/{id}
- Purpose: Delete tasks via chat commands
- Response: Success confirmation
```

### Chatbot-Specific Endpoints
```
POST /api/chat/conversation
- Purpose: Start or continue a conversation
- Request: { message: string, conversationId?: string }
- Response: { response: string, conversationId: string, action?: object }

GET /api/chat/conversation/{id}
- Purpose: Retrieve conversation history
- Response: Array of message objects

DELETE /api/chat/conversation/{id}
- Purpose: Clear conversation history
- Response: Success confirmation
```

## MCP Tools Specification

### Task Management Tools
1. **create_task(parameters)**
   - Parameters: title (required), description (optional), priority (optional), dueDate (optional)
   - Purpose: Creates a new task based on natural language input
   - Returns: Created task object

2. **update_task(task_id, parameters)**
   - Parameters: task_id (required), updates (object with any task fields)
   - Purpose: Updates an existing task based on user request
   - Returns: Updated task object

3. **delete_task(task_id)**
   - Parameters: task_id (required)
   - Purpose: Deletes a task based on user request
   - Returns: Success confirmation

4. **get_tasks(filter_params)**
   - Parameters: Optional filters (status, priority, search_term)
   - Purpose: Retrieves user's tasks with optional filtering
   - Returns: Array of task objects

5. **get_task_stats()**
   - Parameters: None
   - Purpose: Retrieves dashboard statistics for reporting
   - Returns: Statistics object (total, completed, pending counts)

### Authentication Tools
6. **verify_user_session()**
   - Parameters: None
   - Purpose: Validates current user session
   - Returns: User information or error

## AI Agent Capabilities

### Natural Language Understanding
- Task creation from natural language (e.g., "Add a task to buy groceries")
- Task updates via conversation (e.g., "Mark the meeting task as completed")
- Task deletion commands (e.g., "Remove my urgent tasks")
- Filtering and searching (e.g., "Show me my high priority tasks")

### Supported Operations
- **CREATE**: "Add a task to...", "Create a new task for...", "I need to remember to..."
- **READ**: "Show my tasks", "What do I have scheduled?", "List my pending tasks"
- **UPDATE**: "Complete task X", "Change the due date of Y", "Update priority of Z"
- **DELETE**: "Delete task X", "Remove the old task", "Cancel the appointment"

### Conversation Flow Management
- Context awareness across multiple exchanges
- Clarification requests when intent is ambiguous
- Confirmation prompts for destructive operations
- Error recovery and graceful degradation

## Integration Points

### Frontend-Backend Communication
- WebSocket connection for real-time chat updates
- REST API calls for task operations
- Session validation for each chat interaction
- Error handling and user feedback

### Authentication Integration
- User session verification before any task operations
- Permission checks for task access
- Session persistence across chat interactions
- Logout handling during active conversations

## Security Considerations

### Authentication & Authorization
- All chatbot operations require valid user authentication
- Task operations limited to user's own tasks
- Session validation on each API call
- Rate limiting for chat endpoints

### Data Protection
- Conversation history encrypted at rest
- Message content validation and sanitization
- API key management for AI services
- Audit logging for chatbot interactions

### Input Validation
- Natural language input sanitization
- Parameter validation for MCP tool calls
- SQL injection prevention for database operations
- Cross-site scripting (XSS) prevention

## Performance Considerations

### Caching Strategy
- Conversation context caching for improved response times
- Task data caching to reduce database queries
- API response caching for frequently accessed data

### Scalability
- Stateless chat endpoint design
- Database indexing for conversation queries
- Connection pooling for database operations
- Load balancing support for multiple instances

## Error Handling

### Graceful Degradation
- Fallback responses when AI services are unavailable
- Offline mode for basic functionality
- Error messages in natural language
- Automatic retry mechanisms for transient failures

### Monitoring & Logging
- Conversation success/failure tracking
- AI service response time monitoring
- Error categorization and alerting
- Performance metrics collection