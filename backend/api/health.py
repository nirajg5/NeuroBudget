from fastapi import APIRouter

from core.constants import HEALTHY_MESSAGE

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "healthy",
        "message": HEALTHY_MESSAGE
    }