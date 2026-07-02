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

    result = workflow.run(

        state

    )

    return ChatResponse(

        answer=result["answer"],

        current_agent=result["current_agent"],

        session_id=result["session_id"]

    )