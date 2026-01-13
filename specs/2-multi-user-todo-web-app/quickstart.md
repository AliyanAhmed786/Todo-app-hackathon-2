# Quickstart Guide: Multi-User Web Todo Application (Phase II)

**Feature**: 2-multi-user-todo-web-app
**Date**: 2025-12-23
**Version**: 1.0.0

## Overview

This guide provides instructions for setting up and running the multi-user web todo application. The application consists of a Next.js frontend and a FastAPI backend with Neon PostgreSQL database.

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL client tools
- Neon PostgreSQL account
- Git

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup (FastAPI)

#### Navigate to backend directory
```bash
cd backend
```

#### Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies
```bash
pip install fastapi uvicorn sqlmodel psycopg2-binary python-multipart python-jose[cryptography] passlib[bcrypt] better-exceptions
```

#### Set environment variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://<username>:<password>@<neon-project>.us-east-1.aws.neon.tech/<database-name>?sslmode=require
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days in minutes
NEON_DATABASE_URL=<your-neon-database-url>
```

#### Initialize database
```bash
# Run database migrations or create tables
python -c "
from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.task import Task
engine = create_engine('postgresql://<username>:<password>@<neon-project>.us-east-1.aws.neon.tech/<database-name>?sslmode=require')
SQLModel.metadata.create_all(engine)
"
```

#### Run the backend server
```bash
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup (Next.js)

#### Navigate to frontend directory
```bash
cd frontend  # or cd todo-web if that's where Next.js app is
```

#### Install dependencies
```bash
npm install
```

#### Set environment variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=<your-jwt-secret>
```

#### Run the development server
```bash
npm run dev
```

## Running the Application

1. Start the backend server: `uvicorn src.main:app --reload --port 8000`
2. In a new terminal, start the frontend: `npm run dev`
3. Access the application at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `POST /auth/refresh` - Refresh JWT token

### Tasks
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `password_hash` (String)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Tasks Table
- `id` (Integer, Primary Key, Auto-increment)
- `user_id` (UUID, Foreign Key)
- `title` (String, 1-200 chars)
- `description` (String, 0-1000 chars)
- `status` (Boolean, default false)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Backend Deployment
1. Deploy to a cloud provider (AWS, GCP, Azure, or Vercel/Render)
2. Set environment variables in deployment environment
3. Ensure database connection is properly configured

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or similar hosting service
3. Configure environment variables for production

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Verify Neon PostgreSQL credentials and connection string
2. **Authentication Issues**: Check JWT secret keys match between frontend and backend
3. **CORS Errors**: Ensure backend allows requests from frontend origin
4. **Environment Variables**: Verify all required environment variables are set

### Debugging Tips

1. Check the API documentation at `/docs` and `/redoc` endpoints
2. Enable debug logging in both frontend and backend
3. Verify database schema matches the defined models
4. Ensure Better Auth is properly configured

## Next Steps

1. Complete the full task breakdown using `/sp.tasks`
2. Implement backend API endpoints
3. Create frontend components
4. Integrate authentication
5. Add comprehensive tests
6. Deploy to staging environment