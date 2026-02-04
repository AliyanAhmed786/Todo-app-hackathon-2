// Client-side authentication utilities for Next.js Pages Router
// Get Better Auth session token from browser cookies
export function getClientToken(): string | null {
  if (typeof window === 'undefined') {
    // Running on the server-side during SSR
    return null;
  }

  try {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith('better-auth.session_token=')) {
        return cookie.substring('better-auth.session_token='.length);
      }
    }
    return null;
  } catch (error) {
    console.error('Error getting Better Auth token from cookies:', error);
    return null;
  }
}

// Check if user is authenticated on the client (sync)
export function isAuthenticated(): boolean {
  const token = getClientToken();
  return token !== null && token !== undefined && token !== '';
}

// Alternative async version for potential future API validation
export async function isAuthenticatedAsync(): Promise<boolean> {
  const token = getClientToken();
  if (!token) return false;

  // In a real implementation, you might want to validate the token with your backend
  // For now, we'll just check if it exists
  return token !== null && token !== undefined && token !== '';
}

// Get user ID from Better Auth session on the client (sync)
export function getClientUserId(): string | null {
  // In Better Auth implementation, we need to validate the session against the backend
  // This typically requires a backend call, so we return null here
  // Actual user ID should be retrieved via the session endpoint
  return null;
}

// Set Better Auth token in browser cookies (sync) - This is handled by the backend
export function setClientToken(token: string): void {
  // Better Auth tokens are set by the backend, not the frontend
  console.warn('Setting Better Auth token from frontend is not recommended. Tokens should be set by the backend.');
}

// Remove Better Auth token from browser cookies (sync)
export function removeClientToken(): void {
  if (typeof window === 'undefined') {
    // Running on the server-side during SSR
    return;
  }

  try {
    document.cookie = 'better-auth.session_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; samesite=strict;';
  } catch (error) {
    console.error('Error removing Better Auth token from cookies:', error);
  }
}
