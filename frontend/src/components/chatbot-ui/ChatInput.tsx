'use client';

import React, { useState } from 'react';

interface ChatInputProps {
  onSend: (text: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSend(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex space-x-2">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
        className="flex-1 bg-white/60 border border-white/40 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-coral-300 focus:border-coral-400 transition-all duration-200 placeholder-gray-400"
        aria-label="Type your message"
      />
      <button
        type="submit"
        disabled={!inputValue.trim()}
        className={`p-[10px] rounded-xl transition-all duration-300 focus:ring-2 focus:ring-coral-300 focus:outline-none ${
          inputValue.trim()
            ? 'bg-gradient-to-r from-coral-600 to-coral-700 text-white hover:shadow-xl hover:shadow-coral-500/30 hover:-translate-y-0.5 active:scale-95'
            : 'bg-gray-400 text-gray-200 cursor-not-allowed'
        }`}
        aria-label="Send message"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="w-5 h-5"
        >
          <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
        </svg>
      </button>
    </form>
  );
};

export default ChatInput;