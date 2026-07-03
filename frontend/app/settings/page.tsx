'use client';

import { motion } from 'framer-motion';
import {
  Settings as SettingsIcon,
  Server,
  Database,
  Cloud,
  Bot,
  GitBranch,
  Zap,
  RefreshCw,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Moon,
  Activity,
} from 'lucide-react';
import { AppShell } from '@/components/layout/app-shell';
import { ThemeToggle } from '@/components/layout/theme-toggle';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useHealth } from '@/hooks/use-health';
import { API_BASE_URL } from '@/services/api';

const serviceIcons: Record<string, typeof Server> = {
  fastapi: Zap,
  postgresql: Database,
  pinecone: Cloud,
  openrouter: Bot,
  langgraph: GitBranch,
};

export default function SettingsPage() {
  const { health, loading, error, refresh } = useHealth();

  const services = [
    { name: 'FastAPI', key: 'fastapi', icon: Zap, desc: 'Backend API server' },
    { name: 'PostgreSQL', key: 'postgresql', icon: Database, desc: 'Relational database' },
    { name: 'Pinecone', key: 'pinecone', icon: Cloud, desc: 'Vector database' },
    { name: 'OpenRouter', key: 'openrouter', icon: Bot, desc: 'LLM provider' },
    { name: 'LangGraph', key: 'langgraph', icon: GitBranch, desc: 'Multi-agent workflow' },
  ];

  const getStatusInfo = (key: string) => {
    if (loading) return { status: 'loading', color: 'text-warning', bg: 'bg-warning/15' };
    if (error) return { status: 'offline', color: 'text-destructive', bg: 'bg-destructive/15' };

    // Check health data
    const svc = health?.services?.[key];
    const overallHealthy = health?.status === 'healthy';

    if (key === 'fastapi') {
      return overallHealthy
        ? { status: 'online', color: 'text-success', bg: 'bg-success/15' }
        : { status: 'offline', color: 'text-destructive', bg: 'bg-destructive/15' };
    }

    if (svc?.status === 'healthy') return { status: 'online', color: 'text-success', bg: 'bg-success/15' };
    if (svc?.status === 'unhealthy') return { status: 'offline', color: 'text-destructive', bg: 'bg-destructive/15' };
    if (svc?.status === 'degraded') return { status: 'degraded', color: 'text-warning', bg: 'bg-warning/15' };

    // If API is healthy but no specific service info, assume online
    return overallHealthy
      ? { status: 'online', color: 'text-success', bg: 'bg-success/15' }
      : { status: 'unknown', color: 'text-muted-foreground', bg: 'bg-muted/30' };
  };

  return (
    <AppShell>
      <div className="mx-auto max-w-4xl space-y-6">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Settings</h2>
          <p className="text-sm text-muted-foreground">Manage your app preferences and monitor backend services</p>
        </div>

        {/* Appearance */}
        <Card className="glass border-white/5 p-6">
          <div className="mb-4 flex items-center gap-2">
            <SettingsIcon className="h-5 w-5 text-chart-1" />
            <h3 className="text-base font-semibold">Appearance</h3>
          </div>
          <div className="flex items-center justify-between rounded-xl border border-border bg-card/40 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-chart-4/15">
                <Moon className="h-5 w-5 text-chart-4" />
              </div>
              <div>
                <p className="text-sm font-medium">Theme</p>
                <p className="text-xs text-muted-foreground">Toggle between dark and light mode</p>
              </div>
            </div>
            <ThemeToggle />
          </div>
        </Card>

        {/* API Configuration */}
        <Card className="glass border-white/5 p-6">
          <div className="mb-4 flex items-center gap-2">
            <Server className="h-5 w-5 text-chart-2" />
            <h3 className="text-base font-semibold">API Configuration</h3>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between rounded-xl border border-border bg-card/40 p-4">
              <div>
                <p className="text-sm font-medium">Backend URL</p>
                <p className="text-xs text-muted-foreground font-mono">{API_BASE_URL}</p>
              </div>
              <Badge variant="secondary" className="font-mono text-xs">FastAPI</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-border bg-card/40 p-4">
              <div>
                <p className="text-sm font-medium">API Endpoints</p>
                <p className="text-xs text-muted-foreground">7 endpoints available</p>
              </div>
              <div className="flex flex-wrap gap-1 justify-end max-w-xs">
                {['chat', 'upload', 'transactions', 'reports', 'goals', 'forecast', 'health'].map((ep) => (
                  <Badge key={ep} variant="outline" className="text-xs font-mono">{ep}</Badge>
                ))}
              </div>
            </div>
          </div>
        </Card>

        {/* Service Health */}
        <Card className="glass border-white/5 p-6">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-chart-3" />
              <h3 className="text-base font-semibold">Service Health</h3>
            </div>
            <Button
              size="sm"
              variant="outline"
              onClick={refresh}
              disabled={loading}
              className="gap-2"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>

          {/* Overall status */}
          <div className="mb-4 flex items-center gap-3 rounded-xl border border-border bg-card/40 p-4">
            <motion.div
              animate={{ scale: loading ? [1, 1.2, 1] : 1 }}
              transition={{ duration: 1, repeat: loading ? Infinity : 0 }}
              className={`h-3 w-3 rounded-full ${
                loading ? 'bg-warning' : error ? 'bg-destructive' : 'bg-success'
              }`}
            />
            <div className="flex-1">
              <p className="text-sm font-medium">
                {loading ? 'Checking services...' : error ? 'Backend unreachable' : 'All systems operational'}
              </p>
              <p className="text-xs text-muted-foreground">
                {error
                  ? 'Make sure your FastAPI backend is running at localhost:8000'
                  : health?.timestamp
                  ? `Last checked: ${new Date(health.timestamp).toLocaleTimeString()}`
                  : 'Auto-refreshes every 30 seconds'}
              </p>
            </div>
            {health?.version && (
              <Badge variant="secondary" className="text-xs">v{health.version}</Badge>
            )}
          </div>

          {/* Individual services */}
          <div className="grid gap-3 sm:grid-cols-2">
            {services.map((svc, i) => {
              const statusInfo = getStatusInfo(svc.key);
              const Icon = svc.icon;
              return (
                <motion.div
                  key={svc.key}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="flex items-center gap-3 rounded-xl border border-border bg-card/40 p-4"
                >
                  <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${statusInfo.bg}`}>
                    <Icon className={`h-5 w-5 ${statusInfo.color}`} />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{svc.name}</p>
                    <p className="text-xs text-muted-foreground">{svc.desc}</p>
                  </div>
                  <div className="flex items-center gap-1.5">
                    {statusInfo.status === 'online' && <CheckCircle2 className="h-4 w-4 text-success" />}
                    {statusInfo.status === 'offline' && <XCircle className="h-4 w-4 text-destructive" />}
                    {statusInfo.status === 'loading' && <RefreshCw className="h-4 w-4 animate-spin text-warning" />}
                    {statusInfo.status === 'degraded' && <AlertCircle className="h-4 w-4 text-warning" />}
                    {statusInfo.status === 'unknown' && <AlertCircle className="h-4 w-4 text-muted-foreground" />}
                    <span className={`text-xs font-medium capitalize ${statusInfo.color}`}>
                      {statusInfo.status}
                    </span>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </Card>

        {/* About */}
        <Card className="glass border-white/5 p-6">
          <div className="mb-4 flex items-center gap-2">
            <Bot className="h-5 w-5 text-chart-4" />
            <h3 className="text-base font-semibold">About NeuroBudget</h3>
          </div>
          <div className="space-y-2 text-sm text-muted-foreground">
            <p>
              NeuroBudget is an AI-powered financial copilot that uses a multi-agent LangGraph workflow
              to analyze transactions, forecast spending, and provide intelligent financial planning.
            </p>
            <div className="flex flex-wrap gap-2 pt-2">
              <Badge variant="outline">Next.js 15</Badge>
              <Badge variant="outline">FastAPI</Badge>
              <Badge variant="outline">LangGraph</Badge>
              <Badge variant="outline">Pinecone</Badge>
              <Badge variant="outline">OpenRouter</Badge>
              <Badge variant="outline">PostgreSQL</Badge>
            </div>
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
