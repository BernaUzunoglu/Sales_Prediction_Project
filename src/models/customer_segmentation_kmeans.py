import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from config import Config
import joblib

# 1. Veri Yükleme
file_path = Config.PROJECT_ROOT / "src/data/processed/customer_features.csv"
df = pd.read_csv(file_path)

# 2. Sayısal Özellikler
numerical_cols = [
    "total_spent",
    "num_orders",
    "avg_order_value",
    "num_products",
    "recency"
]
X = df[numerical_cols]

# 3. Normalizasyon
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 4. Elbow Yöntemi ile K değeri analizi
inertia = []
for k in range(1, 11):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    inertia.append(model.inertia_)

# Elbow grafiği
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertia, marker='o')
plt.title("Elbow Method - Optimal K")
plt.xlabel("Küme Sayısı (k)")
plt.ylabel("Inertia")
plt.grid(True)
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/customer_knn_elbow_plot.png")
plt.close()

# 5. K-Means (k=4 ile)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["segment"] = kmeans.fit_predict(X_scaled)

# 6. Model Kalite Değeri
# Inertia (İçsel Hata) - modelin tahmin ettiği her bir küme için verilerin merkezine olan uzaklığın toplamını ifade eder.
print("Inertia:", kmeans.inertia_)

# Silhouette skoru, her bir örneğin kendi kümesiyle ne kadar uyumlu olduğunu ve diğer kümelerden ne kadar farklı olduğunu ölçen bir metriktir.
silhouette = silhouette_score(X_scaled, df["segment"])
print(f"✅ Silhouette Score: {silhouette:.4f}")

# 7. Segment Özeti
segment_summary = df.groupby("segment")[numerical_cols].mean().round(2)
segment_summary["customer_count"] = df["segment"].value_counts().sort_index()
print("🔎 Segment Özeti:\n", segment_summary)

# 8. Görsel Segment Analizi
plt.figure(figsize=(12, 10))
for i, col in enumerate(numerical_cols):
    plt.subplot(3, 2, i+1)
    sns.barplot(data=df, x="segment", y=col, palette="Set2")
    plt.title(f"{col} by Segment")
    plt.xlabel("Segment")
    plt.ylabel(col)
plt.tight_layout()
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/segment_features.png")
plt.close()

# 9. Segment İsimlendirme
segment_map = {
    0: "Unengaged",
    1: "Potential Loyalists",
    2: "Champions",
    3: "Regulars"
}
df["segment_name"] = df["segment"].map(segment_map)

# Modeli, scaler'ı ve segment haritasını tek dosyada sakla
segment_pipeline = {
    "model": kmeans,
    "scaler": scaler,
    "segment_map": segment_map
}

# Kaydetme yolu
model_path = Config.PROJECT_ROOT / "src/models/saved_models/customer_segmentation_pipeline.pkl"
joblib.dump(segment_pipeline, model_path)

print(f"✅ Segmentasyon modeli kaydedildi: {model_path}")

# 10. Tahmin için örnek müşteri
new_customer = pd.DataFrame([{
    "total_spent": 2500,
    "num_orders": 8,
    "avg_order_value": 312.5,
    "num_products": 5,
    "recency": 15
}])
new_scaled = scaler.transform(new_customer)
predicted_segment = kmeans.predict(new_scaled)[0]
print(f"🎯 Yeni müşteri segmenti: {segment_map[predicted_segment]}")

# 11. Segmentli veri kaydet
csv_path = Config.PROJECT_ROOT / "src/models/model_results/customer_segments.csv"
df.to_csv(csv_path, index=False)
print(f"✅ Segmentli veri kaydedildi: {csv_path}")
