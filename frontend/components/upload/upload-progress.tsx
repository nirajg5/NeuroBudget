'use client';

import { motion } from 'framer-motion';
import { CheckCircle, Loader2, AlertCircle } from 'lucide-react';

interface UploadProgressProps {
  progress: number;
  status: 'idle' | 'uploading' | 'success' | 'error';
  message?: string;
}

export function UploadProgress({ progress, status, message }: UploadProgressProps) {
  if (status === 'idle') return null;

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      className="space-y-3"
    >
      <div className="flex items-center gap-3">
        {status === 'uploading' && <Loader2 className="h-5 w-5 animate-spin text-chart-1" />}
        {status === 'success' && <CheckCircle className="h-5 w-5 text-success" />}
        {status === 'error' && <AlertCircle className="h-5 w-5 text-destructive" />}
        <span className="text-sm font-medium">
          {status === 'uploading' && 'Uploading and processing...'}
          {status === 'success' && 'Upload complete!'}
          {status === 'error' && 'Upload failed'}
        </span>
        {status === 'uploading' && (
          <span className="ml-auto text-sm font-semibold text-chart-1">{progress.toFixed(0)}%</span>
        )}
      </div>

      {status === 'uploading' && (
        <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
          <motion.div
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
            className="h-full rounded-full bg-gradient-to-r from-chart-1 to-chart-4"
          />
        </div>
      )}

      {message && (
        <p className={`text-sm ${status === 'error' ? 'text-destructive' : 'text-muted-foreground'}`}>
          {message}
        </p>
      )}
    </motion.div>
  );
}
