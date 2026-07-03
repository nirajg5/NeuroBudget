'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  Brain,
  ArrowRight,
  MessageSquare,
  Upload,
  BarChart3,
  Target,
  FileText,
  Sparkles,
  Database,
  Bot,
  GitBranch,
  Cloud,
  Zap,
  Shield,
  TrendingUp,
} from 'lucide-react';
import { Footer } from '@/components/layout/footer';
import { Button } from '@/components/ui/button';

const features = [
  {
    icon: MessageSquare,
    title: 'AI Financial Chat',
    description: 'Chat with an AI copilot that understands your financial data and provides personalized insights.',
    gradient: 'from-chart-1 to-chart-4',
  },
  {
    icon: Upload,
    title: 'CSV Upload & Parsing',
    description: 'Upload transaction CSVs with automatic categorization, validation, and intelligent processing.',
    gradient: 'from-chart-2 to-chart-6',
  },
  {
    icon: BarChart3,
    title: 'Advanced Analytics',
    description: 'Interactive charts for expense breakdowns, merchant rankings, trends, and spending heatmaps.',
    gradient: 'from-chart-3 to-chart-5',
  },
  {
    icon: Target,
    title: 'Smart Planning',
    description: 'Set savings goals, track progress, and get AI-powered budget recommendations.',
    gradient: 'from-chart-4 to-chart-1',
  },
  {
    icon: FileText,
    title: 'Automated Reports',
    description: 'Generate monthly financial summaries with downloadable PDF reports.',
    gradient: 'from-chart-5 to-chart-3',
  },
  {
    icon: TrendingUp,
    title: 'Financial Forecasting',
    description: 'Predict future spending patterns and savings with AI-driven forecasting models.',
    gradient: 'from-chart-6 to-chart-2',
  },
];

const techStack = [
  { name: 'Next.js 15', icon: Zap, desc: 'App Router' },
  { name: 'FastAPI', icon: Zap, desc: 'Python Backend' },
  { name: 'PostgreSQL', icon: Database, desc: 'Relational DB' },
  { name: 'Pinecone', icon: Cloud, desc: 'Vector Database' },
  { name: 'LangGraph', icon: GitBranch, desc: 'Multi-Agent' },
  { name: 'OpenRouter', icon: Bot, desc: 'LLM Provider' },
];

const agents = [
  { name: 'Transaction Analyst', desc: 'Categorizes and analyzes spending patterns', icon: BarChart3 },
  { name: 'Budget Advisor', desc: 'Recommends budgets and savings strategies', icon: Target },
  { name: 'Risk Assessor', desc: 'Evaluates financial risk and health score', icon: Shield },
  { name: 'Forecast Agent', desc: 'Predicts future income and expenses', icon: TrendingUp },
];

const architectureSteps = [
  { step: '01', title: 'Data Ingestion', desc: 'CSV uploads are parsed and stored in PostgreSQL with vector embeddings in Pinecone.' },
  { step: '02', title: 'Multi-Agent Processing', desc: 'LangGraph orchestrates specialized AI agents that analyze transactions, assess risk, and generate insights.' },
  { step: '03', title: 'AI Reasoning', desc: 'OpenRouter LLM powers natural language understanding for chat, summaries, and recommendations.' },
  { step: '04', title: 'Intelligent Output', desc: 'Real-time dashboards, forecasts, and reports delivered through a modern Next.js frontend.' },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Animated background */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute left-1/4 top-0 h-[500px] w-[500px] rounded-full bg-chart-1/10 blur-[150px]" />
        <div className="absolute right-1/4 top-1/3 h-[400px] w-[400px] rounded-full bg-chart-4/10 blur-[150px]" />
        <div className="absolute bottom-0 left-1/3 h-[400px] w-[400px] rounded-full bg-chart-5/5 blur-[150px]" />
      </div>

      {/* Nav */}
      <nav className="relative z-10 flex items-center justify-between px-6 py-5 md:px-12">
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-chart-1 to-chart-4 shadow-lg shadow-chart-1/20">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <span className="text-lg font-bold">
            Neuro<span className="gradient-text">Budget</span>
          </span>
        </div>
        <div className="hidden items-center gap-6 md:flex">
          <Link href="/dashboard" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Dashboard</Link>
          <Link href="/chat" className="text-sm text-muted-foreground hover:text-foreground transition-colors">AI Chat</Link>
          <Link href="/analytics" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Analytics</Link>
          <Link href="/settings" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Settings</Link>
        </div>
        <Link href="/dashboard">
          <Button className="gap-2 bg-gradient-to-r from-chart-1 to-chart-4 text-white hover:opacity-90">
            Launch App <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </nav>

      {/* Hero */}
      <section className="relative z-10 mx-auto max-w-7xl px-6 pt-20 pb-32 text-center md:px-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="inline-flex items-center gap-2 rounded-full border border-border bg-card/40 px-4 py-1.5 backdrop-blur-xl"
        >
          <Sparkles className="h-3.5 w-3.5 text-chart-1" />
          <span className="text-xs font-medium text-muted-foreground">Powered by LangGraph Multi-Agent AI</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mt-8 text-5xl font-bold tracking-tight md:text-7xl"
        >
          Your AI-Powered
          <br />
          <span className="gradient-text">Financial Copilot</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl"
        >
          NeuroBudget analyzes your transactions, forecasts spending, and provides
          intelligent financial planning — all powered by a multi-agent AI workflow.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
        >
          <Link href="/dashboard">
            <Button size="lg" className="gap-2 bg-gradient-to-r from-chart-1 to-chart-4 text-white hover:opacity-90 px-8">
              Get Started <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
          <Link href="/chat">
            <Button size="lg" variant="outline" className="gap-2 border-border bg-card/40 backdrop-blur-xl">
              <MessageSquare className="h-4 w-4" /> Try AI Chat
            </Button>
          </Link>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mx-auto mt-20 grid max-w-3xl grid-cols-2 gap-4 md:grid-cols-4"
        >
          {[
            { value: '4', label: 'AI Agents' },
            { value: '7', label: 'API Endpoints' },
            { value: 'Real-time', label: 'Streaming Chat' },
            { value: '100%', label: 'Type Safe' },
          ].map((stat, i) => (
            <div key={i} className="glass rounded-2xl p-5">
              <p className="text-2xl font-bold gradient-text">{stat.value}</p>
              <p className="mt-1 text-xs text-muted-foreground">{stat.label}</p>
            </div>
          ))}
        </motion.div>
      </section>

      {/* Features */}
      <section className="relative z-10 mx-auto max-w-7xl px-6 py-20 md:px-12">
        <div className="text-center">
          <h2 className="text-3xl font-bold md:text-4xl">Everything you need to manage finances</h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted-foreground">
            A complete AI financial toolkit — from transaction analysis to intelligent forecasting.
          </p>
        </div>

        <div className="mt-16 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.05 }}
              className="group glass rounded-2xl p-6 transition-all hover:border-white/10 hover:shadow-xl hover:shadow-chart-1/5"
            >
              <div className={`flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${feature.gradient} shadow-lg`}>
                <feature.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="mt-4 text-lg font-semibold">{feature.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* AI Agents */}
      <section className="relative z-10 mx-auto max-w-7xl px-6 py-20 md:px-12">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-border bg-card/40 px-4 py-1.5">
            <Bot className="h-3.5 w-3.5 text-chart-4" />
            <span className="text-xs font-medium text-muted-foreground">LangGraph Multi-Agent System</span>
          </div>
          <h2 className="mt-6 text-3xl font-bold md:text-4xl">Meet your AI agents</h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted-foreground">
            Specialized AI agents work together to analyze, advise, and forecast your finances.
          </p>
        </div>

        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {agents.map((agent, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.08 }}
              className="glass rounded-2xl p-6 text-center"
            >
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-chart-4/20 to-chart-1/10">
                <agent.icon className="h-7 w-7 text-chart-4" />
              </div>
              <h3 className="mt-4 font-semibold">{agent.name}</h3>
              <p className="mt-2 text-xs text-muted-foreground">{agent.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Architecture */}
      <section className="relative z-10 mx-auto max-w-7xl px-6 py-20 md:px-12">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-border bg-card/40 px-4 py-1.5">
            <GitBranch className="h-3.5 w-3.5 text-chart-2" />
            <span className="text-xs font-medium text-muted-foreground">System Architecture</span>
          </div>
          <h2 className="mt-6 text-3xl font-bold md:text-4xl">How it works</h2>
        </div>

        <div className="mt-16 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {architectureSteps.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.1 }}
              className="relative glass rounded-2xl p-6"
            >
              <span className="text-4xl font-bold text-chart-1/30">{step.step}</span>
              <h3 className="mt-2 font-semibold">{step.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{step.desc}</p>
              {i < architectureSteps.length - 1 && (
                <ArrowRight className="absolute -right-3 top-1/2 hidden h-5 w-5 text-chart-1/30 lg:block" />
              )}
            </motion.div>
          ))}
        </div>
      </section>

      {/* Tech Stack */}
      <section className="relative z-10 mx-auto max-w-7xl px-6 py-20 md:px-12">
        <div className="text-center">
          <h2 className="text-3xl font-bold md:text-4xl">Built with modern technology</h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted-foreground">
            A production-grade stack combining the best of AI and web technologies.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
          {techStack.map((tech, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.3, delay: i * 0.05 }}
              className="glass flex flex-col items-center rounded-2xl p-5 text-center transition-all hover:border-chart-1/30"
            >
              <tech.icon className="h-7 w-7 text-chart-1" />
              <p className="mt-3 text-sm font-semibold">{tech.name}</p>
              <p className="text-xs text-muted-foreground">{tech.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="relative z-10 mx-auto max-w-5xl px-6 py-20 md:px-12">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="gradient-border relative overflow-hidden rounded-3xl"
        >
          <div className="rounded-3xl bg-gradient-to-br from-chart-1/10 via-card/40 to-chart-4/10 p-12 text-center backdrop-blur-xl">
            <h2 className="text-3xl font-bold md:text-4xl">Ready to take control of your finances?</h2>
            <p className="mx-auto mt-4 max-w-xl text-muted-foreground">
              Start by uploading your transactions and let AI do the heavy lifting.
            </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Link href="/upload">
                <Button size="lg" className="gap-2 bg-gradient-to-r from-chart-1 to-chart-4 text-white hover:opacity-90 px-8">
                  Upload Data <Upload className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/dashboard">
                <Button size="lg" variant="outline" className="gap-2 border-border bg-card/40 backdrop-blur-xl">
                  View Dashboard <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </div>
        </motion.div>
      </section>

      <Footer />
    </div>
  );
}
