"""
Chat API
"""

from fastapi import APIRouter

from schemas.chat import ChatRequest
from schemas.chat import ChatResponse

from models.state import create_state

from agents.workflow import workflow


router = APIRouter(

    prefix="/chat",

    tags=["Chat"]

)


# ==========================================================
# Chat Endpoint
# ==========================================================

@router.post(

    "",

    response_model=ChatResponse

)

def chat(

    request: ChatRequest

):

    state = create_state(

        question=request.question,

        session_id=request.session_id

    )

    result = workflow.run(state)

    return ChatResponse(

        answer=result.get("answer", ""),

        current_agent=result.get("current_agent", ""),

        session_id=result.get("session_id", request.session_id),

        workflow_status=result.get("workflow_status", "completed"),

        execution_time=result.get("execution_time", 0.0)

    )