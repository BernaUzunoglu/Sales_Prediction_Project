import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
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

# 5. Veriyi Eğitim ve Test Kümesine Ayır
X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)

# 6. KMeans Modelini Eğit
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(X_train)

# 7. Eğitim Kümesi Performansı
train_labels = kmeans.predict(X_train)
train_silhouette = silhouette_score(X_train, train_labels)
train_inertia = kmeans.inertia_

# 8. Test Kümesi Performansı
test_labels = kmeans.predict(X_test)
test_silhouette = silhouette_score(X_test, test_labels)
test_inertia = sum(
    ((X_test[i] - kmeans.cluster_centers_[test_labels[i]])**2).sum()
    for i in range(len(X_test))
)

print(f"✅ Train Silhouette Score: {train_silhouette:.4f}")
print(f"✅ Train Inertia: {train_inertia:.2f}")
print(f"✅ Test Silhouette Score: {test_silhouette:.4f}")
print(f"✅ Test Inertia: {test_inertia:.2f}")