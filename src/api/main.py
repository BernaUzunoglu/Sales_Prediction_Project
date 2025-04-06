from fastapi import FastAPI, Request
from api.routes import predict, retrain, health, products, sales_summary, customer_segment_predict
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.utils.errors import ERRORS

# FastAPI Başlatma Noktası
# routes/ içindeki tüm endpoint’leri burada dahil ediyoruz.

app = FastAPI(
    title="ML Based Sales Prediction API",
    description="A FastAPI project for predicting sales using trained models.",
    version="1.0.0"
)
# 🚨 Tip hataları için özel yakalayıcı
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_errors = []
    for error in exc.errors():
        custom_errors.append({
            "field": error.get("loc")[-1],
            "message": error.get("msg"),
            "type": error.get("type")
        })

    return JSONResponse(
        status_code=422,
        content={
            "error_code": 1004,
            "error_message": ERRORS.get(1004, "Geçersiz veri formatı."),
            "details": custom_errors
        }
    )
# Endpoint'leri ekliyoruz
app.include_router(health.router, prefix="/health", tags=["Health Check"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
# app.include_router(train.router, prefix="/train", tags=["Training"])
app.include_router(products.router, prefix="/product", tags=["Products"])
app.include_router(sales_summary.router)
app.include_router(customer_segment_predict.router)
app.include_router(retrain.router, prefix="/retrain")

print("📡 Aktif ROUTE'lar:")
for route in app.routes:
    print(f"{route}")