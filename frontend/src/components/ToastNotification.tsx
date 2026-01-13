// ToastNotification component for displaying success/error messages
import React, { useEffect } from 'react';

interface ToastNotificationProps {
  message: string;
  type: 'success' | 'error' | 'info';
  visible: boolean;
  onClose: () => void;
}

const ToastNotification: React.FC<ToastNotificationProps> = ({
  message,
  type,
  visible,
  onClose
}) => {
  useEffect(() => {
    if (visible) {
      const timer = setTimeout(() => {
        onClose();
      }, 5000); // Auto-hide after 5 seconds

      return () => clearTimeout(timer);
    }
  }, [visible, onClose]);

  if (!visible) return null;

  const getToastStyle = () => {
    switch (type) {
      case 'success':
        return 'bg-gradient-to-r from-green-500/90 to-green-600/90 text-white';
      case 'error':
        return 'bg-gradient-to-r from-red-500/90 to-red-600/90 text-white';
      case 'info':
        return 'bg-gradient-to-r from-blue-500/90 to-blue-600/90 text-white';
      default:
        return 'bg-gradient-to-r from-gray-500/90 to-gray-600/90 text-white';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50">
      <div className={`backdrop-blur-xl ${getToastStyle()} p-4 rounded-xl shadow-xl shadow-gray-900/20 border border-white/20 max-w-sm`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            {type === 'success' && (
              <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            )}
            {type === 'error' && (
              <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            )}
            {type === 'info' && (
              <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            )}
            <span className="font-medium">{message}</span>
          </div>
          <button
            onClick={onClose}
            className="ml-4 text-white/80 hover:text-white"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ToastNotification;
