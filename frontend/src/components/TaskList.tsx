import React, { useState, useEffect, useImperativeHandle, forwardRef } from 'react';
import { CheckCircle, Edit3, Trash2, Plus, Calendar, Check, X } from 'lucide-react';
import { taskAPI } from '../services/api';
import TaskEditModal from './TaskEditModal';

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: 'High' | 'Medium' | 'Low';
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
  metaData?: any; // Preserve backend meta_data field for AI context
}

interface TaskListProps {
  onTaskChange?: (updatedTasks: Task[]) => void; // Callback to notify parent when tasks are modified
  onTaskAction?: () => Promise<void>; // Function to fetch dashboard stats from parent (renamed prop)
}

export interface TaskListRef {
  refreshTasks: () => Promise<void>;
}

const TaskList = forwardRef<TaskListRef, TaskListProps>(({ onTaskChange, onTaskAction }, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFilter, setSelectedFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  // Expose refreshTasks function to parent component via ref
  useImperativeHandle(ref, () => ({
    refreshTasks: fetchTasks
  }));

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await taskAPI.getTasks();
      // Handle different response formats - API might return tasks in a 'tasks' property or directly as an array
      const tasksData = Array.isArray(response.data) ? response.data : (response.data.tasks || []);
      const transformedTasks = tasksData.map((task: any) => ({
        id: String(task.id), // Ensure ID remains as string for Better Auth compatibility
        title: task.title,
        description: task.description || '',
        completed: task.status,
        priority: task.priority === 3 ? 'High' : task.priority === 2 ? 'Medium' : 'Low', // Fixed mapping: 3=High, 2=Medium, 1=Low
        dueDate: task.due_date,
        createdAt: task.created_at,
        updatedAt: task.updated_at,
        metaData: task.meta_data // Preserve backend meta_data field for AI context
      }));
      setTasks(transformedTasks);
    } catch (err: any) {
      setError('Failed to fetch tasks. Please try again.');
      setTasks([]); // Set to empty array on error
    } finally {
      setLoading(false);
    }
  };

  // Filter and search tasks
  const filteredTasks = tasks.filter(task => {
    const matchesFilter = selectedFilter === 'all' ||
      (selectedFilter === 'completed' && task.completed) ||
      (selectedFilter === 'pending' && !task.completed);

    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.description.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  const toggleTaskCompletion = async (taskId: string, currentStatus: boolean) => {
    // Optimistic update: update UI immediately
    const updatedTasks = tasks.map(task =>
      task.id === taskId ? { ...task, completed: !currentStatus } : task
    );
    setTasks(updatedTasks);

    try {
      // Find the task to get its details
      const task = tasks.find(t => t.id === taskId);
      if (!task) {
        throw new Error('Task not found');
      }

      // Map frontend priority (High,Medium,Low) to backend priority (3,2,1)
      const priorityMap: Record<'High' | 'Medium' | 'Low', number> = {
        'High': 3,  // Backend expects High = 3
        'Medium': 2, // Backend expects Medium = 2
        'Low': 1     // Backend expects Low = 1
      };

      // Use string taskId for Better Auth compatibility (don't convert to Number)
      const response = await taskAPI.updateTask(taskId, {
        title: task.title,
        description: task.description,
        status: !currentStatus,
        priority: priorityMap[task.priority]
      });

      // Update local state (in case the API response has different data)
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === taskId ? { ...task, completed: !currentStatus } : task
      ));

      // CRITICAL: Pass updated tasks to parent for optimistic stats update
      if (onTaskChange) {
        onTaskChange(updatedTasks);
      }

      // Backend validation - refresh stats from API
      if (onTaskAction) {
        await onTaskAction();
      }
    } catch (err: any) {
      // Rollback the optimistic update on error
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, completed: currentStatus } : task
      ));

      // Set specific error message for 422 status (Unprocessable Entity)
      if (err?.response?.status === 422) {
        setError('ID type mismatch error. Please try again.');
      } else {
        setError('Failed to update task. Please try again.');
      }

      console.error('Error toggling task completion:', err);

      // Only refetch tasks on error to prevent UI flickering on success
      await fetchTasks();
    }
  };

  const deleteTask = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    // Validate task ID (keep as string for Better Auth compatibility)
    if (!taskId) {
      console.error('Invalid task ID provided for deletion:', taskId);
      setError('Invalid task ID. Cannot delete task.');
      return;
    }

    // Diagnostic logging
    console.log('\n🗑️ DELETE ATTEMPT:');
    console.log('  Task ID:', taskId, '(type:', typeof taskId + ')');

    // Keep reference for potential rollback
    const taskBeforeDelete = tasks.find(task => task.id === taskId);

    try {
      // Use string taskId for Better Auth compatibility (don't convert to Number)
      const response = await taskAPI.deleteTask(taskId);
      console.log('✅ DELETE SUCCESS:');
      console.log('  Status:', response.status);
      console.log('  Data:', response.data);

      // Only remove from UI after successful deletion
      const updatedTasks = tasks.filter(task => task.id !== taskId);
      setTasks(updatedTasks);

      // Consolidate update operations to prevent race conditions
      await consolidateUpdates(updatedTasks);
    } catch (err: any) {
      // Detailed error logging
      console.error('\n❌ DELETE ERROR:');
      console.error('  Task ID:', taskId);
      console.error('  Status:', err?.response?.status);
      console.error('  Status Text:', err?.response?.statusText);
      console.error('  Error Data:', err?.response?.data);
      console.error('  Error Message:', err.message);
      console.error('  Error Type:', err.code);
      console.error('  Task Existed:', !!taskBeforeDelete);

      // Set specific error message for 422 status (Unprocessable Entity)
      if (err?.response?.status === 422) {
        setError('ID type mismatch error. Please try again.');
      } else {
        setError('Failed to delete task. Please try again.');
      }

      console.error('Error deleting task:', err);
    }
  };

  const openTaskModal = (task: Task) => {
    setSelectedTask(task);
    setIsModalOpen(true);
  };

  const closeTaskModal = () => {
    setIsModalOpen(false);
    setSelectedTask(null);
  };

  // Consolidate update operations to prevent race conditions
  const consolidateUpdates = async (updatedTasks: Task[]) => {
    // Only fetch tasks once to update the UI
    await fetchTasks();

    // Pass updated tasks to parent for optimistic stats update
    if (onTaskChange) {
      onTaskChange(updatedTasks);
    }

    // Backend validation - refresh stats from API
    if (onTaskAction) {
      await onTaskAction();
    }
  };

  const handleTaskUpdate = async (updatedTask: Task) => {
    const updatedTasks = tasks.map(task =>
      task.id === updatedTask.id ? updatedTask : task
    );
    setTasks(updatedTasks);

    // Refresh tasks and stats after modal update
    await fetchTasks();

    // Pass updated tasks to parent for optimistic stats update
    if (onTaskChange) {
      onTaskChange(updatedTasks);
    }

    // Backend validation
    if (onTaskAction) {
      await onTaskAction();
    }
  };

  const handleTaskDelete = async (taskId: string) => {
    // Validate task ID (keep as string for Better Auth compatibility)
    if (!taskId) {
      console.error('Invalid task ID provided for deletion:', taskId);
      setError('Invalid task ID. Cannot delete task.');
      return;
    }

    const updatedTasks = tasks.filter(task => task.id !== taskId);
    setTasks(updatedTasks);

    // Use consolidated updates to prevent race conditions
    await consolidateUpdates(updatedTasks);
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="w-8 h-8 border-4 border-coral-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
        <div className="flex items-center justify-between">
          <span>{error}</span>
          <button
            onClick={fetchTasks}
            className="ml-4 px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filter buttons */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => setSelectedFilter('all')}
          className={`px-5 py-2.5 rounded-xl font-semibold transition-all duration-300 ${selectedFilter === 'all'
            ? 'bg-gradient-to-r from-coral-600 to-coral-700 text-white shadow-lg shadow-coral-500/30 hover:shadow-xl hover:-translate-y-0.5'
            : 'backdrop-blur-xl bg-white/50 text-gray-700 hover:bg-white/70 border border-white/40'
            }`}
        >
          All
        </button>
        <button
          onClick={() => setSelectedFilter('pending')}
          className={`px-5 py-2.5 rounded-xl font-semibold transition-all duration-300 ${selectedFilter === 'pending'
            ? 'bg-gradient-to-r from-coral-600 to-coral-700 text-white shadow-lg shadow-coral-500/30 hover:shadow-xl hover:-translate-y-0.5'
            : 'backdrop-blur-xl bg-white/50 text-gray-700 hover:bg-white/70 border border-white/40'
            }`}
        >
          Pending
        </button>
        <button
          onClick={() => setSelectedFilter('completed')}
          className={`px-5 py-2.5 rounded-xl font-semibold transition-all duration-300 ${selectedFilter === 'completed'
            ? 'bg-gradient-to-r from-coral-600 to-coral-700 text-white shadow-lg shadow-coral-500/30 hover:shadow-xl hover:-translate-y-0.5'
            : 'backdrop-blur-xl bg-white/50 text-gray-700 hover:bg-white/70 border border-white/40'
            }`}
        >
          Completed
        </button>
      </div>

      {/* Search bar */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search tasks..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-3 backdrop-blur-xl bg-white/50 border border-white/40 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-coral-400 focus:border-coral-400 focus:bg-white/60 transition-all duration-200"
        />
      </div>

      {/* Task grid */}
      <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-8">
        {filteredTasks.length > 0 ? (
          filteredTasks.map((task) => (
            <div
              key={task.id}
              className={`backdrop-blur-2xl bg-white/40 rounded-2xl p-6 shadow-xl hover:shadow-2xl hover:scale-[1.03] transition-all duration-300 ${task.completed
                ? 'border-2 border-green-400/50 opacity-75'
                : 'border-2 border-coral-400/50 hover:border-coral-500/70'
                }`}
            >
              <div className="flex items-start">
                {/* Checkbox */}
                <button
                  onClick={() => toggleTaskCompletion(task.id, task.completed)}
                  className="min-h-[44px] min-w-[44px] flex items-center justify-center mr-3 mt-1"
                  aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
                >
                  {task.completed ? (
                    <CheckCircle className="w-6 h-6 text-green-600" />
                  ) : (
                    <div className="w-6 h-6 border-2 border-gray-400 rounded-full" />
                  )}
                </button>

                <div
                  className="flex-1 cursor-pointer"
                  onClick={() => openTaskModal(task)}
                >
                  <h3
                    className={`font-bold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900 dark:text-coral-500'
                      }`}
                  >
                    {task.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-500 text-sm line-clamp-3 mt-1">
                    {task.description}
                  </p>

                  <div className="flex items-center justify-between mt-3">
                    {/* Priority badge */}
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${task.priority === 'High'
                        ? 'bg-red-600 text-white'
                        : task.priority === 'Medium'
                          ? 'bg-yellow-600 text-white'
                          : 'bg-green-600 text-white'
                        }`}
                    >
                      {task.priority}
                    </span>

                    {/* Due date */}
                    {task.dueDate && (
                      <div className="flex items-center text-xs text-gray-500">
                        <Calendar className="w-3 h-3 mr-1" />
                        {new Date(task.dueDate).toLocaleDateString('en-US', {
                          month: '2-digit',
                          day: '2-digit',
                          year: 'numeric',
                        })}
                      </div>
                    )}
                  </div>
                </div>

                {/* Action buttons */}
                <div className="flex flex-col space-y-2 ml-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation(); // Prevent triggering the card click
                      openTaskModal(task);
                    }}
                    className="min-h-[44px] min-w-[44px] flex items-center justify-center text-coral-600 hover:text-coral-700 backdrop-blur-xl bg-coral-50/50 rounded-full hover:bg-coral-100/70 transition-all duration-200"
                    aria-label="Edit task"
                  >
                    <Edit3 className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => deleteTask(task.id)}
                    className="min-h-[44px] min-w-[44px] flex items-center justify-center text-red-600 hover:text-red-700 backdrop-blur-xl bg-red-50/50 rounded-full hover:bg-red-100/70 transition-all duration-200"
                    aria-label="Delete task"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center py-8">
            <p className="text-gray-600 dark:text-gray-400">No tasks found</p>
          </div>
        )}
      </div>

      {/* Add Task Button */}
      <div className="fixed bottom-8 right-8">
        <button
          onClick={() => window.location.href = '/dashboard/create'}
          className="min-h-14 min-w-14 bg-gradient-to-r from-coral-600 to-coral-700 text-white rounded-full flex items-center justify-center shadow-2xl shadow-coral-500/40 hover:scale-110 hover:shadow-3xl hover:shadow-coral-500/50 transition-all duration-300 active:scale-95"
          aria-label="Add new task"
        >
          <Plus className="w-6 h-6" />
        </button>
      </div>

      {/* Task Edit Modal */}
      {selectedTask && (
        <TaskEditModal
          task={selectedTask}
          isOpen={isModalOpen}
          onClose={closeTaskModal}
          onTaskUpdate={handleTaskUpdate}
          onTaskDelete={handleTaskDelete}
        />
      )}
    </div>
  );
});

export default TaskList;
