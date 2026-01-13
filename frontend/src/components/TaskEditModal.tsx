import React, { useState, useEffect } from 'react';
import Modal from './Modal';
import { taskAPI } from '../services/api';

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: 'High' | 'Medium' | 'Low';
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
}

interface TaskEditModalProps {
  task: Task;
  isOpen: boolean;
  onClose: () => void;
  onTaskUpdate: (updatedTask: Task) => void;
  onTaskDelete: (taskId: string) => void;
}

const TaskEditModal: React.FC<TaskEditModalProps> = ({
  task,
  isOpen,
  onClose,
  onTaskUpdate,
  onTaskDelete
}) => {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description);
  const [priority, setPriority] = useState<'High' | 'Medium' | 'Low'>(task.priority);
  const [dueDate, setDueDate] = useState(task.dueDate || '');
  const [completed, setCompleted] = useState(task.completed);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      setTitle(task.title);
      setDescription(task.description);
      setPriority(task.priority);
      setDueDate(task.dueDate || '');
      setCompleted(task.completed);
    }
  }, [task, isOpen]);

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

      const response = await taskAPI.updateTask(parseInt(task.id, 10), {
        title,
        description,
        status: completed,
        priority: priorityMap[priority],
        due_date: dueDate
      });

      onTaskUpdate({
        ...task,
        title,
        description,
        completed,
        priority,
        dueDate,
        updatedAt: response.data.updated_at || new Date().toISOString()
      });
      onClose();
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    // Validate task ID before conversion
    if (!task.id || isNaN(parseInt(task.id, 10)) || parseInt(task.id, 10) <= 0) {
      console.error('Invalid task ID provided for deletion:', task.id);
      setError('Invalid task ID. Cannot delete task.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await taskAPI.deleteTask(parseInt(task.id, 10));

      onTaskDelete(task.id);
      onClose();
    } catch (err: any) {
      console.error('Error deleting task:', err);
      setError(err.message || 'Failed to delete task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleCompletion = async () => {
    const newCompletedStatus = !completed;
    setCompleted(newCompletedStatus);

    try {
      // Map frontend priority (High,Medium,Low) to backend priority (3,2,1)
      const priorityMap: Record<'High' | 'Medium' | 'Low', number> = {
        'High': 3,
        'Medium': 2,
        'Low': 1
      };

      const response = await taskAPI.updateTask(parseInt(task.id, 10), {
        title,
        description,
        status: newCompletedStatus,
        priority: priorityMap[priority],
        due_date: dueDate
      });

      onTaskUpdate({
        ...task,
        completed: newCompletedStatus,
        updatedAt: response.data.updated_at || new Date().toISOString()
      });
    } catch (err) {
      console.error('Error updating task completion:', err);
      setCompleted(!newCompletedStatus); // Revert the UI change on error
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Edit Task">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="backdrop-blur-xl bg-red-100/80 border border-red-400/60 text-red-700 px-4 py-3 rounded-2xl relative mb-4" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <div className="flex items-center mb-4">
          <button
            type="button"
            onClick={toggleCompletion}
            className={`min-h-[44px] min-w-[44px] flex items-center justify-center mr-3 ${completed ? 'text-green-600' : 'text-gray-400'
              }`}
            aria-label={completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            {completed ? (
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            ) : (
              <div className="w-6 h-6 border-2 border-gray-400 rounded-full" />
            )}
          </button>
          <h2 className={`text-xl font-bold ${completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {title}
          </h2>
        </div>

        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title
          </label>
          <input
            id="title"
            name="title"
            type="text"
            required
            className="appearance-none block w-full px-3 py-3 bg-white/60 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 sm:text-sm"
            placeholder="Task title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            rows={4}
            className="appearance-none block w-full px-3 py-3 bg-white/60 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 sm:text-sm"
            placeholder="Task description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              id="priority"
              name="priority"
              className="appearance-none block w-full px-3 py-3 bg-white/60 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 sm:text-sm"
              value={priority}
              onChange={(e) => setPriority(e.target.value as 'High' | 'Medium' | 'Low')}
            >
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>

          <div>
            <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-1">
              Due Date
            </label>
            <input
              id="dueDate"
              type="date"
              className="appearance-none block w-full px-3 py-3 bg-white/60 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 sm:text-sm"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
          </div>
        </div>

        <div className="flex justify-between pt-4">
          <button
            type="button"
            onClick={handleDelete}
            disabled={loading}
            className="px-4 py-2.5 backdrop-blur-xl bg-gradient-to-r from-red-500/80 to-red-600/80 border border-red-300/40 text-white rounded-xl hover:shadow-xl hover:shadow-red-500/30 hover:-translate-y-0.5 active:scale-95 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed focus:ring-2 focus:ring-red-300 focus:outline-none"
          >
            Delete
          </button>

          <div className="flex space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 backdrop-blur-xl bg-white/60 text-gray-700 rounded-xl border border-white/60 hover:bg-white/80 hover:border-white/80 transition-all duration-300 shadow-lg shadow-gray-900/5 focus:ring-2 focus:ring-coral-300 focus:outline-none"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className={`px-4 py-2.5 text-white rounded-xl transition-all duration-300 focus:ring-2 focus:ring-coral-300 focus:outline-none ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-coral-600 to-coral-700 hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95'
                }`}
            >
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      </form>
    </Modal>
  );
};

export default TaskEditModal;
