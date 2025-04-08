from fastapi import APIRouter, HTTPException
from api.models.retrain_request_model import RetrainPayload
from api.utils.model_loader import load_model
from models.feature_engineering import create_features
from config import Config
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime

# Şu anki tarih ve saat
now = datetime.now()

# Gün-Ay-Yıl formatında yazdırma
formatted_date = now.strftime("%d-%m-%Y")
print("Tarih:", formatted_date)

router = APIRouter()

@router.post("/retrain", tags=["Retrain"])
def retrain_model(payload: RetrainPayload):
    try:
        # 🔄 Yeni gelen veriyi DataFrame'e çevir
        df_new = pd.DataFrame([d.dict() for d in payload.data])
        df_new["order_date"] = pd.to_datetime(df_new[["year", "month", "day"]])
        df_new = df_new[["order_date", "product_id", "quantity"]]
        df_new["year"] = df_new["order_date"].dt.year
        df_new["month"] = df_new["order_date"].dt.month
        df_new["day"] = df_new["order_date"].dt.day

        # 📂 Eski veriyi yükle
        old_data_path = Config.PROJECT_ROOT / "src/data/processed/sales_forecasting_data.csv"
        df_old = pd.read_csv(old_data_path, parse_dates=["order_date"])

        # 🔗 Verileri birleştir
        df_combined = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates()
        df_combined["order_date"] = pd.to_datetime(df_combined["order_date"])
        df_combined["year"] = df_combined["order_date"].dt.year
        df_combined["month"] = df_combined["order_date"].dt.month
        df_combined["day"] = df_combined["order_date"].dt.day
        df_combined = df_combined.sort_values("order_date")

        # 🧠 Özellik mühendisliği
        features = create_features(df_combined, df_combined).fillna(0)

        # 🎯 Tahmin hedefi
        X = features.drop(columns=["quantity"], errors="ignore")
        y = df_combined.groupby(["product_id", "order_date"])["quantity"].sum().reset_index()["quantity"]
        print("X shape:", X.shape)
        print("y shape:", y.shape)
        print(features[["product_id", "year", "month", "day"]].head())
        print(y.head())
        print(features.describe())
        print(features.isnull().sum())

        # 📦 Eski modeli yükle
        model_path = Config.PROJECT_ROOT / "src/models/saved_models/sales_pipeline_model.pkl"
        last_model_path = Config.PROJECT_ROOT / f"src/models/saved_models/sales_pipeline_model_{formatted_date}.pkl"
        old_model = load_model(model_path)
        y_old_pred = old_model.predict(X)
        rmse_old = mean_squared_error(y, y_old_pred)

        # 🆕 Yeni modeli eğit
        new_model = LinearRegression()
        new_model.fit(X, y)
        y_new_pred = new_model.predict(X)
        rmse_new = mean_squared_error(y, y_new_pred)

        # 📌 Kıyasla ve kaydet
        if rmse_new <= rmse_old:
            joblib.dump(new_model, last_model_path)
            return {
                "message": "✅ Yeni model başarıyla eğitildi ve kaydedildi."
                # "rmse_old": rmse_old,
                # "rmse_new": rmse_new
            }
        else:
            return {
                "message": "⚠️ Yeni model eski modelden daha kötü. Eski model korunuyor."
                # "rmse_old": rmse_old,
                # "rmse_new": rmse_new
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model yeniden eğitilemedi: {str(e)}")
