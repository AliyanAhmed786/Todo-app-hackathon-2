/**
 * Authentication utility functions
 * Provides helper functions for cookie-based authentication with Better Auth
 */

/**
 * Get a cookie value by name
 * @param name Cookie name
 * @returns Cookie value or null if not found
 */
export const getCookie = (name: string): string | null => {
    if (typeof document === 'undefined') {
        return null;
    }

    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) {
        return parts.pop()?.split(';').shift() || null;
    }

    return null;
};

/**
 * Check if user has an active session
 * @returns boolean indicating if session token exists
 */
export const hasActiveSession = (): boolean => {
    return getCookie('better-auth.session_token') !== null;
};

/**
 * Clear all authentication cookies
 * Used during logout
 */
export const clearAuthCookies = (): void => {
    if (typeof document === 'undefined') {
        return;
    }

    // Clear Better Auth session token
    document.cookie = 'better-auth.session_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    // Clear any legacy tokens
    document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
};

/**
 * Check if the current error is an authentication error
 * @param error Error object
 * @returns boolean indicating if it's an auth error
 */
export const isAuthError = (error: any): boolean => {
    return error?.response?.status === 401 || error?.response?.status === 403;
};

/**
 * Redirect to login page
 * Clears auth cookies before redirecting
 */
export const redirectToLogin = (): void => {
    if (typeof window === 'undefined') {
        return;
    }

    console.log('Redirecting to login due to authentication error');
    clearAuthCookies();
    window.location.href = '/login';
};

/**
 * Validate if the current session is still active
 * Checks both JWT token and Better Auth session cookie
 * @returns boolean indicating if session is valid
 */
export const isValidSession = (): boolean => {
    // Check for JWT token
    const jwtToken = localStorage.getItem('access_token');
    if (jwtToken) {
        try {
            // Decode JWT to check expiration
            const base64Url = jwtToken.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));

            const decodedToken = JSON.parse(jsonPayload);
            const currentTime = Math.floor(Date.now() / 1000);

            // Check if token is expired
            if (decodedToken.exp && decodedToken.exp < currentTime) {
                console.log('JWT token has expired');
                localStorage.removeItem('access_token');
                return false;
            }

            return true;
        } catch (error) {
            console.error('Error decoding JWT token:', error);
            localStorage.removeItem('access_token');
            return false;
        }
    }

    // Check for Better Auth session cookie
    const hasBetterAuthSession = document.cookie.includes('better-auth.session_token');
    return hasBetterAuthSession;
};

export const getUserIdFromToken = () => {
  if (typeof document === 'undefined') return null;
  // This is a placeholder to stop the build error. 
  // If your Navbar actually needs the ID, it should ideally get it from the session.
  return null; 
};

export const logout = () => {
  if (typeof window !== 'undefined') {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = "/login";
  }
};