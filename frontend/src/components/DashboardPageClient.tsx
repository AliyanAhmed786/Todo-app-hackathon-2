'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authClient, signOut } from '../lib/authClient';
import ErrorBoundary from './ErrorBoundary';
import { taskAPI, dashboardAPI } from '../services/api';
import dynamic from 'next/dynamic';
import ChatBot from './chatbot-ui/ChatBot';
import { TaskListRef } from './TaskList';

// Dynamically import TaskList to avoid SSR issues
const DynamicTaskList = dynamic(() => import('./TaskList'), {
  loading: () => <div className="text-center py-8">Loading tasks...</div>,
  ssr: false
});

export const DashboardPageClient: React.FC = () => {
  const router = useRouter();
  const { data: session, isPending } = authClient.useSession();
  const taskListRef = useRef<TaskListRef>(null);
  const [user, setUser] = useState<{ id: string; name?: string; email?: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [authChecked, setAuthChecked] = useState(false);
  const [dashboardStats, setDashboardStats] = useState({
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0
  });
  const [statsLoading, setStatsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Define fetchDashboardStats outside of useEffect and memoize it
  const fetchDashboardStats = useCallback(async () => {
    setStatsLoading(true);
    setError(null); // Clear previous errors
    try {
      // Use the API service
      const response = await dashboardAPI.getStats();

      const data = response.data;

      if (data) {
        // Check if the response has the expected structure
        if (data.total_tasks !== undefined && data.completed_tasks !== undefined && data.pending_tasks !== undefined) {
          setDashboardStats({
            totalTasks: data.total_tasks || 0,
            completedTasks: data.completed_tasks || 0,
            pendingTasks: data.pending_tasks || 0
          });
          setError(null); // Clear any previous errors on success
        } else {
          // Unexpected response format
          setDashboardStats({
            totalTasks: 0,
            completedTasks: 0,
            pendingTasks: 0
          });
          setError('Unexpected response format from dashboard API.');
          console.error('Unexpected response format from dashboard API:', data);
        }
      } else {
        // Empty response
        setDashboardStats({
          totalTasks: 0,
          completedTasks: 0,
          pendingTasks: 0
        });
        setError('Empty response from dashboard API.');
        console.error('Empty response from dashboard API');
      }
    } catch (err: any) {
      console.error('Error fetching dashboard statistics:', err);
      console.error('Error message:', err.message || err);

      // Set fallback data
      setDashboardStats({
        totalTasks: 0,
        completedTasks: 0,
        pendingTasks: 0
      });

      // Set appropriate error message
      if (err.message && (err.message.includes('Network') || err.message.includes('Failed to fetch') || err.message.includes('timeout'))) {
        setError('Unable to connect to the backend server. Please check if the server is running.');
      } else if (err.response?.status === 401 || err.response?.status === 403) {
        setError('Authentication error. Please log in again.');
      } else {
        setError('Failed to fetch dashboard statistics. Please try again.');
      }
    } finally {
      setStatsLoading(false);
    }
  }, []); // Empty dependency array since dashboardAPI is stable

  useEffect(() => {
    // Handle pending state
    if (isPending) {
      setLoading(true);
      return;
    }

    // Check if user is authenticated
    if (session?.user) {
      // User is authenticated, set user data
      setUser({
        id: session.user.id,
        email: session.user.email,
        name: session.user.name
      });

      // Mark auth as checked before fetching stats
      setAuthChecked(true);
      setLoading(false);

      // Only fetch dashboard statistics AFTER auth is confirmed
      fetchDashboardStats();
    } else {
      // User is not authenticated, redirect to login
      console.warn('No active session found, redirecting to login');
      router.push('/login');
      return;
    }
  }, [session, isPending, router, fetchDashboardStats]); // Include session and isPending in dependencies

  const handleLogout = async () => {
    try {
      // Use Better Auth logout
      await signOut();
      // Redirect to login page
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Even if logout fails, redirect to login
      router.push('/login');
    }
  };

  // Don't render anything until authentication is checked on the client
  if (!authChecked) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-coral-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-coral-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-white">
        {/* Glassmorphic Header */}
        <header className="fixed w-full top-0 z-50 backdrop-blur-xl bg-white/70 border-b border-gray-200/50 shadow-lg">
          <div className="max-w-7xl mx-auto px-6">
            <div className="flex justify-between h-16 items-center">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-coral-600 to-coral-700 bg-clip-text text-transparent">
                  TodoApp
                </h1>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm font-medium text-gray-700">Welcome, {user?.name || 'User'}</span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-gradient-to-r from-coral-600 to-coral-700 text-white text-sm font-semibold rounded-xl hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95 focus:ring-2 focus:ring-coral-300 focus:outline-none transition-all duration-300"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </header>

        <main className="pt-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-10">
            <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
            <p className="mt-3 text-base text-gray-600">Track and manage your tasks efficiently</p>
          </div>

          {/* Error message */}
          {error && (
            <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              <div className="flex items-center justify-between">
                <span>{error}</span>
                <button
                  onClick={fetchDashboardStats}
                  disabled={statsLoading}
                  className="ml-4 px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {statsLoading ? 'Retrying...' : 'Retry'}
                </button>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {statsLoading ? (
              <div className="col-span-3 flex justify-center py-8">
                <div className="w-8 h-8 border-4 border-coral-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : (
              <>
                {/* Total Tasks Card - Glassmorphic */}
                <div
                  className="backdrop-blur-xl bg-gradient-to-br from-coral-500/10 to-coral-600/20 p-8 rounded-2xl border border-coral-300/30 shadow-xl shadow-coral-900/10 hover:shadow-2xl hover:shadow-coral-500/20 hover:-translate-y-1 transition-all duration-300"
                  role="region"
                  aria-labelledby="total-tasks-title"
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 id="total-tasks-title" className="text-sm font-semibold text-coral-700 uppercase tracking-wide">Total Tasks</h3>
                    <div className="p-3 rounded-xl bg-coral-500/20 backdrop-blur-sm">
                      <svg className="w-6 h-6 text-coral-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                      </svg>
                    </div>
                  </div>
                  <p className="text-5xl font-bold bg-gradient-to-r from-coral-600 to-coral-700 bg-clip-text text-transparent mb-6" aria-label={`Total tasks: ${dashboardStats.totalTasks}`}>{dashboardStats.totalTasks}</p>
                  <div className="w-full bg-coral-100/30 rounded-full h-2.5">
                    <div
                      className="bg-gradient-to-r from-coral-500 to-coral-600 h-2.5 rounded-full shadow-lg shadow-coral-500/30 transition-all duration-500"
                      style={{ width: dashboardStats.totalTasks > 0 ? '100%' : '0%' }}
                    ></div>
                  </div>
                </div>

                {/* Completed Tasks Card - Glassmorphic */}
                <div
                  className="backdrop-blur-xl bg-gradient-to-br from-blue-500/10 to-blue-600/20 p-8 rounded-2xl border border-blue-300/30 shadow-xl shadow-blue-900/10 hover:shadow-2xl hover:shadow-blue-500/20 hover:-translate-y-1 transition-all duration-300"
                  role="region"
                  aria-labelledby="completed-tasks-title"
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 id="completed-tasks-title" className="text-sm font-semibold text-blue-700 uppercase tracking-wide">Completed</h3>
                    <div className="p-3 rounded-xl bg-blue-500/20 backdrop-blur-sm">
                      <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                  </div>
                  <p className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-blue-700 bg-clip-text text-transparent mb-6" aria-label={`Completed tasks: ${dashboardStats.completedTasks}`}>{dashboardStats.completedTasks}</p>
                  <div className="w-full bg-blue-100/30 rounded-full h-2.5">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-blue-600 h-2.5 rounded-full shadow-lg shadow-blue-500/30 transition-all duration-500"
                      style={{
                        width: dashboardStats.totalTasks > 0
                          ? `${(dashboardStats.completedTasks / dashboardStats.totalTasks) * 100}%`
                          : '0%'
                      }}
                    ></div>
                  </div>
                </div>

                {/* Pending Tasks Card - Glassmorphic */}
                <div
                  className="backdrop-blur-xl bg-gradient-to-br from-green-500/10 to-green-600/20 p-8 rounded-2xl border border-green-300/30 shadow-xl shadow-green-900/10 hover:shadow-2xl hover:shadow-green-500/20 hover:-translate-y-1 transition-all duration-300"
                  role="region"
                  aria-labelledby="pending-tasks-title"
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 id="pending-tasks-title" className="text-sm font-semibold text-green-700 uppercase tracking-wide">Pending</h3>
                    <div className="p-3 rounded-xl bg-green-500/20 backdrop-blur-sm">
                      <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                  </div>
                  <p className="text-5xl font-bold bg-gradient-to-r from-green-600 to-green-700 bg-clip-text text-transparent mb-6" aria-label={`Pending tasks: ${dashboardStats.pendingTasks}`}>{dashboardStats.pendingTasks}</p>
                  <div className="w-full bg-green-100/30 rounded-full h-2.5">
                    <div
                      className="bg-gradient-to-r from-green-500 to-green-600 h-2.5 rounded-full shadow-lg shadow-green-500/30 transition-all duration-500"
                      style={{
                        width: dashboardStats.totalTasks > 0
                          ? `${(dashboardStats.pendingTasks / dashboardStats.totalTasks) * 100}%`
                          : '0%'
                      }}
                    ></div>
                  </div>
                </div>
              </>
            )}
          </div>

          {/* Manual refresh button */}
          <div className="flex justify-center mb-8">
            <button
              onClick={fetchDashboardStats}
              disabled={statsLoading}
              className="p-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-semibold rounded-xl hover:shadow-xl hover:shadow-blue-500/30 hover:-translate-y-0.5 active:scale-95 focus:ring-2 focus:ring-blue-300 focus:outline-none transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {statsLoading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Refreshing...
                </span>
              ) : (
                <span className="flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  Refresh Stats
                </span>
              )}
            </button>
          </div>

          <div className="mb-6">
            <Link
              href="/dashboard"
              className="inline-block p-[10px] bg-gradient-to-r from-coral-600 to-coral-700 text-white text-base font-semibold rounded-xl hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95 focus:ring-2 focus:ring-coral-300 focus:outline-none transition-all duration-300"
            >
              View & Manage Tasks
            </Link>
          </div>

          <div className="mt-8 backdrop-blur-xl bg-gradient-to-br from-gray-50/80 to-white/60 p-8 rounded-2xl border border-gray-200/50 shadow-xl hover:shadow-2xl transition-all duration-300">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg className="w-5 h-5 text-coral-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              Recent Activity
            </h3>
            <p className="text-gray-600">Check your task list for recent updates and activities.</p>
          </div>

          {/* Task Cards Section */}
          <div className="mt-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Your Tasks</h3>
            <DynamicTaskList
              ref={taskListRef}
              onTaskChange={(updatedTasks) => {
                // Calculate stats instantly from local tasks for immediate feedback
                if (updatedTasks && updatedTasks.length > 0) {
                  const completedCount = updatedTasks.filter(t => t.completed).length;
                  const pendingCount = updatedTasks.filter(t => !t.completed).length;

                  setDashboardStats({
                    totalTasks: updatedTasks.length,
                    completedTasks: completedCount,
                    pendingTasks: pendingCount
                  });

                  console.log('📊 Optimistic stats update:', {
                    total: updatedTasks.length,
                    completed: completedCount,
                    pending: pendingCount
                  });
                }
                // Backend validation (still happens for accuracy)
                fetchDashboardStats();
              }}
              onTaskAction={fetchDashboardStats}
            />
          </div>
        </main>

        {/* ChatBot Component - Positioned to avoid overlapping with New Task button */}
        <ChatBot
          position="bottom-24 right-8"
          userId={user?.id}
          onTaskChange={async () => {
            // CRITICAL: Trigger both dashboard stats refresh AND task list refresh
            // to ensure the UI matches the database (per requirement 21)
            await fetchDashboardStats();
            if (taskListRef.current) {
              await taskListRef.current.refreshTasks();
            }
          }}
        />
      </div>
    </ErrorBoundary>
  );
};

export default DashboardPageClient;
