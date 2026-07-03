'use client';

import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { Target, Shield, Sparkles, TrendingUp, Calendar, PiggyBank, AlertCircle } from 'lucide-react';
import { AppShell } from '@/components/layout/app-shell';
import { ChartCard } from '@/components/dashboard/chart-card';
import { StatCard } from '@/components/dashboard/stat-card';
import { StatCardSkeleton, ChartSkeleton } from '@/components/shared/skeleton';
import { ErrorBanner } from '@/components/shared/error-banner';
import { EmptyState } from '@/components/shared/empty-state';
import { BudgetProgressChart } from '@/components/charts/budget-progress-chart';
import { MonthlyTrendChart } from '@/components/charts/monthly-trend-chart';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useFetch } from '@/hooks/use-fetch';
import { getGoals, getForecast, getTransactions } from '@/services/api';
import { formatCurrency, formatDate } from '@/utils/format';
import { Goal, Transaction } from '@/types';

export default function PlanningPage() {
  const { data: goalsData, loading: goalsLoading, error: goalsError, refetch } = useFetch(getGoals, []);
  const { data: forecastData, loading: forecastLoading } = useFetch(getForecast, []);
  const { data: txData } = useFetch(getTransactions, []);

  const goals: Goal[] = goalsData?.goals || goalsData || [];
  const transactions: Transaction[] = txData?.transactions || txData || [];

  const budgetData = useMemo(() => {
    const categoryMap: Record<string, number> = {};
    for (const tx of transactions) {
      if (tx.type !== 'income' && tx.amount < 0) {
        categoryMap[tx.category] = (categoryMap[tx.category] || 0) + Math.abs(tx.amount);
      }
    }
    return Object.entries(categoryMap)
      .map(([category, spent]) => ({ category, budget: spent * 1.25, spent }))
      .sort((a, b) => b.spent - a.spent)
      .slice(0, 5);
  }, [transactions]);

  const forecastTrend = useMemo(() => {
    if (forecastData?.forecast) {
      return forecastData.forecast.map((f: { month: string; expense: number }) => ({ month: f.month, amount: f.expense }));
    }
    return [];
  }, [forecastData]);

  const emergencyFund = useMemo(() => {
    const monthlyExpense = transactions.length > 0
      ? transactions.filter(t => t.type !== 'income' && t.amount < 0).reduce((s, t) => s + Math.abs(t.amount), 0) / Math.max(1, new Set(transactions.map(t => t.date?.slice(0, 7))).size)
      : 0;
    const target = monthlyExpense * 6;
    const current = goals.find(g => g.name?.toLowerCase().includes('emergency'))?.current_amount || target * 0.3;
    return { target, current, monthlyExpense };
  }, [transactions, goals]);

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Financial Planning</h2>
          <p className="text-sm text-muted-foreground">Set goals, track progress, and get AI-powered recommendations</p>
        </div>

        {goalsError && <ErrorBanner message={goalsError} onRetry={refetch} />}

        {/* Summary cards */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {goalsLoading ? (
            <>
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
            </>
          ) : (
            <>
              <StatCard title="Active Goals" value={`${goals.length}`} icon={Target} gradient="from-chart-1/20 to-chart-4/10" delay={0} />
              <StatCard title="Total Target" value={formatCurrency(goals.reduce((s, g) => s + (g.target_amount || 0), 0))} icon={PiggyBank} gradient="from-chart-2/20 to-chart-6/10" delay={0.05} />
              <StatCard title="Total Saved" value={formatCurrency(goals.reduce((s, g) => s + (g.current_amount || 0), 0))} icon={TrendingUp} gradient="from-success/20 to-chart-2/10" delay={0.1} />
              <StatCard title="Emergency Fund" value={`${((emergencyFund.current / Math.max(1, emergencyFund.target)) * 100).toFixed(0)}%`} icon={Shield} gradient="from-warning/20 to-chart-3/10" delay={0.15} />
            </>
          )}
        </div>

        {/* Goals grid */}
        <div>
          <h3 className="mb-4 text-lg font-semibold">Savings Goals</h3>
          {goalsLoading ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              <ChartSkeleton />
              <ChartSkeleton />
              <ChartSkeleton />
            </div>
          ) : goals.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {goals.map((goal, i) => {
                const pct = goal.target_amount > 0 ? Math.min(100, (goal.current_amount / goal.target_amount) * 100) : 0;
                const remaining = Math.max(0, goal.target_amount - goal.current_amount);
                const priorityColor = goal.priority === 'high' ? 'text-destructive' : goal.priority === 'medium' ? 'text-warning' : 'text-success';

                return (
                  <motion.div
                    key={goal.id || i}
                    initial={{ opacity: 0, y: 16 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                  >
                    <Card className="glass border-white/5 p-5 transition-all hover:border-white/10 hover:shadow-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-chart-1/20 to-chart-4/10">
                            <Target className="h-5 w-5 text-chart-1" />
                          </div>
                          <div>
                            <p className="font-semibold">{goal.name}</p>
                            {goal.category && <Badge variant="secondary" className="text-xs">{goal.category}</Badge>}
                          </div>
                        </div>
                        {goal.priority && (
                          <span className={`text-xs font-medium capitalize ${priorityColor}`}>{goal.priority}</span>
                        )}
                      </div>

                      <div className="mt-4">
                        <div className="mb-1.5 flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">{formatCurrency(goal.current_amount)}</span>
                          <span className="text-muted-foreground">{formatCurrency(goal.target_amount)}</span>
                        </div>
                        <div className="relative h-2.5 w-full overflow-hidden rounded-full bg-muted">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${pct}%` }}
                            transition={{ duration: 0.8, delay: i * 0.05 }}
                            className="h-full rounded-full bg-gradient-to-r from-chart-1 to-chart-4"
                          />
                        </div>
                        <div className="mt-2 flex items-center justify-between text-xs">
                          <span className="font-semibold text-chart-1">{pct.toFixed(0)}% complete</span>
                          <span className="text-muted-foreground">{formatCurrency(remaining)} left</span>
                        </div>
                      </div>

                      {goal.deadline && (
                        <div className="mt-3 flex items-center gap-1.5 text-xs text-muted-foreground">
                          <Calendar className="h-3 w-3" />
                          Due {formatDate(goal.deadline)}
                        </div>
                      )}
                    </Card>
                  </motion.div>
                );
              })}
            </div>
          ) : (
            <Card className="glass border-white/5">
              <EmptyState
                icon={Target}
                title="No goals set yet"
                description="Your savings goals will appear here once they're created in the backend."
              />
            </Card>
          )}
        </div>

        {/* Emergency fund + Budget recommendations */}
        <div className="grid gap-4 lg:grid-cols-2">
          {/* Emergency fund */}
          <ChartCard title="Emergency Fund" description="6 months of expenses target" icon={Shield}>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-3xl font-bold">{formatCurrency(emergencyFund.current)}</p>
                  <p className="text-xs text-muted-foreground">of {formatCurrency(emergencyFund.target)} target</p>
                </div>
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-warning/15">
                  <Shield className="h-8 w-8 text-warning" />
                </div>
              </div>
              <div className="relative h-3 w-full overflow-hidden rounded-full bg-muted">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(100, (emergencyFund.current / Math.max(1, emergencyFund.target)) * 100)}%` }}
                  transition={{ duration: 0.8 }}
                  className="h-full rounded-full bg-gradient-to-r from-warning to-chart-3"
                />
              </div>
              <div className="flex items-center gap-2 rounded-lg border border-border bg-card/40 p-3">
                <AlertCircle className="h-4 w-4 shrink-0 text-warning" />
                <p className="text-xs text-muted-foreground">
                  Aim for 3-6 months of expenses. Monthly expense: {formatCurrency(emergencyFund.monthlyExpense)}
                </p>
              </div>
            </div>
          </ChartCard>

          {/* Budget recommendations */}
          <ChartCard title="Budget Recommendations" description="AI-suggested category budgets" icon={PiggyBank}>
            {budgetData.length > 0 ? (
              <BudgetProgressChart data={budgetData} />
            ) : (
              <EmptyState icon={PiggyBank} title="No budget data" description="Upload transactions to get recommendations." />
            )}
          </ChartCard>
        </div>

        {/* AI Planning Summary */}
        <ChartCard title="AI Planning Summary" description="Insights from your AI copilot" icon={Sparkles}>
          {forecastLoading ? (
            <ChartSkeleton />
          ) : forecastData?.summary || forecastData?.recommendations?.length ? (
            <div className="space-y-3">
              {forecastData.summary && (
                <div className="rounded-xl border border-border bg-card/40 p-4">
                  <p className="text-sm text-muted-foreground">{forecastData.summary}</p>
                </div>
              )}
              {forecastData.recommendations && forecastData.recommendations.length > 0 && (
                <div className="space-y-2">
                  {forecastData.recommendations.map((rec: string, i: number) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="flex items-start gap-3 rounded-xl border border-border bg-card/40 p-3"
                    >
                      <div className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-chart-1/15 text-xs font-bold text-chart-1">
                        {i + 1}
                      </div>
                      <p className="text-sm text-muted-foreground">{rec}</p>
                    </motion.div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <EmptyState icon={Sparkles} title="No AI summary yet" description="Upload transactions and generate a forecast to get planning insights." />
          )}
        </ChartCard>

        {/* Forecast trend */}
        {forecastTrend.length > 0 && (
          <ChartCard title="Expense Forecast" description="Projected spending trend" icon={TrendingUp}>
            <MonthlyTrendChart data={forecastTrend} name="Forecast" color="hsl(var(--chart-4))" />
          </ChartCard>
        )}
      </div>
    </AppShell>
  );
}
