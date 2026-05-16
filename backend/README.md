# NeuroBudget — AI Financial Copilot

An intelligent financial assistant built with FastAPI, LangGraph, FAISS, and OpenRouter.

---

## Architecture

```
User Request
     ↓
FastAPI Endpoints
     ↓
LangGraph Multi-Agent Workflow
  ├── ExpenseAgent   → categorizes & totals spending
  ├── InsightAgent   → LLM-generated insights (OpenRouter)
  ├── RiskAgent      → detects anomalies & overspending
  └── PlanningAgent  → creates savings plans
     ↓
FAISS (RAG retrieval) + SQLite (storage)
     ↓
JSON Response (with Plotly chart data)
```

---

## Setup Instructions

### 1. Clone and navigate

```bash
cd NeuroBudget/backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your OpenRouter API key:

```
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Get your free API key at: https://openrouter.ai

### 5. Run the server

```bash
python app.py
```

Or with uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the API docs

Open: http://localhost:8000/docs

---

## API Endpoints

### `GET /health`
Health check.

```json
{
  "status": "ok",
  "model": "openai/gpt-4o-mini",
  "version": "1.0.0"
}
```

---

### `POST /chat`
Conversational AI financial assistant.

**Request:**
```json
{
  "message": "How much did I spend on food this month?",
  "session_id": "user_123"
}
```

**Response:**
```json
{
  "response": "Based on your transactions, you spent ₹2,740 on food this month across 7 transactions. Swiggy and Zomato account for 65% of this. Consider cooking at home 2-3 times a week to save around ₹800/month.",
  "reasoning": "Response generated using 5 past messages + RAG context (30 transactions indexed). Model: openai/gpt-4o-mini.",
  "session_id": "user_123",
  "timestamp": "2024-01-30T10:30:00"
}
```

---

### `POST /upload-csv`
Upload a bank statement CSV or PDF.

**Form data:** `file` (multipart)

**Response:**
```json
{
  "message": "Successfully processed 30 transactions.",
  "filename": "january_statement.csv",
  "rows_processed": 30,
  "categories_found": ["Food", "Transport", "Shopping", "Entertainment", "Groceries"],
  "total_amount": 31551.0,
  "preview": [
    {
      "date": "2024-01-01",
      "description": "Swiggy Order - Biryani",
      "amount": 350.0,
      "category": "Food",
      "source": "january_statement.csv"
    }
  ]
}
```

---

### `GET /insights`
Full financial analysis with AI summary.

**Response:**
```json
{
  "total_spending": 31551.0,
  "top_category": "Shopping",
  "top_category_amount": 7297.0,
  "savings_estimate": 6310.2,
  "average_daily_spend": 1051.7,
  "spending_by_category": {
    "Shopping": 7297.0,
    "Food": 2740.0,
    "Transport": 2380.0,
    "Entertainment": 2767.0,
    "Groceries": 2900.0,
    "Health": 990.0,
    "Utilities": 3498.0,
    "Travel": 4650.0,
    "Education": 799.0
  },
  "spending_trend": [
    {"date": "2024-01-01", "amount": 350.0},
    {"date": "2024-01-02", "amount": 180.0}
  ],
  "alerts": [
    {
      "type": "overspending",
      "message": "Shopping is 23.1% of total spending",
      "severity": "medium",
      "amount": 7297.0
    }
  ],
  "ai_summary": "**Summary:** Your January spending totalled ₹31,551 with Shopping (23%) and Travel (15%) as the biggest drains...",
  "reasoning": "ExpenseAgent: Analyzed 30 transactions → InsightAgent: Generated LLM insights → RiskAgent: Risk score=25/100 → PlanningAgent: Generated final response"
}
```

---

### `POST /goal-plan`
Create a savings plan for a financial goal.

**Request:**
```json
{
  "target_amount": 100000,
  "timeline_months": 6,
  "monthly_income": 60000,
  "goal_name": "Emergency Fund"
}
```

**Response:**
```json
{
  "goal_name": "Emergency Fund",
  "target_amount": 100000.0,
  "timeline_months": 6,
  "monthly_savings_required": 16666.67,
  "is_achievable": true,
  "steps": [
    {
      "month": 1,
      "target_savings": 16666.67,
      "cumulative_savings": 16666.67,
      "suggested_cuts": [
        "Reduce Entertainment by 15% — save ₹415/month",
        "Reduce Shopping by 15% — save ₹1,095/month"
      ]
    }
  ],
  "recommendations": [
    "Cut Netflix and Spotify to save ₹768/month",
    "Reduce Swiggy/Zomato orders from 7 to 3 per week — saves ₹1,200/month",
    "Use public transport twice a week instead of Uber — saves ₹600/month",
    "Set a ₹3,000 monthly shopping budget with a wishlist cooling period"
  ],
  "chart_data": { "type": "line", "data": [...], "layout": {...} },
  "reasoning": "Goal of ₹100,000 requires saving ₹16,666.67/month over 6 months. This is achievable."
}
```

---

### `GET /risk-analysis`
Detect financial risks and anomalies.

**Response:**
```json
{
  "overall_risk_level": "low",
  "risk_score": 25.0,
  "risk_factors": [
    {
      "risk_type": "overspending",
      "description": "Shopping is 23.1% of total spending",
      "affected_category": "Shopping",
      "amount": 7297.0,
      "severity": "medium",
      "suggestion": "Try reducing Shopping spending by 20% next month."
    }
  ],
  "anomalies": [
    {
      "date": "2024-01-19",
      "description": "Amazon Prime Subscription",
      "amount": 1499.0,
      "category": "Entertainment"
    }
  ],
  "safe_to_spend": 6310.2,
  "reasoning": "Your risk score of 25/100 indicates low financial risk. The main concern is Shopping at 23% of your budget. Consider setting a monthly shopping cap of ₹5,000."
}
```

---

## Testing with Sample Data

```bash
# Upload sample CSV
curl -X POST http://localhost:8000/upload-csv \
  -F "file=@sample_transactions.csv"

# Get insights
curl http://localhost:8000/insights

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Where am I spending the most?", "session_id": "test"}'

# Goal plan
curl -X POST http://localhost:8000/goal-plan \
  -H "Content-Type: application/json" \
  -d '{"target_amount": 50000, "timeline_months": 3, "goal_name": "Laptop Fund"}'

# Risk analysis
curl http://localhost:8000/risk-analysis
```

---

## Project Structure

```
backend/
├── app.py              ← FastAPI app + all endpoints
├── config.py           ← Settings (pydantic-settings + dotenv)
├── requirements.txt
├── .env.example
├── sample_transactions.csv
│
├── agents/
│   ├── expense_agent.py   ← Calculates spending stats
│   ├── insight_agent.py   ← LLM-generated insights
│   ├── risk_agent.py      ← Anomaly + overspending detection
│   ├── planning_agent.py  ← Savings plan generation
│   └── workflow.py        ← LangGraph StateGraph orchestration
│
├── tools/
│   ├── file_parser.py     ← CSV/PDF parsing + normalization
│   ├── categorizer.py     ← Rule-based expense categorization
│   ├── calculator.py      ← Financial math utilities
│   └── charts.py          ← Plotly-compatible chart builders
│
├── rag/
│   ├── embeddings.py      ← sentence-transformers embedding
│   ├── vectorstore.py     ← FAISS index management
│   └── retriever.py       ← RAG query + context formatting
│
├── database/
│   ├── db.py              ← SQLAlchemy SQLite models
│   └── chat_memory.py     ← Conversation history storage
│
├── models/
│   ├── schemas.py         ← Pydantic request/response models
│   └── state.py           ← LangGraph AgentState TypedDict
│
├── uploads/               ← Uploaded files stored here
└── vectorstore/           ← FAISS index files stored here
```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| OpenRouter (not OpenAI direct) | Cost-flexible, model-agnostic |
| SQLite | Zero-config, perfect for MVP |
| FAISS local | No server needed, fast similarity search |
| sentence-transformers | Free local embeddings, no API key |
| LangGraph | Clean multi-agent orchestration with typed state |
| Rule-based categorization | Fast, transparent, no LLM needed for basic labeling |
| Explainable AI | Every response includes `reasoning` field |
