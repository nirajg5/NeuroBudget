"""
Insight Agent

Generates financial insights, summaries,
spending trends, and recommendations.
"""

from models.state import GraphState

from rag.rag_pipeline import RAGPipeline

from core.logger import logger


class InsightAgent:

    """
    Financial Insight Agent
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

        logger.info("Insight Agent Started...")

        question = state["question"]

        result = self.rag.ask(question)

        state["retrieved_documents"] = result["sources"]

        state["answer"] = result["answer"]

        state["insights"] = {

            "summary": result["answer"],

            "documents_used": result["retrieved_documents"],

            "status": "completed"

        }

        state["current_agent"] = "InsightAgent"

        logger.success("Insight Agent Finished.")

        return state


# =====================================================
# LangGraph Node
# =====================================================

insight_agent = InsightAgent()


def insight_node(
    state: GraphState
):

    return insight_agent.run(state)