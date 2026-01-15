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
}