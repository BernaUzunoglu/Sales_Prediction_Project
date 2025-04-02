from pydantic import BaseModel

# Pydantic İstek Modeli - API’ye gelen JSON verisinin doğruluğunu sağlar.
class PredictionRequest(BaseModel):
    product_id: int
    year: int
    month: int
    day: int
