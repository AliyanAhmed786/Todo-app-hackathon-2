// This is a stub to bypass the missing @tanstack/react-query dependency
export const queryClient = {
  getQueryData: () => null,
  setQueryData: () => {},
  invalidateQueries: () => Promise.resolve(),
} as any;