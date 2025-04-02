from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.database import get_db
from data.models.product import Product  # ✔️ bu doğru path

router = APIRouter()

print("✅ /product router")
@router.get("/", tags=["Products"])
def list_products(db: Session = Depends(get_db)):
    print("✅ /products endpoint'ine giriş yapıldı")
    products = db.query(Product).all()
    return [{"id": p.product_id, "name": p.product_name} for p in products]


