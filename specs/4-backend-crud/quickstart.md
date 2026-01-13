# Quickstart Guide: Backend CRUD API for Todo App

## Prerequisites

- Python 3.13+
- pip package manager
- Neon PostgreSQL account (or local PostgreSQL instance)

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
pip install fastapi uvicorn sqlmodel python-jose[cryptography] slowapi asyncpg psycopg2-binary
```

### 4. Set up environment variables
Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todoapp
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5. Initialize the database
```bash
# Run database migrations to create tables
# This will be implemented in the backend code
```

### 6. Run the development server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login existing user
- `POST /auth/logout` - Logout user

### Tasks
- `GET /api/{userId}/tasks` - Get all tasks for user
- `POST /api/{userId}/tasks` - Create new task
- `GET /api/{userId}/tasks/{taskId}` - Get specific task
- `PUT /api/{userId}/tasks/{taskId}` - Update task
- `DELETE /api/{userId}/tasks/{taskId}` - Delete task

## Testing the API

### Using the built-in docs
- Visit `http://localhost:8000/docs` for interactive API documentation
- Test endpoints directly from the browser interface

### Using curl
```bash
# Create a new user
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'

# Login to get JWT token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
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
- priority (int, 1-3, default 1)
- created_at (datetime, auto-generated)
- updated_at (datetime, auto-updated)
- user_id (int, foreign key to User)

### User Model
- id (int, primary key, auto-increment)
- name (str, max 100 characters)
- email (str, unique, max 200 characters)
- password_hash (str)
- created_at (datetime, auto-generated)
- updated_at (datetime, auto-updated)

## Security Features

- JWT-based authentication with refresh token rotation
- Rate limiting (100 requests per minute per user)
- Input validation for all API endpoints
- SQL injection prevention through parameterized queries
- Password hashing using secure algorithms

## Development

### Adding new endpoints
1. Create new route functions in the appropriate router file
2. Add proper type hints and validation
3. Include comprehensive error handling
4. Update the OpenAPI specification if needed

### Running tests
```bash
# Tests will be implemented in the backend code
```

## Deployment

### For Production
1. Set production environment variables
2. Configure SSL certificates
3. Set up a reverse proxy (nginx)
4. Use a process manager (gunicorn) for multiple workers

### Environment Variables for Production
```env
DATABASE_URL=postgresql+asyncpg://username:password@neon-db-url:5432/todoapp
SECRET_KEY=production-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
DEBUG=False
```