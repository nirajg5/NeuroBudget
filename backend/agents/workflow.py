"""
workflow.py — LangGraph StateGraph definition.
Orchestrates the 4-agent pipeline: Expense → Insight → Risk → Planning.

Graph flow:
    START
      ↓
  expense_agent
      ↓
  insight_agent
      ↓
  risk_agent
      ↓
  planning_agent
      ↓
    END
"""

from langgraph.graph import StateGraph, END
from models.state import AgentState
from agents.expense_agent import expense_agent
from agents.insight_agent import insight_agent
from agents.risk_agent import risk_agent
from agents.planning_agent import planning_agent


def build_workflow() -> StateGraph:
    """
    Build and compile the LangGraph workflow.
    Returns a compiled graph ready to invoke.
    """

    # Create graph with our shared state type
    graph = StateGraph(AgentState)

    # Register all agent nodes
    graph.add_node("expense_agent", expense_agent)
    graph.add_node("insight_agent", insight_agent)
    graph.add_node("risk_agent", risk_agent)
    graph.add_node("planning_agent", planning_agent)

    # Linear flow: each agent feeds into the next
    graph.set_entry_point("expense_agent")
    graph.add_edge("expense_agent", "insight_agent")
    graph.add_edge("insight_agent", "risk_agent")
    graph.add_edge("risk_agent", "planning_agent")
    graph.add_edge("planning_agent", END)

    return graph.compile()


def run_workflow(
    user_message: str,
    transactions: list,
    session_id: str = "default"
) -> AgentState:
    """
    Run the full multi-agent workflow.

    Args:
        user_message: The user's query
        transactions: List of transaction dicts from DB
        session_id: Conversation session ID

    Returns:
        Final AgentState with all agent outputs populated
    """
    app = build_workflow()

    initial_state: AgentState = {
        "user_message": user_message,
        "session_id": session_id,
        "transactions_df": None,
        "raw_transactions": transactions,
        "expense_analysis": {},
        "insights": {},
        "risk_flags": {},
        "savings_plan": {},
        "final_response": "",
        "reasoning_chain": [],
        "errors": [],
    }

    result = app.invoke(initial_state)
    return result
