import pandas as pd
from datetime import timedelta
from config import Config

# 1. CSV'den veriyi oku
file_path = f"{Config.PROJECT_ROOT}src/data/processed/customer_data.csv"
df = pd.read_csv(file_path, parse_dates=["order_date"])

# 2. Referans tarih: verideki en son sipariş tarihi + 1 gün
reference_date = df["order_date"].max() + timedelta(days=1)

# 3. Müşteri bazlı davranışsal öznitelikleri üret
customer_features = df.groupby("customer_id").agg(
    total_spent=("total_price", "sum"),                      # Toplam harcama
    num_orders=("order_id", pd.Series.nunique),              # Sipariş sayısı
    avg_order_value=("total_price", "mean"),                 # Ortalama sipariş tutarı
    num_products=("product_id", pd.Series.nunique),          # Farklı ürün sayısı
    last_order_date=("order_date", "max"),                   # En son sipariş tarihi
    country=("country", "first"),                            # Ülke
    city=("city", "first")                                   # Şehir
).reset_index()

# 4. Recency (en son siparişten itibaren geçen gün sayısı)
customer_features["recency"] = (reference_date - customer_features["last_order_date"]).dt.days

# 5. Analize dahil edilmeyecek kolonları çıkar
customer_features.drop(columns=["last_order_date"], inplace=True)

# 6. Dosyaya yaz (isteğe bağlı)
output_path = f"{Config.PROJECT_ROOT}src/data/processed/customer_features.csv"
customer_features.to_csv(output_path, index=False)
print(f"✅ Özellikler başarıyla kaydedildi: {output_path}")
