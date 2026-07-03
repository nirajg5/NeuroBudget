"""
Chat Schemas
"""

from pydantic import BaseModel


# ==========================================================
# Chat Request
# ==========================================================

class ChatRequest(BaseModel):

    question: str

    session_id: str = "default"


# ==========================================================
# Chat Response
# ==========================================================

class ChatResponse(BaseModel):

    answer: str

    current_agent: str

    session_id: str

    workflow_status: str

    execution_time: float