'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { dashboardAPI } from '../../services/api';
import { authClient, signOut } from '../../lib/authClient';
import TaskList from '../../components/TaskList';

export function DashboardPageClient() {
  const router = useRouter();
  const [user, setUser] = useState<{ id: string; name?: string; email?: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0 });

  const fetchStats = useCallback(async () => {
    try {
      const response = await dashboardAPI.getStats();
      setStats({
        total: response.data.total_tasks || 0,
        completed: response.data.completed_tasks || 0,
        pending: response.data.pending_tasks || 0
      });
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      // Set default values on error
      setStats({ total: 0, completed: 0, pending: 0 });
    }
  }, []);

  useEffect(() => {
    const checkAuthAndLoadData = async () => {
      try {
        // Check if user is authenticated by getting session
        const session = await authClient.getSession();
        if (session?.user) {
          // User is authenticated, set user data
          setUser({
            id: session.user.id,
            email: session.user.email,
            name: session.user.name
          });

          // Fetch stats after user is authenticated
          await fetchStats();
        } else {
          // User is not authenticated, redirect to login
          router.push('/login');
          return;
        }
      } catch (error) {
        console.error('Error checking authentication:', error);
        router.push('/login');
        return;
      } finally {
        setLoading(false);
      }
    };

    checkAuthAndLoadData();
  }, [router, fetchStats]);

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 via-white to-gray-100">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-coral-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      {/* Glassmorphic Header */}
      <header className="fixed w-full top-0 z-50 backdrop-blur-xl bg-white/70 border-b border-white/40 shadow-lg shadow-gray-900/5">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-coral-600 to-coral-700 bg-clip-text text-transparent">
                TodoApp
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user?.name || 'User'}</span>
              <button
                onClick={handleLogout}
                className="p-[10px] bg-gradient-to-r from-coral-600 to-coral-700 text-white text-sm font-semibold rounded-xl hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95 focus:ring-2 focus:ring-coral-300 focus:outline-none transition-all duration-300"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="pt-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900">Task Dashboard</h1>
          <p className="mt-2 text-gray-600">Organize and manage your tasks efficiently</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="backdrop-blur-xl bg-gradient-to-br from-coral-500/20 to-coral-600/20 p-6 rounded-2xl border border-coral-300/30 shadow-lg shadow-coral-900/10">
            <div className="flex items-center">
              <div className="p-3 rounded-xl bg-coral-500/20 backdrop-blur-sm mr-4">
                <svg className="w-6 h-6 text-coral-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 002 2" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-coral-700 mb-1">Total Tasks</h3>
                <p className="text-3xl font-bold text-coral-600">{stats.total}</p>
              </div>
            </div>
          </div>
          <div className="backdrop-blur-xl bg-gradient-to-br from-green-500/20 to-green-600/20 p-6 rounded-2xl border border-green-300/30 shadow-lg shadow-green-900/10">
            <div className="flex items-center">
              <div className="p-3 rounded-xl bg-green-500/20 backdrop-blur-sm mr-4">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-green-700 mb-1">Completed</h3>
                <p className="text-3xl font-bold text-green-600">{stats.completed}</p>
              </div>
            </div>
          </div>
          <div className="backdrop-blur-xl bg-gradient-to-br from-amber-500/20 to-amber-600/20 p-6 rounded-2xl border border-amber-300/30 shadow-lg shadow-amber-900/10">
            <div className="flex items-center">
              <div className="p-3 rounded-xl bg-amber-500/20 backdrop-blur-sm mr-4">
                <svg className="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-amber-700 mb-1">Pending</h3>
                <p className="text-3xl font-bold text-amber-600">{stats.pending}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <Link
            href="/dashboard"
            className="inline-block p-[10px] bg-gradient-to-r from-coral-600 to-coral-700 text-white text-base font-semibold rounded-xl hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95 focus:ring-2 focus:ring-coral-300 focus:outline-none transition-all duration-300"
          >
            View & Manage Tasks
          </Link>
        </div>

        <div className="mt-8 backdrop-blur-xl bg-white/40 p-6 rounded-2xl border border-white/60 shadow-xl shadow-gray-900/10">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <p className="text-gray-600">Check your task list for recent updates and activities.</p>
        </div>

        {/* Task List Section - Pass fetchStats function to child component */}
        <div className="mt-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Your Tasks</h3>
          {/* Import and use TaskList component that accepts fetchStats prop */}
          <TaskList onTaskChange={fetchStats} onTaskAction={fetchStats} />
        </div>
      </main>
    </div>
  );
}
