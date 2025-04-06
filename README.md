
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

## 📚 Proje Dokümantasyonları (docs/ klasörü)

- [API Document](https://github.com/BernaUzunoglu/Sales_Prediction_Project/blob/main/docs/API.DOCS.md) → Tüm endpoint açıklamaları, örnek istek/yanıt yapıları, validasyon ve hata mesajları.
- [Data Dictionary](https://github.com/BernaUzunoglu/Sales_Prediction_Project/blob/main/docs/DATA_DICTIONARY.md) → Kullanılan tablolar ve  veri setlerindeki kolonlar, veri tipleri, açıklamalar ve modellerdeki feature-target alan tanımlamaları .
- [Arhitecture](https://github.com/BernaUzunoglu/Sales_Prediction_Project/blob/main/docs/ARCHITECTURE.md) → Projenin mimarisi, klasör yapısı, teknoloji yığını, veri akışı ve model mimarisi.
- [Project Structure](https://github.com/BernaUzunoglu/Sales_Prediction_Project/blob/main/docs/PROJECT_STRUCTURE.md) → Klasör ve dosya yapısının açıklaması (tree formatında).
- [Project Documentation](https://github.com/BernaUzunoglu/Sales_Prediction_Project/blob/main/docs/PROJECT_DOCUMENTATION.md) → Genel proje istek dökümantasyonu ve yapılacaklar listesi.

---

## ✨ Özellikler

- 🔮 **Satış Tahmini**: Kullanıcıdan alınan `product_id`, `year`, `month`, `day` girdilerine karşılık olarak model, geçmiş verilerden beslenen **zaman serisi özellikleri** ile birlikte satış tahmini üretir. Bu özellikler arasında `lag` değerleri, hareketli ortalamalar (`moving_avg`) ve kümülatif satışlar gibi veriler yer alır. 
    * Detaylar için bkz: [Data Dictionary – Feature Engineering](https://github.com/BernaUzunoglu/Sales_Prediction_Project/blob/main/docs/DATA_DICTIONARY.md#-sales_forecasting_datacsv).

- 👥 **Müşteri Segmentasyonu**: Müşteri özellikleri (`total_spent`, `num_orders`, `recency` vb.) kullanılarak müşteriler belirli segmentlere atanır (`segment_id`, `segment_name`). Bu işlem, müşteri davranış modellerinin anlaşılmasını sağlar. 
    * Kullanılan değişkenler için bkz: [Data Dictionary – Customer Features](https://github.com/BernaUzunoglu/Sales_Prediction_Project/blob/main/docs/DATA_DICTIONARY.md#-customer_featurescsv).

- 📦 **Ürün Listesi**: `/products` endpoint’i, sistemde kayıtlı ürünlerin listesini döner. Bu veriler Northwind veritabanındaki `Products` tablosundan elde edilir.

- 📈 **Satış Özeti**: `/sales_summary` endpoint’i, ürün bazlı toplam satış miktarlarını döner. Bu bilgiler, `order_details` üzerinden türetilmiş toplam satışlara dayanmaktadır.

- ✅ **Swagger UI ve ReDoc**: API testlerini hızlı ve görsel şekilde yapabileceğiniz arayüzler sunar.


---

## 🐳 Docker ile Çalıştırma (Alternatif Yöntem)

Bu projeyi Docker ile izole bir ortamda kolayca çalıştırabilirsiniz.

### 1. Docker Image Oluştur

Proje dizininde terminal açarak:

```bash
docker build -t sales-predict-api .
```
Bu komut, Dockerfile'daki talimatlara göre bir image oluşturur.

### 2. Docker Container Başlat
```bash
docker run -p 8000:8000 sales-predict-api
```
Bu komut, image'ı bir container olarak başlatır ve localhost:8000 üzerinden API'ye erişmenizi sağlar.

- Eğer `Docker Desktop` GUI kullanıyorsan, **"Run" ederken portları manuel olarak ekle**:  
  - Host port: `8000`  
  - Container port: `8000`


- Tarayıcıda `http://0.0.0.0:8000` çalışmaz, **doğru adres `http://localhost:8000` veya `127.0.0.1:8000`**'dir.


---

### ⚠️ Unutma!

- `.env` ve `.env.docker`dosyalarını  unutma! 
- `.env.example` ve `.env.docker.example` dosyalarını örnek alarak bu dosyaları( `.env` , `.env.docker`) oluştur.


---

## 🛠️ Katkı

Pull request’ler ve issue’lar memnuniyetle karşılanır. Projeye katkıda bulunmak için fork'layabilir, geliştirme yaptıktan sonra gönderebilirsiniz.
