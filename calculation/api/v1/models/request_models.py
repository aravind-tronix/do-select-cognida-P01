from typing import Dict, List

from pydantic import BaseModel, field_validator


class CalculationRequest(BaseModel):
    data: List[Dict]
    formulas: List[Dict]

    # Field validator for 'data'
    @field_validator("data")
    def check_data_not_empty(cls, v):
        if not v:
            raise ValueError("data list cannot be empty")
        for item in v:
            if not isinstance(item, dict) or not item:
                raise ValueError("Each item in data must be a non-empty dictionary")
        return v

    # Field validator for 'formulas'
    @field_validator("formulas")
    def check_formulas_not_empty(cls, v):
        if not v:
            raise ValueError("formulas list cannot be empty")
        for item in v:
            if not isinstance(item, dict) or not item:
                raise ValueError("Each item in formulas must be a non-empty dictionary")
        return v
