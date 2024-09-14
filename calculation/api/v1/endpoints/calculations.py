from fastapi import APIRouter, Query, HTTPException
from calculation.api.v1.models.request_models import CalculationRequest
from calculation.api.v1.services.identifier import split_and_identify

router = APIRouter()


@router.post("/api/execute-formula")
async def execute_formula(data: CalculationRequest):
    res = await split_and_identify(data.formulas, data.data)
    # print(res)
    return {"message": data}
