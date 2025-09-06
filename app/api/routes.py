"""
Main API router configuration
"""
from fastapi import APIRouter
from app.api.endpoints import data, ingestion

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
