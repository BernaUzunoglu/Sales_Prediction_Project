import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report, silhouette_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix
from config import Config

import joblib

# 1. Veri Yükleme
file_path = Config.PROJECT_ROOT / "src/data/processed/customer_features.csv"
df = pd.read_csv(file_path)

# 2. Sayısal Özellikler
numerical_cols = ["total_spent", "num_orders", "avg_order_value", "num_products", "recency"]
X = df[numerical_cols]

# 3. Normalizasyon
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Kümeleme için KMeans Modeli ile Segmentasyon Yap
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["segment"] = kmeans.fit_predict(X_scaled)

# 4. Küme Sayısını Belirleme (Elbow Yöntemi)
inertia = []
silhouette_scores = []
k_range = range(2, 11)  # Küme sayısını 2-10 arasında test edelim

for k in k_range:
    model = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(model, X_scaled, df["segment"], cv=5, scoring='accuracy')
    inertia.append(scores.mean())  # KNN için inertia yerine accuracy alıyoruz
    silhouette_scores.append(scores.mean())

# En iyi K değerini belirleme
best_k = k_range[silhouette_scores.index(max(silhouette_scores))]
print(f"📌 En iyi K değeri: {best_k}")

# Elbow grafiği
plt.figure(figsize=(8, 5))
plt.plot(k_range, inertia, marker='o')
plt.title("Elbow Method - Optimal K")
plt.xlabel("K Değeri")
plt.ylabel("Ortalama Doğruluk")
plt.grid(True)
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/customer_knn_elbow_plot.png")
plt.close()

# 5. Veriyi Eğitim ve Test Kümesine Ayırma
X_train, X_test, y_train, y_test = train_test_split(X_scaled, df["segment"], test_size=0.2, random_state=42)

# 6. KNN Modeli ile Eğitme
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)

# 7. Model Doğruluk Testi
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Doğruluk Skoru: {accuracy:.4f}")
print("🔍 Sınıflandırma Raporu:\n", classification_report(y_test, y_pred))

# 8. Confusion Matrix Görselleştirme

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, cmap="Blues", fmt="d")
plt.xlabel("Tahmin Edilen")
plt.ylabel("Gerçek")
plt.title("Confusion Matrix")
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/knn_confusion_matrix.png")
plt.close()

# 9. Model Kaydetme
knn_pipeline = {
    "model": knn,
    "scaler": scaler
}
model_path = Config.PROJECT_ROOT / "src/models/saved_models/customer_knn_model.pkl"
joblib.dump(knn_pipeline, model_path)
print(f"✅ KNN Modeli kaydedildi: {model_path}")

# 10. Yeni Müşteri İçin Tahmin
new_customer = pd.DataFrame([{
    "total_spent": 2500,
    "num_orders": 8,
    "avg_order_value": 312.5,
    "num_products": 5,
    "recency": 15
}])
new_scaled = scaler.transform(new_customer)
predicted_segment = knn.predict(new_scaled)[0]
print(f"🎯 Yeni müşteri segmenti: {predicted_segment}")

# 11. Segmentli Veri Kaydetme
csv_path = Config.PROJECT_ROOT / "src/models/model_results/customer_knn_segments.csv"
df.to_csv(csv_path, index=False)
print(f"✅ Segmentli veri kaydedildi: {csv_path}")
