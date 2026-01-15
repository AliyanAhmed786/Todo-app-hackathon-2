'use client';

import React, { useState } from 'react';
import ChatWindow from './ChatWindow';
import { ChatBotProps } from './types';

const ChatBot: React.FC<ChatBotProps> = ({ isOpen: propIsOpen, onClose, position = "bottom-6 right-6" }) => {
  const [isOpen, setIsOpen] = useState(propIsOpen || false);

  const toggleChat = () => {
    const newOpenState = !isOpen;
    setIsOpen(newOpenState);
    if (onClose && !newOpenState) {
      onClose();
    }
  };

  if (propIsOpen !== undefined) {
    // Controlled component
    if (!propIsOpen) return null;
    return (
      <div className={`fixed ${position} z-50 w-full max-w-md`}>
        <div className="backdrop-blur-2xl bg-white/40 border border-white/60 rounded-3xl shadow-xl shadow-gray-900/10 overflow-hidden">
          <ChatWindow />
        </div>
      </div>
    );
  }

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className={`fixed ${position} z-50 p-4 bg-gradient-to-r from-coral-600 to-coral-700 text-white rounded-full shadow-xl shadow-coral-500/30 hover:shadow-2xl hover:shadow-coral-500/40 transition-all duration-300 focus:ring-2 focus:ring-coral-300 focus:outline-none`}
          aria-label="Open chat"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            className="w-6 h-6"
          >
            <path fillRule="evenodd" d="M4.804 21.644A6.707 6.707 0 006 21.75a6.721 6.721 0 003.583-1.029c.774.182 1.584.279 2.417.279 5.322 0 9.75-3.97 9.75-9 0-5.03-4.428-9-9.75-9s-9.75 3.97-9.75 9c0 2.409 1.025 4.587 2.674 6.192.232.226.277.428.254.543a3.73 3.73 0 01-.814 1.686.75.75 0 00.44 1.223zM8.25 10.875a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25zM10.875 12a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0zm4.875-1.125a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25z" clipRule="evenodd" />
          </svg>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className={`fixed ${position} z-50 w-full max-w-md`}>
          <div className="backdrop-blur-2xl bg-white/40 border border-white/60 rounded-3xl shadow-xl shadow-gray-900/10 overflow-hidden">
            <div className="flex justify-between items-center p-4 border-b border-white/60">
              <h3 className="font-semibold text-gray-900">Todo Assistant</h3>
              <button
                onClick={toggleChat}
                className="text-gray-500 hover:text-gray-700 transition-colors"
                aria-label="Close chat"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  className="w-5 h-5"
                >
                  <path fillRule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
            <ChatWindow />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatBot;