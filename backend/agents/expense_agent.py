"""
expense_agent.py — First agent in the LangGraph workflow.
Analyzes transaction data: totals, category breakdown, spending patterns.
"""

from typing import Dict, Any
from models.state import AgentState
from tools.calculator import (
    total_spending,
    spending_by_category,
    top_category,
    daily_average_spending,
)
from tools.charts import spending_pie_chart, spending_bar_chart


def expense_agent(state: AgentState) -> AgentState:
    """
    Expense Agent — analyzes raw transactions and computes spending stats.

    Reads:
        state["raw_transactions"]

    Writes:
        state["expense_analysis"]
        state["reasoning_chain"] (appends)
    """
    reasoning = state.get("reasoning_chain", [])
    errors = state.get("errors", [])

    try:
        transactions = state.get("raw_transactions", [])

        if not transactions:
            state["expense_analysis"] = {
                "total": 0,
                "by_category": {},
                "top_category": ("Other", 0),
                "daily_average": 0,
                "charts": {},
                "transaction_count": 0,
            }
            reasoning.append("ExpenseAgent: No transactions found — returning empty analysis.")
            state["reasoning_chain"] = reasoning
            return state

        # Core calculations
        total = total_spending(transactions)
        by_cat = spending_by_category(transactions)
        top_cat = top_category(transactions)
        daily_avg = daily_average_spending(transactions)

        # Chart data
        pie = spending_pie_chart(by_cat)
        bar = spending_bar_chart(by_cat)

        state["expense_analysis"] = {
            "total": total,
            "by_category": by_cat,
            "top_category": top_cat,
            "daily_average": daily_avg,
            "transaction_count": len(transactions),
            "charts": {
                "pie": pie,
                "bar": bar,
            },
        }

        reasoning.append(
            f"ExpenseAgent: Analyzed {len(transactions)} transactions. "
            f"Total spend: ₹{total:,.2f}. "
            f"Top category: {top_cat[0]} (₹{top_cat[1]:,.2f}). "
            f"Daily average: ₹{daily_avg:,.2f}."
        )

    except Exception as e:
        errors.append(f"ExpenseAgent error: {str(e)}")
        state["expense_analysis"] = {}
        reasoning.append(f"ExpenseAgent: Failed with error — {str(e)}")

    state["reasoning_chain"] = reasoning
    state["errors"] = errors
    return state
