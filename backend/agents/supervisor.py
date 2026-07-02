"""
Supervisor Agent

Routes the user question
to the appropriate agent.
"""

from models.state import GraphState

from agents.expense_agent import expense_node
from agents.insight_agent import insight_node
from agents.risk_agent import risk_node
from agents.planning_agent import planning_node

from core.logger import logger


class SupervisorAgent:

    """
    LangGraph Supervisor
    """

    # =====================================================
    # Decide Agent
    # =====================================================

    def route(
        self,
        question: str
    ) -> str:

        question = question.lower()

        # ---------------- Expense ----------------

        expense_keywords = [

            "expense",
            "spent",
            "shopping",
            "merchant",
            "food",
            "travel",
            "amazon",
            "flipkart",
            "swiggy",
            "payment"

        ]

        # ---------------- Insight ----------------

        insight_keywords = [

            "summary",
            "insight",
            "analysis",
            "report",
            "recommend",
            "trend"

        ]

        # ---------------- Risk ----------------

        risk_keywords = [

            "risk",
            "overspending",
            "overspend",
            "anomaly",
            "fraud",
            "large",
            "high spending"

        ]

        # ---------------- Planning ----------------

        planning_keywords = [

            "goal",
            "budget",
            "save",
            "saving",
            "plan",
            "planning",
            "laptop",
            "vacation",
            "car",
            "house",
            "emergency"

        ]

        if any(word in question for word in expense_keywords):

            return "ExpenseAgent"

        if any(word in question for word in insight_keywords):

            return "InsightAgent"

        if any(word in question for word in risk_keywords):

            return "RiskAgent"

        if any(word in question for word in planning_keywords):

            return "PlanningAgent"

        return "InsightAgent"

    # =====================================================
    # Execute
    # =====================================================

    def run(
        self,
        state: GraphState
    ) -> GraphState:

        logger.info("Supervisor Started...")

        agent = self.route(

            state["question"]

        )

        state["current_agent"] = "Supervisor"

        state["next_agent"] = agent

        logger.info(

            f"Routing to {agent}"

        )

        if agent == "ExpenseAgent":

            return expense_node(state)

        elif agent == "InsightAgent":

            return insight_node(state)

        elif agent == "RiskAgent":

            return risk_node(state)

        elif agent == "PlanningAgent":

            return planning_node(state)

        return insight_node(state)


supervisor = SupervisorAgent()


def supervisor_node(
    state: GraphState
):

    return supervisor.run(state)