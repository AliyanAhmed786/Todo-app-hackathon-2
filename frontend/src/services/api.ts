// API service for communicating with the backend
import axios, { AxiosResponse } from 'axios';
import { authClient } from '../lib/authClient';
import { redirectToLogin, isAuthError, isValidSession } from '../utils/auth';

// Base URL for the API (can be configured via environment variables)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000, // 90 seconds to accommodate multi-turn workflows (list_tasks -> update_task) taking 40-60 seconds
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Required for Better Auth session cookies
});

// Request interceptor to log requests
api.interceptors.request.use(
  async (config) => {
    // Log the request for debugging
    console.debug('Making API request:', config.method?.toUpperCase(), config.url, {
      hasBetterAuthCookie: document.cookie.includes('better-auth.session_token')
    });

    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle authentication errors
api.interceptors.response.use(
  (response) => {
    // Log successful responses for debugging
    console.debug('API response received:', response.config.method?.toUpperCase(), response.config.url, response.status);
    return response;
  },
  (error) => {
    // Log error responses for debugging
    console.error('API error occurred:', {
      method: error.config?.method?.toUpperCase(),
      url: error.config?.url,
      status: error.response?.status,
      message: error.message,
      data: error.response?.data
    });

    // Handle authentication errors (401 Unauthorized, 403 Forbidden)
    if (isAuthError(error)) {
      console.error('Authentication error occurred:', error.response?.status, error.response?.data);
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
    const response = await api.post('/api/auth/logout');
    // Clear JWT token from localStorage
    localStorage.removeItem('access_token');
    return response;
  },
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
  getTask: async (taskId: string | number): Promise<AxiosResponse> => {
    return api.get(`/api/tasks/${taskId}`);
  },

  // Update a task with optimistic locking
  updateTask: async (taskId: string | number, taskData: {
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
  deleteTask: async (taskId: string | number): Promise<AxiosResponse> => {
    // Validate task ID
    if (typeof taskId === 'number' && (!Number.isInteger(taskId) || taskId <= 0)) {
      throw new Error(`Invalid task ID: ${taskId}. Task ID must be a positive integer.`);
    }
    if (typeof taskId === 'string' && (!/^\d+$/.test(taskId) || parseInt(taskId) <= 0)) {
      throw new Error(`Invalid task ID: ${taskId}. Task ID must be a positive integer.`);
    }
    return api.delete(`/api/tasks/${taskId}`);
  },
};

// Chat API functions
export const chatAPI = {
  // Send a message in a conversation
  sendMessage: async (userId: string, messageData: { message: string; conversation_id?: string }): Promise<AxiosResponse> => {
    return api.post(`/api/chat/${userId}/conversation`, messageData);
  },

  // Get conversation history
  getConversationHistory: async (userId: string, conversationId: string): Promise<AxiosResponse> => {
    return api.get(`/api/chat/${userId}/conversation/${conversationId}`);
  },

  // Delete a conversation
  deleteConversation: async (userId: string, conversationId: string): Promise<AxiosResponse> => {
    return api.delete(`/api/chat/${userId}/conversation/${conversationId}`);
  },
};
export default api;



