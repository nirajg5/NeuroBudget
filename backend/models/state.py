"""
state.py — LangGraph shared state definition.
This TypedDict flows through all agents in the workflow graph.
"""

from typing import TypedDict, List, Dict, Any, Optional
import pandas as pd


class AgentState(TypedDict):
    """
    Shared state passed between LangGraph agents.
    Each agent reads from and writes to this state.
    """

    # Input
    user_message: str                   # Original user query
    session_id: str                     # Conversation session

    # Transaction data (loaded from DB or CSV)
    transactions_df: Optional[Any]      # pandas DataFrame (Any to avoid serialization issues)
    raw_transactions: List[Dict]        # List of transaction dicts

    # Agent outputs — each agent populates its section
    expense_analysis: Dict[str, Any]    # From ExpenseAgent
    insights: Dict[str, Any]           # From InsightAgent
    risk_flags: Dict[str, Any]         # From RiskAgent
    savings_plan: Dict[str, Any]       # From PlanningAgent

    # Final assembled response
    final_response: str
    reasoning_chain: List[str]         # Explainable AI: step-by-step reasoning log

    # Errors (if any agent fails gracefully)
    errors: List[str]
