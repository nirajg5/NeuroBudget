from fastapi import APIRouter

from api.upload import router as upload_router
from api.chat import router as chat_router
from api.transactions import router as transaction_router
from api.goal import router as goals_router
from api.forcast import router as forecast_router
from api.reports import router as reports_router
from api.dashboard import router as dashboard_router
from api.analytics import router as analytics_router

api_router = APIRouter()

api_router.include_router(upload_router)
api_router.include_router(chat_router)
api_router.include_router(transaction_router)
api_router.include_router(goals_router)
api_router.include_router(forecast_router)
api_router.include_router(reports_router)
api_router.include_router(dashboard_router)
api_router.include_router(analytics_router)