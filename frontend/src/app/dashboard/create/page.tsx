'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Check, X } from 'lucide-react';
import { taskAPI } from '../../../services/api'; // Import the API service

const CreateTaskPage = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'High' | 'Medium' | 'Low'>('Medium');
  const [dueDate, setDueDate] = useState('');
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Use the taskAPI service which has proper authentication configuration
      // The API service is already configured with withCredentials: true
      // which will automatically send the Better Auth session cookie
      await taskAPI.createTask({
        title,
        description,
        category,
        priority: priority === 'High' ? 3 : priority === 'Medium' ? 2 : 1
        // Note: due_date is not supported in task creation, only in updates
      });

      router.push('/dashboard');
    } catch (err: any) {
      console.error('Error creating task:', err);

      // Handle authentication errors specifically
      if (err.response?.status === 401 || err.response?.status === 403) {
        // Redirect to login if authentication fails
        router.push('/login');
        return;
      } else if (err.message === 'Network Error' || err.code === 'ERR_NETWORK') {
        setError('Cannot connect to server. Ensure backend is running.');
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError(err.message || 'Failed to create task.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden p-4">
      {/* Animated Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
        {/* Animated Gradient Blobs */}
        <div className="absolute top-0 -left-4 w-72 h-72 bg-gradient-to-br from-coral-400 to-coral-600 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
        <div className="absolute top-0 -right-4 w-72 h-72 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
      </div>

      {/* Main Content */}
      <div className="w-full max-w-2xl relative z-10">
        <div className="backdrop-blur-2xl bg-white/30 rounded-3xl border border-white/50 shadow-2xl shadow-black/10 p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-coral-600 to-coral-700 bg-clip-text text-transparent mb-2 drop-shadow-sm">
              TodoApp
            </h1>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-coral-600 via-coral-700 to-coral-800 bg-clip-text text-transparent mb-2">Create New Task</h2>
            <p className="text-gray-600 font-medium">Add a new task to your list</p>
          </div>

          {error && (
            <div className="mb-6 backdrop-blur-xl bg-gradient-to-r from-red-100/70 to-red-200/70 border border-red-400/50 text-red-700 px-4 py-3 rounded-2xl relative flex items-start shadow-lg">
              <svg className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path>
              </svg>
              <span className="block sm:inline font-medium">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="title" className="block text-sm font-semibold text-gray-700 mb-2">
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
                className="w-full px-4 py-3 bg-white/50 backdrop-blur-md border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-400 focus:border-coral-400 focus:bg-white/60 transition-all duration-200"
              />
              <div className="text-right text-xs text-gray-500 mt-1 font-medium">
                {title.length}/200
              </div>
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-semibold text-gray-700 mb-2">
                Description
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Enter task description"
                maxLength={1000}
                rows={4}
                className="w-full px-4 py-3 bg-white/50 backdrop-blur-md border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-400 focus:border-coral-400 focus:bg-white/60 transition-all duration-200 resize-y"
              />
              <div className="text-right text-xs text-gray-500 mt-1 font-medium">
                {description.length}/1000
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="priority" className="block text-sm font-semibold text-gray-700 mb-2">
                  Priority <span className="text-red-500">*</span>
                </label>
                <select
                  id="priority"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value as 'High' | 'Medium' | 'Low')}
                  className="w-full px-4 py-3 bg-white/50 backdrop-blur-md border border-white/40 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-coral-400 focus:border-coral-400 focus:bg-white/60 transition-all duration-200"
                >
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>

              <div>
                <label htmlFor="dueDate" className="block text-sm font-semibold text-gray-700 mb-2">
                  Due Date
                </label>
                <input
                  id="dueDate"
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="w-full px-4 py-3 bg-white/50 backdrop-blur-md border border-white/40 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-coral-400 focus:border-coral-400 focus:bg-white/60 transition-all duration-200"
                />
              </div>
            </div>

            <div>
              <label htmlFor="category" className="block text-sm font-semibold text-gray-700 mb-2">
                Category/Tags
              </label>
              <input
                id="category"
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="Enter category or tags (comma-separated)"
                className="w-full px-4 py-3 bg-white/50 backdrop-blur-md border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-400 focus:border-coral-400 focus:bg-white/60 transition-all duration-200"
              />
            </div>

            <div className="flex justify-end space-x-4 pt-4">
              <button
                type="button"
                onClick={() => router.back()}
                className="px-6 py-3 backdrop-blur-xl bg-white/50 text-gray-700 font-semibold rounded-xl border border-white/50 hover:bg-white/70 hover:border-white/70 hover:shadow-lg transition-all duration-300 focus:ring-2 focus:ring-coral-300 focus:outline-none flex items-center"
              >
                <X className="w-4 h-4 mr-2" />
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-gradient-to-r from-coral-600 to-coral-700 text-white font-semibold rounded-xl hover:shadow-2xl hover:shadow-coral-500/40 hover:-translate-y-0.5 active:scale-95 focus:ring-2 focus:ring-coral-300 focus:outline-none transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
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
                    Save Task
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

export default CreateTaskPage;
