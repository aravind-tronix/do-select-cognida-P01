from fastapi import APIRouter

from app.calculation.api.v1.models.request_models import CalculationRequest
from app.calculation.api.v1.models.response_model import CalculationResponse
from app.calculation.api.v1.services.process_data import process_data

router = APIRouter()


@router.post("/execute-formula")
async def execute_formula(data: CalculationRequest):
    """
    execute formula route entry point
    data: request body validated with pydantic model
    CalculationRequest: pydantic class model
    """
    result = await process_data(data)
    return CalculationResponse(message=result)
