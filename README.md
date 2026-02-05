---
title: Todo Backend API
emoji: ✅
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Multi-User Web Todo Application (Phase II)
... (rest of your text)



# Multi-User Web Todo Application (Phase II)

A multi-user web todo application with authentication, task management, and responsive UI built with Next.js, FastAPI, and Neon PostgreSQL.

## Overview

This application provides a complete todo management system with:
- User authentication (signup/login with JWT)
- Task CRUD operations (create, read, update, delete)
- User isolation (users only see their own tasks)
- Responsive design for all device sizes
- Secure API with rate limiting

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth JWT
- **ORM**: SQLModel

## Project Structure

```
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── auth.py
│   │   └── tasks.py
│   └── main.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   ├── LoginForm.tsx
│   │   ├── SignupForm.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskList.tsx
│   │   ├── Navbar.tsx
│   │   └── ProtectedRoute.tsx
│   ├── pages/
│   │   ├── login.tsx
│   │   ├── signup.tsx
│   │   ├── dashboard.tsx
│   │   └── task/[id].tsx
│   ├── services/
│   │   └── api.ts
│   └── utils/
│       └── auth.ts
└── tests/
    ├── unit/
    └── integration/
```

## Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL client tools
- Neon PostgreSQL account

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn sqlmodel psycopg2-binary python-multipart python-jose[cryptography] passlib[bcrypt] better-exceptions
```

4. Set environment variables by creating a `.env` file:
```env
DATABASE_URL=postgresql://<username>:<password>@<neon-project>.us-east-1.aws.neon.tech/<database-name>?sslmode=require
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days in minutes
NEON_DATABASE_URL=<your-neon-database-url>
```

5. Run the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set environment variables by creating a `.env.local` file:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=<your-jwt-secret>
```

4. Run the development server:
```bash
npm run dev
```

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

## Running the Application

1. Start the backend server: `uvicorn src.main:app --reload --port 8000`
2. In a new terminal, start the frontend: `npm run dev`
3. Access the application at `http://localhost:3000`

## Development

For development, both backend and frontend can be run in parallel using the setup instructions above. The API is available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

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

## Frontend UI Improvements

This application includes comprehensive UI/UX enhancements:

### Enhanced Authentication Forms
- Password visibility toggle with eye/eye-slash icons
- Real-time password strength validation
- Form validation with visual feedback
- ARIA attributes for accessibility
- Loading states during authentication
- Error handling with suggested solutions

### Improved Dashboard UI
- Dashboard statistics cards showing total, completed, and pending tasks
- Task cards with color-coded priority indicators (P1=Red, P2=Yellow, P3=Green)
- Additional visual indicators for color blindness accessibility
- Responsive grid layout (1 column mobile, 2 tablet, 3 desktop)
- Real-time dashboard statistics from API

### Enhanced Task Management UI
- Task form with real-time validation and character counts
- Visual feedback animations (300ms transitions, strikethrough, opacity changes)
- Priority selection with visual indicators
- Optimistic locking with version numbers for concurrent modifications
- Conflict detection and resolution UI

### Improved Homepage and Navigation
- Engaging homepage with clear value proposition
- Consistent header design across all pages
- Responsive navigation with mobile menu
- Call-to-action buttons

### Accessibility and Loading Improvements
- WCAG 2.1 AA compliant contrast ratios (4.5:1 minimum)
- Focus visibility for keyboard navigation (WCAG 2.4.7)
- Proper name, role, value for UI components (WCAG 4.1.2)
- Loading indicators with spinners
- Toast notifications for user feedback
- Error messages with suggested solutions

### Performance Optimizations
- Page load time under 2 seconds
- 60fps UI responsiveness during interactions
- Image preloading
- Debounce and throttle utilities
- Performance measurement tools
- Simple caching mechanism

## Security Features

- JWT-based authentication with Better Auth
- User isolation (users can only access their own tasks)
- Rate limiting (100 requests/hour per user)
- Input validation and sanitization
- Secure password hashing
- CORS configuration