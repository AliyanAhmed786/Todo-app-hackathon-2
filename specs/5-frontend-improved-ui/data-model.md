# Data Model: Frontend UI Improvements

## UI Component Entities

### Task UI Component
- **name**: TaskCard
- **fields**:
  - id: string (unique identifier)
  - title: string (task title)
  - description: string (task description)
  - priority: 'P1' | 'P2' | 'P3' (priority level)
  - status: 'pending' | 'completed' (completion status)
  - createdAt: Date (creation timestamp)
  - updatedAt: Date (last update timestamp)
- **relationships**: None (represents frontend display of backend Task entity)
- **validation rules**:
  - title: required, max 255 characters
  - priority: must be one of 'P1', 'P2', 'P3'
  - status: must be one of 'pending', 'completed'

### User Feedback UI Component
- **name**: ToastNotification
- **fields**:
  - id: string (unique identifier)
  - type: 'success' | 'error' | 'warning' | 'info' (notification type)
  - message: string (notification message)
  - duration: number (display duration in ms)
  - position: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' (position on screen)
- **relationships**: None (standalone UI component)
- **validation rules**:
  - message: required, max 500 characters
  - type: must be one of specified values

### Authentication Form UI Component
- **name**: AuthFormFields
- **fields**:
  - showPassword: boolean (password visibility state)
  - passwordStrength: number (0-100 scale)
  - validationErrors: object (field-specific validation errors)
  - loading: boolean (form submission state)
- **relationships**: None (form state management)
- **validation rules**: None (state management component)

### Dashboard Stats UI Component
- **name**: DashboardStats
- **fields**:
  - totalTasks: number (total task count)
  - completedTasks: number (completed task count)
  - pendingTasks: number (pending task count)
  - progressPercentage: number (completion percentage)
- **relationships**: None (calculated from task data)
- **validation rules**:
  - all counts: non-negative integers
  - progressPercentage: between 0-100

## State Transitions

### Task Card State Transitions
- **Initial State**: Display task information with action buttons
- **Edit State**: Form with task details for modification
- **Loading State**: During API operations
- **Error State**: When API operations fail

### Authentication Form State Transitions
- **Initial State**: Empty form fields
- **Validation State**: Real-time validation feedback
- **Password Visibility State**: Toggle between showing/hiding password
- **Loading State**: During form submission
- **Success/Error State**: After form submission

## UI Component Relationships

```
DashboardStats
    ↓ (displays)
TaskCard[]

ToastNotification
    ↑ (triggers)
Any UI Component

AuthFormFields
    ↔ (manages)
LoginFormClient/SignupFormClient
```