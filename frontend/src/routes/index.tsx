import { createFileRoute } from "@tanstack/react-router";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip,
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
} from "recharts";
import {
  TrendingUp, TrendingDown, PiggyBank, Wallet, AlertTriangle,
  Sparkles, Target, ArrowUpRight,
} from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Dashboard — NeuroBudget" },
      { name: "description", content: "AI-powered finance dashboard with spending insights, budgets and goals." },
    ],
  }),
  component: Dashboard,
});

const pieData = [
  { name: "Groceries", value: 420 },
  { name: "Rent", value: 1200 },
  { name: "Transport", value: 180 },
  { name: "Entertainment", value: 240 },
  { name: "Utilities", value: 160 },
];
const COLORS = ["var(--chart-1)", "var(--chart-2)", "var(--chart-3)", "var(--chart-4)", "var(--chart-5)"];

const monthly = [
  { m: "Jan", spend: 1800 }, { m: "Feb", spend: 2100 }, { m: "Mar", spend: 1950 },
  { m: "Apr", spend: 2400 }, { m: "May", spend: 2200 }, { m: "Jun", spend: 2600 },
  { m: "Jul", spend: 2300 }, { m: "Aug", spend: 2500 },
];

const transactions = [
  { date: "Aug 12", desc: "Whole Foods", cat: "Groceries", amt: -84.21 },
  { date: "Aug 11", desc: "Salary — Acme Inc", cat: "Income", amt: 4200 },
  { date: "Aug 10", desc: "Uber", cat: "Transport", amt: -18.5 },
  { date: "Aug 09", desc: "Netflix", cat: "Entertainment", amt: -15.99 },
  { date: "Aug 08", desc: "Electric Bill", cat: "Utilities", amt: -92.4 },
];

function StatCard({
  title, value, delta, trend, icon: Icon,
}: { title: string; value: string; delta: string; trend: "up" | "down"; icon: any }) {
  return (
    <Card className="shadow-[var(--shadow-soft)] border-border/60">
      <CardHeader className="flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary-soft text-primary">
          <Icon className="h-4 w-4" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-semibold tracking-tight">{value}</div>
        <div className={`mt-1 flex items-center gap-1 text-xs ${trend === "up" ? "text-[color:var(--success)]" : "text-destructive"}`}>
          {trend === "up" ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
          {delta} vs last month
        </div>
      </CardContent>
    </Card>
  );
}

function Dashboard() {
  return (
    <div className="mx-auto max-w-7xl space-y-6 p-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Welcome back, Alex</h1>
          <p className="text-sm text-muted-foreground">Here's your financial overview for August.</p>
        </div>
        <Button className="gap-2">
          <Sparkles className="h-4 w-4" /> Ask AI
        </Button>
      </div>

      {/* Stat cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Spending" value="$2,500" delta="+8.2%" trend="down" icon={Wallet} />
        <StatCard title="Savings" value="$1,420" delta="+12.4%" trend="up" icon={PiggyBank} />
        <StatCard title="Top Category" value="Rent" delta="$1,200" trend="down" icon={ArrowUpRight} />
        <StatCard title="Monthly Budget" value="$3,000" delta="83% used" trend="up" icon={Target} />
      </div>

      {/* Charts row */}
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="shadow-[var(--shadow-soft)] lg:col-span-2">
          <CardHeader>
            <CardTitle>Monthly Spending</CardTitle>
            <CardDescription>Last 8 months</CardDescription>
          </CardHeader>
          <CardContent className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthly} margin={{ left: -10, right: 10, top: 10 }}>
                <defs>
                  <linearGradient id="spendFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--chart-1)" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="var(--chart-1)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="m" stroke="var(--muted-foreground)" fontSize={12} />
                <YAxis stroke="var(--muted-foreground)" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    background: "var(--card)", border: "1px solid var(--border)",
                    borderRadius: 12, fontSize: 12,
                  }}
                />
                <Area type="monotone" dataKey="spend" stroke="var(--chart-1)" strokeWidth={2} fill="url(#spendFill)" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="shadow-[var(--shadow-soft)]">
          <CardHeader>
            <CardTitle>Spending Breakdown</CardTitle>
            <CardDescription>By category</CardDescription>
          </CardHeader>
          <CardContent className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={85} paddingAngle={3}>
                  {pieData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: "var(--card)", border: "1px solid var(--border)",
                    borderRadius: 12, fontSize: 12,
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Insights row */}
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="shadow-[var(--shadow-soft)] lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-primary" /> AI Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { t: "Reduce dining out by 15%", d: "You spent $310 this month — switching 2 meals/week to home-cooked could save ~$95." },
              { t: "Refinance your subscriptions", d: "We found 3 overlapping streaming services. Consolidating saves $24/mo." },
              { t: "Boost emergency fund", d: "At current rate you'll hit your $5k goal in 4 months — consider +$120/mo to finish in 3." },
            ].map((r) => (
              <div key={r.t} className="rounded-xl border bg-[var(--gradient-soft)] p-4">
                <div className="font-medium text-sm">{r.t}</div>
                <p className="text-xs text-muted-foreground mt-1">{r.d}</p>
              </div>
            ))}
          </CardContent>
        </Card>

        <div className="space-y-4">
          <Card className="shadow-[var(--shadow-soft)] border-[color:var(--warning)]/40">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <AlertTriangle className="h-4 w-4 text-[color:var(--warning)]" /> Risk Alert
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Entertainment spend is <span className="font-medium text-foreground">42% above</span> your usual pattern.
              </p>
              <Badge variant="secondary" className="mt-3">Action suggested</Badge>
            </CardContent>
          </Card>

          <Card className="shadow-[var(--shadow-soft)]">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <Target className="h-4 w-4 text-primary" /> Goal: Vacation Fund
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">$1,820 / $3,000</span>
                <span className="font-medium">61%</span>
              </div>
              <Progress value={61} />
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Transactions */}
      <Card className="shadow-[var(--shadow-soft)]">
        <CardHeader>
          <CardTitle>Recent Transactions</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Description</TableHead>
                <TableHead>Category</TableHead>
                <TableHead className="text-right">Amount</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transactions.map((t) => (
                <TableRow key={t.desc}>
                  <TableCell className="text-muted-foreground">{t.date}</TableCell>
                  <TableCell className="font-medium">{t.desc}</TableCell>
                  <TableCell><Badge variant="outline">{t.cat}</Badge></TableCell>
                  <TableCell className={`text-right font-medium ${t.amt > 0 ? "text-[color:var(--success)]" : ""}`}>
                    {t.amt > 0 ? "+" : ""}${Math.abs(t.amt).toFixed(2)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
