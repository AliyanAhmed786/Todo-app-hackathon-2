// ProtectedRoute component to protect authenticated routes
import React from 'react';
import { isAuthenticated } from '../utils/auth';
import { useRouter } from 'next/router';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = <div>Redirecting to login...</div>
}) => {
  const router = useRouter();

  React.useEffect(() => {
    if (typeof window !== 'undefined' && !isAuthenticated()) {
      // Redirect to login if not authenticated
      router.push('/login');
    }
  }, [router]);

  if (typeof window !== 'undefined' && !isAuthenticated()) {
    return fallback;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
