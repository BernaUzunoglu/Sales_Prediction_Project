from pydantic import BaseModel

class CustomerSegmentRequest(BaseModel):
    total_spent: float
    num_orders: int
    avg_order_value: float
    num_products: int
    recency: float
