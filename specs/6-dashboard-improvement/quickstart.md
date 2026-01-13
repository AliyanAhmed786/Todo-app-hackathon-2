# Quickstart Guide: Dashboard Improvement

**Feature**: 6-dashboard-improvement | **Date**: 2026-01-03

## Prerequisites

- Node.js 18+ with npm/yarn
- Python 3.13+
- PostgreSQL database (or Neon PostgreSQL for cloud)
- Git

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd todo-app
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todoapp
SECRET_KEY=your-super-secret-key-here-keep-it-safe-and-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### Database Setup
```bash
# Run database migrations
cd backend
python -m database.migrations
```

#### Start Backend Server
```bash
cd backend
python main.py
```
Backend will start on `http://localhost:8000`

### 3. Frontend Setup

#### Install Node Dependencies
```bash
cd frontend
npm install
# or
yarn install
```

#### Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

#### Start Frontend Development Server
```bash
cd frontend
npm run dev
# or
yarn dev
```
Frontend will start on `http://localhost:3000`

## Key Endpoints

### Backend API
- Health Check: `GET http://localhost:8000/health`
- Dashboard Stats: `GET http://localhost:8000/api/{userId}/dashboard/stats`
- Tasks: `GET/POST/PUT/DELETE http://localhost:8000/api/{userId}/tasks`

### WebSocket Endpoint
- Real-time updates: `ws://localhost:8000/ws/dashboard/{userId}`

## Feature-Specific Setup

### 1. Dashboard Statistics Implementation
The dashboard statistics endpoint calculates and returns:
- Total tasks count
- Completed tasks count
- Pending tasks count

### 2. Real-Time Updates with WebSocket
To enable real-time dashboard updates:
1. Connect to WebSocket endpoint with user authentication token
2. Subscribe to dashboard updates using the `subscribe_dashboard` message type
3. Handle incoming `dashboard_update` messages to refresh UI

### 3. Task Editing Popup
The enhanced task editing popup includes:
- Priority indicators with icons and text labels
- Smooth animations for open/close transitions
- Responsive sizing (80% of viewport on mobile)
- Form validation with visual indicators

### 4. Token Refresh Mechanism
The system automatically refreshes JWT tokens 5 minutes before expiration using:
- A background timer that checks token expiration
- Silent API call to `/auth/refresh` endpoint
- Automatic token replacement in local storage

## Testing the Implementation

### Frontend Tests
```bash
cd frontend
npm test
# or
yarn test
```

### Backend Tests
```bash
cd backend
pytest
```

## Common Issues and Solutions

### 1. WebSocket Connection Issues
- Ensure the backend server is running
- Check that the JWT token is properly passed as a query parameter
- Verify that CORS settings allow WebSocket connections

### 2. Token Refresh Not Working
- Verify that the ACCESS_TOKEN_EXPIRE_MINUTES setting is properly configured
- Check that the frontend timer is set to refresh 5 minutes before expiration
- Ensure the `/auth/refresh` endpoint is accessible

### 3. Dashboard Statistics Not Updating
- Verify WebSocket connection is established
- Check that the proper event listeners are set up
- Ensure the backend is broadcasting updates on task changes

## Next Steps

1. Run the task generation command: `sp.tasks` to generate implementation tasks
2. Review the generated tasks and begin implementation
3. Test the dashboard improvement features
4. Iterate based on user feedback