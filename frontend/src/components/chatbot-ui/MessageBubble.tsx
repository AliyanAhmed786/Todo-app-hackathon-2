'use client';

import React from 'react';
import { Message } from './types';

interface MessageBubbleProps {
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ text, sender, timestamp }) => {
  const isUser = sender === 'user';

  // Format timestamp
  const timeString = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-xl ${
          isUser
            ? 'bg-gradient-to-r from-coral-600 to-coral-700 text-white rounded-br-md'
            : 'backdrop-blur-xl bg-white/60 border border-white/60 text-gray-800 rounded-bl-md'
        }`}
      >
        <p className="text-sm">{text}</p>
        <p
          className={`text-xs mt-1 ${
            isUser ? 'text-white/80' : 'text-gray-500'
          }`}
        >
          {timeString}
        </p>
      </div>
    </div>
  );
};

export default MessageBubble;