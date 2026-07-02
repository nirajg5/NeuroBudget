from fastapi import APIRouter

from api.upload import router as upload_router
from api.chat import router as chat_router

api_router = APIRouter()

api_router.include_router(upload_router)

api_router.include_router(chat_router)