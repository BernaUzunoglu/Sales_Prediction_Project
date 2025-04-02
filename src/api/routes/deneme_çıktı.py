import pandas as pd
import joblib
from models.feature_engineering import create_features

# Model ve veri yolları
model_path = "C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/models/saved_models/sales_pipeline_model.pkl"
data_path = "C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/sales_forecasting_data.csv"

# Modeli yükle
model = joblib.load(model_path)

# Geçmiş veriyi oku (create_features için gerekli)
ts_data = pd.read_csv(data_path, parse_dates=["order_date"])

# Tahmin edilecek giriş verisi
input_dict = {
    "product_id": 11,
    "year": 2024,
    "month": 4,
    "day": 1
}
input_df = pd.DataFrame([input_dict])

# Özellik mühendisliği uygula (eğer modelde yoksa)
try:
    features = create_features(input_df, ts_data)
except Exception as e:
    print("Feature engineering hatası:", str(e))
    exit()

# Tahmin yap
try:
    prediction = model.predict(features)[0]
    print(f"Tahmin edilen satış adedi: {prediction}")
except Exception as e:
    print("Tahmin yapılamadı:", str(e))
