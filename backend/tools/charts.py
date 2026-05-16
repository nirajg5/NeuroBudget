"""
charts.py — Generates Plotly-compatible JSON chart data.
These dicts can be sent directly to the frontend and rendered with Plotly.js.
"""

from typing import List, Dict, Any


def spending_pie_chart(spending_by_category: Dict[str, float]) -> Dict[str, Any]:
    """
    Pie chart of spending by category.
    Returns Plotly-compatible data + layout dict.
    """
    if not spending_by_category:
        return {}

    labels = list(spending_by_category.keys())
    values = list(spending_by_category.values())

    return {
        "type": "pie",
        "data": [
            {
                "type": "pie",
                "labels": labels,
                "values": values,
                "hole": 0.4,             # Donut chart
                "textinfo": "label+percent",
                "hovertemplate": "<b>%{label}</b><br>Amount: ₹%{value:,.0f}<br>%{percent}<extra></extra>",
            }
        ],
        "layout": {
            "title": {"text": "Spending by Category"},
            "showlegend": True,
            "margin": {"t": 50, "b": 20, "l": 20, "r": 20},
        }
    }


def spending_bar_chart(spending_by_category: Dict[str, float]) -> Dict[str, Any]:
    """
    Horizontal bar chart of spending per category.
    """
    if not spending_by_category:
        return {}

    # Sort by value ascending for horizontal bar (largest at top visually)
    sorted_items = sorted(spending_by_category.items(), key=lambda x: x[1])
    categories = [item[0] for item in sorted_items]
    amounts = [item[1] for item in sorted_items]

    return {
        "type": "bar",
        "data": [
            {
                "type": "bar",
                "orientation": "h",
                "x": amounts,
                "y": categories,
                "text": [f"₹{a:,.0f}" for a in amounts],
                "textposition": "outside",
                "marker": {"color": "#6366f1"},
                "hovertemplate": "<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
            }
        ],
        "layout": {
            "title": {"text": "Category-wise Spending"},
            "xaxis": {"title": "Amount (₹)"},
            "yaxis": {"title": "Category"},
            "margin": {"t": 50, "b": 60, "l": 120, "r": 60},
        }
    }


def savings_goal_line_chart(
    monthly_savings_required: float,
    timeline_months: int,
    target_amount: float
) -> Dict[str, Any]:
    """
    Line chart showing cumulative savings progress towards goal.
    """
    months = list(range(1, timeline_months + 1))
    cumulative = [round(monthly_savings_required * m, 2) for m in months]

    return {
        "type": "line",
        "data": [
            {
                "type": "scatter",
                "mode": "lines+markers",
                "x": [f"Month {m}" for m in months],
                "y": cumulative,
                "name": "Projected Savings",
                "line": {"color": "#10b981", "width": 2},
                "hovertemplate": "%{x}<br>Savings: ₹%{y:,.0f}<extra></extra>",
            },
            {
                "type": "scatter",
                "mode": "lines",
                "x": [f"Month {m}" for m in months],
                "y": [target_amount] * len(months),
                "name": "Goal",
                "line": {"color": "#ef4444", "dash": "dash", "width": 2},
                "hovertemplate": "Goal: ₹%{y:,.0f}<extra></extra>",
            }
        ],
        "layout": {
            "title": {"text": "Savings Progress to Goal"},
            "xaxis": {"title": "Month"},
            "yaxis": {"title": "Amount (₹)"},
            "legend": {"x": 0, "y": 1},
            "margin": {"t": 50, "b": 60, "l": 80, "r": 20},
        }
    }


def spending_trend_chart(transactions: List[Dict]) -> List[Dict[str, Any]]:
    """
    Time-series spending trend — daily or weekly aggregation.
    Returns list of {date, amount} dicts for Plotly scatter/line chart.
    """
    if not transactions:
        return []

    # Group by date
    date_totals: Dict[str, float] = {}
    for t in transactions:
        date = t.get("date", "Unknown")
        date_totals[date] = round(date_totals.get(date, 0) + t.get("amount", 0), 2)

    # Sort by date
    sorted_dates = sorted(date_totals.items())
    return [{"date": d, "amount": a} for d, a in sorted_dates]
