'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { formatCurrency } from '@/utils/format';

interface IncomeVsExpenseChartProps {
  data: Array<{ month: string; income: number; expense: number }>;
}

export function IncomeVsExpenseChart({ data }: IncomeVsExpenseChartProps) {
  if (!data || data.length === 0) {
    return <div className="flex h-[300px] items-center justify-center text-sm text-muted-foreground">No data available</div>;
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
        <XAxis
          dataKey="month"
          stroke="hsl(var(--muted-foreground))"
          fontSize={11}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke="hsl(var(--muted-foreground))"
          fontSize={11}
          tickLine={false}
          axisLine={false}
          tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'hsl(var(--card))',
            border: '1px solid hsl(var(--border))',
            borderRadius: '8px',
            fontSize: '12px',
          }}
          formatter={(value: number) => formatCurrency(value)}
        />
        <Legend
          iconType="circle"
          wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}
        />
        <Line
          type="monotone"
          dataKey="income"
          stroke="hsl(var(--success))"
          strokeWidth={2.5}
          dot={{ fill: 'hsl(var(--success))', r: 3 }}
          activeDot={{ r: 5 }}
          name="Income"
        />
        <Line
          type="monotone"
          dataKey="expense"
          stroke="hsl(var(--destructive))"
          strokeWidth={2.5}
          dot={{ fill: 'hsl(var(--destructive))', r: 3 }}
          activeDot={{ r: 5 }}
          name="Expense"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
