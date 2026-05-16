"""
schemas.py — Pydantic models for request/response validation.
All API inputs and outputs are typed and documented here.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class ExpenseCategory(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    SHOPPING = "Shopping"
    ENTERTAINMENT = "Entertainment"
    UTILITIES = "Utilities"
    HEALTH = "Health"
    EDUCATION = "Education"
    TRAVEL = "Travel"
    GROCERIES = "Groceries"
    FINANCE = "Finance"
    OTHER = "Other"


# ─── Chat ─────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    session_id: str = Field(default="default", description="Session ID for conversation memory")

class ChatResponse(BaseModel):
    response: str
    reasoning: str  # Explainable AI — why the AI said what it said
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ─── Transactions ──────────────────────────────────────────────────────────────

class Transaction(BaseModel):
    id: Optional[int] = None
    date: str
    description: str
    amount: float
    category: Optional[str] = None
    source: Optional[str] = None  # Which file it came from

class TransactionList(BaseModel):
    transactions: List[Transaction]
    total_count: int
    total_amount: float


# ─── CSV Upload ────────────────────────────────────────────────────────────────

class UploadResponse(BaseModel):
    message: str
    filename: str
    rows_processed: int
    categories_found: List[str]
    total_amount: float
    preview: List[Transaction]  # First 5 transactions


# ─── Insights ─────────────────────────────────────────────────────────────────

class SpendingAlert(BaseModel):
    type: str           # "overspending", "spike", "unusual"
    message: str
    severity: str       # "low", "medium", "high"
    amount: Optional[float] = None

class InsightsResponse(BaseModel):
    total_spending: float
    top_category: str
    top_category_amount: float
    savings_estimate: float
    average_daily_spend: float
    spending_by_category: Dict[str, float]   # {category: amount}
    spending_trend: List[Dict[str, Any]]     # Plotly-compatible time series
    alerts: List[SpendingAlert]
    ai_summary: str                          # LLM-generated summary
    reasoning: str                           # Explainable AI


# ─── Goal Planning ────────────────────────────────────────────────────────────

class GoalPlanRequest(BaseModel):
    target_amount: float = Field(..., gt=0, description="Savings goal in INR/USD")
    timeline_months: int = Field(..., gt=0, le=120, description="Timeline to reach goal")
    monthly_income: Optional[float] = Field(None, description="Optional: monthly income")
    goal_name: Optional[str] = Field(default="Savings Goal", description="Name of the goal")

class MonthlySavingStep(BaseModel):
    month: int
    target_savings: float
    cumulative_savings: float
    suggested_cuts: List[str]

class GoalPlanResponse(BaseModel):
    goal_name: str
    target_amount: float
    timeline_months: int
    monthly_savings_required: float
    is_achievable: bool
    steps: List[MonthlySavingStep]
    recommendations: List[str]
    chart_data: Dict[str, Any]   # Plotly-compatible line chart
    reasoning: str


# ─── Risk Analysis ────────────────────────────────────────────────────────────

class RiskFactor(BaseModel):
    risk_type: str      # "overspending", "abnormal_transaction", "budget_spike"
    description: str
    affected_category: Optional[str] = None
    amount: Optional[float] = None
    severity: str       # "low", "medium", "high"
    suggestion: str

class RiskAnalysisResponse(BaseModel):
    overall_risk_level: str   # "low", "medium", "high"
    risk_score: float         # 0-100
    risk_factors: List[RiskFactor]
    anomalies: List[Transaction]
    safe_to_spend: float      # Amount considered safe to spend
    reasoning: str
