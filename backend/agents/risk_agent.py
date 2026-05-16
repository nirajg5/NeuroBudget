"""
risk_agent.py — Third agent in the LangGraph workflow.
Detects financial risks: overspending, abnormal transactions, budget spikes.
Combines rule-based detection with an LLM explanation.
"""

from openai import OpenAI
from config import get_settings
from models.state import AgentState
from tools.calculator import (
    detect_spending_spikes,
    overspending_categories,
    spending_by_category,
)

settings = get_settings()

client = OpenAI(
    base_url=settings.openrouter_base_url,
    api_key=settings.openrouter_api_key,
)


def _compute_risk_score(
    anomalies: list,
    overspending: list,
    total_spending: float
) -> float:
    """
    Heuristic risk score from 0 to 100.
    - Each anomaly adds 10 points
    - Each overspent category adds 15 points
    - High spending base adds up to 20 points
    Capped at 100.
    """
    score = 0.0
    score += len(anomalies) * 10
    score += len(overspending) * 15

    # High total spending increases base risk slightly
    if total_spending > 50000:
        score += 20
    elif total_spending > 20000:
        score += 10
    elif total_spending > 10000:
        score += 5

    return min(score, 100.0)


def risk_agent(state: AgentState) -> AgentState:
    """
    Risk Agent — detects anomalies, overspending, and financial red flags.

    Reads:
        state["raw_transactions"]
        state["expense_analysis"]

    Writes:
        state["risk_flags"]
        state["reasoning_chain"] (appends)
    """
    reasoning = state.get("reasoning_chain", [])
    errors = state.get("errors", [])

    try:
        transactions = state.get("raw_transactions", [])
        analysis = state.get("expense_analysis", {})
        total = analysis.get("total", 0)
        by_cat = analysis.get("by_category", {})

        # Rule-based detection
        anomalies = detect_spending_spikes(transactions, threshold_multiplier=2.0)
        overspending = overspending_categories(by_cat)

        risk_score = _compute_risk_score(anomalies, overspending, total)
        risk_level = (
            "high" if risk_score >= 60
            else "medium" if risk_score >= 30
            else "low"
        )

        # Safe-to-spend = 20% of current total (conservative heuristic)
        safe_to_spend = round(total * 0.20, 2)

        # Ask LLM to explain risks in human language
        risk_context = f"""
Risk Analysis Data:
- Total Spending: ₹{total:,.2f}
- Risk Score: {risk_score}/100
- Anomalous Transactions: {len(anomalies)} detected
- Overspending Categories: {[o.get('category', 'N/A') for o in overspending]}
- Spending Breakdown: {by_cat}

Anomalous transactions:
{chr(10).join([f"  - {a.get('date')}: {a.get('description')} ₹{a.get('amount',0):,.2f}" for a in anomalies[:5]]) or "  None detected"}

Overspending:
{chr(10).join([f"  - {o.get('category')}: {o.get('message', f'over limit by ₹{o.get(\"overage\", 0):,.2f}')}" for o in overspending]) or "  None detected"}
"""

        llm_response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[
                {"role": "system", "content": "You are a financial risk analyst. Be concise and specific."},
                {"role": "user", "content": f"""Analyze these financial risks and explain what the user should do.
                
{risk_context}

Write 2-4 sentences explaining the main risks and one clear action step for each.
Use plain language. Include specific numbers where helpful."""}
            ],
            max_tokens=400,
            temperature=0.3,
        )

        risk_explanation = llm_response.choices[0].message.content.strip()

        state["risk_flags"] = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "anomalies": anomalies[:10],         # Cap at 10
            "overspending": overspending,
            "safe_to_spend": safe_to_spend,
            "explanation": risk_explanation,
        }

        reasoning.append(
            f"RiskAgent: Risk score={risk_score:.0f}/100 ({risk_level}). "
            f"Found {len(anomalies)} anomalies and {len(overspending)} overspending categories."
        )

    except Exception as e:
        errors.append(f"RiskAgent error: {str(e)}")
        state["risk_flags"] = {"risk_score": 0, "risk_level": "unknown", "error": str(e)}
        reasoning.append(f"RiskAgent: Failed — {str(e)}")

    state["reasoning_chain"] = reasoning
    state["errors"] = errors
    return state
