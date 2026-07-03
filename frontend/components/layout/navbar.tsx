'use client';

import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Activity, Bell, Search } from 'lucide-react';
import { ThemeToggle } from './theme-toggle';
import { getHealth } from '@/services/api';

const pageTitles: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/chat': 'AI Chat',
  '/upload': 'Upload Transactions',
  '/analytics': 'Analytics',
  '/planning': 'Financial Planning',
  '/reports': 'Reports',
  '/settings': 'Settings',
};

export function Navbar() {
  const pathname = usePathname();
  const [healthStatus, setHealthStatus] = useState<'healthy' | 'loading' | 'down'>('loading');

  useEffect(() => {
    let active = true;
    getHealth()
      .then(() => active && setHealthStatus('healthy'))
      .catch(() => active && setHealthStatus('down'));
    const interval = setInterval(() => {
      getHealth()
        .then(() => active && setHealthStatus('healthy'))
        .catch(() => active && setHealthStatus('down'));
    }, 30000);
    return () => {
      active = false;
      clearInterval(interval);
    };
  }, []);

  const title = pageTitles[pathname] || 'NeuroBudget';

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-background/60 px-4 backdrop-blur-xl md:px-6 md:pl-8">
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold tracking-tight md:text-xl">{title}</h1>
      </div>

      <div className="flex items-center gap-2 md:gap-3">
        {/* Health indicator */}
        <div className="hidden items-center gap-2 rounded-lg border border-border bg-card/40 px-3 py-1.5 sm:flex">
          <motion.div
            animate={{
              scale: healthStatus === 'healthy' ? [1, 1.3, 1] : 1,
              opacity: healthStatus === 'healthy' ? [0.6, 1, 0.6] : 0.4,
            }}
            transition={{ duration: 2, repeat: Infinity }}
            className={`h-2 w-2 rounded-full ${
              healthStatus === 'healthy'
                ? 'bg-success'
                : healthStatus === 'down'
                ? 'bg-destructive'
                : 'bg-warning'
            }`}
          />
          <span className="text-xs font-medium text-muted-foreground">
            {healthStatus === 'healthy'
              ? 'API Online'
              : healthStatus === 'down'
              ? 'API Offline'
              : 'Checking...'}
          </span>
        </div>

        <button className="hidden h-9 w-9 items-center justify-center rounded-lg border border-border bg-card/40 text-muted-foreground transition-colors hover:text-foreground hover:bg-card/80 md:flex">
          <Search className="h-4 w-4" />
        </button>

        <button className="relative hidden h-9 w-9 items-center justify-center rounded-lg border border-border bg-card/40 text-muted-foreground transition-colors hover:text-foreground hover:bg-card/80 sm:flex">
          <Bell className="h-4 w-4" />
          <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-chart-1" />
        </button>

        <ThemeToggle />

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-chart-1 to-chart-4 text-sm font-semibold text-white">
          NB
        </div>
      </div>
    </header>
  );
}
