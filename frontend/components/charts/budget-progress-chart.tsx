'use client';

import { Progress } from '@/components/ui/progress';
import { motion } from 'framer-motion';
import { formatCurrency } from '@/utils/format';

interface BudgetProgressChartProps {
  data: Array<{
    category: string;
    budget: number;
    spent: number;
  }>;
}

export function BudgetProgressChart({ data }: BudgetProgressChartProps) {
  if (!data || data.length === 0) {
    return <div className="flex h-[200px] items-center justify-center text-sm text-muted-foreground">No budget data available</div>;
  }

  return (
    <div className="space-y-4">
      {data.map((item, i) => {
        const pct = item.budget > 0 ? Math.min(100, (item.spent / item.budget) * 100) : 0;
        const isOver = pct >= 90;
        const isWarning = pct >= 70 && pct < 90;

        return (
          <motion.div
            key={item.category}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <div className="mb-1.5 flex items-center justify-between text-sm">
              <span className="font-medium">{item.category}</span>
              <span className="text-muted-foreground">
                {formatCurrency(item.spent)} / {formatCurrency(item.budget)}
              </span>
            </div>
            <div className="relative h-2.5 w-full overflow-hidden rounded-full bg-muted">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ duration: 0.8, delay: i * 0.05, ease: 'easeOut' }}
                className={`h-full rounded-full ${
                  isOver
                    ? 'bg-gradient-to-r from-destructive to-chart-5'
                    : isWarning
                    ? 'bg-gradient-to-r from-warning to-chart-3'
                    : 'bg-gradient-to-r from-chart-1 to-chart-2'
                }`}
              />
            </div>
            <div className="mt-1 flex items-center justify-between text-xs">
              <span className={isOver ? 'text-destructive' : isWarning ? 'text-warning' : 'text-success'}>
                {pct.toFixed(0)}% used
              </span>
              {isOver && <span className="text-destructive font-medium">Over budget</span>}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
