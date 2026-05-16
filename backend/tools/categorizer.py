"""
categorizer.py — Rule-based expense categorization engine.
Maps transaction descriptions to spending categories using keyword matching.
Falls back to "Other" if no rule matches.
"""

import re
from typing import List, Dict
from models.schemas import ExpenseCategory


# ─── Category Rules ───────────────────────────────────────────────────────────
# Each category maps to a list of keywords (case-insensitive substring match).
# Order matters — first match wins.

CATEGORY_RULES: Dict[str, List[str]] = {
    ExpenseCategory.FOOD: [
        "swiggy", "zomato", "domino", "pizza", "restaurant", "cafe", "coffee",
        "mcdonald", "kfc", "burger", "subway", "dunkin", "starbucks", "food",
        "biryani", "dhaba", "hotel", "dine", "eat", "meal", "lunch", "dinner",
        "breakfast", "snack", "bakery", "bake"
    ],
    ExpenseCategory.GROCERIES: [
        "bigbasket", "grofer", "blinkit", "zepto", "dmart", "reliance fresh",
        "nature basket", "supermarket", "grocery", "vegetables", "fruits",
        "milk", "dairy", "provision", "kirana", "hypermarket"
    ],
    ExpenseCategory.TRANSPORT: [
        "uber", "ola", "rapido", "cab", "taxi", "auto", "metro", "bus",
        "train", "irctc", "flight", "airline", "indigo", "spicejet", "makemytrip",
        "petrol", "fuel", "parking", "toll", "transport", "commute"
    ],
    ExpenseCategory.SHOPPING: [
        "amazon", "flipkart", "myntra", "ajio", "meesho", "snapdeal",
        "nykaa", "shoppers stop", "h&m", "zara", "westside", "max fashion",
        "shopping", "purchase", "buy", "store", "mall", "outlet"
    ],
    ExpenseCategory.ENTERTAINMENT: [
        "netflix", "amazon prime", "hotstar", "disney", "spotify", "youtube",
        "gaana", "jio cinema", "apple tv", "zee5", "sonyliv", "bookmyshow",
        "cinema", "movie", "theatre", "concert", "game", "gaming", "steam",
        "entertainment", "subscription"
    ],
    ExpenseCategory.UTILITIES: [
        "electricity", "water", "gas", "internet", "broadband", "wifi",
        "airtel", "jio", "vodafone", "bsnl", "tata sky", "dish tv",
        "utility", "bill", "recharge", "maintenance", "society", "rent"
    ],
    ExpenseCategory.HEALTH: [
        "apollo", "medplus", "1mg", "pharmeasy", "netmeds", "practo",
        "hospital", "clinic", "doctor", "medicine", "pharmacy", "medical",
        "health", "diagnostic", "lab", "test", "consultation", "gym", "fitness"
    ],
    ExpenseCategory.EDUCATION: [
        "udemy", "coursera", "unacademy", "byju", "khan academy", "college",
        "school", "university", "tuition", "coaching", "course", "book",
        "education", "learning", "training", "library"
    ],
    ExpenseCategory.TRAVEL: [
        "hotel", "resort", "oyo", "airbnb", "booking.com", "trivago",
        "goibibo", "yatra", "holiday", "vacation", "tourism", "travel",
        "trip", "tour", "visa", "passport"
    ],
    ExpenseCategory.FINANCE: [
        "emi", "loan", "insurance", "lic", "hdfc", "sbi", "icici", "axis",
        "mutual fund", "sip", "investment", "nps", "ppf", "tax", "bank",
        "credit card", "debit card", "transfer", "upi", "payment", "finance"
    ],
}


def categorize_transaction(description: str) -> str:
    """
    Match a transaction description to the best expense category.

    Logic:
    1. Clean the description (lowercase, strip extra whitespace)
    2. Check each category's keywords in priority order
    3. Return the first matching category, or "Other"
    """
    if not description:
        return ExpenseCategory.OTHER

    cleaned = description.lower().strip()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in cleaned:
                return category

    return ExpenseCategory.OTHER


def categorize_bulk(descriptions: List[str]) -> List[str]:
    """Batch categorize a list of transaction descriptions."""
    return [categorize_transaction(desc) for desc in descriptions]


def get_category_summary(categories: List[str]) -> Dict[str, int]:
    """Count transactions per category."""
    summary: Dict[str, int] = {}
    for cat in categories:
        summary[cat] = summary.get(cat, 0) + 1
    return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))
