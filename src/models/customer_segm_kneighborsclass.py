import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report, silhouette_score, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
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

# 4. Segment (KMeans) - Ground truth gibi
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["segment"] = kmeans.fit_predict(X_scaled)

# 5. Elbow Yöntemiyle K seçimi
k_range = range(2, 11)
accuracy_scores = []

for k in k_range:
    model = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(model, X_scaled, df["segment"], cv=5, scoring='accuracy')
    accuracy_scores.append(scores.mean())

best_k = k_range[accuracy_scores.index(max(accuracy_scores))]
print(f"📌 En iyi K değeri: {best_k}")

# Elbow Grafiği
plt.figure(figsize=(8, 5))
plt.plot(k_range, accuracy_scores, marker='o')
plt.title("Elbow Method for K (KNN vs Segment)")
plt.xlabel("K (n_neighbors)")
plt.ylabel("Cross-Validated Accuracy")
plt.grid(True)
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/customer_knn_elbow_plot.png")
plt.close()

# 6. Eğitim / Test Bölme
X_train, X_test, y_train, y_test = train_test_split(X_scaled, df["segment"], test_size=0.2, random_state=42)

# 7. Model Eğitimi
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)

# 8. Doğruluk ve Raporlama
y_train_pred = knn.predict(X_train)
y_test_pred = knn.predict(X_test)

train_acc = accuracy_score(y_train, y_train_pred)
test_acc = accuracy_score(y_test, y_test_pred)

print(f"✅ Train Accuracy: {train_acc:.4f}")
print(f"✅ Test Accuracy: {test_acc:.4f}")
print("🔍 Sınıflandırma Raporu:\n", classification_report(y_test, y_test_pred))

# Doğruluk Görselleştirme
plt.figure(figsize=(6, 4))
plt.bar(["Train", "Test"], [train_acc, test_acc], color=["skyblue", "lightgreen"])
plt.ylim(0, 1)
plt.title("Train vs Test Accuracy")
plt.ylabel("Accuracy")
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/train_test_knn_accuracy_comparison.png")
plt.close()

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("KNN Confusion Matrix")
plt.savefig(Config.PROJECT_ROOT / "src/models/model_reports/graphics/knn_confusion_matrix.png")
plt.close()

# 9. Model Kaydetme
pipeline = {"model": knn, "scaler": scaler}
joblib.dump(pipeline, Config.PROJECT_ROOT / "src/models/saved_models/customer_knn_model.pkl")

# 10. Yeni Müşteri Tahmini
new_customer = pd.DataFrame([{
    "total_spent": 2500,
    "num_orders": 8,
    "avg_order_value": 312.5,
    "num_products": 5,
    "recency": 15
}])
new_scaled = scaler.transform(new_customer)
segment = knn.predict(new_scaled)[0]
print(f"🎯 Yeni müşteri segmenti: {segment}")

# 11. Segmentli Veriyi Kaydet
df.to_csv(Config.PROJECT_ROOT / "src/models/model_results/customer_knn_segments.csv", index=False)
