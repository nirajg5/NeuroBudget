'use client';

import { Send, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { useRef, useEffect } from 'react';

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({ value, onChange, onSend, disabled, placeholder }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = 'auto';
    ta.style.height = `${Math.min(ta.scrollHeight, 160)}px`;
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!disabled && value.trim()) onSend();
    }
  };

  return (
    <div className="relative">
      <div className="gradient-border rounded-2xl">
        <div className="flex items-end gap-2 rounded-2xl border border-border bg-card/50 backdrop-blur-xl p-2">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-chart-1/10">
            <Sparkles className="h-4 w-4 text-chart-1" />
          </div>
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder={placeholder || 'Ask about your finances...'}
            rows={1}
            className="flex-1 resize-none bg-transparent py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none disabled:opacity-50 scrollbar-thin"
          />
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={onSend}
            disabled={disabled || !value.trim()}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-chart-1 to-chart-4 text-white shadow-lg shadow-chart-1/20 transition-all disabled:opacity-30 disabled:shadow-none"
          >
            <Send className="h-4 w-4" />
          </motion.button>
        </div>
      </div>
      <p className="mt-2 text-center text-[11px] text-muted-foreground">
        Press Enter to send, Shift+Enter for new line
      </p>
    </div>
  );
}
