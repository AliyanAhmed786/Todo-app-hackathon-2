# Data Model: Web UI for Todo Application

**Feature**: 3-web-ui
**Created**: 2025-12-27
**Author**: Claude Code

## Entity Models

### User Entity
```typescript
interface User {
  id: number;           // Unique identifier, auto-increment
  email: string;        // Unique email address, required
  name?: string;        // Optional user name
  created_at: string;   // ISO timestamp when user was created
}
```

**Validation Rules:**
- `id`: integer, unique, auto-increment
- `email`: string, unique, required, valid email format
- `name`: string, optional, max 255 characters
- `created_at`: ISO 8601 timestamp

### Task Entity
```typescript
interface Task {
  id: number;           // Unique identifier, auto-increment, never recycled
  user_id: number;      // Foreign key to User
  title: string;        // Task title
  description?: string; // Optional task description
  status: boolean;      // Completion status, default: false
  category?: string;    // Task category, optional
  priority?: number;    // Priority level, optional
  created_at: string;   // ISO timestamp when task was created
  updated_at: string;   // ISO timestamp when task was last updated
}
```

**Validation Rules:**
- `id`: integer, unique, auto-increment, never recycles (per spec FR-009)
- `user_id`: integer, foreign key to User, required
- `title`: string, 1-200 characters, required, cannot be only whitespace (per spec FR-011)
- `description`: string, 0-1000 characters, optional (per spec FR-012)
- `status`: boolean, default: false, indicates completion status (per spec FR-010)
- `category`: string, optional, for organization
- `priority`: integer, optional, for prioritization
- `created_at`: ISO 8601 timestamp
- `updated_at`: ISO 8601 timestamp

### TaskCategory Entity
```typescript
interface TaskCategory {
  name: string;         // Category name
  predefined: boolean;  // Whether this is a predefined category
}
```

**Validation Rules:**
- `name`: string, required, one of "Vital Task", "My Task", "Completed" or custom
- `predefined`: boolean, indicates if it's a system-defined category

## State Models

### Authentication State
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  authenticated: boolean;
}
```

### Task Management State
```typescript
interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  filteredTasks: Task[];
  searchTerm: string;
}
```

### UI State
```typescript
interface UIState {
  modalOpen: boolean;
  modalType: 'add' | 'edit' | 'delete' | null;
  selectedTask: Task | null;
  toast: {
    message: string;
    type: 'success' | 'error' | 'info';
    visible: boolean;
  };
}
```

## API Response Models

### Authentication Responses
```typescript
interface LoginResponse {
  user: User;
  token: string;
}

interface SignupResponse {
  user: User;
  token: string;
}

interface LogoutResponse {
  success: boolean;
}
```

### Task API Responses
```typescript
interface GetTasksResponse {
  tasks: Task[];
}

interface CreateTaskResponse {
  task: Task;
}

interface UpdateTaskResponse {
  task: Task;
}

interface DeleteTaskResponse {
  success: boolean;
}
```

## Form Models

### Signup Form
```typescript
interface SignupForm {
  name: string;
  email: string;
  password: string;
}
```

### Login Form
```typescript
interface LoginForm {
  email: string;
  password: string;
}
```

### Task Form
```typescript
interface TaskForm {
  title: string;
  description?: string;
  category?: string;
  priority?: number;
}
```

## Validation Models

### Validation Rules
```typescript
interface ValidationRules {
  title: {
    required: true;
    minLength: 1;
    maxLength: 200;
    pattern: '^[^\\s]+$'; // Not only whitespace
  };
  description: {
    required: false;
    maxLength: 1000;
  };
  email: {
    required: true;
    pattern: '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'; // Basic email pattern
  };
  password: {
    required: true;
    minLength: 8;
  };
}
```

## Error Models

### API Error Response
```typescript
interface APIErrorResponse {
  error: string;
  message: string;
  statusCode: number;
}
```

### Validation Error Response
```typescript
interface ValidationErrorResponse {
  field: string;
  message: string;
  code: string;
}
```