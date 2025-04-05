# 📈 ML Tabanlı Satış Tahmin API'si

Makine öğrenmesi temelli bu proje, belirli ürünler için gelecekteki satış miktarlarını tahmin etmekte ve müşteri segmentlerini sınıflandırmaktadır. FastAPI kullanılarak geliştirilen bu RESTful API, ürün/satış verileri üzerinde analiz yapma ve tahmin üretme imkânı sunar.

---

## 🎯 Projenin Amacı

- Geçmiş verilere dayanarak **ürün satış tahmini yapmak**
- Müşteri davranışlarına göre **müşteri segmentasyonu gerçekleştirmek**
- API üzerinden **ürün ve satış özetlerine erişim sağlamak**

---

## ⚙️ Kurulum ve Çalıştırma

### 1. Bağımlılıkların Kurulumu

```bash
pip install -r requirements.txt
```

### 2. API'yi Başlatma

Proje dizininde aşağıdaki komutu çalıştırarak FastAPI sunucusunu başlatabilirsiniz:

```bash
uvicorn api.main:app --reload --app-dir src
```

### 3. Dokümantasyona Erişim

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📘 API Dokümantasyonu

API'nin tüm endpoint'lerine ait detaylı açıklamalar, örnek istek/yanıt yapıları ve hata yönetimi için [API Dokümantasyonu](./docs/api_documentation.md) dosyasını inceleyebilirsiniz.

---

## 🗂️ Proje Yapısı

```bash
📁 Detaylı klasör yapısı için bkz: [docs/PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md)
ı
```

---

## ✨ Özellikler

- 🔮 Satış tahmini (tarih & ürün bazlı)
- 👥 Müşteri segmentasyonu (harcama, alışveriş alışkanlığına göre)
- 📦 Ürün listesi & 📈 satış özeti endpoint'leri
- ✅ Swagger UI ve ReDoc arayüzleri ile görsel test imkânı

---

## 🛠️ Katkı

Pull request’ler ve issue’lar memnuniyetle karşılanır. Projeye katkıda bulunmak için fork'layabilir, geliştirme yaptıktan sonra gönderebilirsiniz.

---


