import Link from 'next/link';
import { Compass, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function NotFound() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-6">
      <div className="max-w-md text-center">
        <div className="relative mx-auto mb-6">
          <div className="absolute inset-0 rounded-3xl bg-chart-1/20 blur-2xl" />
          <div className="relative flex h-20 w-20 items-center justify-center rounded-3xl bg-gradient-to-br from-chart-1 to-chart-4">
            <Compass className="h-10 w-10 text-white" />
          </div>
        </div>
        <h1 className="text-6xl font-bold gradient-text">404</h1>
        <h2 className="mt-2 text-xl font-semibold">Page not found</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link href="/dashboard">
          <Button className="mt-6 gap-2 bg-gradient-to-r from-chart-1 to-chart-4 text-white hover:opacity-90">
            <ArrowLeft className="h-4 w-4" /> Back to Dashboard
          </Button>
        </Link>
      </div>
    </div>
  );
}
