'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Check, X } from 'lucide-react';

const EditTaskPage = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'High' | 'Medium' | 'Low'>('Medium');
  const [dueDate, setDueDate] = useState('');
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();
  const params = useParams();

  useEffect(() => {
    fetchTask();
  }, []);

  const fetchTask = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/tasks/${params.id}`, {
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies in the request
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - redirect to login
          // Clear any local user state
          // The HTTP-only cookie will be automatically cleared by the backend on logout
          router.push('/login');
          return;
        }
        throw new Error('Failed to fetch task');
      }

      const task = await response.json();

      // Map backend priority (1,2,3) to frontend priority (Low,Medium,High)
      const priorityMap: Record<number, 'High' | 'Medium' | 'Low'> = {
        1: 'Low',
        2: 'Medium',
        3: 'High'
      };

      setTitle(task.title);
      setDescription(task.description);
      setPriority(priorityMap[task.priority] || 'Medium');
      setDueDate(task.due_date || '');
      setCategory(task.category || '');
    } catch (err: any) {
      console.error('Error fetching task:', err);
      setError(err.message || 'Failed to fetch task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Map frontend priority (High,Medium,Low) to backend priority (3,2,1)
      const priorityMap: Record<'High' | 'Medium' | 'Low', number> = {
        'High': 3,
        'Medium': 2,
        'Low': 1
      };

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/tasks/${params.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies in the request
        body: JSON.stringify({
          title,
          description,
          priority: priorityMap[priority],
          due_date: dueDate,
          category
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - redirect to login
          // Clear any local user state
          // The HTTP-only cookie will be automatically cleared by the backend on logout
          router.push('/login');
          return;
        }
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update task');
      }

      // Redirect to dashboard on success
      router.push('/dashboard');
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && title === '') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
        <div className="w-8 h-8 border-4 border-coral-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-4">
      <div className="w-full max-w-2xl">
        <div className="backdrop-blur-xl bg-white/90 dark:bg-slate-900/90 rounded-2xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-coral-600 to-coral-700 bg-clip-text text-transparent mb-2">
              TodoApp
            </h1>
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">Edit Task</h2>
            <p className="text-gray-600 dark:text-gray-300">Update your task details</p>
          </div>

          {error && (
            <div className="mb-6 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Title <span className="text-red-500">*</span>
              </label>
              <input
                id="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter task title"
                required
                maxLength={200}
                className="w-full px-4 py-3 bg-white/80 dark:bg-slate-800/80 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-coral-500 focus:border-transparent transition-all duration-300"
              />
              <div className="text-right text-xs text-gray-500 mt-1">
                {title.length}/200
              </div>
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Description
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Enter task description"
                maxLength={1000}
                rows={4}
                className="w-full px-4 py-3 bg-white/80 dark:bg-slate-800/80 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-coral-500 focus:border-transparent transition-all duration-300 resize-y"
              />
              <div className="text-right text-xs text-gray-500 mt-1">
                {description.length}/1000
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="priority" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Priority <span className="text-red-500">*</span>
                </label>
                <select
                  id="priority"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value as 'High' | 'Medium' | 'Low')}
                  className="w-full px-4 py-3 bg-white/80 dark:bg-slate-800/80 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-coral-500 focus:border-transparent transition-all duration-300"
                >
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>

              <div>
                <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Due Date
                </label>
                <input
                  id="dueDate"
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="w-full px-4 py-3 bg-white/80 dark:bg-slate-800/80 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-coral-500 focus:border-transparent transition-all duration-300"
                />
              </div>
            </div>

            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Category/Tags
              </label>
              <input
                id="category"
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="Enter category or tags (comma-separated)"
                className="w-full px-4 py-3 bg-white/80 dark:bg-slate-800/80 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-coral-500 focus:border-transparent transition-all duration-300"
              />
            </div>

            <div className="flex justify-end space-x-4 pt-4">
              <button
                type="button"
                onClick={() => router.back()}
                className="px-6 py-3 bg-gray-300 text-gray-800 font-medium rounded-lg hover:bg-gray-400 transition-colors duration-300 flex items-center"
              >
                <X className="w-4 h-4 mr-2" />
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-gradient-to-r from-coral-600 to-coral-700 text-white font-semibold rounded-lg hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95 focus:ring-2 focus:ring-coral-300 focus:outline-none transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {loading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Saving...
                  </span>
                ) : (
                  <span className="flex items-center">
                    <Check className="w-4 h-4 mr-2" />
                    Update Task
                  </span>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditTaskPage;