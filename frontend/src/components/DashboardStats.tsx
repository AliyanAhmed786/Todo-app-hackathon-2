import React from 'react';
import { CheckCircle, CheckCircle2, Clock } from 'lucide-react';

interface DashboardStatsProps {
  totalTasks: number;
  completedTasks: number;
  pendingTasks: number;
}

const DashboardStats: React.FC<DashboardStatsProps> = ({
  totalTasks,
  completedTasks,
  pendingTasks
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {/* Total Tasks Card */}
      <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md rounded-xl p-6 shadow-lg hover:scale-105 hover:shadow-2xl transition-all duration-300">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">Total Tasks</h3>
          <div className="p-2 rounded-full bg-coral-100/60 dark:bg-coral-900/60" aria-hidden="true">
            <CheckCircle className="w-5 h-5 text-coral-600 dark:text-coral-400" />
          </div>
        </div>
        <p className="text-4xl font-bold text-coral-600 dark:text-coral-400 mb-3">
          {totalTasks}
        </p>
        <div className="w-full bg-gray-200/50 dark:bg-gray-700/50 rounded-full h-2.5">
          <div
            className="bg-gradient-to-r from-coral-400 to-coral-600 h-2.5 rounded-full"
            style={{ width: totalTasks > 0 ? '100%' : '0%' }}
            aria-hidden="true"
          ></div>
        </div>
      </div>

      {/* Completed Tasks Card */}
      <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md rounded-xl p-6 shadow-lg hover:scale-105 hover:shadow-2xl transition-all duration-300">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">Completed</h3>
          <div className="p-2 rounded-full bg-green-100/60 dark:bg-green-900/60" aria-hidden="true">
            <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />
          </div>
        </div>
        <p className="text-4xl font-bold text-green-600 dark:text-green-400 mb-3">
          {completedTasks}
        </p>
        <div className="w-full bg-gray-200/50 dark:bg-gray-700/50 rounded-full h-2.5">
          <div
            className="bg-gradient-to-r from-green-400 to-green-600 h-2.5 rounded-full"
            style={{
              width: totalTasks > 0
                ? `${(completedTasks / totalTasks) * 100}%`
                : '0%'
            }}
            aria-hidden="true"
          ></div>
        </div>
      </div>

      {/* Pending Tasks Card */}
      <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md rounded-xl p-6 shadow-lg hover:scale-105 hover:shadow-2xl transition-all duration-300">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">Pending</h3>
          <div className="p-2 rounded-full bg-blue-100/60 dark:bg-blue-900/60" aria-hidden="true">
            <Clock className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
        </div>
        <p className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-3">
          {pendingTasks}
        </p>
        <div className="w-full bg-gray-200/50 dark:bg-gray-700/50 rounded-full h-2.5">
          <div
            className="bg-gradient-to-r from-blue-400 to-blue-600 h-2.5 rounded-full"
            style={{
              width: totalTasks > 0
                ? `${(pendingTasks / totalTasks) * 100}%`
                : '0%'
            }}
            aria-hidden="true"
          ></div>
        </div>
      </div>
    </div>
  );
};

export default DashboardStats;
