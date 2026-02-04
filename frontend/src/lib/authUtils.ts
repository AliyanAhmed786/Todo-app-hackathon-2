/**
 * Authentication utility functions for Better Auth integration
 * Provides helper functions to work with Better Auth's session management
 */

import { signIn, signOut, useSession } from './authClient';

/**
 * Signs in a user using Better Auth
 * @param credentials - User credentials (email and password)
 * @returns Promise with sign in result
 */
export const authenticateUser = async (credentials: { email: string; password: string }) => {
  try {
    const result = await signIn(
      credentials.email,
      credentials.password,
      false // Prevent automatic redirect
    );

    return result;
  } catch (error) {
    console.error('Authentication failed:', error);
    throw error;
  }
};

/**
 * Signs out the current user using Better Auth
 * @returns Promise that resolves when sign out is complete
 */
export const logoutUser = async () => {
  try {
    await signOut(false); // Prevent automatic redirect
  } catch (error) {
    console.error('Logout failed:', error);
    throw error;
  }
};

/**
 * Gets the current session using Better Auth
 * @returns Current session data or null if not authenticated
 */
export const getCurrentSession = () => {
  return useSession();
};

/**
 * Checks if the user is authenticated
 * @returns Boolean indicating authentication status
 */
export const isAuthenticated = (): boolean => {
  const session = getCurrentSession();
  return !!session.data?.user;
};

/**
 * Gets the current user data
 * @returns User object or null if not authenticated
 */
export const getCurrentUser = () => {
  const session = getCurrentSession();
  return session.data?.user || null;
};

/**
 * Verifies if the current session is still valid
 * @returns Boolean indicating if session is valid
 */
export const isSessionValid = (): boolean => {
  const session = getCurrentSession();
  return !!session.data && session.status !== 'loading';
};