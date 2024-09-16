from fastapi import APIRouter

from app.calculation.api.v1.endpoints import calculations

router = APIRouter()

router.include_router(calculations.router, prefix="/api/v1", tags=["calculations"])
