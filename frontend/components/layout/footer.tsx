import Link from 'next/link';
import { Brain, Github, Twitter, Linkedin } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-border bg-card/20">
      <div className="mx-auto max-w-7xl px-6 py-12">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-chart-1 to-chart-4">
                <Brain className="h-4 w-4 text-white" />
              </div>
              <span className="text-base font-bold">
                Neuro<span className="gradient-text">Budget</span>
              </span>
            </div>
            <p className="mt-3 text-sm text-muted-foreground">
              AI-powered financial copilot for intelligent budgeting, forecasting, and planning.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold">Product</h4>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              <li><Link href="/dashboard" className="hover:text-foreground transition-colors">Dashboard</Link></li>
              <li><Link href="/chat" className="hover:text-foreground transition-colors">AI Chat</Link></li>
              <li><Link href="/analytics" className="hover:text-foreground transition-colors">Analytics</Link></li>
              <li><Link href="/planning" className="hover:text-foreground transition-colors">Planning</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold">Resources</h4>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              <li><Link href="/upload" className="hover:text-foreground transition-colors">Upload Data</Link></li>
              <li><Link href="/reports" className="hover:text-foreground transition-colors">Reports</Link></li>
              <li><Link href="/settings" className="hover:text-foreground transition-colors">Settings</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold">Connect</h4>
            <div className="mt-3 flex gap-3">
              <a href="#" className="flex h-9 w-9 items-center justify-center rounded-lg border border-border text-muted-foreground transition-colors hover:text-foreground hover:bg-muted">
                <Github className="h-4 w-4" />
              </a>
              <a href="#" className="flex h-9 w-9 items-center justify-center rounded-lg border border-border text-muted-foreground transition-colors hover:text-foreground hover:bg-muted">
                <Twitter className="h-4 w-4" />
              </a>
              <a href="#" className="flex h-9 w-9 items-center justify-center rounded-lg border border-border text-muted-foreground transition-colors hover:text-foreground hover:bg-muted">
                <Linkedin className="h-4 w-4" />
              </a>
            </div>
          </div>
        </div>

        <div className="mt-10 flex flex-col items-center justify-between gap-4 border-t border-border pt-6 sm:flex-row">
          <p className="text-xs text-muted-foreground">
            © {new Date().getFullYear()} NeuroBudget. Built with FastAPI, LangGraph & Next.js.
          </p>
          <p className="text-xs text-muted-foreground">
            Powered by OpenRouter LLM & Pinecone Vector DB
          </p>
        </div>
      </div>
    </footer>
  );
}
