"""
calculator.py — Financial calculation utilities.
Pure Python functions — no LLM needed for math.
"""

from typing import List, Dict, Optional, Tuple
import pandas as pd
from datetime import datetime, timedelta


def total_spending(transactions: List[Dict]) -> float:
    """Sum of all transaction amounts."""
    return round(sum(t.get("amount", 0) for t in transactions), 2)


def spending_by_category(transactions: List[Dict]) -> Dict[str, float]:
    """
    Aggregate total spending per category.
    Returns dict sorted by amount descending.
    Example: {"Food": 5200, "Transport": 1800, ...}
    """
    category_totals: Dict[str, float] = {}
    for t in transactions:
        cat = t.get("category", "Other")
        category_totals[cat] = round(category_totals.get(cat, 0) + t.get("amount", 0), 2)
    return dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True))


def top_category(transactions: List[Dict]) -> Tuple[str, float]:
    """Return (category_name, total_amount) for the highest spending category."""
    by_cat = spending_by_category(transactions)
    if not by_cat:
        return ("Other", 0.0)
    top = max(by_cat.items(), key=lambda x: x[1])
    return top


def estimate_savings(total_spent: float, monthly_income: Optional[float] = None) -> float:
    """
    Estimate savings.
    - If income provided: savings = income - spending
    - If not: assumes 30% savings target on spending
    """
    if monthly_income:
        return round(max(0, monthly_income - total_spent), 2)
    # Heuristic: suggest saving 20% more than current spending level allows
    return round(total_spent * 0.20, 2)


def daily_average_spending(transactions: List[Dict]) -> float:
    """Calculate average spending per day."""
    if not transactions:
        return 0.0
    total = total_spending(transactions)
    # Count unique days
    dates = set(t.get("date", "") for t in transactions if t.get("date"))
    days = max(len(dates), 1)
    return round(total / days, 2)


def monthly_savings_plan(
    target_amount: float,
    timeline_months: int,
    current_spending: float,
    monthly_income: Optional[float] = None
) -> Dict:
    """
    Calculate how much to save per month to reach a goal.

    Returns:
        monthly_required: Amount to save each month
        is_achievable: Whether it's realistic
        suggestions: Category cut suggestions
    """
    monthly_required = round(target_amount / timeline_months, 2)

    # Check if achievable
    if monthly_income:
        current_savings = monthly_income - current_spending
        is_achievable = current_savings >= monthly_required
        surplus = round(current_savings - monthly_required, 2)
    else:
        # Without income data, flag if > 40% of spending
        is_achievable = monthly_required <= (current_spending * 0.4)
        surplus = None

    return {
        "monthly_required": monthly_required,
        "is_achievable": is_achievable,
        "surplus": surplus,
    }


def detect_spending_spikes(transactions: List[Dict], threshold_multiplier: float = 2.0) -> List[Dict]:
    """
    Detect transactions that are unusually large.
    Flags any transaction > (mean + threshold_multiplier * std_dev).
    """
    if len(transactions) < 3:
        return []

    amounts = [t["amount"] for t in transactions]
    df = pd.Series(amounts)
    mean = df.mean()
    std = df.std()
    threshold = mean + (threshold_multiplier * std)

    spikes = [t for t in transactions if t["amount"] > threshold]
    return spikes


def overspending_categories(
    spending_by_cat: Dict[str, float],
    budget_limits: Optional[Dict[str, float]] = None
) -> List[Dict]:
    """
    Identify categories over budget.
    If no budget provided, flags categories > 30% of total spend.
    """
    total = sum(spending_by_cat.values())
    alerts = []

    for cat, amount in spending_by_cat.items():
        if budget_limits and cat in budget_limits:
            if amount > budget_limits[cat]:
                alerts.append({
                    "category": cat,
                    "amount": amount,
                    "limit": budget_limits[cat],
                    "overage": round(amount - budget_limits[cat], 2)
                })
        else:
            # Heuristic: flag if single category > 35% of total
            if total > 0 and (amount / total) > 0.35:
                alerts.append({
                    "category": cat,
                    "amount": amount,
                    "percentage": round((amount / total) * 100, 1),
                    "message": f"{cat} is {round((amount/total)*100,1)}% of total spending"
                })

    return alerts
