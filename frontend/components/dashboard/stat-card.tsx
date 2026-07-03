'use client';

import { motion } from 'framer-motion';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface StatCardProps {
  title: string;
  value: string;
  icon: LucideIcon;
  trend?: number;
  trendLabel?: string;
  gradient?: string;
  delay?: number;
}

export function StatCard({
  title,
  value,
  icon: Icon,
  trend,
  trendLabel,
  gradient = 'from-chart-1/20 to-chart-4/10',
  delay = 0,
}: StatCardProps) {
  const isPositive = (trend ?? 0) >= 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
    >
      <Card className="relative overflow-hidden glass border-white/5 p-5 transition-all hover:border-white/10 hover:shadow-lg hover:shadow-chart-1/5">
        <div className={cn('absolute -right-8 -top-8 h-24 w-24 rounded-full bg-gradient-to-br opacity-20 blur-2xl', gradient)} />

        <div className="relative flex items-start justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="mt-2 text-2xl font-bold tracking-tight">{value}</p>
          </div>
          <div className={cn('flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br', gradient)}>
            <Icon className="h-5 w-5 text-foreground" />
          </div>
        </div>

        {trend !== undefined && (
          <div className="relative mt-3 flex items-center gap-1.5">
            <span
              className={cn(
                'flex items-center gap-1 text-xs font-semibold',
                isPositive ? 'text-success' : 'text-destructive'
              )}
            >
              {isPositive ? <TrendingUp className="h-3.5 w-3.5" /> : <TrendingDown className="h-3.5 w-3.5" />}
              {Math.abs(trend).toFixed(1)}%
            </span>
            {trendLabel && (
              <span className="text-xs text-muted-foreground">{trendLabel}</span>
            )}
          </div>
        )}
      </Card>
    </motion.div>
  );
}
