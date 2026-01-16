'use client';

import React, { useEffect } from 'react';
import { isValidSession } from '../utils/auth';
import { useRouter } from 'next/navigation';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = <div>Redirecting to login...</div>
}) => {
  const router = useRouter();

  useEffect(() => {
    if (typeof window !== 'undefined' && !isValidSession()) {
      // Redirect to login if not authenticated
      router.push('/login');
    }
  }, [router]);

  if (typeof window !== 'undefined' && !isValidSession()) {
    return fallback;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
