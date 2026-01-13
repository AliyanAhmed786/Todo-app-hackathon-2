// DeleteConfirmationModal component with glassmorphic styling
import React from 'react';
import Modal from './Modal';

interface DeleteConfirmationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  taskTitle: string;
  loading?: boolean;
}

const DeleteConfirmationModal: React.FC<DeleteConfirmationModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  taskTitle,
  loading = false
}) => {
  const handleConfirm = () => {
    onConfirm();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Confirm Deletion">
      <div className="text-center">
        <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100/80 backdrop-blur-sm">
          <svg
            className="h-6 w-6 text-red-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
        </div>
        <h3 className="mt-4 text-lg font-medium text-gray-900">
          Are you sure?
        </h3>
        <p className="mt-2 text-sm text-gray-600">
          You are about to delete the task <span className="font-semibold">"{taskTitle}"</span>. This action cannot be undone.
        </p>
        <div className="mt-6 flex justify-center space-x-4">
          <button
            type="button"
            className="p-[10px] backdrop-blur-xl bg-white/60 text-gray-700 text-sm font-semibold rounded-xl border border-white/60 hover:bg-white/80 hover:border-white/80 transition-all duration-300 shadow-lg shadow-gray-900/5 focus:ring-2 focus:ring-coral-300 focus:outline-none"
            onClick={onClose}
          >
            Cancel
          </button>
          <button
            type="button"
            className={`p-[10px] text-white text-sm font-semibold rounded-xl transition-all duration-300 focus:ring-2 focus:ring-coral-300 focus:outline-none ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-red-500 to-red-600 hover:shadow-xl hover:shadow-red-500/30 hover:-translate-y-0.5 active:scale-95'
            }`}
            onClick={handleConfirm}
            disabled={loading}
          >
            {loading ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default DeleteConfirmationModal;
