// ===== Chat =====
// The backend expects: { question: string, session_id: string }
// The response shape is flexible — different LLM agents may return
// different field names, so we accept several common ones.
export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  question: string;
  session_id: string;
}

export interface ChatResponse {
  response?: string;
  answer?: string;
  message?: string;
  content?: string;
  text?: string;
  agent?: string;
  sources?: string[];
  session_id?: string;
  timestamp?: string;
}

// ===== Transactions =====
export interface Transaction {
  id: string;
  date: string;
  description: string;
  merchant: string;
  category: string;
  amount: number;
  type: 'income' | 'expense';
}

export interface TransactionsResponse {
  transactions: Transaction[];
  total?: number;
  count?: number;
}

// ===== Upload =====
export interface UploadResponse {
  message: string;
  rows_processed?: number;
  count?: number;
  filename?: string;
  errors?: string[];
}

// ===== Reports =====
export interface Report {
  id: string;
  title: string;
  period: string;
  summary: string;
  created_at: string;
  date?: string;
  type?: string;
  data?: Record<string, unknown>;
}

export interface ReportsResponse {
  reports: Report[];
}

// ===== Goals / Planning =====
export interface Goal {
  id: string;
  name: string;
  target_amount: number;
  current_amount: number;
  deadline: string;
  category: string;
  priority?: 'low' | 'medium' | 'high';
  description?: string;
}

export interface GoalsResponse {
  goals: Goal[];
}

export interface Forecast {
  forecast: Array<{
    month: string;
    income: number;
    expense: number;
    savings: number;
  }>;
  summary?: string;
  risk_score?: number;
  recommendations?: string[];
}

// ===== Analytics =====
export interface Analytics {
  expense_by_category?: Array<{ category: string; amount: number }>;
  expense_by_merchant?: Array<{ merchant: string; amount: number }>;
  monthly_trend?: Array<{ month: string; income: number; expense: number }>;
  income_vs_expense?: Array<{ month: string; income: number; expense: number }>;
  risk_score?: number;
  top_merchants?: Array<{ merchant: string; amount: number; count: number }>;
  spending_heatmap?: Array<{ day: string; hour: number; value: number }>;
  total_income?: number;
  total_expense?: number;
  total_savings?: number;
  savings_rate?: number;
}

// ===== Health =====
export interface ServiceHealth {
  name: string;
  status: 'healthy' | 'unhealthy' | 'degraded' | 'unknown';
  latency_ms?: number;
  message?: string;
}

export interface HealthResponse {
  status: 'healthy' | 'unhealthy' | 'degraded';
  services?: Record<string, ServiceHealth>;
  timestamp?: string;
  version?: string;
}

// ===== Dashboard aggregate =====
export interface DashboardStats {
  total_income: number;
  total_expense: number;
  total_savings: number;
  risk_score: number;
  savings_rate: number;
  transaction_count: number;
}
