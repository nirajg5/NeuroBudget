'use client';

import { AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <div className="flex min-h-screen items-center justify-center bg-background p-6">
          <div className="max-w-md text-center">
            <div className="relative mx-auto mb-6">
              <div className="absolute inset-0 rounded-2xl bg-destructive/20 blur-xl" />
              <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl border border-destructive/30 bg-destructive/10">
                <AlertCircle className="h-8 w-8 text-destructive" />
              </div>
            </div>
            <h2 className="text-xl font-bold text-foreground">Application Error</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              {error.message || 'A critical error occurred.'}
            </p>
            <Button
              onClick={reset}
              className="mt-6 gap-2 bg-gradient-to-r from-chart-1 to-chart-4 text-white hover:opacity-90"
            >
              <RefreshCw className="h-4 w-4" /> Reload application
            </Button>
          </div>
        </div>
      </body>
    </html>
  );
}
