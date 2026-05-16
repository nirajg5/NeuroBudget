"""
planning_agent.py — Fourth (final) agent in the LangGraph workflow.
Creates personalized savings plans and spending reduction recommendations.
"""

from openai import OpenAI
from config import get_settings
from models.state import AgentState
from tools.calculator import monthly_savings_plan

settings = get_settings()

client = OpenAI(
    base_url=settings.openrouter_base_url,
    api_key=settings.openrouter_api_key,
)


def planning_agent(state: AgentState) -> AgentState:
    """
    Planning Agent — synthesizes all prior agent outputs into a final
    actionable savings plan and a cohesive response.

    Reads:
        state["expense_analysis"]
        state["insights"]
        state["risk_flags"]
        state["user_message"]

    Writes:
        state["savings_plan"]
        state["final_response"]
        state["reasoning_chain"] (appends)
    """
    reasoning = state.get("reasoning_chain", [])
    errors = state.get("errors", [])

    try:
        analysis = state.get("expense_analysis", {})
        insights = state.get("insights", {})
        risk_flags = state.get("risk_flags", {})
        user_msg = state.get("user_message", "")
        total = analysis.get("total", 0)
        by_cat = analysis.get("by_category", {})
        risk_level = risk_flags.get("risk_level", "unknown")

        # Identify categories where spending could be cut
        cut_candidates = []
        discretionary = ["Entertainment", "Shopping", "Food", "Travel"]
        for cat in discretionary:
            if cat in by_cat and by_cat[cat] > 0:
                cut_candidates.append(
                    f"{cat}: ₹{by_cat[cat]:,.2f} (try cutting 20% = ₹{by_cat[cat]*0.2:,.2f} saved)"
                )

        # Full context for LLM planning
        planning_context = f"""
User Question: {user_msg}

Current Financial Picture:
- Total Monthly Spending: ₹{total:,.2f}
- Risk Level: {risk_level.upper()}
- Risk Score: {risk_flags.get('risk_score', 0):.0f}/100

Spending Breakdown:
{chr(10).join([f"  - {k}: ₹{v:,.2f}" for k, v in by_cat.items()])}

Areas to Cut:
{chr(10).join(cut_candidates) if cut_candidates else "  No clear cut candidates identified"}

AI Insights Summary:
{insights.get('ai_summary', 'No insights available')}

Risk Explanation:
{risk_flags.get('explanation', 'No risk data')}
"""

        # Generate comprehensive final response
        final_prompt = f"""You are NeuroBudget, an AI financial copilot. 
        
Based on the full financial analysis below, create a comprehensive, friendly response to the user.

{planning_context}

Your response must include:
1. **Overall Assessment** — 2-3 sentences on their financial health
2. **Key Actions** — 3 specific things they can do this month (with amounts)
3. **Savings Opportunity** — How much they could realistically save if they follow your advice

Be encouraging, specific, and use ₹ amounts. Keep total response under 400 words.
Format with clear headers."""

        final_response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {"role": "system", "content": "You are a helpful, knowledgeable financial advisor. Be concise but specific."},
                {"role": "user", "content": final_prompt}
            ],
            max_tokens=600,
            temperature=0.4,
        )

        final_text = final_response.choices[0].message.content.strip()

        # Build a default savings plan (if no specific goal was given)
        default_goal = total * 6    # 6-month spending as a savings goal
        plan = monthly_savings_plan(
            target_amount=default_goal,
            timeline_months=6,
            current_spending=total,
        )

        state["savings_plan"] = {
            "suggested_monthly_savings": plan["monthly_required"],
            "is_achievable": plan["is_achievable"],
            "cut_candidates": cut_candidates,
            "default_goal": default_goal,
        }

        state["final_response"] = final_text

        reasoning.append(
            f"PlanningAgent: Generated final response. "
            f"Suggested monthly savings: ₹{plan['monthly_required']:,.2f}. "
            f"Plan achievable: {plan['is_achievable']}."
        )

    except Exception as e:
        errors.append(f"PlanningAgent error: {str(e)}")
        state["savings_plan"] = {}
        state["final_response"] = "I was unable to generate a savings plan at this time. Please try again."
        reasoning.append(f"PlanningAgent: Failed — {str(e)}")

    state["reasoning_chain"] = reasoning
    state["errors"] = errors
    return state
