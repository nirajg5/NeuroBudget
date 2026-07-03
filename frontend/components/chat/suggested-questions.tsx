'use client';

import { Lightbulb } from 'lucide-react';
import { motion } from 'framer-motion';

interface SuggestedQuestionsProps {
  questions: string[];
  onSelect: (question: string) => void;
}

export function SuggestedQuestions({ questions, onSelect }: SuggestedQuestionsProps) {
  if (!questions || questions.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
        <Lightbulb className="h-4 w-4 text-chart-3" />
        Suggested questions
      </div>
      <div className="flex flex-wrap gap-2">
        {questions.map((q, i) => (
          <motion.button
            key={i}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05 }}
            onClick={() => onSelect(q)}
            className="rounded-xl border border-border bg-card/40 px-3.5 py-2 text-sm text-muted-foreground transition-all hover:border-chart-1/30 hover:bg-chart-1/5 hover:text-foreground"
          >
            {q}
          </motion.button>
        ))}
      </div>
    </div>
  );
}
