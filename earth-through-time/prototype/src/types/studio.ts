export type Role = 'user' | 'assistant' | 'system';

export interface CodeBlockData {
  id: string;
  language: string;
  code: string;
  title?: string;
}

export interface ChatMessage {
  id: string;
  role: Role;
  content: string;
  timestamp: string;
  tokenCount?: {
    prompt: number;
    completion: number;
  };
  codeBlocks?: CodeBlockData[];
  status?: 'sending' | 'success' | 'error';
}

export interface ModelConfig {
  modelId: string;
  modelName: string;
  temperature: number;
  topP: number;
  maxOutputTokens: number;
  systemInstruction: string;
  safetyLevel: 'standard' | 'strict' | 'permissive';
}

export interface TaskSession {
  id: string;
  title: string;
  category: 'General' | 'Research' | 'Code' | 'Creative' | 'Historical';
  createdAt: string;
  updatedAt: string;
  pinned: boolean;
  messages: ChatMessage[];
  modelConfig: ModelConfig;
}

export interface ToastNotification {
  id: string;
  type: 'success' | 'error' | 'info';
  message: string;
}

export type ThemeMode = 'light' | 'dark';
