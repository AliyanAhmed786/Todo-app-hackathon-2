// API service for communicating with the backend
import axios, { AxiosResponse } from 'axios';
import { authClient } from '../lib/authClient';
import { redirectToLogin, isAuthError } from '../utils/auth';

// Base URL for the API (can be configured via environment variables)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds to accommodate Neon PostgreSQL cold starts and authentication
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable credentials (cookies) for authentication
});

// Request interceptor - no need to add auth headers, cookies are sent automatically
api.interceptors.request.use(
  (config) => {
    // Cookies (including better-auth.session_token) are automatically sent with withCredentials: true
    // No manual token handling needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle authentication errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle authentication errors (401 Unauthorized)
    if (isAuthError(error)) {
      // Redirect to login and clear cookies
      if (typeof window !== 'undefined') {
        redirectToLogin();
      }
    }
    return Promise.reject(error);
  }
);


// Check if running in browser environment
const isBrowser = (): boolean => {
  return typeof window !== 'undefined';
};


// Authentication API functions
export const authAPI = {
  // Register a new user
  register: async (name: string, email: string, password: string): Promise<AxiosResponse> => {
    return api.post('/api/auth/signup', { name, email, password });
  },

  // Login user
  login: async (email: string, password: string): Promise<AxiosResponse> => {
    return api.post('/api/auth/login', { email, password });
  },

  // Refresh access token using refresh token
  refresh: async (refreshToken: string): Promise<AxiosResponse> => {
    return api.post('/api/auth/refresh', { refresh_token: refreshToken });
  },

  // Logout user (client-side only)
  logout: async (): Promise<AxiosResponse> => {
    return api.post('/api/auth/logout');
  },
};

// Get user ID from Better Auth session
const getUserId = async (): Promise<string | null> => {
  try {
    const session = await authClient.getSession();
    if (!session || !session.user) {
      // User is not authenticated
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
      return null;
    }
    const userId = session?.user?.id;
    return userId || null;
  } catch (error) {
    console.error('Error getting user ID:', error);
    // Redirect to login on error
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    return null;
  }
};

// Dashboard API functions
export const dashboardAPI = {
  // Get dashboard statistics
  getStats: async (): Promise<AxiosResponse> => {
    return api.get('/api/dashboard/stats');
  },
};

// Task API functions
export const taskAPI = {
  // Get user's tasks
  getTasks: async (): Promise<AxiosResponse> => {
    return api.get('/api/tasks/');
  },

  // Create a new task
  createTask: async (taskData: {
    title: string;
    description?: string;
    category?: string;
    priority?: number;
    version?: number;
  }): Promise<AxiosResponse> => {
    return api.post('/api/tasks/', taskData);
  },

  // Get a specific task
  getTask: async (taskId: number): Promise<AxiosResponse> => {
    return api.get(`/api/tasks/${taskId}`);
  },

  // Update a task with optimistic locking
  updateTask: async (taskId: number, taskData: {
    title?: string;
    description?: string;
    status?: boolean;
    category?: string;
    priority?: number;
    version?: number;
  }): Promise<AxiosResponse> => {
    return api.put(`/api/tasks/${taskId}`, taskData);
  },

  // Delete a task
  deleteTask: async (taskId: number): Promise<AxiosResponse> => {
    // Validate task ID
    if (!Number.isInteger(taskId) || taskId <= 0) {
      throw new Error(`Invalid task ID: ${taskId}. Task ID must be a positive integer.`);
    }
    return api.delete(`/api/tasks/${taskId}`);
  },
};

export default api;
