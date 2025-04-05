from fastapi import APIRouter, HTTPException
from api.models.request_model import PredictionRequest
from api.utils.model_loader import load_model
from models.feature_engineering import create_features
from api.utils.errors import ERRORS
from config import Config
import pandas as pd
import json
import os

# Eğitimde kullanılan ürün ID’lerini yükle
with open(Config.PROJECT_ROOT / "src" / "models" / "model_results" / "trained_product_ids.json", "r") as f:
    valid_product_ids = json.load(f)

router = APIRouter()

# model_path = f"{Config.PROJECT_ROOT}/src/models/saved_models/sales_pipeline_model.pkl"

# model_path = Config.PROJECT_ROOT / "src" / "models" / "saved_models" / "sales_pipeline_model.pkl"
model_path = Config.PROJECT_ROOT / "src/models/saved_models/sales_pipeline_model.pkl"
data_path = Config.PROJECT_ROOT / "src" / "data" / "processed" / "sales_forecasting_data.csv"

# Modeli ve geçmiş veriyi yükle
model = load_model(model_path)
ts_data = pd.read_csv(data_path, parse_dates=["order_date"])

# 🔮 Tahmin Endpoint
@router.post("/")
def predict(request: PredictionRequest):
    print("🎯 Tahmin endpoint'ine GİRİLDİ")

    try:
        # ✔️ Ürün ID geçerli mi kontrol et
        if request.product_id not in valid_product_ids:
            raise HTTPException(
                status_code=400,
                detail={"error_code": 1001, "error_message": ERRORS[1001]}
            )

        input_df = pd.DataFrame([{
            "product_id": request.product_id,
            "year": request.year,
            "month": request.month,
            "day": request.day
        }])
        print(input_df)

        # 2. Özellik mühendisliği uygula (model pipeline'ında yoksa)
        features = create_features(input_df, ts_data)
        print(input_df)
        print(features)

        # 3. Tahmin yap
        prediction = model.predict(features)[0]

        # 4. Sonucu döndür
        return {
            "product_id": request.product_id,
            "predicted_quantity": prediction
        }
    except HTTPException as he:
        raise he  # zaten özel hata dönüyorsa
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error_code": 9999, "error_message": f"Prediction failed: {str(e)}"}
        )
