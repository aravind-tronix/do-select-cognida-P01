from pydantic import BaseModel


class CalculationResponse(BaseModel):
    message: dict
