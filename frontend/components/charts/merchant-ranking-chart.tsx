'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, Cell } from 'recharts';
import { formatCurrency } from '@/utils/format';

interface MerchantRankingChartProps {
  data: Array<{ merchant: string; amount: number }>;
}

export function MerchantRankingChart({ data }: MerchantRankingChartProps) {
  if (!data || data.length === 0) {
    return <div className="flex h-[300px] items-center justify-center text-sm text-muted-foreground">No data available</div>;
  }

  const sorted = [...data].sort((a, b) => b.amount - a.amount).slice(0, 8);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={sorted} layout="vertical" margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={false} />
        <XAxis
          type="number"
          stroke="hsl(var(--muted-foreground))"
          fontSize={11}
          tickLine={false}
          axisLine={false}
          tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
        />
        <YAxis
          type="category"
          dataKey="merchant"
          stroke="hsl(var(--muted-foreground))"
          fontSize={11}
          tickLine={false}
          axisLine={false}
          width={100}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'hsl(var(--card))',
            border: '1px solid hsl(var(--border))',
            borderRadius: '8px',
            fontSize: '12px',
          }}
          formatter={(value: number) => formatCurrency(value)}
          cursor={{ fill: 'hsl(var(--muted) / 0.3)' }}
        />
        <Bar dataKey="amount" radius={[0, 8, 8, 0]}>
          {sorted.map((_, index) => (
            <Cell key={index} fill={`hsl(var(--chart-${(index % 6) + 1}))`} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
