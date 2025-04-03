from fastapi import FastAPI
from api.routes import predict, retrain, health, products, sales_summary, customer_segment_predict

# FastAPI Başlatma Noktası
# routes/ içindeki tüm endpoint’leri burada dahil ediyoruz.

app = FastAPI(
    title="ML Based Sales Prediction API",
    description="A FastAPI project for predicting sales using trained models.",
    version="1.0.0"
)

# Endpoint'leri ekliyoruz
app.include_router(health.router, prefix="/health", tags=["Health Check"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
# app.include_router(train.router, prefix="/train", tags=["Training"])
app.include_router(products.router, prefix="/product", tags=["Products"])
app.include_router(sales_summary.router)
app.include_router(customer_segment_predict.router)

print("📡 Aktif ROUTE'lar:")
for route in app.routes:
    print(f"{route}")