import pandas as pd
from sqlalchemy import text
from data.database import engine
from config import Config

def load_merged_data():
    query = """
    SELECT 
    c.customer_id,
    c.company_name,
    c.country,
    c.city,
    o.order_id,
    o.order_date,
    od.product_id,
    od.unit_price,
    od.quantity,
    od.discount,
    (od.unit_price * od.quantity * (1 - od.discount)) AS total_price
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_details od ON o.order_id = od.order_id
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

# Kullanım
df = load_merged_data()

df.to_csv(f"{Config.PROJECT_ROOT}src/data/processed/customer_data.csv", index=False)


