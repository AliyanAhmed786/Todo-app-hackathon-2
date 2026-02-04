'use server';

// Server-side API functions using Server Actions for Next.js App Router
import { revalidatePath } from 'next/cache';
import { cookies } from 'next/headers';

// Helper function to get API base URL
function getApiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
}

// Helper function to create fetch options with Better Auth session
async function getServerApiOptions(additionalOptions: any = {}) {
  const cookieStore = await cookies();
  // Get all cookies as a string to forward to the backend API
  const allCookies = [];
  for (const cookie of cookieStore.getAll()) {
    allCookies.push(`${cookie.name}=${cookie.value}`);
  }
  const cookieHeader = allCookies.join('; ');

  const options: any = {
    headers: {
      'Content-Type': 'application/json',
      ...(cookieHeader && { 'Cookie': cookieHeader }),
      ...additionalOptions.headers,
    },
    credentials: 'include',
    ...additionalOptions,
  };

  return options;
}

// Helper function to make server API calls
async function serverApiCall(endpoint: string, options: any = {}) {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${endpoint}`;
  const apiOptions = await getServerApiOptions(options);

  const response = await fetch(url, apiOptions);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || `API call failed: ${response.statusText}`);
  }

  return data;
}

// Note: Auth token handling via cookies is automatic with Better Auth
// No manual token injection needed - backend handles session validation

// Authentication Server Actions
export const authServerActions = {
  // Register a new user
  register: async (name: string, email: string, password: string) => {
    try {
      const data = await serverApiCall('/api/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ name, email, password }),
      });
      return data;
    } catch (error) {
      console.error('Server registration error:', error);
      throw error;
    }
  },

  // Login user
  login: async (email: string, password: string) => {
    try {
      const data = await serverApiCall('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      // Backend automatically sets better-auth.session_token cookie
      return data;
    } catch (error) {
      console.error('Server login error:', error);
      throw error;
    }
  },

  // Logout user
  logout: async () => {
    try {
      const data = await serverApiCall('/api/auth/logout', {
        method: 'POST',
      });
      // Backend automatically clears better-auth.session_token cookie
      return data;
    } catch (error) {
      console.error('Server logout error:', error);
      // Even if the server logout fails, return success
      return { success: true };
    }
  },
};

// Task Server Actions
export const taskServerActions = {
  // Get user's tasks
  getTasks: async () => {
    try {
      const data = await serverApiCall('/api/tasks', {
        method: 'GET',
      });
      return data;
    } catch (error) {
      console.error('Server get tasks error:', error);
      throw error;
    }
  },

  // Create a new task
  createTask: async (taskData: { title: string; description?: string; category?: string; priority?: number }) => {
    try {
      const data = await serverApiCall('/api/tasks', {
        method: 'POST',
        body: JSON.stringify(taskData),
      });
      revalidatePath('/api/tasks');
      return data;
    } catch (error) {
      console.error('Server create task error:', error);
      throw error;
    }
  },

  // Get a specific task
  getTask: async (taskId: number) => {
    try {
      const data = await serverApiCall(`/api/tasks/${taskId}`, {
        method: 'GET',
      });
      return data;
    } catch (error) {
      console.error('Server get task error:', error);
      throw error;
    }
  },

  // Update a task
  updateTask: async (taskId: number, taskData: { title?: string; description?: string; status?: boolean; category?: string; priority?: number }) => {
    try {
      const data = await serverApiCall(`/api/tasks/${taskId}`, {
        method: 'PUT',
        body: JSON.stringify(taskData),
      });
      revalidatePath('/api/tasks');
      revalidatePath(`/api/tasks/${taskId}`);
      return data;
    } catch (error) {
      console.error('Server update task error:', error);
      throw error;
    }
  },

  // Delete a task
  deleteTask: async (taskId: number) => {
    try {
      const data = await serverApiCall(`/api/tasks/${taskId}`, {
        method: 'DELETE',
      });
      revalidatePath('/api/tasks');
      return data;
    } catch (error) {
      console.error('Server delete task error:', error);
      throw error;
    }
  },
};

// Define types for our chat responses
interface ChatResponse {
  response: string;
  conversation_id: string;
  tool_calls: Array<{ id: string; function: { name: string; arguments: string } }>;
  action: { type: string; data: any };
}

interface ActionResult<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// Chat Server Actions
export const chatServerActions = {
  // Send a message to the chat API and get a response from the AI agent
  sendMessage: async (userId: string, message: string, conversationId?: string): Promise<ActionResult<ChatResponse>> => {
    try {
      const requestBody = {
        message,
        ...(conversationId && { conversation_id: conversationId })
      };

      const data = await serverApiCall(`/api/chat/message`, {
        method: 'POST',
        body: JSON.stringify(requestBody),
      });

      return {
        success: true,
        data: data
      };
    } catch (error: any) {
      console.error('Server chat send message error:', error);
      let errorMessage = 'Failed to send message';

      if (error.status === 401) {
        errorMessage = 'Authentication required. Please log in.';
      } else if (error.status === 403) {
        errorMessage = 'Access denied. Please check your permissions.';
      } else if (error.message) {
        errorMessage = error.message;
      }

      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Get conversation history
  getConversationHistory: async (userId: string, conversationId: string): Promise<ActionResult<any>> => {
    try {
      const data = await serverApiCall(`/api/chat/history/${conversationId}`, {
        method: 'GET',
      });

      return {
        success: true,
        data: data
      };
    } catch (error: any) {
      console.error('Server get conversation history error:', error);
      let errorMessage = 'Failed to get conversation history';

      if (error.status === 401) {
        errorMessage = 'Authentication required. Please log in.';
      } else if (error.status === 403) {
        errorMessage = 'Access denied. Please check your permissions.';
      } else if (error.message) {
        errorMessage = error.message;
      }

      return {
        success: false,
        error: errorMessage
      };
    }
  },
};
