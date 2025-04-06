from pydantic import BaseModel, conint
from typing import List
class PredictionRequest(BaseModel):
    product_id: int
    year: int
    month: conint(ge=1, le=12)
    day: conint(ge=1, le=31)
    quantity: int

class RetrainPayload(BaseModel):
    data: List[PredictionRequest]