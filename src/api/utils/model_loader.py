# Model Yükleme Fonksiyonu
# Modeli .pkl veya .joblib dosyasından yükler.
import joblib

# Modeli yükle
def load_model(model_path: str):
    model = joblib.load(model_path)
    return model
