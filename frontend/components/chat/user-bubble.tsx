'use client';

import { motion } from 'framer-motion';
import { User } from 'lucide-react';
import { formatTime } from '@/utils/format';

interface UserBubbleProps {
  content: string;
  timestamp?: string;
}

export function UserBubble({ content, timestamp }: UserBubbleProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex justify-end gap-3"
    >
      <div className="flex max-w-[80%] flex-col items-end gap-1">
        <div className="rounded-2xl rounded-tr-sm border border-chart-1/20 bg-gradient-to-br from-chart-1/15 to-chart-4/10 px-4 py-3">
          <p className="text-sm leading-relaxed text-foreground whitespace-pre-wrap">{content}</p>
        </div>
        {timestamp && (
          <span className="px-1 text-[11px] text-muted-foreground">{formatTime(timestamp)}</span>
        )}
      </div>
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-chart-1 to-chart-4 shadow-lg shadow-chart-1/20">
        <User className="h-4.5 w-4.5 text-white" />
      </div>
    </motion.div>
  );
}
