// Client-side API service for communicating with the backend in Next.js App Router
'use client';

import axios, { AxiosResponse } from 'axios';

// Base URL for the API (can be configured via environment variables)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // Increased to 30 seconds to handle slower backend responses
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable credentials (cookies) for authentication
});

// Check if running in browser environment
const isBrowser = (): boolean => {
  return typeof window !== 'undefined';
};


// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && isBrowser()) {
      // Clear any local user state and redirect to login if unauthorized
      if (typeof window !== 'undefined') {
        // Clear any user state from memory/cache
        // The HTTP-only cookie will be automatically cleared by the backend on logout
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);


// Authentication API functions
export const authAPI = {
  // Register a new user
  register: async (name: string, email: string, password: string): Promise<AxiosResponse> => {
    return api.post('/auth/signup', { name, email, password });
  },

  // Login user
  login: async (email: string, password: string): Promise<AxiosResponse> => {
    return api.post('/auth/login', { email, password });
  },

  // Logout user (client-side only)
  logout: async (): Promise<AxiosResponse> => {
    return api.post('/auth/logout');
  },
};

// Task API functions
export const taskAPI = {
  // Get user's tasks
  getTasks: async (): Promise<AxiosResponse> => {
    return api.get('/api/tasks');
  },

  // Create a new task
  createTask: async (taskData: { title: string; description?: string; category?: string; priority?: number }): Promise<AxiosResponse> => {
    return api.post('/api/tasks', taskData);
  },

  // Get a specific task
  getTask: async (taskId: number): Promise<AxiosResponse> => {
    return api.get(`/api/tasks/${taskId}`);
  },

  // Update a task
  updateTask: async (taskId: number, taskData: { title?: string; description?: string; status?: boolean; category?: string; priority?: number }): Promise<AxiosResponse> => {
    return api.put(`/api/tasks/${taskId}`, taskData);
  },

  // Delete a task
  deleteTask: async (taskId: number): Promise<AxiosResponse> => {
    return api.delete(`/api/tasks/${taskId}`);
  },
};

export default api;
