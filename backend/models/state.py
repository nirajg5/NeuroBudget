"""
Graph State

Shared state used by the LangGraph workflow.
"""

from typing import TypedDict, List, Dict, Any, Optional
from pprint import pprint


class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # =====================================================
    # User Request
    # =====================================================

    question: str
    session_id: str

    # =====================================================
    # Routing
    # =====================================================

    current_agent: str
    next_agent: Optional[str]

    # =====================================================
    # Retrieval
    # =====================================================

    retrieved_documents: List[Dict[str, Any]]

    # =====================================================
    # Prompt
    # =====================================================

    prompt: str

    # =====================================================
    # Final Response
    # =====================================================

    answer: str

    # =====================================================
    # Agent Outputs
    # =====================================================

    expenses: Dict[str, Any]

    insights: Dict[str, Any]

    risks: Dict[str, Any]

    goals: Dict[str, Any]

    planning: Dict[str, Any]

    # =====================================================
    # Workflow
    # =====================================================

    execution_time: float

    workflow_status: str

    # =====================================================
    # Metadata
    # =====================================================

    metadata: Dict[str, Any]

    # =====================================================
    # Error
    # =====================================================

    error: Optional[str]


# ==========================================================
# Create Initial State
# ==========================================================

def create_state(
    question: str,
    session_id: str = "default"
) -> GraphState:

    return {

        "question": question,

        "session_id": session_id,

        "current_agent": "",

        "next_agent": None,

        "retrieved_documents": [],

        "prompt": "",

        "answer": "",

        "expenses": {},

        "insights": {},

        "risks": {},

        "goals": {},

        "planning": {},

        "execution_time": 0.0,

        "workflow_status": "initialized",

        "metadata": {},

        "error": None

    }


# ==========================================================
# Update State
# ==========================================================

def update_state(
    state: GraphState,
    **kwargs
) -> GraphState:

    state.update(kwargs)

    return state


# ==========================================================
# Reset State
# ==========================================================

def reset_state(
    state: GraphState
) -> GraphState:

    state["retrieved_documents"] = []

    state["prompt"] = ""

    state["answer"] = ""

    state["expenses"] = {}

    state["insights"] = {}

    state["risks"] = {}

    state["goals"] = {}

    state["planning"] = {}

    state["execution_time"] = 0.0

    state["workflow_status"] = "initialized"

    state["metadata"] = {}

    state["error"] = None

    state["current_agent"] = ""

    state["next_agent"] = None

    return state


# ==========================================================
# Add Retrieved Documents
# ==========================================================

def add_documents(
    state: GraphState,
    documents: List[Dict[str, Any]]
) -> GraphState:

    state["retrieved_documents"] = documents

    return state


# ==========================================================
# Store Prompt
# ==========================================================

def set_prompt(
    state: GraphState,
    prompt: str
) -> GraphState:

    state["prompt"] = prompt

    return state


# ==========================================================
# Store Final Answer
# ==========================================================

def set_answer(
    state: GraphState,
    answer: str
) -> GraphState:

    state["answer"] = answer

    return state


# ==========================================================
# Store Planning
# ==========================================================

def set_planning(
    state: GraphState,
    planning: Dict[str, Any]
) -> GraphState:

    state["planning"] = planning

    return state


# ==========================================================
# Store Goals
# ==========================================================

def set_goals(
    state: GraphState,
    goals: Dict[str, Any]
) -> GraphState:

    state["goals"] = goals

    return state


# ==========================================================
# Store Insights
# ==========================================================

def set_insights(
    state: GraphState,
    insights: Dict[str, Any]
) -> GraphState:

    state["insights"] = insights

    return state


# ==========================================================
# Store Risks
# ==========================================================

def set_risks(
    state: GraphState,
    risks: Dict[str, Any]
) -> GraphState:

    state["risks"] = risks

    return state


# ==========================================================
# Store Expenses
# ==========================================================

def set_expenses(
    state: GraphState,
    expenses: Dict[str, Any]
) -> GraphState:

    state["expenses"] = expenses

    return state


# ==========================================================
# Set Current Agent
# ==========================================================

def set_current_agent(
    state: GraphState,
    agent: str
) -> GraphState:

    state["current_agent"] = agent

    return state


# ==========================================================
# Set Next Agent
# ==========================================================

def set_next_agent(
    state: GraphState,
    agent: Optional[str]
) -> GraphState:

    state["next_agent"] = agent

    return state


# ==========================================================
# Store Error
# ==========================================================

def set_error(
    state: GraphState,
    error: str
) -> GraphState:

    state["error"] = error

    return state


# ==========================================================
# Pretty Print
# ==========================================================

def print_state(
    state: GraphState
):

    print()

    print("=" * 80)

    print("GRAPH STATE")

    print("=" * 80)

    pprint(state)

    print()