import pandas as pd
from sqlalchemy import text
from data.database import engine  # engine'i direkt import ediyoruz
from config import Config


def load_merged_data():
    """Orders, Order_Details ve Products tablolarını birleştir"""
    query = """
    SELECT 
    o.order_date,
    od.product_id,
    SUM(od.quantity) AS quantity,
    SUM(od.quantity * od.unit_price) AS total_sales
FROM 
    orders o
JOIN 
    order_details od ON o.order_id = od.order_id
GROUP BY 
    o.order_date, od.product_id
ORDER BY 
    o.order_date, od.product_id
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

# Kullanım
df = load_merged_data()

df.to_csv(Config.PROJECT_ROOT / "src/data/processed/sales_forecasting_data.csv", index=False)

