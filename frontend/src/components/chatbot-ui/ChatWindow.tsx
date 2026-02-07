'use client';

import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import { Message } from './types';
import { chatAPI } from '../../services/api';

interface ChatWindowProps {
  userId: string;
  onTaskChange?: () => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ userId, onTaskChange }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello! I'm your Todo Assistant. How can I help you today?",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize conversation for new or existing users
  useEffect(() => {
    const initializeConversation = async () => {
      if (!userId) return;

      let savedConversationId = sessionStorage.getItem('chatbot_conversation_id');

      if (savedConversationId) {
        setConversationId(savedConversationId);
        loadConversationHistory(savedConversationId);
      } else {
        try {
          // Create a new conversation by sending an init message
          const response = await chatAPI.sendMessage(userId, { message: 'init' });
          const newConversationId = response.data.conversation_id;

          if (newConversationId) {
            setConversationId(newConversationId);
            sessionStorage.setItem('chatbot_conversation_id', newConversationId);

            // Optionally load empty history for consistency
            loadConversationHistory(newConversationId);
          }
        } catch (err) {
          console.error('Error initializing conversation for new user:', err);
        }
      }
    };

    initializeConversation();
  }, [userId]);

  // Load conversation history from backend
  const loadConversationHistory = async (convId: string) => {
    if (!userId) {
      console.error('Cannot load conversation history: User not authenticated');
      return;
    }

    try {
      console.log('Loading conversation history for ID:', convId);
      const response = await chatAPI.getConversationHistory(userId, convId);

      const backendMessages = response.data.messages || [];
      const frontendMessages: Message[] = backendMessages.map((msg: any, index: number) => ({
        id: msg.id || Date.now() + index,
        text: msg.content || msg.text || '',
        sender: msg.sender === 'user' ? 'user' : 'bot',
        timestamp: new Date(msg.timestamp || msg.created_at || Date.now()),
      }));

      setMessages((prevMessages) => (frontendMessages.length > 0 ? frontendMessages : prevMessages));
      console.log('Loaded', frontendMessages.length, 'messages from conversation history');
    } catch (error) {
      console.error('Error loading conversation history:', error);
    }
  };

  // Handle sending a message
  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    if (!userId || userId.trim() === '') {
      console.error('User ID is missing or empty');
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Authentication error. Please refresh the page.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      return;
    }

    const userMessage: Message = {
      id: Date.now(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const messageData: { message: string; conversation_id?: string } = { message: text };
      if (conversationId) messageData.conversation_id = conversationId;

      const response = await chatAPI.sendMessage(userId, messageData);
      const { response: botResponse, conversation_id: newConversationId, action } = response.data;

      if (newConversationId) {
        setConversationId(newConversationId);
        sessionStorage.setItem('chatbot_conversation_id', newConversationId);
      }

      if (action && action.type && action.type.startsWith('task_') && onTaskChange) {
        console.log('🔄 Task action detected:', action.type, 'Triggering task list refresh...');
        onTaskChange();
      }

      const botMessage: Message = {
        id: Date.now() + 1,
        text: botResponse,
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
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

  // Start a new conversation
  const handleNewChat = () => {
    sessionStorage.removeItem('chatbot_conversation_id');
    setConversationId(null);
    setMessages([
      {
        id: 1,
        text: "Hello! I'm your Todo Assistant. How can I help you today?",
        sender: 'bot',
        timestamp: new Date(),
      },
    ]);
  };

  // Scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="flex flex-col h-full max-w-md mx-auto max-h-[70vh]">
      {/* Chat Header */}
      <div className="backdrop-blur-2xl bg-white/40 border border-white/60 rounded-t-3xl p-4 mb-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 bg-coral-600 rounded-full"></div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Todo Assistant</h2>
              <p className="text-xs text-gray-600">Online • Ready to help</p>
            </div>
          </div>
          <button
            onClick={handleNewChat}
            className="text-xs bg-white/60 hover:bg-white/80 px-2 py-1 rounded-md transition-colors"
            title="Start new conversation"
          >
            New Chat
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto max-h-[calc(70vh-10rem)] p-4 space-y-4 bg-white/20 backdrop-blur-xl border-x border-white/60">
        {messages.map((message) => (
          <MessageBubble key={message.id} text={message.text} sender={message.sender} timestamp={message.timestamp} />
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
