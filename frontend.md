# Frontend Architecture and Implementation

## Overview
The frontend is a Next.js application that provides a modern user interface for the Todo application. It features a glassmorphic UI design with responsive components and real-time updates.

## Technology Stack
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom glassmorphic design
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **State Management**: React hooks (useState, useEffect, etc.)

## Project Structure
```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   └── dashboard/       # Dashboard routes and pages
│   ├── components/          # Reusable React components
│   ├── services/            # API services and client utilities
│   └── utils/               # Utility functions
├── public/                  # Static assets
└── package.json             # Dependencies and scripts
```

## Key Components

### Dashboard Components
- `DashboardPageClient.tsx` - Main dashboard client component with stats and task management
- `TaskList.tsx` - Displays and manages tasks with filtering and search
- `TaskForm.tsx` - Form for creating and updating tasks
- `TaskEditModal.tsx` - Modal for editing tasks
- `EditTaskForm.tsx` - Alternative form for task editing

### Authentication Components
- `LoginForm.tsx` - User login form
- `SignupForm.tsx` - User registration form
- `LoginFormClient.tsx` - Client-side login component
- `SignupFormClient.tsx` - Client-side signup component

### UI Components
- `Modal.tsx` - Reusable modal component
- `ToastNotification.tsx` - Notification system
- `ErrorBoundary.tsx` - Error boundary component

## API Services

### Primary API Service
- `services/api.ts` - Main API service with:
  - `authAPI` - Authentication endpoints
  - `dashboardAPI` - Dashboard statistics
  - `taskAPI` - Task management endpoints

### Client-Side API Service
- `services/api-client.ts` - Client-side API service for App Router components

## API Endpoints Used

### Task Management
- `GET /api/tasks` - Retrieve user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/refresh` - Token refresh

## Key Features

### Glassmorphic Design
- Modern glass-like UI elements with backdrop blur
- Gradient backgrounds and subtle shadows
- Responsive design for all screen sizes

### Task Management
- Create, read, update, delete (CRUD) operations
- Task filtering (all, pending, completed)
- Search functionality
- Optimistic updates for instant UI feedback
- Priority levels (High, Medium, Low)
- Due dates and categories

### Dashboard
- Statistics display (total, completed, pending tasks)
- Progress indicators
- Real-time updates

### Authentication
- JWT-based authentication
- Token storage in localStorage
- Protected routes and components

## State Management
- Component-level state with useState
- Side effects with useEffect
- Form state management
- Task list state with optimistic updates
- Authentication state

## Styling Approach
- Tailwind CSS utility classes
- Custom CSS for glassmorphic effects
- Responsive design with mobile-first approach
- Consistent color scheme and typography
- Accessible UI components

## Error Handling
- Component error boundaries
- Form validation
- API error handling
- Network error detection
- User-friendly error messages

## Security Considerations
- Authorization headers for API calls
- Token-based authentication
- Input validation
- Secure token storage (with improvements needed)

## Performance Optimizations
- Client-side rendering where appropriate
- Efficient state updates
- Component memoization (where applicable)
- Optimized API calls

## Environment Configuration
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL
- Default: `http://localhost:8000`

## Development Notes
- The frontend is designed to work with a backend API
- Authentication tokens are stored in localStorage (for development)
- API calls are made using axios with interceptors
- Components are designed to be reusable and modular