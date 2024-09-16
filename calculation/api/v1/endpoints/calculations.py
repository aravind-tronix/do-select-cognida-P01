from fastapi import APIRouter, Query, HTTPException
from calculation.api.v1.models.request_models import CalculationRequest
from calculation.api.v1.services.process_data import process_data

router = APIRouter()


@router.post("/api/execute-formula")
async def execute_formula(data: CalculationRequest):
    result = await process_data(data)
    return {"message": result}
