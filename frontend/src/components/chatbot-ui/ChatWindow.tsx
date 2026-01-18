'use client';

import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import { Message } from './types';
import { chatAPI } from '../../services/api';

interface ChatWindowProps {
  userId?: string;
  onTaskChange?: () => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ userId, onTaskChange }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: 'Hello! I\'m your Todo Assistant. How can I help you today?',
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    // Check if user is authenticated
    if (!userId) {
      console.error('User not authenticated');
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'You must be logged in to use the chatbot.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      return;
    }

    // Add user message
    const userMessage: Message = {
      id: Date.now(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      // Prepare the message data
      const messageData: { message: string; conversation_id?: string } = {
        message: text
      };

      if (conversationId) {
        messageData.conversation_id = conversationId;
      }

      // Send the message to the backend API using the chatAPI service
      const response = await chatAPI.sendMessage(userId, messageData);

      // Extract the bot response, conversation ID, and action information
      const { response: botResponse, conversation_id: newConversationId, action } = response.data;

      // Update conversation ID if it's the first message in the conversation
      if (newConversationId && !conversationId) {
        setConversationId(newConversationId);
      }

      // Check if the action is task-related and trigger refresh callback
      if (action && action.type && typeof action.type === 'string' && action.type.startsWith('task_') && onTaskChange) {
        console.log('🔄 Task action detected:', action.type, 'Triggering task list refresh...');
        onTaskChange(); // Trigger task list refresh when chat modifies tasks
      }

      // Add bot response to messages
      const botMessage: Message = {
        id: Date.now() + 1,
        text: botResponse,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="flex flex-col h-full max-w-md mx-auto max-h-[70vh]">
      {/* Chat Header */}
      <div className="backdrop-blur-2xl bg-white/40 border border-white/60 rounded-t-3xl p-4 mb-0">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-coral-600 rounded-full"></div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Todo Assistant</h2>
            <p className="text-xs text-gray-600">Online • Ready to help</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto max-h-[calc(70vh-10rem)] p-4 space-y-4 bg-white/20 backdrop-blur-xl border-x border-white/60">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            text={message.text}
            sender={message.sender}
            timestamp={message.timestamp}
          />
        ))}

        {isTyping && (
          <div className="flex items-center space-x-2 ml-4">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
            <span className="text-sm text-gray-500">Typing...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="backdrop-blur-2xl bg-white/40 border border-white/60 rounded-b-3xl p-4 pt-3">
        <ChatInput onSend={handleSendMessage} />
      </div>
    </div>
  );
};

export default ChatWindow;