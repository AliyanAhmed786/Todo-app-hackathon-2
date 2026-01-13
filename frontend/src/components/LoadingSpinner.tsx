// LoadingSpinner component for loading states
import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 'md', text }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  return (
    <div className="flex flex-col items-center justify-center py-8 backdrop-blur-xl bg-white/40 rounded-3xl border border-white/60 shadow-xl shadow-gray-900/10 p-8">
      <div className={`${sizeClasses[size]} border-4 border-t-coral-600 border-r-coral-600 border-b-transparent border-l-transparent rounded-full animate-spin`}></div>
      {text && <p className="mt-4 text-gray-700 font-medium">{text}</p>}
    </div>
  );
};

export default LoadingSpinner;
