import { createFileRoute } from "@tanstack/react-router";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  BarChart, Bar, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid,
} from "recharts";
import { Target, AlertTriangle, Sparkles, TrendingUp, Plus } from "lucide-react";

export const Route = createFileRoute("/insights")({
  head: () => ({
    meta: [
      { title: "Financial Insights — NeuroBudget" },
      { name: "description", content: "Budget insights, goal planning and risk alerts powered by AI." },
    ],
  }),
  component: InsightsPage,
});

const budgets = [
  { cat: "Groceries", spent: 420, limit: 500 },
  { cat: "Rent", spent: 1200, limit: 1200 },
  { cat: "Transport", spent: 180, limit: 250 },
  { cat: "Entertainment", spent: 240, limit: 200 },
  { cat: "Utilities", spent: 160, limit: 200 },
];

const compare = [
  { m: "May", you: 2200, avg: 2400 },
  { m: "Jun", you: 2600, avg: 2450 },
  { m: "Jul", you: 2300, avg: 2480 },
  { m: "Aug", you: 2500, avg: 2500 },
];

const goals = [
  { name: "Vacation Fund", current: 1820, target: 3000 },
  { name: "Emergency Fund", current: 3200, target: 5000 },
  { name: "New Laptop", current: 600, target: 1500 },
];

function InsightsPage() {
  return (
    <div className="mx-auto max-w-7xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Financial Insights</h1>
        <p className="text-sm text-muted-foreground">Track budgets, plan goals, and stay ahead of risks.</p>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        {/* Budget insights */}
        <Card className="shadow-[var(--shadow-soft)] lg:col-span-2">
          <CardHeader>
            <CardTitle>Budget Insights</CardTitle>
            <CardDescription>How each category is tracking this month</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {budgets.map((b) => {
              const pct = Math.min(100, Math.round((b.spent / b.limit) * 100));
              const over = b.spent > b.limit;
              return (
                <div key={b.cat}>
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{b.cat}</span>
                    <span className={over ? "text-destructive" : "text-muted-foreground"}>
                      ${b.spent} / ${b.limit}
                    </span>
                  </div>
                  <Progress value={pct} className={over ? "[&>div]:bg-destructive" : ""} />
                </div>
              );
            })}
          </CardContent>
        </Card>

        {/* Risk alert */}
        <Card className="shadow-[var(--shadow-soft)] border-[color:var(--warning)]/40">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <AlertTriangle className="h-4 w-4 text-[color:var(--warning)]" /> Risk Alerts
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="rounded-xl border bg-background p-3">
              <div className="text-sm font-medium">Entertainment over budget</div>
              <p className="mt-1 text-xs text-muted-foreground">$240 spent vs $200 limit (+20%).</p>
              <Badge variant="destructive" className="mt-2">High</Badge>
            </div>
            <div className="rounded-xl border bg-background p-3">
              <div className="text-sm font-medium">Recurring spike detected</div>
              <p className="mt-1 text-xs text-muted-foreground">Coffee shops are up 35% this month.</p>
              <Badge variant="secondary" className="mt-2">Medium</Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Trend chart */}
      <Card className="shadow-[var(--shadow-soft)]">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-primary" /> You vs Average
          </CardTitle>
          <CardDescription>Your monthly spending compared to similar households</CardDescription>
        </CardHeader>
        <CardContent className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={compare} margin={{ left: -10, right: 10, top: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="m" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip
                contentStyle={{
                  background: "var(--card)", border: "1px solid var(--border)",
                  borderRadius: 12, fontSize: 12,
                }}
              />
              <Bar dataKey="you" fill="var(--chart-1)" radius={[8, 8, 0, 0]} />
              <Bar dataKey="avg" fill="var(--chart-3)" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Goals */}
      <Card className="shadow-[var(--shadow-soft)]">
        <CardHeader className="flex-row items-center justify-between space-y-0">
          <div>
            <CardTitle className="flex items-center gap-2"><Target className="h-4 w-4 text-primary" /> Goal Planning</CardTitle>
            <CardDescription>Track progress toward your savings goals</CardDescription>
          </div>
          <Button variant="outline" size="sm" className="gap-1">
            <Plus className="h-4 w-4" /> New goal
          </Button>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3">
          {goals.map((g) => {
            const pct = Math.round((g.current / g.target) * 100);
            return (
              <div key={g.name} className="rounded-xl border bg-[var(--gradient-soft)] p-4">
                <div className="text-sm font-medium">{g.name}</div>
                <div className="mt-2 text-xl font-semibold">${g.current.toLocaleString()}</div>
                <div className="text-xs text-muted-foreground">of ${g.target.toLocaleString()}</div>
                <Progress value={pct} className="mt-3" />
                <div className="mt-1 text-right text-xs text-muted-foreground">{pct}%</div>
              </div>
            );
          })}
        </CardContent>
      </Card>

      <Card className="shadow-[var(--shadow-soft)]">
        <CardHeader>
          <CardTitle className="flex items-center gap-2"><Sparkles className="h-4 w-4 text-primary" /> AI Recommendations</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-2">
          <div className="rounded-xl border p-4">
            <div className="text-sm font-medium">Move $200 to high-yield savings</div>
            <p className="mt-1 text-xs text-muted-foreground">Based on your buffer, you can safely shift $200 to earn ~4.2% APY.</p>
          </div>
          <div className="rounded-xl border p-4">
            <div className="text-sm font-medium">Cancel duplicate subscriptions</div>
            <p className="mt-1 text-xs text-muted-foreground">We detected overlap between two music apps. Cancelling saves $11/mo.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
