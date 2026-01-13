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

    clearAuthCookies();
    window.location.href = '/login';
};
