"""
Risk Agent

Detects overspending, unusual transactions,
and financial risks.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from database.db import SessionLocal
from database.models import Transaction

from models.state import GraphState

from rag.rag_pipeline import RAGPipeline

from core.logger import logger


class RiskAgent:

    """
    Financial Risk Analysis Agent
    """

    def __init__(self):

        self.db: Session = SessionLocal()

        self.rag = RAGPipeline()

    # =====================================================
    # Calculate Average Expense
    # =====================================================

    def average_expense(self):

        avg = (

            self.db.query(

                func.avg(Transaction.amount)

            )

            .filter(

                Transaction.flow == "Expense"

            )

            .scalar()

        )

        return float(avg or 0)

    # =====================================================
    # Large Transactions
    # =====================================================

    def large_transactions(self):

        average = self.average_expense()

        threshold = average * 2

        transactions = (

            self.db.query(Transaction)

            .filter(

                Transaction.amount >= threshold

            )

            .all()

        )

        return transactions

    # =====================================================
    # Risk Score
    # =====================================================

    def calculate_risk_score(self):

        average = self.average_expense()

        risky = len(self.large_transactions())

        score = min(

            100,

            int((risky * 10) + (average / 1000))

        )

        return score

    # =====================================================
    # Recommendations
    # =====================================================

    def recommendations(
        self,
        score
    ):

        recommendations = []

        if score >= 80:

            recommendations.append(

                "Your spending risk is extremely high."

            )

            recommendations.append(

                "Reduce discretionary spending immediately."

            )

        elif score >= 60:

            recommendations.append(

                "Monitor shopping and travel expenses."

            )

        elif score >= 40:

            recommendations.append(

                "Your spending is moderately healthy."

            )

        else:

            recommendations.append(

                "Your financial risk is low."

            )

        return recommendations

    # =====================================================
    # Execute
    # =====================================================

    def run(
        self,
        state: GraphState
    ) -> GraphState:

        logger.info("Risk Agent Started...")

        score = self.calculate_risk_score()

        large_txns = self.large_transactions()

        advice = self.recommendations(score)

        rag_result = self.rag.ask(

            state["question"]

        )

        state["retrieved_documents"] = rag_result["sources"]

        state["answer"] = rag_result["answer"]

        state["risks"] = {

            "risk_score": score,

            "large_transactions": len(large_txns),

            "recommendations": advice,

            "status": "completed"

        }

        state["current_agent"] = "RiskAgent"

        logger.success("Risk Agent Finished.")

        return state


risk_agent = RiskAgent()


def risk_node(
    state: GraphState
):

    return risk_agent.run(state)