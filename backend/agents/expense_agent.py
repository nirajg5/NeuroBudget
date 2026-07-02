"""
Expense Agent

Handles all expense-related questions.
"""

from models.state import GraphState

from rag.rag_pipeline import RAGPipeline

from core.logger import logger


class ExpenseAgent:

    """
    Expense Analysis Agent
    """

    def __init__(self):

        self.rag = RAGPipeline()

    # =====================================================
    # Execute
    # =====================================================

    def run(
        self,
        state: GraphState
    ) -> GraphState:

        logger.info("Expense Agent Started...")

        question = state["question"]

        result = self.rag.ask(question)

        state["retrieved_documents"] = result["sources"]

        state["answer"] = result["answer"]

        state["expenses"] = {

            "documents": result["retrieved_documents"],

            "status": "completed"

        }

        state["current_agent"] = "ExpenseAgent"

        logger.success("Expense Agent Finished.")

        return state
    

expense_agent = ExpenseAgent()


def expense_node(
    state: GraphState
):

    return expense_agent.run(state)