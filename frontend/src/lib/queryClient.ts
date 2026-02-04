import { QueryClient } from '@tanstack/react-query';

/**
 * Global query client configuration for React Query
 * Provides default settings for all queries and mutations
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Refetch on window focus disabled to reduce API calls
      refetchOnWindowFocus: false,
      // Don't retry failed queries by default
      retry: false,
      // Stale time of 1 minute before considering data stale
      staleTime: 60 * 1000,
    },
    mutations: {
      // Don't retry failed mutations by default
      retry: false,
    },
  },
});