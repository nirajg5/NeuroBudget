'use client';

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileSpreadsheet, CheckCircle2, AlertCircle, Upload, Database, FileCheck, BarChart3 } from 'lucide-react';
import { AppShell } from '@/components/layout/app-shell';
import { UploadZone } from '@/components/upload/upload-zone';
import { UploadProgress } from '@/components/upload/upload-progress';
import { PreviewTable } from '@/components/upload/preview-table';
import { ErrorBanner } from '@/components/shared/error-banner';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { uploadCSV, getTransactions } from '@/services/api';
import type { Transaction, UploadResponse } from '@/types';
import { toast } from '@/hooks/use-toast';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [progress, setProgress] = useState(0);
  const [uploadMessage, setUploadMessage] = useState('');
  const [rowsProcessed, setRowsProcessed] = useState(0);
  const [previewTx, setPreviewTx] = useState<Transaction[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = useCallback(async () => {
    if (!file) return;

    setUploadStatus('uploading');
    setProgress(0);
    setError(null);

    try {
      const result = (await uploadCSV(file, (pct) => {
        setProgress(pct);
      })) as UploadResponse;

      setProgress(100);
      setUploadStatus('success');
      setRowsProcessed(result.rows_processed || result.count || 0);
      setUploadMessage(result.message || 'File processed successfully');

      // Fetch preview transactions after successful upload
      try {
        const txData = await getTransactions();
        const txs = txData?.transactions || txData || [];
        setPreviewTx(txs);
      } catch {
        // Preview is optional — upload itself succeeded
      }

      toast({
        title: 'Upload successful',
        description: `${result.rows_processed || 0} rows processed`,
      });
    } catch (err: unknown) {
      setUploadStatus('error');
      const msg = (err as { message?: string })?.message || 'Upload failed. Please check your CSV format.';
      setUploadMessage(msg);
      setError(msg);
      toast({
        title: 'Upload failed',
        description: msg,
        variant: 'destructive',
      });
    }
  }, [file]);

  const handleReset = () => {
    setFile(null);
    setUploadStatus('idle');
    setProgress(0);
    setUploadMessage('');
    setRowsProcessed(0);
    setPreviewTx([]);
    setError(null);
  };

  return (
    <AppShell>
      <div className="mx-auto max-w-4xl space-y-6">
        {/* Header */}
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Upload Transactions</h2>
          <p className="text-sm text-muted-foreground">
            Upload a CSV file of your transactions for AI analysis
          </p>
        </div>

        {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

        {/* Upload zone */}
        <Card className="glass border-white/5 p-6">
          <UploadZone
            onFileSelected={setFile}
            disabled={uploadStatus === 'uploading'}
            selectedFile={file}
            onClear={handleReset}
          />

          {/* Upload progress */}
          <div className="mt-4">
            <UploadProgress progress={progress} status={uploadStatus} message={uploadMessage} />
          </div>

          {/* Upload button */}
          {file && uploadStatus === 'idle' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 flex justify-end"
            >
              <Button
                onClick={handleUpload}
                className="gap-2 bg-gradient-to-r from-chart-1 to-chart-4 text-white hover:opacity-90"
              >
                <Upload className="h-4 w-4" /> Upload & Process
              </Button>
            </motion.div>
          )}

          {/* Success actions */}
          {uploadStatus === 'success' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 flex justify-end gap-2"
            >
              <Button variant="outline" onClick={handleReset} className="gap-2">
                Upload Another
              </Button>
            </motion.div>
          )}
        </Card>

        {/* Upload statistics */}
        <AnimatePresence>
          {uploadStatus === 'success' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="grid gap-4 sm:grid-cols-3"
            >
              <Card className="glass border-white/5 p-5">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-success/15">
                    <FileCheck className="h-5 w-5 text-success" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">{rowsProcessed}</p>
                    <p className="text-xs text-muted-foreground">Rows Processed</p>
                  </div>
                </div>
              </Card>
              <Card className="glass border-white/5 p-5">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-chart-1/15">
                    <Database className="h-5 w-5 text-chart-1" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">{previewTx.length}</p>
                    <p className="text-xs text-muted-foreground">Transactions Loaded</p>
                  </div>
                </div>
              </Card>
              <Card className="glass border-white/5 p-5">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-chart-4/15">
                    <CheckCircle2 className="h-5 w-5 text-chart-4" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">100%</p>
                    <p className="text-xs text-muted-foreground">Success Rate</p>
                  </div>
                </div>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Preview table */}
        {previewTx.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="mb-3 flex items-center gap-2">
              <BarChart3 className="h-4 w-4 text-chart-1" />
              <h3 className="text-base font-semibold">Transaction Preview</h3>
            </div>
            <PreviewTable transactions={previewTx} maxRows={10} />
          </motion.div>
        )}

        {/* CSV format guide */}
        <Card className="glass border-white/5 p-6">
          <div className="flex items-center gap-2 mb-3">
            <FileSpreadsheet className="h-4 w-4 text-chart-2" />
            <h3 className="text-base font-semibold">Expected CSV Format</h3>
          </div>
          <p className="text-sm text-muted-foreground mb-3">
            Your CSV should include the following columns:
          </p>
          <div className="rounded-lg border border-border bg-muted/30 p-4 font-mono text-xs text-muted-foreground">
            date,description,merchant,category,amount,type
            <br />
            2024-01-15,Coffee Shop,Starbucks,Food & Dining,-5.50,expense
            <br />
            2024-01-15,Salary,Acme Corp,Income,5000.00,income
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
