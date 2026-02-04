// Server-side authentication utilities for Next.js App Router
import { cookies } from 'next/headers';

// Get Better Auth session token from cookies (async)
export async function getServerToken(): Promise<string | null> {
  try {
    const cookieStore = await cookies();
    const token = cookieStore.get('better-auth.session_token');
    return token ? token.value : null;
  } catch (error) {
    // If cookies are not available (during static generation), return null
    console.error('Error getting Better Auth token from cookies:', error);
    return null;
  }
}

// Check if user is authenticated on the server (async)
export async function isServerAuthenticated(): Promise<boolean> {
  const token = await getServerToken();
  return token !== null && token !== undefined && token !== '';
}

// Get user ID from Better Auth session on the server (async)
export async function getServerUserId(): Promise<string | null> {
  // In Better Auth implementation, we need to validate the session against the backend
  // This typically requires a backend call, so we return null here
  // Actual user ID should be retrieved via the session endpoint
  return null;
}

// Set Better Auth token in cookies (async) - This is handled by the backend
export async function setServerToken(token: string): Promise<void> {
  // Better Auth tokens are set by the backend, not the frontend
  console.warn('Setting Better Auth token from frontend is not recommended. Tokens should be set by the backend.');
}

// Remove Better Auth token from cookies (async)
export async function removeServerToken(): Promise<void> {
  (await cookies()).delete('better-auth.session_token');
}
