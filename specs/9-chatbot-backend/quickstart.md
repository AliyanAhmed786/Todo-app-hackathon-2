# Chatbot Backend Quickstart Guide

## 1. Prerequisites

### 1.1 System Requirements
- Python 3.13+
- Node.js 18+ (for frontend, if developing full stack)
- PostgreSQL (Neon or local instance)
- Docker (optional, for containerized development)

### 1.2 Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 1.3 Environment Variables
Create a `.env` file in the backend directory:
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MCP Server
MCP_SERVER_URL=http://localhost:8001
```

## 2. Database Setup

### 2.1 Run Migrations
```bash
# Apply database migrations
python -m alembic upgrade head

# Or create new migrations if needed
python -m alembic revision --autogenerate -m "Add conversation and message tables"
```

### 2.2 Verify Tables
After running the application, verify that the new tables are created:
- `conversations` table
- `messages` table

## 3. MCP Server Setup

### 3.1 Install MCP SDK
```bash
pip install mcp-sdk
```

### 3.2 Start MCP Server
```bash
# Navigate to MCP server directory
cd backend/mcp

# Start the MCP server
python server.py
```

## 4. Running the Application

### 4.1 Start Backend
```bash
# From backend directory
uvicorn main:app --reload --port 8000
```

### 4.2 Start MCP Server Separately
```bash
# In a separate terminal
cd backend/mcp
python server.py
```

## 5. API Testing

### 5.1 Test Authentication
```bash
# Get JWT token from existing auth system
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

### 5.2 Test Chat Endpoint
```bash
# Replace USER_ID with actual user ID and TOKEN with JWT
curl -X POST http://localhost:8000/api/USER_ID/chat \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": null
  }'
```

Expected response:
```json
{
  "response": "I've created a task 'buy groceries' for you.",
  "conversation_id": "generated-uuid-here",
  "tool_calls": [...],
  "action": {
    "type": "task_created",
    "data": {...}
  }
}
```

## 6. Key Endpoints

### 6.1 Chat Endpoint
- **URL**: `POST /api/{user_id}/chat`
- **Authentication**: JWT Bearer token
- **Function**: Process natural language and execute tasks

### 6.2 Conversation Management (Future)
- **URL**: `GET /api/{user_id}/chat/conversations`
- **Authentication**: JWT Bearer token
- **Function**: List user's conversations

## 7. Development Workflow

### 7.1 Adding MCP Tools
1. Create tool function in `backend/mcp/tools.py`
2. Register tool with MCP server in `backend/mcp/server.py`
3. Test tool individually
4. Integrate with OpenAI agent

### 7.2 Testing Changes
```bash
# Run backend tests
pytest tests/ -v

# Run specific chat endpoint tests
pytest tests/test_chat_endpoint.py -v

# Run integration tests
pytest tests/test_chat_integration.py -v
```

## 8. Common Issues & Solutions

### 8.1 JWT Token Issues
- **Problem**: 401 Unauthorized errors
- **Solution**: Verify JWT secret key and token format

### 8.2 Database Connection Issues
- **Problem**: Cannot connect to database
- **Solution**: Check DATABASE_URL and ensure PostgreSQL is running

### 8.3 OpenAI API Issues
- **Problem**: API errors or timeouts
- **Solution**: Verify OPENAI_API_KEY and check rate limits

### 8.4 MCP Server Connection Issues
- **Problem**: Tools not being called
- **Solution**: Ensure MCP server is running and accessible

## 9. Configuration

### 9.1 Environment Variables Reference
| Variable | Purpose | Default |
|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `JWT_SECRET_KEY` | JWT signing key | Required |
| `DATABASE_URL` | Database connection string | Required |
| `MCP_SERVER_URL` | MCP server location | http://localhost:8001 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiry duration | 60 |

## 10. Next Steps

1. Implement the 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
2. Connect OpenAI agent to MCP tools
3. Test end-to-end functionality
4. Add error handling and logging
5. Deploy to staging environment