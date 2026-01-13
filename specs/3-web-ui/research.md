# Research Document: Web UI for Todo Application

**Feature**: 3-web-ui
**Created**: 2025-12-27
**Author**: Claude Code

## API Endpoint Research

### Authentication API Endpoints
Based on the project structure and constitution requirements (Phase II: FastAPI, SQLModel, Neon PostgreSQL, Better Auth), the authentication endpoints will likely follow standard patterns:

- **Signup**: `POST /api/auth/register` or `/api/users`
- **Login**: `POST /api/auth/login`
- **Logout**: `POST /api/auth/logout` or `DELETE /api/auth/session`
- **User Profile**: `GET /api/auth/me` or `GET /api/users/me`

### Task Management API Endpoints
Based on the spec requirements and constitution technology stack, the task endpoints will follow REST conventions:

- **Get Tasks**: `GET /api/tasks?userId={id}`
- **Create Task**: `POST /api/tasks`
- **Update Task**: `PUT /api/tasks/{id}`
- **Delete Task**: `DELETE /api/tasks/{id}`

## Database Schema Research

### User Schema
Based on the spec and constitution Phase II technology stack (SQLModel, Neon PostgreSQL):

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Task Schema
Based on the spec and constitution Phase II technology stack:

```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  status BOOLEAN DEFAULT FALSE,
  category VARCHAR(100),
  priority INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Authentication Flow Research

### JWT Implementation
- **Token Storage**: localStorage (as specified in spec and constitution)
- **Token Refresh**: Likely handled by backend API
- **Token Expiration**: Standard JWT expiration (likely 24 hours)
- **Security**: Tokens will be included in Authorization header as `Bearer <token>`

### Session Management
- **Login**: User credentials → API → JWT token → localStorage
- **Session Check**: Check for token in localStorage on page load
- **Logout**: Remove token from localStorage and clear user state
- **Protected Routes**: Redirect to login if no valid token exists

## Glassmorphism Implementation Research

### Browser Support
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+ (as per spec NFR-004)
- **Fallback Strategy**: For browsers without `backdrop-filter` support:
  - Use solid backgrounds with reduced opacity (e.g., `bg-white/40` becomes `bg-gray-200`)
  - Maintain visual hierarchy with shadows and borders
  - Graceful degradation without losing core functionality

### Performance Considerations
- **Hardware Acceleration**: Use `transform` and `opacity` properties for animations
- **Layer Management**: Use `will-change` property for elements with frequent updates
- **Efficient Rendering**: Implement virtual scrolling for large task lists (100+ tasks)

## Environment Variables Research

### Required Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXT_PUBLIC_JWT_SECRET_KEY`: (Optional, for client-side verification)
- `NEXT_PUBLIC_APP_NAME`: Application name for display

## Deployment Strategy Research

### Next.js Deployment Options
- **Vercel**: Native Next.js platform, optimal performance
- **Netlify**: Good Next.js support with serverless functions
- **AWS Amplify**: Enterprise-grade deployment
- **GitHub Pages**: Static export option (limited functionality)

## Third-Party Libraries Research

### Recommended Libraries
- **React Hook Form**: For form validation and management
- **React Query / SWR**: For API caching and state management
- **Framer Motion**: For advanced animations (if needed beyond Tailwind)
- **React Hot Toast**: For toast notifications
- **Axios**: For HTTP requests with interceptors

## Accessibility Research

### WCAG 2.1 AA Compliance Points
- **Color Contrast**: Minimum 4.5:1 for text, 3:1 for UI components
- **Keyboard Navigation**: All interactive elements accessible via Tab
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Focus Indicators**: Visible focus states for keyboard users
- **Alt Text**: Descriptive alt text for images