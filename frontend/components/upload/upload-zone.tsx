'use client';

import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileText, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

interface UploadZoneProps {
  onFileSelected: (file: File) => void;
  disabled?: boolean;
  selectedFile?: File | null;
  onClear?: () => void;
}

export function UploadZone({ onFileSelected, disabled, selectedFile, onClear }: UploadZoneProps) {
  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.csv'],
    },
    maxFiles: 1,
    disabled,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) onFileSelected(acceptedFiles[0]);
    },
  });

  if (selectedFile) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex items-center gap-4 rounded-2xl border border-chart-2/30 bg-chart-2/5 p-5"
      >
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-chart-2/15">
          <FileText className="h-6 w-6 text-chart-2" />
        </div>
        <div className="flex-1">
          <p className="text-sm font-semibold">{selectedFile.name}</p>
          <p className="text-xs text-muted-foreground">
            {(selectedFile.size / 1024).toFixed(1)} KB · CSV file
          </p>
        </div>
        {!disabled && (
          <button
            onClick={onClear}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-destructive/10 hover:text-destructive"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </motion.div>
    );
  }

  return (
    <div
      {...getRootProps()}
      className={cn(
        'relative cursor-pointer rounded-2xl border-2 border-dashed p-12 text-center transition-all',
        isDragActive
          ? 'border-chart-1 bg-chart-1/10 scale-[1.01]'
          : 'border-border bg-card/30 hover:border-chart-1/40 hover:bg-card/50',
        isDragReject && 'border-destructive bg-destructive/5',
        disabled && 'cursor-not-allowed opacity-50'
      )}
    >
      <input {...getInputProps()} />
      <motion.div
        animate={isDragActive ? { y: -4 } : { y: 0 }}
        className="flex flex-col items-center"
      >
        <div className="relative mb-4">
          <div className="absolute inset-0 rounded-2xl bg-chart-1/20 blur-xl" />
          <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-chart-1/20 to-chart-4/10">
            <UploadCloud className={cn('h-8 w-8', isDragActive ? 'text-chart-1' : 'text-muted-foreground')} />
          </div>
        </div>
        <p className="text-base font-semibold">
          {isDragActive ? 'Drop your CSV here' : 'Drag & drop your CSV file'}
        </p>
        <p className="mt-1 text-sm text-muted-foreground">
          or click to browse — supports .csv files up to 10MB
        </p>
      </motion.div>
    </div>
  );
}
