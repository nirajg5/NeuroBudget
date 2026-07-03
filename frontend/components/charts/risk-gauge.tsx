'use client';

import { RadialBarChart, RadialBar, ResponsiveContainer, PolarAngleAxis } from 'recharts';
import { getRiskColor, getRiskLabel } from '@/utils/format';

interface RiskGaugeProps {
  score: number;
  size?: number;
}

export function RiskGauge({ score, size = 200 }: RiskGaugeProps) {
  const clampedScore = Math.min(100, Math.max(0, score || 0));
  const { label } = getRiskLabel(clampedScore);
  const color = getRiskColor(clampedScore);

  return (
    <div className="flex flex-col items-center">
      <div style={{ width: size, height: size }} className="relative">
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart
            innerRadius="72%"
            outerRadius="100%"
            data={[{ value: clampedScore }]}
            startAngle={90}
            endAngle={-270}
          >
            <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
            <RadialBar
              background={{ fill: 'hsl(var(--muted) / 0.4)' }}
              dataKey="value"
              cornerRadius={20}
              fill={color}
            />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-bold" style={{ color }}>
            {clampedScore.toFixed(0)}
          </span>
          <span className="text-xs font-medium text-muted-foreground">/ 100</span>
        </div>
      </div>
      <p className="mt-2 text-sm font-semibold" style={{ color }}>
        {label}
      </p>
    </div>
  );
}
