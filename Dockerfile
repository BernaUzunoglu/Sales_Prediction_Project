# Python imajı
FROM python:3.11-slim

# Ortam ayarları
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Çalışma dizini
WORKDIR /app

# Sistem kütüphaneleri
RUN apt-get update && apt-get install -y gcc libpq-dev git

# Gerekli dosyaları kopyala
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# 🌱 .env dosyasını .env.docker'dan oluştur
COPY .env.docker .env

# 📦 Tüm proje dosyalarını kopyala
COPY . .

# PYTHONPATH ve proje kökü
ENV PYTHONPATH=/app/src
ENV PROJECT_ROOT=/app/

# Uvicorn ile API başlat
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
