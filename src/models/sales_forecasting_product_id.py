# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from config import Config

# Load the sales data
file_path = Config.PROJECT_ROOT / "src/data/processed/sales_forecasting_data.csv"
# csv dosyasını okurken date kolonunu datetime parse ederek ekleyelim.
df = pd.read_csv(file_path, parse_dates=['order_date'])

# Select a specific product for forecasting (e.g., product_id = 11)
product_id = 11
product_df = df[df['product_id'] == product_id]

# Aggregate data by order_date to get daily total quantity
# he günü ayrı bir grup yapalım.
ts_data = product_df.groupby('order_date')['quantity'].sum().asfreq('D', fill_value=0)
ts_data = ts_data.reset_index()
ts_data['order_date'] = pd.to_datetime(ts_data['order_date'])

# Feature engineering: extract date features
ts_data['year'] = ts_data['order_date'].dt.year
ts_data['month'] = ts_data['order_date'].dt.month
ts_data['day'] = ts_data['order_date'].dt.day
ts_data['dayofweek'] = ts_data['order_date'].dt.dayofweek
ts_data['dayofyear'] = ts_data['order_date'].dt.dayofyear

# Create lag features for previous days for better prediction(last 14 dyas sales data)
for lag in range(1, 15):
    ts_data[f'lag_{lag}'] = ts_data['quantity'].shift(lag).fillna(0)

# Create moving average features
# rolling(window=7) → last 7 day data
ts_data['moving_avg_7'] = ts_data['quantity'].rolling(window=7).mean().fillna(0)
ts_data['moving_avg_14'] = ts_data['quantity'].rolling(window=14).mean().fillna(0)
# .ewm(span=7, adjust=False) → 7 days EMA calculate -  (Exponential Moving Average, EMA)
ts_data['exp_moving_avg_7'] = ts_data['quantity'].ewm(span=7, adjust=False).mean()

# Add cumulative sales and average sales per day
# Gün geçtikçe birikmiş toplam satış miktarını elde edelim.
ts_data['cumulative_sales'] = ts_data['quantity'].cumsum()
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

# Make predictions
rf_pred = rf_model.predict(X_test)
xgb_pred = xgb_model.predict(X_test)
lr_pred = lr_model.predict(X_test)

# Evaluate models
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))

print(f'Random Forest RMSE: {rf_rmse}')
print(f'XGBoost RMSE: {xgb_rmse}')
print(f'Linear Regression RMSE: {lr_rmse}')

# Random Forest Train RMSE
train_pred_rf = rf_model.predict(X_train)
train_rmse_rf = np.sqrt(mean_squared_error(y_train, train_pred_rf))
print(f'Random Forest Train RMSE: {train_rmse_rf}')

# Random Forest Cross-Validation RMSE
cv_scores_rf = cross_val_score(rf_model, X, y, cv=5, scoring='neg_mean_squared_error')
cv_rmse_rf = np.sqrt(-cv_scores_rf)
print(f'Random Forest Cross-Validation RMSE: {cv_rmse_rf.mean()}')

# XGBoost Train RMSE
train_pred_xgb = xgb_model.predict(X_train)
train_rmse_xgb = np.sqrt(mean_squared_error(y_train, train_pred_xgb))
print(f'XGBoost Train RMSE: {train_rmse_xgb}')

# XGBoost Cross-Validation RMSE
# cv_scores_xgb = cross_val_score(xgb_model, X, y, cv=5, scoring='neg_mean_squared_error')
# cv_rmse_xgb = np.sqrt(-cv_scores_xgb)
# print(f'XGBoost Cross-Validation RMSE: {cv_rmse_xgb.mean()}')


# Linear Regression Train RMSE
train_pred_lr = lr_model.predict(X_train)
train_rmse_lr = np.sqrt(mean_squared_error(y_train, train_pred_lr))
print(f'Linear Regression Train RMSE: {train_rmse_lr}')

# Linear Regression Cross-Validation RMSE
cv_scores_lr = cross_val_score(lr_model, X, y, cv=5, scoring='neg_mean_squared_error')
cv_rmse_lr = np.sqrt(-cv_scores_lr)
print(f'Linear Regression Cross-Validation RMSE: {cv_rmse_lr.mean()}')


# Plot actual vs predicted values
plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label='Actual Data', color='blue')
plt.plot(rf_pred, label='Random Forest Prediction', color='green')
plt.plot(xgb_pred, label='XGBoost Prediction', color='orange')
plt.plot(lr_pred, label='Linear Regression Prediction', color='red')
plt.title(f'Sales Forecast for Product {product_id} - Model Comparison')
plt.xlabel('Time')
plt.ylabel('Quantity Sold')
plt.legend()
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/sales_forcasting_model_result.png")
plt.show()


# Plot Train vs Test RMSE using Line Plot
train_errors = [train_rmse_lr, np.sqrt(mean_squared_error(y_train, rf_model.predict(X_train))), np.sqrt(mean_squared_error(y_train, xgb_model.predict(X_train)))]
test_errors = [lr_rmse, rf_rmse, xgb_rmse]

plt.figure(figsize=(10, 6))
model_names = ['Linear Regression', 'Random Forest', 'XGBoost']
plt.plot(model_names, train_errors, marker='o', linestyle='-', label='Train RMSE', color='blue')
plt.plot(model_names, test_errors, marker='o', linestyle='--', label='Test RMSE', color='orange')
plt.title('Train vs Test RMSE Comparison')
plt.ylabel('RMSE')
plt.xlabel('Model Name')
plt.legend()
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/sales_forcasting_train_test_rmse.png")
plt.show()

# Save the predictions to a CSV
predictions_df = pd.DataFrame({
    'actual_quantity': y_test.values,
    'rf_predicted': rf_pred,
    'xgb_predicted': xgb_pred,
    'lr_predicted': lr_pred
})
predictions_df.to_csv('model_results/ml_sales_forecast_results.csv', index=False)
print('Prediction results saved to ml_sales_forecast_results.csv')
