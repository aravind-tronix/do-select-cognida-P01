from pydantic import BaseModel


class CalculationRequest(BaseModel):
    data: list[dict]
    formulas: list[dict]
