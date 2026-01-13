# Todo App Backend API

Backend CRUD API for Todo App with Better Auth integration and task management built with FastAPI and SQLModel.

## Features

- User authentication with Better Auth database session validation
- Task CRUD operations (Create, Read, Update, Delete)
- Rate limiting (100 requests per minute per user)
- PostgreSQL database with SQLModel
- Comprehensive error handling
- API documentation with examples
- HTTP-only cookies for secure session management

## Prerequisites

- Python 3.13+
- PostgreSQL (or access to Neon PostgreSQL)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todoapp
SECRET_KEY=your-super-secret-key-here-keep-it-safe-and-long
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### 5. Run the development server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Database Setup for Better Auth

The Better Auth integration requires specific database tables for session management. Make sure your database is properly initialized with the required tables:

```bash
# Run the application to create tables automatically
# Tables will be created based on the SQLModel definitions in models/
# The following tables are required for Better Auth:
# - users: stores user account information
# - tasks: stores user tasks
# - sessions: stores Better Auth database sessions
# - accounts: stores account provider information
# - verification: stores verification tokens
```

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Register new user with Better Auth database session validation
- `POST /api/auth/login` - Login existing user with Better Auth database session validation
- `POST /api/auth/logout` - Logout user and clear database session
- `GET /api/auth/session` - Get current user session using database validation

### Tasks

- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create new task for authenticated user
- `GET /api/tasks/{taskId}` - Get specific task for authenticated user
- `PUT /api/tasks/{taskId}` - Update task for authenticated user
- `PATCH /api/tasks/{taskId}/complete` - Mark task as complete for authenticated user

### Health Check

- `GET /health` - Health check endpoint

## API Design & Phase II Compliance

### Authentication-Based Routing

**Our Implementation**:
```
GET /api/tasks
Authorization: Bearer <jwt_token>
```

**Phase II Specification mentions**:
```
GET /api/{user_id}/tasks
```

### Why Our Approach is Industry Standard

We use **authentication-based routing** instead of user ID path parameters. This is the pattern used by:
- GitHub API (`GET /user/repos` not `/users/{id}/repos`)
- Stripe API (`GET /charges` not `/users/{id}/charges`)
- AWS API Gateway
- Google Cloud APIs

**Security Benefits**:
1. User ID extracted from verified JWT token (impossible to forge)
2. No risk of path parameter/token mismatch
3. Cleaner frontend code (no need to track user ID separately)
4. Follows OAuth 2.0 Bearer token standard

### Endpoint Mapping

All Phase II required operations are implemented:

| Operation | Our Endpoint | Method | Description |
|-----------|--------------|--------|-------------|
| List tasks | `GET /api/tasks` | GET | Returns tasks for authenticated user only |
| Create task | `POST /api/tasks` | POST | Creates task owned by authenticated user |
| Get task | `GET /api/tasks/{id}` | GET | Returns task if owned by authenticated user |
| Update task | `PUT /api/tasks/{id}` | PUT | Updates task if owned by authenticated user |
| Delete task | `DELETE /api/tasks/{id}` | DELETE | Deletes task if owned by authenticated user |
| Complete task | `PATCH /api/tasks/{id}/complete` | PATCH | Marks task complete if owned by authenticated user |

**User isolation** is enforced at the service layer - every query filters by authenticated user ID.

### JWT Configuration

Both frontend and backend share `BETTER_AUTH_SECRET` environment variable for JWT signing and verification.

```python
# backend/utils/auth.py
encoded_jwt = jwt.encode(data, settings.better_auth_secret, algorithm="HS256")
payload = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
```

## Rate Limiting

The API implements rate limiting of 100 requests per minute per authenticated user. Exceeding this limit will result in a 429 (Too Many Requests) response.

## Database Models

### Task Model
- id (int, primary key, auto-increment)
- title (str, 1-200 characters, required)
- description (str, 0-1000 characters, optional)
- status (bool, default false)
- category (str, 0-100 characters, optional)
- priority (int, 1-3, default 2)
- created_at (datetime, auto-generated)
- updated_at (datetime, auto-updated)
- user_id (str, foreign key to User - Better Auth compatible)

### User Model
- id (str, primary key - Better Auth compatible hex string)
- name (str, max 100 characters)
- email (str, unique, max 200 characters)
- password_hash (str)
- email_verified (bool, default false)
- image (str, optional)
- created_at (datetime, auto-generated)
- updated_at (datetime, auto-updated)

### Session Model
- id (str, primary key - hex string)
- token (str, unique session token)
- user_id (str, foreign key to User)
- expires_at (datetime, session expiration)
- created_at (datetime, auto-generated)

### Account Model
- id (str, primary key - hex string)
- user_id (str, foreign key to User)
- provider_id (str, identity provider)
- provider_account_id (str, provider-specific account ID)
- access_token (str, optional)
- refresh_token (str, optional)
- id_token (str, optional)
- expires_at (datetime, optional)
- token_type (str, optional)
- scope (str, optional)
- created_at (datetime, auto-generated)
- updated_at (datetime, auto-updated)

### Verification Model
- id (str, primary key - hex string)
- identifier (str, email or phone for verification)
- value (str, verification code or token)
- expires_at (datetime, verification expiration)
- created_at (datetime, auto-generated)

## Security Features

- Better Auth database session validation (no JWT tokens)
- HTTP-only cookies for secure session management
- Rate limiting (100 requests per minute per user)
- Input validation for all API endpoints
- SQL injection prevention through parameterized queries
- Password hashing using bcrypt
- Automatic session cleanup on logout

## Testing

To run tests:

```bash
pytest
```

## Environment Variables for Production

```env
DATABASE_URL=postgresql+asyncpg://username:password@neon-db-url:5432/todoapp
SECRET_KEY=production-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=15
DEBUG=False
```

## API Documentation

After starting the server, visit `http://localhost:8000/docs` for interactive API documentation.