# Model Yükleme Fonksiyonu
# Modeli .pkl veya .joblib dosyasından yükler.
import joblib
import sys
import os

# src klasörünün üst dizinini import yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# Modeli yükle
def load_model(model_path: str):
    model = joblib.load(str(model_path))
    return model
