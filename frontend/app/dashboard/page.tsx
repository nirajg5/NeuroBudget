'use client';

import { useMemo } from 'react';
import Link from 'next/link';
import {
  Wallet,
  TrendingDown,
  PiggyBank,
  ShieldCheck,
  ArrowRight,
  Sparkles,
  Activity,
  FileText,
} from 'lucide-react';
import { AppShell } from '@/components/layout/app-shell';
import { StatCard } from '@/components/dashboard/stat-card';
import { ChartCard } from '@/components/dashboard/chart-card';
import { StatCardSkeleton, ChartSkeleton, TableSkeleton } from '@/components/shared/skeleton';
import { ErrorBanner } from '@/components/shared/error-banner';
import { EmptyState } from '@/components/shared/empty-state';
import { ExpensePieChart } from '@/components/charts/expense-pie-chart';
import { IncomeVsExpenseChart } from '@/components/charts/income-vs-expense-chart';
import { RiskGauge } from '@/components/charts/risk-gauge';
import { BudgetProgressChart } from '@/components/charts/budget-progress-chart';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useFetch } from '@/hooks/use-fetch';
import { getTransactions, getForecast, getReports, getHealth } from '@/services/api';
import { formatCurrency, formatRelativeTime } from '@/utils/format';
import { Transaction, Report } from '@/types';

export default function DashboardPage() {
  const { data: txData, loading: txLoading, error: txError, refetch: refetchTx } = useFetch(getTransactions, []);
  const { data: forecastData, loading: forecastLoading } = useFetch(getForecast, []);
  const { data: reportsData, loading: reportsLoading } = useFetch(getReports, []);
  const { data: healthData } = useFetch(getHealth, []);

  const transactions: Transaction[] = txData?.transactions || txData || [];
  const reports: Report[] = reportsData?.reports || reportsData || [];

  const stats = useMemo(() => {
    let income = 0, expense = 0;
    const categoryMap: Record<string, number> = {};
    const monthlyMap: Record<string, { income: number; expense: number }> = {};

    for (const tx of transactions) {
      const amt = Math.abs(tx.amount || 0);
      if (tx.type === 'income' || tx.amount > 0) {
        income += amt;
      } else {
        expense += amt;
        categoryMap[tx.category] = (categoryMap[tx.category] || 0) + amt;
      }
      const month = tx.date?.slice(0, 7) || 'Unknown';
      if (!monthlyMap[month]) monthlyMap[month] = { income: 0, expense: 0 };
      if (tx.type === 'income' || tx.amount > 0) monthlyMap[month].income += amt;
      else monthlyMap[month].expense += amt;
    }

    const savings = income - expense;
    const savingsRate = income > 0 ? (savings / income) * 100 : 0;
    const riskScore = forecastData?.risk_score ?? (savingsRate < 0 ? 80 : savingsRate < 10 ? 60 : savingsRate < 20 ? 40 : 20);

    // Compute real month-over-month trends from the data
    const sortedMonths = Object.entries(monthlyMap).sort((a, b) => a[0].localeCompare(b[0]));
    const lastMonth = sortedMonths[sortedMonths.length - 1]?.[1];
    const prevMonth = sortedMonths[sortedMonths.length - 2]?.[1];
    const incomeTrend = lastMonth && prevMonth && prevMonth.income > 0
      ? ((lastMonth.income - prevMonth.income) / prevMonth.income) * 100
      : 0;
    const expenseTrend = lastMonth && prevMonth && prevMonth.expense > 0
      ? ((lastMonth.expense - prevMonth.expense) / prevMonth.expense) * 100
      : 0;

    const pieData = Object.entries(categoryMap)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 6);

    const lineData = sortedMonths
      .map(([month, vals]) => ({
        month: new Date(month + '-01').toLocaleDateString('en-US', { month: 'short' }),
        income: vals.income,
        expense: vals.expense,
      }));

    return { income, expense, savings, savingsRate, riskScore, incomeTrend, expenseTrend, pieData, lineData };
  }, [transactions, forecastData]);

  const budgetData = useMemo(() => {
    const categories = stats.pieData.slice(0, 5);
    return categories.map((c) => ({
      category: c.name,
      budget: c.value * 1.2,
      spent: c.value,
    }));
  }, [stats]);

  const recentTx = transactions.slice(0, 6);
  const recentReports = reports.slice(0, 3);

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Welcome header */}
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-2xl font-bold tracking-tight">Welcome back</h2>
            <p className="text-sm text-muted-foreground">Here's your financial overview</p>
          </div>
          <Link href="/chat">
            <Button className="gap-2 bg-gradient-to-r from-chart-1 to-chart-4 text-white hover:opacity-90">
              <Sparkles className="h-4 w-4" /> Ask AI Copilot
            </Button>
          </Link>
        </div>

        {txError && <ErrorBanner message={txError} onRetry={refetchTx} />}

        {/* Stat cards */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {txLoading ? (
            <>
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
            </>
          ) : (
            <>
              <StatCard
                title="Total Income"
                value={formatCurrency(stats.income)}
                icon={Wallet}
                trend={stats.incomeTrend}
                trendLabel="vs last month"
                gradient="from-success/20 to-chart-2/10"
                delay={0}
              />
              <StatCard
                title="Total Expense"
                value={formatCurrency(stats.expense)}
                icon={TrendingDown}
                trend={stats.expenseTrend}
                trendLabel="vs last month"
                gradient="from-destructive/20 to-chart-5/10"
                delay={0.05}
              />
              <StatCard
                title="Total Savings"
                value={formatCurrency(stats.savings)}
                icon={PiggyBank}
                trend={stats.savingsRate}
                trendLabel="savings rate"
                gradient="from-chart-1/20 to-chart-4/10"
                delay={0.1}
              />
              <StatCard
                title="Risk Score"
                value={`${stats.riskScore.toFixed(0)}/100`}
                icon={ShieldCheck}
                gradient="from-warning/20 to-chart-3/10"
                delay={0.15}
              />
            </>
          )}
        </div>

        {/* Charts row */}
        <div className="grid gap-4 lg:grid-cols-3">
          {/* Expense overview */}
          <div className="lg:col-span-2">
            {txLoading ? (
              <ChartSkeleton />
            ) : (
              <ChartCard
                title="Income vs Expense"
                description="Monthly comparison over time"
                icon={Activity}
              >
                {stats.lineData.length > 0 ? (
                  <IncomeVsExpenseChart data={stats.lineData} />
                ) : (
                  <EmptyState icon={Activity} title="No transaction data" description="Upload a CSV to see your income vs expense trends." />
                )}
              </ChartCard>
            )}
          </div>

          {/* Risk gauge */}
          <div>
            {forecastLoading ? (
              <ChartSkeleton />
            ) : (
              <ChartCard title="Risk Assessment" description="AI-powered risk score" icon={ShieldCheck}>
                <RiskGauge score={stats.riskScore} />
              </ChartCard>
            )}
          </div>
        </div>

        {/* Second row */}
        <div className="grid gap-4 lg:grid-cols-3">
          {/* Expense by category */}
          <div>
            {txLoading ? (
              <ChartSkeleton />
            ) : (
              <ChartCard title="Expense by Category" description="Where your money goes" icon={Wallet}>
                {stats.pieData.length > 0 ? (
                  <ExpensePieChart data={stats.pieData} />
                ) : (
                  <EmptyState icon={Wallet} title="No expense data" />
                )}
              </ChartCard>
            )}
          </div>

          {/* Budget progress */}
          <div>
            {txLoading ? (
              <ChartSkeleton />
            ) : (
              <ChartCard title="Budget Progress" description="Category spending vs budget" icon={PiggyBank}>
                {budgetData.length > 0 ? (
                  <BudgetProgressChart data={budgetData} />
                ) : (
                  <EmptyState icon={PiggyBank} title="No budget data" />
                )}
              </ChartCard>
            )}
          </div>

          {/* AI Insight widget */}
          <div>
            <ChartCard title="AI Insight" description="Latest from your AI copilot" icon={Sparkles}>
              <div className="space-y-3">
                {forecastData?.recommendations && forecastData.recommendations.length > 0 ? (
                  forecastData.recommendations.slice(0, 3).map((rec: string, i: number) => (
                    <div key={i} className="rounded-xl border border-border bg-card/40 p-3">
                      <div className="flex items-start gap-2">
                        <div className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-chart-1" />
                        <p className="text-sm text-muted-foreground">{rec}</p>
                      </div>
                    </div>
                  ))
                ) : forecastData?.summary ? (
                  <div className="rounded-xl border border-border bg-card/40 p-3">
                    <p className="text-sm text-muted-foreground">{forecastData.summary}</p>
                  </div>
                ) : (
                  <EmptyState
                    icon={Sparkles}
                    title="No insights yet"
                    description="Upload transactions and chat with AI to get personalized insights."
                    action={
                      <Link href="/chat">
                        <Button size="sm" variant="outline" className="gap-2">
                          <Sparkles className="h-3.5 w-3.5" /> Ask AI
                        </Button>
                      </Link>
                    }
                  />
                )}
              </div>
            </ChartCard>
          </div>
        </div>

        {/* Bottom row */}
        <div className="grid gap-4 lg:grid-cols-3">
          {/* Recent transactions */}
          <div className="lg:col-span-2">
            <ChartCard
              title="Recent Transactions"
              description="Your latest activity"
              icon={Activity}
              action={
                <Link href="/analytics">
                  <Button size="sm" variant="ghost" className="gap-1 text-xs">
                    View all <ArrowRight className="h-3 w-3" />
                  </Button>
                </Link>
              }
            >
              {txLoading ? (
                <TableSkeleton rows={5} />
              ) : recentTx.length > 0 ? (
                <div className="space-y-2">
                  {recentTx.map((tx, i) => (
                    <div key={i} className="flex items-center justify-between rounded-lg border border-border bg-card/30 px-3 py-2.5">
                      <div className="flex items-center gap-3">
                        <div className={`flex h-9 w-9 items-center justify-center rounded-lg ${tx.type === 'income' || tx.amount > 0 ? 'bg-success/10' : 'bg-destructive/10'}`}>
                          <Wallet className={`h-4 w-4 ${tx.type === 'income' || tx.amount > 0 ? 'text-success' : 'text-destructive'}`} />
                        </div>
                        <div>
                          <p className="text-sm font-medium">{tx.description || tx.merchant}</p>
                          <p className="text-xs text-muted-foreground">{tx.category} · {formatRelativeTime(tx.date)}</p>
                        </div>
                      </div>
                      <span className={`text-sm font-semibold ${tx.type === 'income' || tx.amount > 0 ? 'text-success' : 'text-destructive'}`}>
                        {tx.type === 'income' || tx.amount > 0 ? '+' : '-'}{formatCurrency(Math.abs(tx.amount))}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState
                  icon={Activity}
                  title="No transactions yet"
                  description="Upload a CSV file to get started."
                  action={
                    <Link href="/upload">
                      <Button size="sm" className="gap-2 bg-gradient-to-r from-chart-1 to-chart-4 text-white">
                        Upload CSV
                      </Button>
                    </Link>
                  }
                />
              )}
            </ChartCard>
          </div>

          {/* Latest reports + Health */}
          <div className="space-y-4">
            <ChartCard title="Latest Reports" description="Recent financial summaries" icon={FileText}>
              {reportsLoading ? (
                <TableSkeleton rows={3} />
              ) : recentReports.length > 0 ? (
                <div className="space-y-2">
                  {recentReports.map((report, i) => (
                    <Link key={i} href="/reports" className="block rounded-lg border border-border bg-card/30 px-3 py-2.5 transition-colors hover:border-chart-1/30 hover:bg-chart-1/5">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium">{report.title || report.period}</p>
                        <Badge variant="secondary" className="text-xs">{report.type || 'Monthly'}</Badge>
                      </div>
                      <p className="mt-1 text-xs text-muted-foreground">{formatRelativeTime(report.created_at || report.date)}</p>
                    </Link>
                  ))}
                </div>
              ) : (
                <EmptyState icon={FileText} title="No reports yet" />
              )}
            </ChartCard>

            {/* Health status widget */}
            <ChartCard title="System Health" description="Backend service status" icon={Activity}>
              <div className="space-y-2">
                {[
                  { name: 'FastAPI', status: healthData?.status === 'healthy' ? 'healthy' : 'unknown' },
                  { name: 'PostgreSQL', status: healthData?.services?.postgresql?.status || 'unknown' },
                  { name: 'Pinecone', status: healthData?.services?.pinecone?.status || 'unknown' },
                  { name: 'OpenRouter', status: healthData?.services?.openrouter?.status || 'unknown' },
                ].map((svc) => (
                  <div key={svc.name} className="flex items-center justify-between rounded-lg border border-border bg-card/30 px-3 py-2">
                    <span className="text-sm">{svc.name}</span>
                    <div className="flex items-center gap-2">
                      <div className={`h-2 w-2 rounded-full ${svc.status === 'healthy' ? 'bg-success' : svc.status === 'unhealthy' ? 'bg-destructive' : 'bg-warning'}`} />
                      <span className="text-xs text-muted-foreground capitalize">{svc.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </ChartCard>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
