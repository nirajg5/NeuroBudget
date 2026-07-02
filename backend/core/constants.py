"""
Application Constants
"""

# ============================================================
# Categories
# ============================================================

EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Travel",
    "Education",
    "Fuel",
    "Investment",
    "Insurance",
    "Bills",
    "Rent",
    "EMI",
    "Tax",
    "Grocery",
    "Salary",
    "Other"
]

# ============================================================
# Payment Methods
# ============================================================

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash"
]

# ============================================================
# Transaction Types
# ============================================================

TRANSACTION_TYPES = [
    "Debit",
    "Credit"
]

# ============================================================
# LangGraph Agents
# ============================================================

AGENTS = [
    "expense",
    "insight",
    "risk",
    "planning",
    "forecast"
]

# ============================================================
# Supported File Types
# ============================================================

SUPPORTED_EXTENSIONS = [
    ".csv"
]

# ============================================================
# Pinecone
# ============================================================

TOP_K_RESULTS = 5

VECTOR_DIMENSION = 384

SIMILARITY_METRIC = "cosine"

# ============================================================
# API Tags
# ============================================================

API_TAGS = [
    "Upload",
    "Chat",
    "Insights",
    "Risk",
    "Planning",
    "Forecast",
    "Reports",
    "Health"
]

# ============================================================
# Health Messages
# ============================================================

HEALTHY_MESSAGE = "NeuroBudget Backend Running"

WELCOME_MESSAGE = "Welcome to NeuroBudget AI Financial Copilot"

# ============================================================
# Prompt Templates
# ============================================================

SYSTEM_PROMPT = """
You are NeuroBudget,
an AI-powered Financial Copilot.

Your responsibilities are:

- Analyze financial transactions
- Explain spending patterns
- Detect risks
- Generate savings plans
- Forecast expenses
- Provide personalized financial advice

Always answer in a professional, concise, and helpful manner.
"""