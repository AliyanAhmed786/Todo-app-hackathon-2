export interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export interface ChatBotProps {
  isOpen?: boolean;
  onClose?: () => void;
  position?: string;
  userId?: string;
  onTaskChange?: () => void;
}

export interface ChatWindowProps {
  userId?: string;
  onTaskChange?: () => void;
}