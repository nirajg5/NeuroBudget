"""
Planning Agent

Creates savings plans, budget plans,
and financial goal recommendations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from database.db import SessionLocal
from database.models import Transaction, Goal
from models.state import create_state

from models.state import GraphState

from rag.rag_pipeline import RAGPipeline

from core.logger import logger


class PlanningAgent:
    """
    Planning Agent
    """

    def __init__(self):

        self.db: Session = SessionLocal()

        self.rag = RAGPipeline()

    # =====================================================
    # Total Income
    # =====================================================

    def total_income(self):

        income = (

            self.db.query(

                func.sum(Transaction.amount)

            )

            .filter(

                Transaction.flow == "Income"

            )

            .scalar()

        )

        return float(income or 0)

    # =====================================================
    # Total Expense
    # =====================================================

    def total_expense(self):

        expense = (

            self.db.query(

                func.sum(Transaction.amount)

            )

            .filter(

                Transaction.flow == "Expense"

            )

            .scalar()

        )

        return float(expense or 0)
    
    # =====================================================
    # Disposable Income
    # =====================================================

    def disposable_income(self):

        return (

            self.total_income()

            -

            self.total_expense()

        )
    
    # =====================================================
    # Load Goals
    # =====================================================

    def load_goals(self):

        goals = (

            self.db.query(Goal)

            .all()

        )

        return goals
    # =====================================================
    # Active Goals
    # =====================================================

    def active_goals(self):

        goals = (

            self.db.query(Goal)

            .filter(

                Goal.status == "Active"

            )

            .all()

        )

        return goals
    
    # =====================================================
    # Completed Goals
    # =====================================================

    def completed_goals(self):

        goals = (

            self.db.query(Goal)

            .filter(

                Goal.status == "Completed"

            )

            .all()

        )

        return goals
    # =====================================================
    # Goal Count
    # =====================================================

    def goal_count(self):

        return (

            self.db.query(Goal)

            .count()

        )
    # =====================================================
    # Planning Summary
    # =====================================================

    def planning_summary(self):

        summary = {

            "total_income": self.total_income(),

            "total_expense": self.total_expense(),

            "disposable_income": self.disposable_income(),

            "total_goals": self.goal_count(),

            "active_goals": len(self.active_goals()),

            "completed_goals": len(self.completed_goals())

        }

        return summary
    

    # =====================================================
    # Monthly Savings Required
    # =====================================================

    def monthly_savings_required(
        self,
        target_amount: float,
        current_amount: float,
        deadline_months: int
    ):

        remaining = max(
            target_amount - current_amount,
            0
        )

        if deadline_months <= 0:
            return remaining

        return round(
            remaining / deadline_months,
            2
        )

    # =====================================================
    # Goal Feasibility
    # =====================================================

    def goal_feasible(
        self,
        target_amount: float,
        current_amount: float,
        deadline_months: int
    ):

        monthly_required = self.monthly_savings_required(
            target_amount,
            current_amount,
            deadline_months
        )

        disposable = self.disposable_income()

        return disposable >= monthly_required

    # =====================================================
    # Estimated Completion Time
    # =====================================================

    def estimated_completion_months(
        self,
        target_amount: float,
        current_amount: float
    ):

        disposable = self.disposable_income()

        if disposable <= 0:
            return None

        remaining = max(
            target_amount - current_amount,
            0
        )

        months = remaining / disposable

        return round(months, 1)

    # =====================================================
    # Savings Recommendation
    # =====================================================

    def savings_recommendation(
        self,
        target_amount: float,
        current_amount: float,
        deadline_months: int
    ):

        monthly_required = self.monthly_savings_required(
            target_amount,
            current_amount,
            deadline_months
        )

        disposable = self.disposable_income()

        feasible = disposable >= monthly_required

        if feasible:

            message = (
                f"You should save ₹{monthly_required:.2f} "
                f"per month to reach your goal."
            )

        else:

            shortage = monthly_required - disposable

            message = (
                f"Your goal is difficult with your current finances. "
                f"You need an additional ₹{shortage:.2f} per month."
            )

        return {
            "monthly_required": monthly_required,
            "disposable_income": disposable,
            "feasible": feasible,
            "recommendation": message
        }

    # =====================================================
    # Analyze Goal
    # =====================================================

    def analyze_goal(self, goal):

        recommendation = self.savings_recommendation(
            target_amount=goal.target_amount,
            current_amount=goal.current_amount,
            deadline_months=goal.deadline_months
        )

        completion = self.estimated_completion_months(
            target_amount=goal.target_amount,
            current_amount=goal.current_amount
        )

        return {
            "goal_name": goal.goal_name,
            "target_amount": goal.target_amount,
            "current_amount": goal.current_amount,
            "deadline_months": goal.deadline_months,
            "estimated_completion": completion,
            **recommendation
        }

    # =====================================================
    # Analyze Active Goals
    # =====================================================

    def analyze_active_goals(self):

        goals = self.active_goals()

        reports = []

        for goal in goals:
            reports.append(
                self.analyze_goal(goal)
            )

        return reports
    
    # =====================================================
# Monthly Budget Allocation (50/30/20 Rule)
# =====================================================

 # =====================================================
# Monthly Budget Allocation (50/30/20 Rule)
# =====================================================

    def budget_plan(self):

       income = self.total_income()

       return {

        "monthly_income": round(income, 2),

        "needs_budget": round(income * 0.50, 2),

        "wants_budget": round(income * 0.30, 2),

        "savings_budget": round(income * 0.20, 2)

    }
    
# =====================================================
# Emergency Fund
# =====================================================

    def emergency_fund(self):

      expense = self.total_expense()

      monthly_expense = expense / 12 if expense > 0 else 0

      return {

        "recommended_fund": round(monthly_expense * 6, 2),

        "monthly_expense": round(monthly_expense, 2)

    }

# =====================================================
# Savings Capacity
# =====================================================

    def savings_capacity(self):

      disposable = self.disposable_income()

      if disposable <= 0:

        return {

            "status": "Low",

            "monthly_savings": 0

        }

      elif disposable < 5000:

        return {

            "status": "Moderate",

            "monthly_savings": disposable

        }

      else:

        return {

            "status": "Excellent",

            "monthly_savings": disposable

        }
      

# =====================================================
# Financial Planning Report
# =====================================================

    def financial_plan(self):

     return {

        "summary": self.planning_summary(),

        "budget": self.budget_plan(),

        "emergency_fund": self.emergency_fund(),

        "savings_capacity": self.savings_capacity(),

        "goal_analysis": self.analyze_active_goals()

     }
    

    def planning_prompt(
      self,
      question: str,
      report: dict
    ):

      return f"""
      You are an AI Financial Planning Assistant.

      User Question:
      {question}

      Financial Report:
      {report}

      Instructions:

      1. Explain whether the financial goal is achievable.
      2. Mention disposable income.
      3. Mention monthly savings required.
      4. Mention emergency fund recommendation.
      5. Give practical financial advice.
      6. Answer using the provided report only.
     """
    

# =====================================================
# Execute Planning Agent
# =====================================================

    def run(
      self,
      state: GraphState
    ) -> GraphState:

     logger.info("Planning Agent Started...")

    # ---------------------------------------
    # Financial Report
    # ---------------------------------------

     report = self.financial_plan()

    # ---------------------------------------
    # Retrieve Financial Context
    # ---------------------------------------

     rag_result = self.rag.ask(

        state["question"]

     )

    # ---------------------------------------
    # Build Planning Prompt
    # ---------------------------------------

     prompt = self.planning_prompt(

        state["question"],

        report

    )

    # ---------------------------------------
    # Ask LLM
    # ---------------------------------------

     explanation = self.rag.generate_answer(

        prompt

    )

    # ---------------------------------------
    # Update Graph State
    # ---------------------------------------

     state["retrieved_documents"] = rag_result["sources"]

     state["prompt"] = prompt

     state["answer"] = explanation

     state["planning"] = report
 
     state["goals"] = report["goal_analysis"]

     state["current_agent"] = "PlanningAgent"
 
     logger.success("Planning Agent Finished.")

     return state
    

planning_agent = PlanningAgent()


def planning_node(
       state: GraphState
    ):

    return planning_agent.run(state)