// src/lib/authClient.ts
// Remove Better Auth client since backend uses custom implementation
// Just export the custom functions that match the backend API


// Create custom signIn function that calls the correct backend endpoint
export const signIn = async (email: string, password: string, redirect?: boolean) => {
  const response = await fetch(`${process.env["NEXT_PUBLIC_API_BASE_URL"] ?? "http://localhost:8000"}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json', // Added for content negotiation
    },
    credentials: 'include',
    body: JSON.stringify({
      email: email.trim().toLowerCase(), // Normalized
      password: password
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    return {
      error: {
        message: data.detail || 'Login failed',
        status: response.status
      }
    };
  }

  return {
    data: data,
    error: null
  };
};

// Create custom signUp function that calls the correct backend endpoint
export const signUp = async (name: string, email: string, password: string, redirect?: boolean) => {
  const response = await fetch(`${process.env["NEXT_PUBLIC_API_BASE_URL"] ?? "http://localhost:8000"}/api/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json', // Added for consistency
    },
    credentials: 'include',
    body: JSON.stringify({
      name: name,
      email: email.trim().toLowerCase(), // Normalized
      password: password
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    return {
      error: {
        message: data.detail || 'Registration failed',
        status: response.status
      }
    };
  }

  return {
    data: data,
    error: null
  };
};

// Create custom signOut function that calls the correct backend endpoint
export const signOut = async (redirect?: boolean) => {
  const response = await fetch(`${process.env["NEXT_PUBLIC_API_BASE_URL"] ?? "http://localhost:8000"}/api/auth/logout`, {
    method: 'POST',
    credentials: 'include', // Important for cookies
  });

  const data = await response.json();

  if (!response.ok) {
    return {
      error: {
        message: data.detail || 'Logout failed',
        status: response.status
      }
    };
  }

  return {
    data: data,
    error: null
  };
};

// Custom useSession hook that calls the backend session endpoint directly
import { useState, useEffect } from 'react';

export function useSession() {
  const [session, setSession] = useState<{
    data: { user: any } | null;
    status: 'loading' | 'authenticated' | 'unauthenticated';
    update: (data: any) => void;
  }>({
    data: null,
    status: 'loading',
    update: () => {}
  });

  useEffect(() => {
    let isMounted = true;

    const fetchSession = async () => {
      try {
        const response = await fetch(`${process.env["NEXT_PUBLIC_API_BASE_URL"] ?? "http://localhost:8000"}/api/auth/session`, {
          method: 'GET',
          credentials: 'include', // Important for cookies
        });

        const data = await response.json();

        if (isMounted) {
          setSession({
            data: data.user ? { user: data.user } : null,
            status: data.user ? 'authenticated' : 'unauthenticated',
            update: (newData: any) => setSession(prev => ({ ...prev, data: newData }))
          });
        }
      } catch (error) {
        console.error('Session fetch error:', error);
        if (isMounted) {
          setSession(prev => ({
            ...prev,
            data: null,
            status: 'unauthenticated',
            update: prev.update
          }));
        }
      }
    };

    fetchSession();

    return () => {
      isMounted = false;
    };
  }, []);

  return session;
}

// Imperative getSession function for use in components that need to fetch session data imperatively
export async function getSession() {
  try {
    const response = await fetch(`${process.env["NEXT_PUBLIC_API_BASE_URL"] ?? "http://localhost:8000"}/api/auth/session`, {
      method: 'GET',
      credentials: 'include', // Important for cookies
    });

    const data = await response.json();

    return {
      user: data.user || null,
      authenticated: !!data.user
    };
  } catch (error) {
    console.error('Session fetch error:', error);
    return {
      user: null,
      authenticated: false
    };
  }
}

// Export authClient for compatibility
export const authClient = {
  useSession: useSession,
  getSession: getSession
};