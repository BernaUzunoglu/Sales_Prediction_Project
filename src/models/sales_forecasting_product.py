# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from config import Config
import joblib
import os

# Load the sales data
file_path = f"{Config.PROJECT_ROOT}src/data/processed/sales_forecasting_data.csv"
df = pd.read_csv(file_path, parse_dates=['order_date'])

# Aggregate data by order_date and product_id to get daily total quantity
ts_data = df.groupby(['order_date', 'product_id'])['quantity'].sum().reset_index()
ts_data['order_date'] = pd.to_datetime(ts_data['order_date'])

# Feature engineering: extract date features
ts_data['year'] = ts_data['order_date'].dt.year
ts_data['month'] = ts_data['order_date'].dt.month
ts_data['day'] = ts_data['order_date'].dt.day
ts_data['dayofweek'] = ts_data['order_date'].dt.dayofweek
ts_data['dayofyear'] = ts_data['order_date'].dt.dayofyear

# Create lag features for previous days for better prediction (last 14 days sales data)
for lag in range(1, 15):
    ts_data[f'lag_{lag}'] = ts_data.groupby('product_id')['quantity'].shift(lag).fillna(0)

# Create moving average features
ts_data['moving_avg_7'] = ts_data.groupby('product_id')['quantity'].transform(lambda x: x.rolling(window=7).mean().fillna(0))
ts_data['moving_avg_14'] = ts_data.groupby('product_id')['quantity'].transform(lambda x: x.rolling(window=14).mean().fillna(0))
ts_data['exp_moving_avg_7'] = ts_data.groupby('product_id')['quantity'].transform(lambda x: x.ewm(span=7, adjust=False).mean())

# Add cumulative sales and average sales per day
ts_data['cumulative_sales'] = ts_data.groupby('product_id')['quantity'].cumsum()
ts_data['avg_sales_per_day'] = ts_data['cumulative_sales'] / (ts_data.index + 1)

# Define features and target
X = ts_data.drop(columns=['order_date', 'quantity'])
y = ts_data['quantity']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

# Initialize models
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
xgb_model = XGBRegressor(n_estimators=100, random_state=42)
lr_model = LinearRegression()

# Fit models
rf_model.fit(X_train, y_train)
xgb_model.fit(X_train, y_train)
lr_model.fit(X_train, y_train)

# Save the best model (choose the one with lowest RMSE)
models = {'random_forest': rf_model, 'xgboost': xgb_model, 'linear_regression': lr_model}
best_model_name = 'linear_regression'  # En iyi model olarak Linear seçtik (daha sonra değişebilir)

# En iyi modeli kaydet
# Modeli Kaydetmek İçin Yol Belirle
model_dir = "saved_models"
os.makedirs(model_dir, exist_ok=True)

# Modeli Kaydet
model_path = os.path.join(model_dir, "sales_model.pkl")
joblib.dump(models[best_model_name], model_path)
print(f"Model saved to {model_path}")

# Model Performansını Test Etme
predictions = models[best_model_name].predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"Best Model Test RMSE: {rmse}")

# Save the predictions to a CSV
predictions_df = pd.DataFrame({
    'actual_quantity': y_test.values,
    'predicted_quantity': predictions
})
predictions_df.to_csv('model_results/ml_sales_forecast_results.csv', index=False)
print('Prediction results saved to ml_sales_forecast_results.csv')
