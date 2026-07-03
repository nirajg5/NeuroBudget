'use client';

import { useMemo } from 'react';
import { Wallet, BarChart3, TrendingUp, Store, ShieldCheck, Calendar } from 'lucide-react';
import { AppShell } from '@/components/layout/app-shell';
import { ChartCard } from '@/components/dashboard/chart-card';
import { StatCard } from '@/components/dashboard/stat-card';
import { StatCardSkeleton, ChartSkeleton } from '@/components/shared/skeleton';
import { ErrorBanner } from '@/components/shared/error-banner';
import { EmptyState } from '@/components/shared/empty-state';
import { ExpensePieChart } from '@/components/charts/expense-pie-chart';
import { ExpenseBarChart } from '@/components/charts/expense-bar-chart';
import { IncomeVsExpenseChart } from '@/components/charts/income-vs-expense-chart';
import { MonthlyTrendChart } from '@/components/charts/monthly-trend-chart';
import { RiskGauge } from '@/components/charts/risk-gauge';
import { MerchantRankingChart } from '@/components/charts/merchant-ranking-chart';
import { useFetch } from '@/hooks/use-fetch';
import { getTransactions, getForecast } from '@/services/api';
import { formatCurrency } from '@/utils/format';
import { Transaction } from '@/types';

export default function AnalyticsPage() {
  const { data: txData, loading, error, refetch } = useFetch(getTransactions, []);
  const { data: forecastData } = useFetch(getForecast, []);

  const transactions: Transaction[] = txData?.transactions || txData || [];

  const analytics = useMemo(() => {
    let income = 0, expense = 0;
    const categoryMap: Record<string, number> = {};
    const merchantMap: Record<string, number> = {};
    const monthlyMap: Record<string, { income: number; expense: number; amount: number }> = {};

    for (const tx of transactions) {
      const amt = Math.abs(tx.amount || 0);
      if (tx.type === 'income' || tx.amount > 0) {
        income += amt;
      } else {
        expense += amt;
        categoryMap[tx.category] = (categoryMap[tx.category] || 0) + amt;
        merchantMap[tx.merchant] = (merchantMap[tx.merchant] || 0) + amt;
      }
      const month = tx.date?.slice(0, 7) || 'Unknown';
      if (!monthlyMap[month]) monthlyMap[month] = { income: 0, expense: 0, amount: 0 };
      if (tx.type === 'income' || tx.amount > 0) monthlyMap[month].income += amt;
      else {
        monthlyMap[month].expense += amt;
        monthlyMap[month].amount += amt;
      }
    }

    const pieData = Object.entries(categoryMap).map(([name, value]) => ({ name, value })).sort((a, b) => b.value - a.value);
    const barData = pieData.slice(0, 6);
    const merchantData = Object.entries(merchantMap).map(([merchant, amount]) => ({ merchant, amount })).sort((a, b) => b.amount - a.amount);
    const lineData = Object.entries(monthlyMap).sort((a, b) => a[0].localeCompare(b[0])).map(([month, vals]) => ({
      month: new Date(month + '-01').toLocaleDateString('en-US', { month: 'short' }),
      income: vals.income,
      expense: vals.expense,
    }));
    const trendData = Object.entries(monthlyMap).sort((a, b) => a[0].localeCompare(b[0])).map(([month, vals]) => ({
      month: new Date(month + '-01').toLocaleDateString('en-US', { month: 'short' }),
      amount: vals.amount,
    }));

    const savings = income - expense;
    const savingsRate = income > 0 ? (savings / income) * 100 : 0;
    const riskScore = forecastData?.risk_score ?? (savingsRate < 0 ? 80 : savingsRate < 10 ? 60 : savingsRate < 20 ? 40 : 20);

    return { income, expense, savings, savingsRate, riskScore, pieData, barData, merchantData, lineData, trendData };
  }, [transactions, forecastData]);

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Financial Analytics</h2>
          <p className="text-sm text-muted-foreground">Deep dive into your spending patterns and financial health</p>
        </div>

        {error && <ErrorBanner message={error} onRetry={refetch} />}

        {/* Summary stats */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {loading ? (
            <>
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
            </>
          ) : (
            <>
              <StatCard title="Total Income" value={formatCurrency(analytics.income)} icon={Wallet} gradient="from-success/20 to-chart-2/10" delay={0} />
              <StatCard title="Total Expense" value={formatCurrency(analytics.expense)} icon={BarChart3} gradient="from-destructive/20 to-chart-5/10" delay={0.05} />
              <StatCard title="Net Savings" value={formatCurrency(analytics.savings)} icon={TrendingUp} gradient="from-chart-1/20 to-chart-4/10" delay={0.1} />
              <StatCard title="Savings Rate" value={`${analytics.savingsRate.toFixed(1)}%`} icon={ShieldCheck} gradient="from-chart-3/20 to-chart-6/10" delay={0.15} />
            </>
          )}
        </div>

        {/* Charts grid */}
        <div className="grid gap-4 lg:grid-cols-2">
          {/* Expense by category - pie */}
          {loading ? <ChartSkeleton /> : (
            <ChartCard title="Expense by Category" description="Distribution across categories" icon={BarChart3}>
              {analytics.pieData.length > 0 ? (
                <ExpensePieChart data={analytics.pieData} />
              ) : (
                <EmptyState icon={BarChart3} title="No data available" description="Upload transactions to see analytics." />
              )}
            </ChartCard>
          )}

          {/* Expense by category - bar */}
          {loading ? <ChartSkeleton /> : (
            <ChartCard title="Top Categories" description="Highest spending categories" icon={Wallet}>
              {analytics.barData.length > 0 ? (
                <ExpenseBarChart data={analytics.barData} />
              ) : (
                <EmptyState icon={Wallet} title="No data available" />
              )}
            </ChartCard>
          )}

          {/* Income vs Expense */}
          {loading ? <ChartSkeleton /> : (
            <ChartCard title="Income vs Expense" description="Monthly comparison" icon={TrendingUp}>
              {analytics.lineData.length > 0 ? (
                <IncomeVsExpenseChart data={analytics.lineData} />
              ) : (
                <EmptyState icon={TrendingUp} title="No data available" />
              )}
            </ChartCard>
          )}

          {/* Monthly expense trend */}
          {loading ? <ChartSkeleton /> : (
            <ChartCard title="Monthly Expense Trend" description="Spending over time" icon={Calendar}>
              {analytics.trendData.length > 0 ? (
                <MonthlyTrendChart data={analytics.trendData} name="Expense" color="hsl(var(--chart-5))" />
              ) : (
                <EmptyState icon={Calendar} title="No trend data" />
              )}
            </ChartCard>
          )}

          {/* Top merchants */}
          {loading ? <ChartSkeleton /> : (
            <ChartCard title="Top Merchants" description="Where you spend the most" icon={Store}>
              {analytics.merchantData.length > 0 ? (
                <MerchantRankingChart data={analytics.merchantData} />
              ) : (
                <EmptyState icon={Store} title="No merchant data" />
              )}
            </ChartCard>
          )}

          {/* Risk gauge */}
          {loading ? <ChartSkeleton /> : (
            <ChartCard title="Risk Gauge" description="AI-assessed financial risk" icon={ShieldCheck}>
              <RiskGauge score={analytics.riskScore} />
            </ChartCard>
          )}
        </div>

        {/* Spending heatmap placeholder */}
        <ChartCard title="Spending Heatmap" description="Activity by day and time" icon={Calendar}>
          {transactions.length > 0 ? (
            <SpendingHeatmap transactions={transactions} />
          ) : (
            <EmptyState icon={Calendar} title="No heatmap data" description="Upload transactions to see your spending heatmap." />
          )}
        </ChartCard>
      </div>
    </AppShell>
  );
}

function SpendingHeatmap({ transactions }: { transactions: Transaction[] }) {
  const heatmap = useMemo(() => {
    const grid: Record<string, number[]> = {};
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    for (const d of days) grid[d] = new Array(24).fill(0);

    for (const tx of transactions) {
      if (tx.type === 'income' || tx.amount > 0) continue;
      const date = new Date(tx.date);
      const day = days[date.getDay()];
      const hour = date.getHours();
      grid[day][hour] += Math.abs(tx.amount);
    }

    const maxVal = Math.max(...Object.values(grid).flat());
    return { grid, days, maxVal };
  }, [transactions]);

  const getColor = (value: number) => {
    if (value === 0) return 'hsl(var(--muted) / 0.2)';
    const intensity = Math.min(1, value / (heatmap.maxVal || 1));
    return `hsl(var(--chart-1) / ${0.15 + intensity * 0.85})`;
  };

  return (
    <div className="overflow-x-auto scrollbar-thin">
      <div className="min-w-[600px]">
        <div className="flex">
          <div className="w-10" />
          {Array.from({ length: 24 }).map((_, h) => (
            <div key={h} className="flex-1 text-center text-[9px] text-muted-foreground">
              {h % 3 === 0 ? `${h}h` : ''}
            </div>
          ))}
        </div>
        {heatmap.days.map((day) => (
          <div key={day} className="flex items-center gap-1">
            <div className="w-10 text-xs text-muted-foreground">{day}</div>
            <div className="flex flex-1 gap-0.5">
              {heatmap.grid[day].map((val, h) => (
                <div
                  key={h}
                  className="h-6 flex-1 rounded-sm transition-colors hover:ring-1 hover:ring-chart-1"
                  style={{ backgroundColor: getColor(val) }}
                  title={`${day} ${h}:00 — ${val.toFixed(2)}`}
                />
              ))}
            </div>
          </div>
        ))}
        <div className="mt-3 flex items-center justify-end gap-2 text-xs text-muted-foreground">
          <span>Less</span>
          <div className="flex gap-0.5">
            {[0.2, 0.4, 0.6, 0.8, 1].map((o) => (
              <div key={o} className="h-3 w-6 rounded-sm" style={{ backgroundColor: `hsl(var(--chart-1) / ${o})` }} />
            ))}
          </div>
          <span>More</span>
        </div>
      </div>
    </div>
  );
}
