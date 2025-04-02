from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from data.database import get_db
from data.models.order_detail import OrderDetail
from data.models.product import Product

router = APIRouter()

@router.get("/sales_summary", tags=["Sales Summary"])
def sales_summary(db: Session = Depends(get_db)):
    summary = (
        db.query(
            Product.product_name,
            func.sum(OrderDetail.quantity).label("total_quantity")
        )
        .join(OrderDetail, Product.product_id == OrderDetail.product_id)
        .group_by(Product.product_name)
        .all()
    )

    return [{"product_name": row.product_name, "total_quantity": row.total_quantity} for row in summary]
