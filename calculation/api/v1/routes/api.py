from fastapi import APIRouter
from calculation.api.v1.endpoints import calculations

router = APIRouter()

router.include_router(calculations.router, tags=["calculations"])
