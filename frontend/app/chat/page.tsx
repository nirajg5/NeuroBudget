'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Trash2, Brain, RotateCcw } from 'lucide-react';
import { AppShell } from '@/components/layout/app-shell';
import { UserBubble } from '@/components/chat/user-bubble';
import { AIBubble } from '@/components/chat/ai-bubble';
import { ChatInput } from '@/components/chat/chat-input';
import { SuggestedQuestions } from '@/components/chat/suggested-questions';
import { ErrorBanner } from '@/components/shared/error-banner';
import { Button } from '@/components/ui/button';
import { useChat } from '@/hooks/use-chat';

const suggestedQuestions = [
  'How much did I spend last month?',
  'What are my top spending categories?',
  'Can you analyze my spending patterns?',
  'What\'s my financial risk score?',
  'How can I improve my savings?',
  'Create a budget recommendation for me.',
];

export default function ChatPage() {
  const { messages, isLoading, error, sendMessage, retryLast, clearChat } = useChat();
  const [input, setInput] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    sendMessage(input);
    setInput('');
  };

  const handleSuggestion = (q: string) => {
    if (isLoading) return;
    sendMessage(q);
  };

  return (
    <AppShell>
      <div className="flex h-[calc(100vh-5rem)] flex-col">
        {/* Chat header */}
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-chart-4 to-chart-5 shadow-lg shadow-chart-4/20">
              <Brain className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold">NeuroBudget AI</h2>
              <p className="text-xs text-muted-foreground">
                {isLoading ? 'Thinking...' : 'Ready to help with your finances'}
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            {error && (
              <Button
                variant="outline"
                size="sm"
                onClick={retryLast}
                disabled={isLoading}
                className="gap-2"
              >
                <RotateCcw className="h-3.5 w-3.5" /> Retry
              </Button>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={clearChat}
              disabled={messages.length === 0 || isLoading}
              className="gap-2"
            >
              <Trash2 className="h-3.5 w-3.5" /> Clear
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={clearChat}
              disabled={isLoading}
              className="gap-2"
            >
              <Plus className="h-3.5 w-3.5" /> New Chat
            </Button>
          </div>
        </div>

        {error && <ErrorBanner message={error} onRetry={retryLast} />}

        {/* Messages area */}
        <div className="flex-1 overflow-y-auto scrollbar-thin">
          {messages.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="mb-8 text-center"
              >
                <div className="relative mx-auto mb-6">
                  <div className="absolute inset-0 rounded-3xl bg-chart-4/20 blur-2xl" />
                  <div className="relative flex h-20 w-20 items-center justify-center rounded-3xl bg-gradient-to-br from-chart-4 to-chart-5 shadow-2xl shadow-chart-4/30">
                    <Brain className="h-10 w-10 text-white" />
                  </div>
                </div>
                <h3 className="text-xl font-bold">How can I help you today?</h3>
                <p className="mt-2 text-sm text-muted-foreground">
                  Ask me anything about your finances, spending, or budget planning.
                </p>
              </motion.div>
              <div className="w-full max-w-2xl">
                <SuggestedQuestions questions={suggestedQuestions} onSelect={handleSuggestion} />
              </div>
            </div>
          ) : (
            <div className="mx-auto max-w-3xl space-y-6 py-4">
              <AnimatePresence initial={false}>
                {messages.map((msg, i) => (
                  <div key={i}>
                    {msg.role === 'user' ? (
                      <UserBubble content={msg.content} timestamp={msg.timestamp} />
                    ) : (
                      <AIBubble
                        content={msg.content}
                        timestamp={msg.timestamp}
                        streaming={isLoading && i === messages.length - 1}
                        agent="NeuroBudget AI"
                      />
                    )}
                  </div>
                ))}
              </AnimatePresence>
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="mt-4 border-t border-border pt-4">
          <div className="mx-auto max-w-3xl">
            <ChatInput
              value={input}
              onChange={setInput}
              onSend={handleSend}
              disabled={isLoading}
              placeholder="Ask about your spending, savings, or financial goals..."
            />
          </div>
        </div>
      </div>
    </AppShell>
  );
}
