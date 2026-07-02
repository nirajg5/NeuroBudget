from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.constants import WELCOME_MESSAGE

from api.router import api_router

app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION,

    description=WELCOME_MESSAGE,

    docs_url="/docs",

    redoc_url="/redoc",

    openapi_url="/openapi.json"

)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ==========================================================
# Register All API Routers
# ==========================================================

app.include_router(api_router)


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/", tags=["Home"])
def root():

    return {

        "message": WELCOME_MESSAGE,

        "application": settings.APP_NAME,

        "version": settings.APP_VERSION,

        "docs": "/docs"

    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health", tags=["Health"])
def health():

    return {

        "status": "healthy"

    }