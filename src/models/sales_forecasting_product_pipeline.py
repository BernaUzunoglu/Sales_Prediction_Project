import pandas as pd
import numpy as np
import os
import joblib
import json
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from config import Config
# create_features fonksiyonunu modülden al
from models.feature_engineering import create_features

# CSV yolunu tanımla
file_path = Config.PROJECT_ROOT / "src/data/processed/sales_forecasting_data.csv"


# Veri setini oku
df = pd.read_csv(file_path, parse_dates=["order_date"])

# order_date özelliklerini çıkart
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['day'] = df['order_date'].dt.day

# ts_data oluştur: aggregate edilmiş, tarih ve ürün bazlı satış verisi
ts_data = df.groupby(['order_date', 'product_id'])['quantity'].sum().reset_index()
ts_data['order_date'] = pd.to_datetime(ts_data['order_date'])
ts_data['year'] = ts_data['order_date'].dt.year
ts_data['month'] = ts_data['order_date'].dt.month
ts_data['day'] = ts_data['order_date'].dt.day

trained_product_ids = ts_data['product_id'].unique().tolist()

# Kaydet
with open(Config.PROJECT_ROOT / "src/models/model_results/trained_product_ids.json", "w") as f:
    json.dump(trained_product_ids, f)

# Sadece kullanıcıdan alınabilecek sütunlar: (model bu inputla çalışacak)
X_raw = ts_data[['product_id', 'year', 'month', 'day']].copy()
y = ts_data['quantity'].copy()

pipeline = Pipeline([
    ("feature_engineering", FunctionTransformer(create_features,
                                                kw_args={"ts_data": ts_data},
                                                validate=False)),
    ("model", LinearRegression())
])

# Modeli eğit
pipeline.fit(X_raw, y)

# Modeli Kaydetmek İçin Yol Belirle
model_dir = "saved_models"
os.makedirs(model_dir, exist_ok=True)

# Modeli Kaydet
model_path = os.path.join(model_dir, "sales_pipeline_model.pkl")
joblib.dump(pipeline, model_path)

print(f"✅ Pipeline içeren model kaydedildi: {model_path}")
