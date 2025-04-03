from fastapi import APIRouter, HTTPException
from api.models.request_model import PredictionRequest
from api.utils.model_loader import load_model
from models.feature_engineering import create_features


import pandas as pd

router = APIRouter()

# Model ve geçmiş verilerin yolu
model_path = "C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/models/saved_models/sales_pipeline_model.pkl"
data_path = "C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_forecasting_data.csv"

# Modeli ve geçmiş veriyi yükle
model = load_model(model_path)
ts_data = pd.read_csv(data_path, parse_dates=["order_date"])

# 🔮 Tahmin Endpoint
@router.post("/")
def predict(request: PredictionRequest):
    print("🎯 Tahmin endpoint'ine GİRİLDİ")

    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction could not be made: {str(e)}")
