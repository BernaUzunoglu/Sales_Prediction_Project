import pandas as pd
import numpy as np
import sqlite3  # Veritabanı bağlantısı için
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Veriyi Yükleme
data = pd.read_csv("C:/Users/BERNA/OneDrive/Masaüstü/Turkcell/ML_Based_Sales_Prediction_API_Project/src/data/processed/category_revenue.csv")


# 2️⃣ Özellik mühendisliği (Feature Engineering)
data['category_id'] = data['category_id'].astype(int)
data['totalrevenue'] = data['totalrevenue'].astype(float)

# 3️⃣ Bağımsız ve bağımlı değişkenleri ayır
X = data[['category_id']]
y = data['totalrevenue']

# Veriyi eğitim ve test setlerine böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4️⃣ Modeli eğit
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5️⃣ Modeli değerlendirme
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"MAE: {mae}")
print(f"RMSE: {rmse}")

# 6️⃣ Yeni tahmin yapma (Örnek kategori ID = 5 için)
kategori_5 = np.array([[5]])
predicted_revenue = model.predict(kategori_5)
print(f"Tahmini Gelir (Kategori 5): {predicted_revenue[0]}")
