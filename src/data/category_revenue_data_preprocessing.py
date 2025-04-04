import pandas as pd
from sqlalchemy import text
from database import engine  # engine'i direkt import ediyoruz
import warnings
from config import Config

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
warnings.simplefilter(action="ignore")

def load_merged_data():
    """Orders, Order_Details ve Products tablolarını birleştir"""
    query = """
    SELECT c.category_id, c.category_name, SUM(od.unit_price * od.quantity) AS TotalRevenue
    FROM categories c
    JOIN products p ON c.category_id = p.category_id
    JOIN order_details od ON p.product_id = od.product_id
    JOIN orders o ON od.order_id = o.order_id
    GROUP BY c.category_id, c.category_name
    ORDER BY TotalRevenue DESC
    """
    with engine.connect() as conn:
        data = pd.read_sql(text(query), conn)
    return data

# Kullanım
df = load_merged_data()

df.to_csv(f"{Config.PROJECT_ROOT}src/data/processed/category_revenue.csv", index=False)



