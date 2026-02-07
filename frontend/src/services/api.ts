// API service for communicating with the backend
import axios, { AxiosResponse } from 'axios';
import { authClient } from '../lib/authClient';
import { redirectToLogin, isAuthError, isValidSession } from '../utils/auth';

// Base URL for the API (can be configured via environment variables)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000, // 90 seconds to accommodate multi-turn workflows
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Required for Better Auth session cookies
});

// Request interceptor to log requests
api.interceptors.request.use(
  async (config) => {
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
    console.debug('API response received:', response.config.method?.toUpperCase(), response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('API error occurred:', {
      method: error.config?.method?.toUpperCase(),
      url: error.config?.url,
      status: error.response?.status,
      message: error.message,
      data: error.response?.data
    });

    if (isAuthError(error)) {
      console.error('Authentication error occurred:', error.response?.status, error.response?.data);
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
  register: async (name: string, email: string, password: string): Promise<AxiosResponse> => {
    return api.post('/api/auth/signup', { name, email, password });
  },
  login: async (email: string, password: string): Promise<AxiosResponse> => {
    return api.post('/api/auth/login', { email, password });
  },
  refresh: async (refreshToken: string): Promise<AxiosResponse> => {
    return api.post('/api/auth/refresh', { refresh_token: refreshToken });
  },
  logout: async (): Promise<AxiosResponse> => {
    const response = await api.post('/api/auth/logout');
    localStorage.removeItem('access_token');
    return response;
  },
};

// Dashboard API functions
export const dashboardAPI = {
  getStats: async (): Promise<AxiosResponse> => {
    return api.get('/api/dashboard/stats');
  },
};

// Task API functions
export const taskAPI = {
  getTasks: async (): Promise<AxiosResponse> => {
    return api.get('/api/tasks/');
  },
  createTask: async (taskData: {
    title: string;
    description?: string;
    category?: string;
    priority?: number;
    version?: number;
  }): Promise<AxiosResponse> => {
    return api.post('/api/tasks/', taskData);
  },
  getTask: async (taskId: string | number): Promise<AxiosResponse> => {
    return api.get(`/api/tasks/${taskId}`);
  },
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
  deleteTask: async (taskId: string | number): Promise<AxiosResponse> => {
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
  sendMessage: async (userId: string, messageData: { message: string; conversation_id?: string; }): Promise<AxiosResponse> => {
    return api.post(`/api/chat/conversation`, messageData);
  },

  // Get conversation history
  getConversationHistory: async (conversationId: string, convId: string): Promise<AxiosResponse> => {
    return api.get(`/api/chat/conversation/${conversationId}`);
  },

  // Delete a conversation
  deleteConversation: async (conversationId: string): Promise<AxiosResponse> => {
    return api.delete(`/api/chat/conversation/${conversationId}`);
  },
};

export default api;
