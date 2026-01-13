// TaskForm component for creating and updating tasks
import React, { useState, useEffect, useCallback } from 'react';
import { taskAPI } from '../services/api';
import ToastNotification from './ToastNotification';

interface Task {
  id: number;
  title: string;
  description: string;
  status: boolean;
  category?: string;
  priority?: number;
  version?: number;
  created_at: string;
  updated_at: string;
}

interface TaskFormProps {
  taskId?: number; // Optional: if provided, it's an edit form
  onTaskSubmit?: () => void;
  onCancel?: () => void;
  initialData?: Task;
}

const TaskForm: React.FC<TaskFormProps> = ({ taskId, onTaskSubmit, onCancel, initialData }) => {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [category, setCategory] = useState(initialData?.category || '');
  const [priority, setPriority] = useState(initialData?.priority || 1);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [version, setVersion] = useState(initialData?.version || 1);
  const [toast, setToast] = useState({
    message: '',
    type: 'success' as 'success' | 'error' | 'info',
    visible: false
  });

  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title);
      setDescription(initialData.description);
      setCategory(initialData.category || '');
      setPriority(initialData.priority || 1);
      setVersion(initialData.version || 1);
    }
  }, [initialData]);

  const validateForm = useCallback(() => {
    if (!title.trim()) {
      setError('Title is required');
      return false;
    }

    if (title.length < 1 || title.length > 200) {
      setError('Title must be between 1 and 200 characters');
      return false;
    }

    if (description.length > 1000) {
      setError('Description must be no more than 1000 characters');
      return false;
    }

    return true;
  }, [title, description]);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setError('');

    try {
      if (taskId) {
        // Update existing task with version for optimistic locking
        await taskAPI.updateTask(taskId, {
          title,
          description,
          category,
          priority,
          version: version + 1  // Increment version for optimistic locking
        });
        setVersion(version + 1); // Update local version after successful update
        setToast({
          message: 'Task updated successfully',
          type: 'success',
          visible: true
        });
      } else {
        // Create new task
        await taskAPI.createTask({
          title,
          description,
          category,
          priority,
          version: 1  // Initialize version for new task
        });
        setToast({
          message: 'Task created successfully',
          type: 'success',
          visible: true
        });
      }

      // Reset form
      setTitle('');
      setDescription('');
      setCategory('');
      setPriority(1);
      setVersion(1); // Reset version for new tasks

      // Call the success callback
      if (onTaskSubmit) {
        onTaskSubmit();
      }
    } catch (err: any) {
      console.error('Task operation error:', err);

      // Handle optimistic locking conflict (409 Conflict)
      if (err.response?.status === 409) {
        setError('Task was modified by another user. Please refresh and try again.');
        setToast({
          message: 'Task was modified by another user. Please refresh and try again.',
          type: 'error',
          visible: true
        });
      } else {
        // Display proper error message for all other errors
        let errorMessage = 'Task operation failed. Please try again.';

        if (err.message === 'Network Error' || err.code === 'ERR_NETWORK') {
          errorMessage = 'Unable to connect to the backend server. Please ensure the backend is running on http://127.0.0.1:8000';
        } else if (err.response?.status === 401) {
          errorMessage = 'Session expired. Please log in again.';
        } else if (err.response?.status === 403) {
          errorMessage = 'Access denied. You can only modify your own tasks.';
        } else if (err.response?.data?.detail) {
          errorMessage = err.response.data.detail;
        }

        setError(errorMessage);
        setToast({
          message: errorMessage,
          type: 'error',
          visible: true
        });
      }
    } finally {
      setLoading(false);
    }
  }, [taskId, title, description, category, priority, version, onTaskSubmit, validateForm]);

  return (
    <div className="w-full backdrop-blur-2xl bg-white/40 p-4 sm:p-6 rounded-3xl border border-white/60 shadow-xl shadow-gray-900/10">
      <h2 className="text-xl font-bold text-gray-900 mb-4">
        {taskId ? 'Edit Task' : 'Create New Task'}
      </h2>

      <form onSubmit={handleSubmit}>
        {error && (
          <div className="backdrop-blur-xl bg-gradient-to-r from-red-100/60 to-red-200/60 border border-red-400/60 text-red-700 px-4 py-3 rounded-2xl relative mb-4 flex items-start" role="alert">
            <svg className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path>
            </svg>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <div className="relative">
            <input
              id="title"
              name="title"
              type="text"
              required
              className={`appearance-none block w-full px-4 py-3 bg-white/60 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 sm:text-sm transition-all duration-200 ${title ? (title.length >= 1 && title.length <= 200 ? 'focus:ring-green-300 focus:border-green-400' : 'focus:ring-red-300 focus:border-red-400') : ''
                } ${error && !title.trim() ? 'border-red-400/60 focus:ring-red-300 focus:border-red-400' : ''
                }`}
              placeholder="Task title (1-200 characters)"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              maxLength={200}
            />
            {title && (
              <div className={`absolute right-3 top-2.5 text-xs ${title.length > 200 ? 'text-red-500' : 'text-gray-500'
                }`}>
                {title.length}/200
              </div>
            )}
          </div>
          {title && title.length > 200 && (
            <p className="mt-1 text-xs text-red-600">Title must be no more than 200 characters</p>
          )}
        </div>

        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <div className="relative">
            <textarea
              id="description"
              name="description"
              rows={4}
              className="appearance-none block w-full px-4 py-3 bg-white/60 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 sm:text-sm transition-all duration-200"
              placeholder="Task description (optional, up to 1000 characters)"
              value={description}
              onChange={(e) => {
                setDescription(e.target.value);
              }}
              maxLength={1000}
            />
            {description && (
              <div className="absolute right-3 bottom-2 text-xs text-gray-500">
                {description.length}/1000
              </div>
            )}
          </div>
          {description && description.length > 1000 && (
            <p className="mt-1 text-xs text-red-600">Description must be no more than 1000 characters</p>
          )}
        </div>

        <div className="mb-4">
          <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <input
            id="category"
            name="category"
            type="text"
            className="appearance-none block w-full px-4 py-3 bg-white/60 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 sm:text-sm transition-all duration-200"
            placeholder="Task category (optional)"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
        </div>

        <div className="mb-4">
          <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            className="appearance-none block w-full px-4 py-3 bg-white/60 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 sm:text-sm transition-all duration-200"
            value={priority}
            onChange={(e) => setPriority(Number(e.target.value))}
          >
            <option value={3}>High (P1)</option>
            <option value={2}>Medium (P2)</option>
            <option value={1}>Low (P3)</option>
          </select>
          <div className="mt-1 text-xs text-gray-500">
            Priority levels: High (Red), Medium (Amber), Low (Green)
          </div>
        </div>

        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-2 sm:space-y-0">
          <div>
            {taskId && onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="w-full sm:w-auto backdrop-blur-xl bg-white/60 text-gray-700 py-2.5 px-4 rounded-xl border border-white/60 hover:bg-white/80 hover:border-white/80 transition-all duration-300 shadow-lg shadow-gray-900/5 focus:ring-2 focus:ring-coral-300 focus:outline-none flex items-center justify-center"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                Cancel
              </button>
            )}
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className={`w-full sm:w-auto p-[10px] flex items-center justify-center ${loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-coral-600 to-coral-700 hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95'
                } text-white rounded-xl transition-all duration-300 focus:ring-2 focus:ring-coral-300 focus:outline-none`}
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {taskId ? 'Updating...' : 'Creating...'}
                </>
              ) : (
                taskId ? 'Update Task' : 'Create Task'
              )}
            </button>
          </div>
        </div>
      </form>

      <ToastNotification
        message={toast.message}
        type={toast.type}
        visible={toast.visible}
        onClose={() => setToast({ ...toast, visible: false })}
      />
    </div>
  );
};

export default TaskForm;
