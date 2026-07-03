'use client';

import { motion } from 'framer-motion';
import { Brain, Copy, Check } from 'lucide-react';
import { useState } from 'react';
import { MarkdownRenderer } from './markdown-renderer';
import { TypingIndicator } from './typing-indicator';
import { formatTime } from '@/utils/format';
import { toast } from '@/hooks/use-toast';

interface AIBubbleProps {
  content: string;
  timestamp?: string;
  streaming?: boolean;
  agent?: string;
}

export function AIBubble({ content, timestamp, streaming, agent }: AIBubbleProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    toast({ title: 'Copied to clipboard' });
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex gap-3"
    >
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-chart-4 to-chart-5 shadow-lg shadow-chart-4/20">
        <Brain className="h-4.5 w-4.5 text-white" />
      </div>
      <div className="flex max-w-[80%] flex-col gap-1">
        {agent && (
          <span className="px-1 text-[11px] font-medium text-chart-4">{agent}</span>
        )}
        <div className="rounded-2xl rounded-tl-sm border border-border bg-card/40 backdrop-blur-sm px-4 py-3">
          {streaming && !content ? (
            <TypingIndicator />
          ) : (
            <MarkdownRenderer content={content} />
          )}
        </div>
        <div className="flex items-center gap-2 px-1">
          {timestamp && (
            <span className="text-[11px] text-muted-foreground">{formatTime(timestamp)}</span>
          )}
          {!streaming && content && (
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 text-[11px] text-muted-foreground transition-colors hover:text-foreground"
            >
              {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
              {copied ? 'Copied' : 'Copy'}
            </button>
          )}
        </div>
      </div>
    </motion.div>
  );
}
