# NeuroBudget - AI Financial Copilot

An intelligent multi-agent financial assistant powered by LangGraph, FAISS, and OpenRouter.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-0.1.9-orange" />
  <img src="https://img.shields.io/badge/OpenRouter-GPT--4o--mini-purple" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

---

## Overview

NeuroBudget is an AI-powered personal finance assistant that helps users:

- Upload and analyze bank statements
- Categorize expenses automatically
- Generate financial insights
- Detect overspending and anomalies
- Build savings plans
- Chat with financial data using AI + RAG

The system combines:

- **FastAPI**
- **LangGraph Multi-Agent Workflows**
- **FAISS Vector Search**
- **OpenRouter LLMs**
- **SQLite**
- **Sentence Transformers**

---

# Features

## AI Financial Chat

Ask questions like:

- "How much did I spend on food?"
- "Where am I overspending?"
- "What are my biggest expenses?"

Powered using:
- RAG Retrieval
- OpenRouter GPT models
- Session memory

---

## Smart Expense Categorization

Automatically categorizes transactions into:

| Category | Examples |
|---|---|
| Food | Swiggy, Zomato |
| Transport | Uber, Ola |
| Shopping | Amazon, Flipkart |
| Entertainment | Netflix, Spotify |
| Utilities | Airtel, Jio |
| Travel | Airbnb, Goibibo |

---

## Financial Insights

Generate:
- Spending summaries
- Top categories
- Daily averages
- Savings estimates
- AI-generated recommendations

---

## Goal Planning

Create savings plans such as:

- Emergency Fund
- Laptop Purchase
- Vacation Planning

The AI calculates:
- Monthly savings required
- Goal achievability
- Personalized recommendations

---

## Risk Analysis

Detect:
- Overspending
- Budget spikes
- Spending anomalies
- Unsafe spending patterns

---

# Architecture

```text
User Request
     |
     v
FastAPI Endpoints
/chat  /upload-csv  /insights  /goal-plan  /risk-analysis
     |
     v
LangGraph Multi-Agent Workflow
     |
     +--> ExpenseAgent
     +--> InsightAgent
     +--> RiskAgent
     +--> PlanningAgent
     |
     v
FAISS Vector Search + SQLite
     |
     v
JSON Response + Plotly Chart Data
```

---

# Project Structure

```text
NeuroBudget/backend/

├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── sample_transactions.csv

├── agents/
│   ├── expense_agent.py
│   ├── insight_agent.py
│   ├── risk_agent.py
│   ├── planning_agent.py
│   └── workflow.py

├── tools/
│   ├── file_parser.py
│   ├── categorizer.py
│   ├── calculator.py
│   └── charts.py

├── rag/
│   ├── embeddings.py
│   ├── vectorstore.py
│   └── retriever.py

├── database/
│   ├── db.py
│   └── chat_memory.py

├── models/
│   ├── schemas.py
│   └── state.py

├── uploads/
└── vectorstore/
```

---

# Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| AI Workflow | LangGraph |
| LLM Provider | OpenRouter |
| Embeddings | sentence-transformers |
| Vector Database | FAISS |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Data Processing | Pandas |
| PDF Parsing | pdfplumber |
| Charts | Plotly JSON |

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/nirajg5/NeuroBudget.git
cd NeuroBudget/backend
```

---

## 2. Create Virtual Environment

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create `.env`

```env
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

---

## 5. Run Application

```bash
python app.py
```

OR

```bash
uvicorn app:app --reload
```

---

# API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/chat` | POST | AI financial assistant |
| `/upload-csv` | POST | Upload bank statement |
| `/insights` | GET | Financial analysis |
| `/goal-plan` | POST | Savings planning |
| `/risk-analysis` | GET | Risk detection |

---

# Example API Usage

## Upload CSV

```bash
curl -X POST http://localhost:8000/upload-csv \
-F "file=@sample_transactions.csv"
```

---

## Chat with AI

```bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d "{\"message\":\"How much did I spend on food?\",\"session_id\":\"user_1\"}"
```

---

## Get Insights

```bash
curl http://localhost:8000/insights
```

---

# Example Response

```json
{
  "total_spending": 31551.0,
  "top_category": "Shopping",
  "average_daily_spend": 1051.7,
  "risk_score": 25,
  "ai_summary": "Shopping and travel are your largest expenses."
}
```

---

# Why NeuroBudget?

## Explainable AI

Every response includes reasoning and transparency.

---

## Local-First Architecture

- SQLite storage
- Local FAISS vector database
- No expensive cloud vector DB required

---

## Cost Efficient

Uses:
- OpenRouter
- Local embeddings
- Rule-based categorization

to minimize LLM costs.

---

# Future Improvements
- Authentication
- Budget forecasting
- Monthly reports
- Real-time notifications
- Mobile app integration


# 
