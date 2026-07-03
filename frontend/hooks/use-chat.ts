'use client';

import { useState, useCallback, useRef } from 'react';
import { chat } from '@/services/api';
import type { ChatMessage, ChatResponse } from '@/types';

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (content: string) => Promise<void>;
  retryLast: () => Promise<void>;
  clearChat: () => void;
}

const SESSION_ID = 'default';

/** Extract the text from a chat response that may use any common field name. */
function extractResponseText(data: ChatResponse): string {
  return (
    data.response ||
    data.answer ||
    data.message ||
    data.content ||
    data.text ||
    (typeof data === 'string' ? data : '')
  );
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Use a ref to avoid stale-closure issues when messages update rapidly.
  const messagesRef = useRef<ChatMessage[]>([]);
  messagesRef.current = messages;

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return;

    const now = new Date().toISOString();
    const userMessage: ChatMessage = { role: 'user', content, timestamp: now };

    setMessages((prev) => [...prev, userMessage]);
    setError(null);
    setIsLoading(true);

    // Add a placeholder assistant message that shows the typing indicator.
    setMessages((prev) => [
      ...prev,
      { role: 'assistant', content: '', timestamp: new Date().toISOString() },
    ]);

    try {
      const data = await chat(content, SESSION_ID);
      const text = extractResponseText(data as ChatResponse);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: 'assistant',
          content: text || 'I apologize, but I could not generate a response. Please try again.',
          timestamp: new Date().toISOString(),
        };
        return updated;
      });
    } catch (err: unknown) {
      const msg = (err as { message?: string })?.message || 'Failed to get response';
      setError(msg);
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: 'assistant',
          content: `I encountered an error: ${msg}. Please try again.`,
          timestamp: new Date().toISOString(),
        };
        return updated;
      });
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  const retryLast = useCallback(async () => {
    const current = messagesRef.current;
    // Find the last user message
    let lastUserContent = '';
    for (let i = current.length - 1; i >= 0; i--) {
      if (current[i].role === 'user') {
        lastUserContent = current[i].content;
        break;
      }
    }
    if (!lastUserContent || isLoading) return;

    // Remove the last assistant message (the error/placeholder) before retrying
    setMessages((prev) => {
      const updated = [...prev];
      if (updated.length > 0 && updated[updated.length - 1].role === 'assistant') {
        updated.pop();
      }
      return updated;
    });

    // Re-send the last user question
    // Temporarily set isLoading false so sendMessage doesn't bail
    setIsLoading(false);
    await sendMessage(lastUserContent);
  }, [isLoading, sendMessage]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return { messages, isLoading, error, sendMessage, retryLast, clearChat };
}
