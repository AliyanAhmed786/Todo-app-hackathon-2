# Frontend Architecture Overview

## Project Structure
```
frontend/
├── next-env.d.ts              # Next.js type definitions
├── package.json              # Project dependencies and scripts
├── postcss.config.js         # PostCSS configuration for Tailwind
├── public/                   # Static assets
├── src/                      # Source code
│   ├── app/                  # Next.js 13+ App Router pages
│   │   ├── dashboard/        # Dashboard pages and components
│   │   │   ├── create/page.tsx
│   │   │   ├── edit/[id]/page.tsx
│   │   │   ├── page.tsx
│   │   │   └── DashboardPageClient.tsx
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   ├── error.tsx
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── loading.tsx
│   │   ├── not-found.tsx
│   │   └── page.tsx
│   ├── components/           # Reusable UI components
│   │   ├── chatbot-ui/       # Chatbot UI components
│   │   │   ├── ChatBot.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── index.ts
│   │   │   └── types.ts
│   │   ├── __tests__/        # Component tests
│   │   │   └── TaskList.test.tsx
│   │   ├── DashboardPageClient.tsx
│   │   ├── DashboardStats.tsx
│   │   ├── DeleteConfirmationModal.tsx
│   │   ├── EditTaskForm.tsx
│   │   ├── ErrorBoundary.tsx
│   │   ├── HomePage.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── LoginForm.tsx
│   │   ├── LoginFormClient.tsx
│   │   ├── Modal.tsx
│   │   ├── Navbar.tsx
│   │   ├── ProtectedRoute.tsx
│   │   ├── SignupForm.tsx
│   │   ├── SignupFormClient.tsx
│   │   ├── TaskEditModal.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskList.tsx
│   │   ├── test.txt
│   │   └── ToastNotification.tsx
│   ├── lib/                  # Shared libraries
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── authClient.ts
│   ├── pages/                # Legacy Next.js pages (if needed)
│   │   └── homepage.tsx
│   ├── services/             # Service layer
│   │   ├── api.ts
│   │   └── api-client.ts
│   ├── styles/               # CSS styles
│   │   ├── accessibility.css
│   │   └── responsive.css
│   ├── tests/                # Test files
│   │   └── integration.test.ts
│   └── utils/                # Utility functions
│       ├── accessibility-audit.ts
│       ├── auth.ts
│       └── performance.ts
├── tailwind.config.ts        # Tailwind CSS configuration
└── tsconfig.json             # TypeScript configuration
```

## Core Components

### 1. App Router Pages (src/app/)
- **page.tsx**: Home page entry point
- **layout.tsx**: Root layout with global styles and providers
- **error.tsx**: Global error boundary component
- **loading.tsx**: Global loading state component
- **not-found.tsx**: 404 page component

### 2. Authentication Pages (src/app/{login,signup})
- **login/page.tsx**: Login page with form
- **signup/page.tsx**: Registration page with form
- **LoginFormClient.tsx**: Client-side login form with validation
- **SignupFormClient.tsx**: Client-side signup form with validation
- **ProtectedRoute.tsx**: Route protection wrapper for authenticated access

### 3. Dashboard Pages (src/app/dashboard/)
- **page.tsx**: Main dashboard page
- **create/page.tsx**: Task creation page
- **edit/[id]/page.tsx**: Task editing page with dynamic route
- **DashboardPageClient.tsx**: Client-side dashboard with state management
- **DashboardStats.tsx**: Dashboard statistics display component

### 4. Core Components (src/components/)
- **TaskList.tsx**: Display and manage tasks with filtering/search
- **TaskForm.tsx**: Form for creating new tasks
- **TaskEditModal.tsx**: Modal for editing existing tasks
- **EditTaskForm.tsx**: Form specifically for editing tasks
- **Modal.tsx**: Generic modal component
- **DeleteConfirmationModal.tsx**: Confirmation modal for deletions
- **Navbar.tsx**: Navigation bar with authentication status
- **LoadingSpinner.tsx**: Loading state indicator
- **ToastNotification.tsx**: Notification system for user feedback
- **ErrorBoundary.tsx**: Component-level error boundary

### 5. Chatbot UI (src/components/chatbot-ui/)
- **ChatBot.tsx**: Main chatbot component with open/close functionality
- **ChatWindow.tsx**: Chat interface window with message history
- **ChatInput.tsx**: Input field for sending messages
- **MessageBubble.tsx**: Individual message display component
- **types.ts**: TypeScript interfaces for chat messages
- **index.ts**: Export file for easy imports

### 6. Authentication Logic (src/lib/, src/utils/)
- **authClient.ts**: Client-side authentication utilities
- **auth.ts**: Authentication helper functions
- **api.ts** (in lib): Authentication API calls

### 7. API Services (src/services/)
- **api.ts**: Main API service with axios configuration
- **api-client.ts**: Client-side API wrapper

### 8. Styling (src/styles/, tailwind.config.ts)
- **globals.css**: Global CSS styles
- **accessibility.css**: Accessibility-focused styles
- **responsive.css**: Responsive design utilities
- **tailwind.config.ts**: Tailwind CSS customization with glassmorphism and coral theme

### 9. Utilities (src/utils/)
- **performance.ts**: Performance monitoring utilities
- **accessibility-audit.ts**: Accessibility checking utilities
- **auth.ts**: Authentication utility functions

## Technologies Used

### Framework & Libraries
- **Next.js 13+**: React framework with App Router
- **React 18**: UI library with concurrent features
- **TypeScript**: Static type checking
- **Tailwind CSS**: Utility-first CSS framework with glassmorphism styling
- **Lucide React**: Icon library
- **Better Auth**: Authentication library
- **Axios**: HTTP client for API requests
- **Socket.io-client**: Real-time communication

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Glassmorphism Design**: Frosted glass UI effect
- **Coral Accent Colors**: Primary color scheme
- **Responsive Design**: Mobile-first approach

## Key Features

### 1. Authentication System
- User registration with validation
- Secure login/logout functionality
- Protected routes and components
- Session management

### 2. Task Management
- Create, read, update, delete operations
- Task filtering (all, pending, completed)
- Search functionality
- Priority levels (High, Medium, Low)
- Due date tracking
- Real-time updates

### 3. Dashboard Analytics
- Task statistics visualization
- Progress tracking
- Performance metrics

### 4. Real-time Features
- WebSocket integration for live updates
- Real-time task synchronization

### 5. Accessibility Features
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- WCAG compliance considerations

### 6. Responsive Design
- Mobile-first approach
- Tablet and desktop optimized layouts
- Touch-friendly interfaces

## UI/UX Design

### Visual Style
- **Glassmorphism**: Frosted glass effect with transparency
- **Coral Accents**: Consistent coral color scheme for branding
- **Gradient Effects**: Subtle gradients for depth
- **Blur Effects**: Backdrop blur for modern glass effect
- **Smooth Transitions**: Animated interactions

### Component Design
- **Reusable Components**: Modular, composable UI elements
- **Consistent Styling**: Unified design language throughout
- **Interactive Elements**: Hover, focus, and active states
- **Feedback Mechanisms**: Loading states, notifications, confirmations

## State Management

### Client-Side State
- React hooks (useState, useEffect, useContext)
- Local component state for forms and UI interactions
- Client-side caching for improved performance

### Data Flow
- API calls through centralized service layer
- Error handling and loading states
- Optimistic updates for better UX
- Real-time synchronization via WebSockets

## Routing

### Next.js App Router
- **Home**: `/` - Landing page
- **Login**: `/login` - Authentication page
- **Signup**: `/signup` - Registration page
- **Dashboard**: `/dashboard` - Main application view
- **Create Task**: `/dashboard/create` - Task creation form
- **Edit Task**: `/dashboard/edit/[id]` - Task editing form

### Protected Routes
- Authentication checks on protected pages
- Redirect handling for unauthorized access
- Session persistence

## API Integration

### Service Layer
- Centralized API endpoints
- Request/response interceptors
- Error handling and retry logic
- Authentication token management

### Data Models
- Consistent data structures between frontend and backend
- TypeScript interfaces for type safety
- Validation before API calls

## Testing

### Component Testing
- Jest and React Testing Library for unit tests
- Integration tests for component interactions
- Mock services for API calls

### End-to-End Testing
- Integration tests covering user flows
- API integration testing

## Performance Optimization

### Code Splitting
- Dynamic imports for route-based splitting
- Component lazy loading
- Bundle size optimization

### Caching
- API response caching
- Component memoization
- Image optimization

## Security Considerations
- Input sanitization
- Secure authentication flow
- CSRF protection
- Proper error handling without information leakage
- Secure API communication