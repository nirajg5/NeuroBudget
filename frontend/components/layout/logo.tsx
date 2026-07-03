'use client';

import { Brain } from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export function Logo({ collapsed = false }: { collapsed?: boolean }) {
  return (
    <Link href="/" className="flex items-center gap-2.5 group">
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.4 }}
        className="relative flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-chart-1 to-chart-4 shadow-lg shadow-chart-1/20"
      >
        <Brain className="h-5 w-5 text-white" />
        <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-chart-1 to-chart-4 opacity-0 blur-md transition-opacity group-hover:opacity-50" />
      </motion.div>
      {!collapsed && (
        <div className="flex flex-col leading-none">
          <span className="text-lg font-bold tracking-tight">
            Neuro<span className="gradient-text">Budget</span>
          </span>
          <span className="text-[10px] font-medium text-muted-foreground">
            AI Financial Copilot
          </span>
        </div>
      )}
    </Link>
  );
}
