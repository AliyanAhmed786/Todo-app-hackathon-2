# Quickstart Guide: Web UI for Todo Application

**Feature**: 3-web-ui
**Created**: 2025-12-27
**Author**: Claude Code

## Prerequisites

Before starting development, ensure you have the following installed:

- Node.js 18+ (LTS recommended)
- npm 8+ or yarn 1.22+
- Git
- A code editor (VS Code recommended)

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Navigate to the Web UI Directory

```bash
cd frontend  # or wherever the Next.js app will be located
```

### 3. Install Dependencies

```bash
npm install
# or
yarn install
```

### 4. Environment Configuration

Create a `.env.local` file in the root of your Next.js project:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/v1
# Add other environment variables as needed
```

## Development Server

### 1. Start the Development Server

```bash
npm run dev
# or
yarn dev
```

### 2. Access the Application

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

The project follows this structure:

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   ├── pages/              # Next.js pages
│   │   ├── index.tsx       # Homepage
│   │   ├── signup.tsx      # Signup page
│   │   ├── login.tsx       # Login page
│   │   └── dashboard.tsx   # Dashboard page
│   ├── services/           # API services and authentication
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Utility functions
│   ├── styles/             # Global styles and theme
│   └── types/              # TypeScript type definitions
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

## Key Features Implementation

### 1. Glassmorphic Design System

The application implements a premium glassmorphic design system:

- Use `backdrop-blur-2xl bg-white/40` for glassmorphic cards
- Apply `border border-white/60` for glassmorphic borders
- Use `bg-gradient-to-r from-coral-600 to-coral-700` for primary gradients
- Implement hover effects: `hover:-translate-y-2 hover:shadow-2xl hover:shadow-coral-500/20`

### 2. Authentication Flow

The authentication system includes:

- Signup page with glassmorphic form panel
- Login page with glassmorphic form panel
- Protected routes for dashboard
- JWT token management in localStorage

### 3. Task Management

The dashboard includes:

- Glassmorphic task cards with hover effects
- Task CRUD operations
- Search and filtering functionality
- Category organization

## API Integration

The application integrates with the backend API using:

- axios or fetch for HTTP requests
- JWT tokens for authentication
- TypeScript interfaces for type safety

Example API call:

```typescript
// In services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
});

// Add JWT token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## Running Tests

### Unit Tests

```bash
npm run test
# or
yarn test
```

### End-to-End Tests

```bash
npm run test:e2e
# or
yarn test:e2e
```

## Building for Production

### 1. Build the Application

```bash
npm run build
# or
yarn build
```

### 2. Start Production Server

```bash
npm start
# or
yarn start
```

## Environment Variables

The following environment variables are required:

- `NEXT_PUBLIC_API_BASE_URL`: The base URL for the backend API
- `NEXT_PUBLIC_JWT_SECRET_KEY`: (Optional) For client-side JWT verification
- `NEXT_PUBLIC_APP_NAME`: Application name for display

## Troubleshooting

### Common Issues

1. **Glassmorphism not rendering**:
   - Check browser compatibility
   - Ensure Tailwind CSS is properly configured
   - Verify backdrop-filter support

2. **Authentication issues**:
   - Verify JWT token is stored in localStorage
   - Check API endpoint configuration
   - Ensure proper headers are sent with requests

3. **API connection errors**:
   - Verify backend server is running
   - Check API URL configuration
   - Confirm network connectivity

### Development Tips

- Use the browser's developer tools to inspect glassmorphic effects
- Monitor network requests in the Network tab
- Use React Developer Tools for component debugging