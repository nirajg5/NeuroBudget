"""
app.py — NeuroBudget FastAPI application.
Main entry point. Defines all API endpoints.

Endpoints:
  POST /chat             — Conversational AI assistant
  POST /upload-csv       — CSV/PDF upload and parsing
  GET  /insights         — Financial analysis and charts
  POST /goal-plan        — Savings goal planning
  GET  /risk-analysis    — Risk detection and alerts
  GET  /health           — Health check
"""

import os
import shutil
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from openai import OpenAI

from config import get_settings
from database.db import init_db, get_db, TransactionModel
from database.chat_memory import save_message, get_history
from models.schemas import (
    ChatRequest, ChatResponse,
    UploadResponse, Transaction,
    InsightsResponse, SpendingAlert,
    GoalPlanRequest, GoalPlanResponse, MonthlySavingStep,
    RiskAnalysisResponse, RiskFactor,
)
from tools.file_parser import parse_csv, parse_pdf, dataframe_to_transactions
from tools.calculator import (
    total_spending, spending_by_category, top_category,
    daily_average_spending, estimate_savings,
    detect_spending_spikes, overspending_categories,
    monthly_savings_plan,
)
from tools.charts import (
    spending_pie_chart, spending_bar_chart,
    savings_goal_line_chart, spending_trend_chart,
)
from agents.workflow import run_workflow
from rag.vectorstore import add_transactions
from rag.retriever import build_rag_context

# ─── App Setup ────────────────────────────────────────────────────────────────

settings = get_settings()

app = FastAPI(
    title="NeuroBudget — AI Financial Copilot",
    description="An intelligent financial assistant powered by LangGraph multi-agent AI.",
    version="1.0.0",
)

# Allow all origins for development (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenRouter client
openrouter_client = OpenAI(
    base_url=settings.openrouter_base_url,
    api_key=settings.openrouter_api_key,
)


@app.on_event("startup")
def startup():
    """Initialize DB tables on app start."""
    init_db()
    print("✅ NeuroBudget API started. Database initialized.")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _get_all_transactions(db: Session) -> List[dict]:
    """Fetch all transactions from DB as list of dicts."""
    rows = db.query(TransactionModel).all()
    return [
        {
            "id": r.id,
            "date": r.date,
            "description": r.description,
            "amount": r.amount,
            "category": r.category,
            "source": r.source,
        }
        for r in rows
    ]


# ─── Health Check ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "model": settings.openrouter_model,
        "version": "1.0.0"
    }


# ─── Chat Endpoint ────────────────────────────────────────────────────────────

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Conversational AI endpoint.

    - Retrieves conversation history for context
    - Pulls relevant transactions via RAG
    - Calls OpenRouter LLM with full context
    - Saves conversation to memory
    """
    session_id = request.session_id
    user_message = request.message

    # Get past conversation history
    history = get_history(db, session_id, limit=8)

    # RAG: retrieve relevant financial context
    rag_context = build_rag_context(user_message, top_k=5)

    # Get summary stats for context
    transactions = _get_all_transactions(db)
    total = total_spending(transactions)
    by_cat = spending_by_category(transactions)

    system_prompt = f"""You are NeuroBudget, a friendly and knowledgeable AI financial copilot.

Current user financial snapshot:
- Total tracked spending: ₹{total:,.2f}
- Number of transactions: {len(transactions)}
- Spending by category: {by_cat}

Relevant transactions from their history:
{rag_context}

Instructions:
- Answer financial questions clearly and specifically
- Always reference the user's actual data when relevant
- Explain your reasoning (Explainable AI)
- Be encouraging but honest about financial risks
- Use ₹ for currency amounts
- Keep responses under 300 words unless a detailed plan is needed"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        response = openrouter_client.chat.completions.create(
            model=settings.openrouter_model,
            messages=messages,
            max_tokens=500,
            temperature=0.5,
        )
        ai_response = response.choices[0].message.content.strip()
        reasoning = (
            f"Response generated using {len(history)} past messages + RAG context "
            f"({len(transactions)} transactions indexed). Model: {settings.openrouter_model}."
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {str(e)}")

    # Persist conversation
    save_message(db, session_id, "user", user_message)
    save_message(db, session_id, "assistant", ai_response)

    return ChatResponse(
        response=ai_response,
        reasoning=reasoning,
        session_id=session_id,
    )


# ─── CSV/PDF Upload ───────────────────────────────────────────────────────────

@app.post("/upload-csv", response_model=UploadResponse, tags=["Upload"])
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a bank statement CSV or PDF.

    - Saves file to uploads/ directory
    - Parses and normalizes transactions
    - Categorizes each transaction
    - Stores in SQLite database
    - Indexes in FAISS vector store for RAG
    """
    allowed_types = ["text/csv", "application/pdf", "application/octet-stream"]
    filename = file.filename or "upload"
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext not in ["csv", "pdf"]:
        raise HTTPException(status_code=400, detail="Only CSV and PDF files are supported.")

    # Save uploaded file
    save_path = os.path.join(settings.upload_dir, filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Parse file
    if ext == "csv":
        df, error = parse_csv(save_path, filename)
    else:
        df, error = parse_pdf(save_path, filename)

    if error:
        raise HTTPException(status_code=422, detail=f"Parsing error: {error}")

    if df.empty:
        raise HTTPException(status_code=422, detail="No valid transactions found in file.")

    # Save to database
    transactions_data = dataframe_to_transactions(df)
    for t in transactions_data:
        row = TransactionModel(
            date=t["date"],
            description=t["description"],
            amount=t["amount"],
            category=t["category"],
            source=t["source"],
        )
        db.add(row)
    db.commit()

    # Index in FAISS for RAG
    add_transactions(transactions_data)

    # Build response
    categories_found = list(set(t["category"] for t in transactions_data))
    total_amt = total_spending(transactions_data)
    preview = [Transaction(**t) for t in transactions_data[:5]]

    return UploadResponse(
        message=f"Successfully processed {len(transactions_data)} transactions.",
        filename=filename,
        rows_processed=len(transactions_data),
        categories_found=categories_found,
        total_amount=total_amt,
        preview=preview,
    )


# ─── Insights ─────────────────────────────────────────────────────────────────

@app.get("/insights", response_model=InsightsResponse, tags=["Analysis"])
def get_insights(
    session_id: str = Query(default="default"),
    db: Session = Depends(get_db)
):
    """
    Return comprehensive financial insights.

    Uses the full LangGraph multi-agent workflow to analyze all transactions.
    """
    transactions = _get_all_transactions(db)

    if not transactions:
        raise HTTPException(
            status_code=404,
            detail="No transactions found. Please upload a CSV or PDF first."
        )

    # Run multi-agent workflow
    result = run_workflow(
        user_message="Give me a full financial analysis with insights",
        transactions=transactions,
        session_id=session_id,
    )

    expense = result.get("expense_analysis", {})
    insights = result.get("insights", {})
    risk = result.get("risk_flags", {})

    # Build spending alerts from risk data
    alerts = []
    for anomaly in risk.get("anomalies", [])[:3]:
        alerts.append(SpendingAlert(
            type="abnormal_transaction",
            message=f"Unusual transaction: {anomaly.get('description')} — ₹{anomaly.get('amount', 0):,.2f}",
            severity="medium",
            amount=anomaly.get("amount"),
        ))
    for overspend in risk.get("overspending", [])[:3]:
        alerts.append(SpendingAlert(
            type="overspending",
            message=overspend.get("message", f"Overspending in {overspend.get('category')}"),
            severity="high" if risk.get("risk_score", 0) > 60 else "medium",
            amount=overspend.get("amount"),
        ))

    top_cat_name, top_cat_amount = expense.get("top_category", ("Other", 0))
    total = expense.get("total", 0)
    savings = estimate_savings(total)
    trend_data = spending_trend_chart(transactions)

    reasoning = " → ".join(result.get("reasoning_chain", []))

    return InsightsResponse(
        total_spending=total,
        top_category=top_cat_name,
        top_category_amount=top_cat_amount,
        savings_estimate=savings,
        average_daily_spend=expense.get("daily_average", 0),
        spending_by_category=expense.get("by_category", {}),
        spending_trend=trend_data,
        alerts=alerts,
        ai_summary=insights.get("ai_summary", ""),
        reasoning=reasoning,
    )


# ─── Goal Planning ────────────────────────────────────────────────────────────

@app.post("/goal-plan", response_model=GoalPlanResponse, tags=["Planning"])
def create_goal_plan(
    request: GoalPlanRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a personalized savings plan to reach a financial goal.

    Takes target amount, timeline, and optional income.
    Returns month-by-month savings steps with Plotly chart data.
    """
    transactions = _get_all_transactions(db)
    total_spent = total_spending(transactions)
    by_cat = spending_by_category(transactions)

    # Calculate how much to save per month
    plan = monthly_savings_plan(
        target_amount=request.target_amount,
        timeline_months=request.timeline_months,
        current_spending=total_spent,
        monthly_income=request.monthly_income,
    )

    monthly_required = plan["monthly_required"]
    is_achievable = plan["is_achievable"]

    # Build month-by-month steps
    steps = []
    # Identify top 3 discretionary categories for cut suggestions
    discretionary = ["Entertainment", "Shopping", "Food", "Travel", "Groceries"]
    cut_suggestions = []
    for cat in discretionary:
        if cat in by_cat:
            suggested_cut = round(by_cat[cat] * 0.15, 2)
            cut_suggestions.append(f"Reduce {cat} by 15% — save ₹{suggested_cut:,.2f}/month")

    for month in range(1, request.timeline_months + 1):
        steps.append(MonthlySavingStep(
            month=month,
            target_savings=monthly_required,
            cumulative_savings=round(monthly_required * month, 2),
            suggested_cuts=cut_suggestions[:2],  # Top 2 suggestions each month
        ))

    # Generate LLM recommendations
    plan_context = f"""
Goal: {request.goal_name} — ₹{request.target_amount:,.2f} in {request.timeline_months} months
Monthly savings needed: ₹{monthly_required:,.2f}
Current monthly spending: ₹{total_spent:,.2f}
Monthly income: {f'₹{request.monthly_income:,.2f}' if request.monthly_income else 'Not provided'}
Top spending categories: {dict(list(by_cat.items())[:5])}
Goal achievable: {is_achievable}
"""

    try:
        llm_resp = openrouter_client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {"role": "system", "content": "You are a financial planning expert."},
                {"role": "user", "content": f"""Create 4 specific, practical recommendations to help achieve this savings goal.
                
{plan_context}

Each recommendation should be actionable and include a specific ₹ amount or % to cut.
Format as a numbered list. Be encouraging."""}
            ],
            max_tokens=350,
            temperature=0.4,
        )
        recommendations_text = llm_resp.choices[0].message.content.strip()
        recommendations = [
            line.strip().lstrip("1234567890.)- ").strip()
            for line in recommendations_text.split("\n")
            if line.strip() and any(c.isalpha() for c in line)
        ][:5]
    except Exception:
        recommendations = cut_suggestions[:4]

    chart_data = savings_goal_line_chart(monthly_required, request.timeline_months, request.target_amount)

    reasoning = (
        f"Goal of ₹{request.target_amount:,.2f} requires saving ₹{monthly_required:,.2f}/month over "
        f"{request.timeline_months} months. Current spending is ₹{total_spent:,.2f}/month. "
        f"{'This is achievable.' if is_achievable else 'This requires significant spending cuts.'}"
    )

    return GoalPlanResponse(
        goal_name=request.goal_name or "Savings Goal",
        target_amount=request.target_amount,
        timeline_months=request.timeline_months,
        monthly_savings_required=monthly_required,
        is_achievable=is_achievable,
        steps=steps,
        recommendations=recommendations,
        chart_data=chart_data,
        reasoning=reasoning,
    )


# ─── Risk Analysis ────────────────────────────────────────────────────────────

@app.get("/risk-analysis", response_model=RiskAnalysisResponse, tags=["Risk"])
def risk_analysis(db: Session = Depends(get_db)):
    """
    Detect financial risks in the user's transaction history.

    Identifies:
    - Overspending in categories
    - Abnormal/spike transactions
    - Budget risk score
    """
    transactions = _get_all_transactions(db)

    if not transactions:
        raise HTTPException(
            status_code=404,
            detail="No transactions found. Please upload data first."
        )

    total = total_spending(transactions)
    by_cat = spending_by_category(transactions)

    # Detect anomalies and overspending
    anomalies = detect_spending_spikes(transactions, threshold_multiplier=2.0)
    overspending = overspending_categories(by_cat)

    # Compute risk score
    score = min(len(anomalies) * 10 + len(overspending) * 15, 100)
    risk_level = "high" if score >= 60 else "medium" if score >= 30 else "low"

    # Build RiskFactor list
    risk_factors = []
    for item in overspending[:5]:
        risk_factors.append(RiskFactor(
            risk_type="overspending",
            description=item.get("message", f"High spending in {item.get('category')}"),
            affected_category=item.get("category"),
            amount=item.get("amount"),
            severity="high" if score >= 60 else "medium",
            suggestion=f"Try reducing {item.get('category')} spending by 20% next month.",
        ))
    for anomaly in anomalies[:5]:
        risk_factors.append(RiskFactor(
            risk_type="abnormal_transaction",
            description=f"Unusually large transaction: {anomaly.get('description')}",
            affected_category=anomaly.get("category"),
            amount=anomaly.get("amount"),
            severity="medium",
            suggestion="Review this transaction to ensure it was intentional.",
        ))

    # LLM reasoning
    try:
        risk_prompt = f"""Briefly explain (2-3 sentences) what these financial risks mean for the user and what they should prioritize:
Risk Score: {score}/100 ({risk_level.upper()} risk)
Anomalous transactions: {len(anomalies)}
Overspending categories: {[o.get('category') for o in overspending]}
Total spending: ₹{total:,.2f}"""

        llm_resp = openrouter_client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {"role": "system", "content": "You are a concise financial risk analyst."},
                {"role": "user", "content": risk_prompt}
            ],
            max_tokens=200,
            temperature=0.3,
        )
        reasoning = llm_resp.choices[0].message.content.strip()
    except Exception as e:
        reasoning = f"Risk score: {score}/100. {len(anomalies)} anomalies detected. {len(overspending)} categories over target."

    return RiskAnalysisResponse(
        overall_risk_level=risk_level,
        risk_score=score,
        risk_factors=risk_factors,
        anomalies=[Transaction(**a) for a in anomalies[:10]],
        safe_to_spend=round(total * 0.20, 2),
        reasoning=reasoning,
    )


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=settings.app_host, port=settings.app_port, reload=settings.debug)
