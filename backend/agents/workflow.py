"""
LangGraph Workflow

Creates the multi-agent workflow.
"""

from langgraph.graph import StateGraph
from langgraph.graph import END

from models.state import GraphState

from agents.supervisor import supervisor_node
from agents.expense_agent import expense_node
from agents.insight_agent import insight_node
from agents.risk_agent import risk_node
from agents.planning_agent import planning_node

from core.logger import logger

class NeuroBudgetWorkflow:

    """
    LangGraph Workflow
    """

    def __init__(self):

        self.graph = self.build_graph()

    def build_graph(self):

        workflow = StateGraph(GraphState)

        # ============================
        # Nodes
        # ============================

        workflow.add_node(

            "Supervisor",

            supervisor_node

        )

        workflow.add_node(

            "ExpenseAgent",

            expense_node

        )

        workflow.add_node(

            "InsightAgent",

            insight_node

        )

        workflow.add_node(

            "RiskAgent",

            risk_node

        )

        workflow.add_node(

            "PlanningAgent",

            planning_node
        )

        workflow.set_entry_point(

            "Supervisor"

        )

        workflow.add_conditional_edges(

            "Supervisor",

            lambda state: state["next_agent"],

            {

                "ExpenseAgent": "ExpenseAgent",

                "InsightAgent": "InsightAgent",

                "RiskAgent": "RiskAgent",

                "PlanningAgent": "PlanningAgent"

            }

        )

        workflow.add_edge(

            "ExpenseAgent",

            END

        )

        workflow.add_edge(

            "InsightAgent",

            END

        )

        workflow.add_edge(

            "RiskAgent",

            END

        )

        workflow.add_edge(

            "PlanningAgent",

            END

        )

        logger.success(

            "LangGraph Workflow Created."

        )

        return workflow.compile()
    

    def run(

        self,

        state: GraphState

    ):

        logger.info(

            "Running LangGraph Workflow..."

        )

        return self.graph.invoke(state)
    
workflow = NeuroBudgetWorkflow()