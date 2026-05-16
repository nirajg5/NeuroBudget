"""
insight_agent.py — Second agent in the LangGraph workflow.
Uses the LLM (via OpenRouter) to generate human-readable financial insights
grounded in the expense analysis data and relevant RAG context.
"""

from openai import OpenAI
from config import get_settings
from models.state import AgentState
from rag.retriever import build_rag_context

settings = get_settings()

# OpenRouter client — drop-in replacement for OpenAI SDK
client = OpenAI(
    base_url=settings.openrouter_base_url,
    api_key=settings.openrouter_api_key,
)


def insight_agent(state: AgentState) -> AgentState:
    """
    Insight Agent — calls the LLM to summarize financial patterns in plain English.

    Reads:
        state["expense_analysis"]
        state["user_message"]

    Writes:
        state["insights"]
        state["reasoning_chain"] (appends)
    """
    reasoning = state.get("reasoning_chain", [])
    errors = state.get("errors", [])

    try:
        analysis = state.get("expense_analysis", {})
        user_msg = state.get("user_message", "Give me financial insights")

        # Retrieve relevant transactions for RAG grounding
        rag_context = build_rag_context(user_msg, top_k=5)

        # Build structured context for the LLM
        expense_context = f"""
Financial Summary:
- Total Spending: ₹{analysis.get('total', 0):,.2f}
- Transaction Count: {analysis.get('transaction_count', 0)}
- Daily Average: ₹{analysis.get('daily_average', 0):,.2f}
- Top Category: {analysis.get('top_category', ('N/A', 0))[0]} (₹{analysis.get('top_category', ('N/A', 0))[1]:,.2f})
- Spending by Category: {analysis.get('by_category', {})}

Relevant Transactions (from vector search):
{rag_context}
"""

        prompt = f"""You are NeuroBudget, an expert AI financial advisor.
        
User's question: {user_msg}

{expense_context}

Provide clear, actionable financial insights. Structure your response as:
1. Summary: 2-3 sentences summarizing spending
2. Key Observations: bullet points of important patterns
3. Recommendations: 2-3 specific, practical suggestions

Be specific with numbers. Explain WHY each insight matters.
Keep your response concise and friendly."""

        response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {"role": "system", "content": "You are an expert financial advisor who explains things clearly with data-driven insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.4,
        )

        ai_response = response.choices[0].message.content.strip()

        state["insights"] = {
            "ai_summary": ai_response,
            "total": analysis.get("total", 0),
            "by_category": analysis.get("by_category", {}),
            "top_category": analysis.get("top_category", ("N/A", 0)),
            "daily_average": analysis.get("daily_average", 0),
            "charts": analysis.get("charts", {}),
        }

        reasoning.append(
            f"InsightAgent: Generated LLM insights using expense data and {len(rag_context.splitlines())} RAG context lines."
        )

    except Exception as e:
        errors.append(f"InsightAgent error: {str(e)}")
        state["insights"] = {"ai_summary": "Insights unavailable.", "error": str(e)}
        reasoning.append(f"InsightAgent: Failed — {str(e)}")

    state["reasoning_chain"] = reasoning
    state["errors"] = errors
    return state
