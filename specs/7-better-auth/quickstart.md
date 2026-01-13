# Quickstart Guide: Better Auth Integration

## Prerequisites

- Node.js 18+ for frontend
- Python 3.13+ for backend
- Neon PostgreSQL database instance
- Better Auth client library installed in frontend

## Backend Setup

### 1. Install Better Auth Server Dependencies

```bash
# Add to backend/requirements.txt
better-auth-server==1.0.0  # Use actual Better Auth server package
```

### 2. Configure Better Auth Server

Create `backend/auth/better_auth_config.py`:

```python
from better_auth import auth
from config import settings

# Initialize Better Auth with Neon DB integration
better_auth = auth(
    secret=settings.better_auth_secret,
    database_url=settings.database_url,
    # Additional configuration options
    session: {
        # Session configuration
        cookie_name: "better-auth.session_token",
        cookie_options: {
            http_only: True,
            secure: False,  # Set to True in production with HTTPS
            same_site: "lax",
        }
    }
)
```

### 3. Update Authentication Middleware

Replace existing JWT middleware with Better Auth database validation:

```python
# backend/middleware/auth.py
from fastapi import HTTPException, Request
from sqlmodel import select
from models.session import Session
from database.session import get_db_session

async def validate_session_from_db(request: Request):
    # Get session token from HTTP-only cookie
    session_token = request.cookies.get("better-auth.session_token")

    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Query session from database
    async for db in get_db_session():
        result = await db.exec(
            select(Session).where(
                Session.token == session_token,
                Session.expires_at > datetime.utcnow()
            )
        )
        session = result.first()

        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")

        return session.user_id
```

## Frontend Setup

### 1. Update Better Auth Client Configuration

```typescript
// frontend/src/lib/authClient.ts
import { createAuthClient } from 'better-auth';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
  fetchOptions: {
    credentials: 'include',  // Include cookies in requests
  },
});
```

### 2. Update API Calls to Use HTTP-only Cookies

All API calls should automatically include HTTP-only cookies when `credentials: 'include'` is set.

## Database Migration

### 1. Create Better Auth Tables

Run the following SQL to create required tables:

```sql
-- Session table
CREATE TABLE "session" (
  "id" TEXT PRIMARY KEY,
  "token" TEXT NOT NULL UNIQUE,
  "user_id" TEXT NOT NULL,
  "expires_at" TIMESTAMP NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Account table
CREATE TABLE "account" (
  "id" TEXT PRIMARY KEY,
  "user_id" TEXT NOT NULL,
  "provider_id" TEXT NOT NULL,
  "provider_account_id" TEXT NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User table
CREATE TABLE "user" (
  "id" TEXT PRIMARY KEY,
  "email" TEXT NOT NULL UNIQUE,
  "email_verified" BOOLEAN DEFAULT FALSE,
  "name" TEXT,
  "image" TEXT,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verification table
CREATE TABLE "verification" (
  "id" TEXT PRIMARY KEY,
  "identifier" TEXT NOT NULL,
  "value" TEXT NOT NULL,
  "expires_at" TIMESTAMP NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Foreign key and cascade constraints
ALTER TABLE "session" ADD FOREIGN KEY ("user_id") REFERENCES "user"("id") ON DELETE CASCADE;
ALTER TABLE "account" ADD FOREIGN KEY ("user_id") REFERENCES "user"("id") ON DELETE CASCADE;
ALTER TABLE "task" ADD FOREIGN KEY ("user_id") REFERENCES "user"("id") ON DELETE CASCADE;
```

## Environment Variables

### Backend (.env)
```env
# Better Auth configuration
BETTER_AUTH_SECRET=your-better-auth-secret-key-here-keep-it-safe-and-long
BETTER_AUTH_URL=http://localhost:8000

# Database configuration (Neon)
DATABASE_URL=postgresql+asyncpg://username:password@ep-your-neon-endpoint.region.neon.tech/dbname
```

### Frontend (.env.local)
```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

## Testing Authentication Flow

1. Navigate to the registration page and create a new account
2. Verify that the session is stored in an HTTP-only cookie
3. Access protected routes to ensure authentication works
4. Test logout functionality to ensure session is properly cleared
5. Verify that account deletion triggers cascade deletion of related data