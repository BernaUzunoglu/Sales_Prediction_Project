# 📘 ML Based Sales Prediction API Dokümantasyonu

API ayağa kaldıralım : uvicorn api.main:app --reload --app-dir src

## 🔧 Temel Bilgiler

| Alan        | Açıklama                                        |
|-------------|-------------------------------------------------|
| Base URL    | `http://127.0.0.1:8000`                         |
| API Formatı | RESTful JSON API                               |
| Framework   | FastAPI                                         |
| Swagger UI  | `http://127.0.0.1:8000/docs`                   |
| Redoc       | `http://127.0.0.1:8000/redoc`                  |

---

## 📌 Endpoint Listesi

### 1. `/health` – API Sağlık Kontrolü ✅

- **Method**: `GET`
- **Amaç**: API ayakta mı test etmek.
- **Response**:

```json
{
  "status": "API is running smoothly!"
}
```

---

### 2. `/products` – Ürün Listesi 📦

- **Method**: `GET`
- **Amaç**: Veritabanındaki ürünleri listeler.
- **Response**:

```json
[
  {
    "id": 1,
    "name": "Chai"
  },
  {
    "id": 2,
    "name": "Chang"
  }
]
```

---

### 3. `/predict` – Satış Tahmini 🔮

- **Method**: `POST`
- **Amaç**: Belirli bir ürün ve tarihe göre satış tahmini yapar.
- **Request Body**:

```json
{
  "product_id": 11,
  "year": 2024,
  "month": 4,
  "day": 1
}
```

- **Response**:

```json
{
  "product_id": 11,
  "predicted_quantity": 12.35
}
```

---

### 4. `/sales_summary` – Satış Özeti 📈

- **Method**: `GET`
- **Amaç**: Ürün bazlı toplam satış miktarlarını getirir.
- **Response**:

```json
[
  {
    "product_name": "Chai",
    "total_quantity": 350
  },
  {
    "product_name": "Chang",
    "total_quantity": 270
  }
]
```
### 5. `/predict-segment` – Müşteri Segmenti

## 🎯 Açıklama
Verilen müşteri özelliklerine göre hangi **müşteri segmentine** ait olduğunu tahmin eder. K-Means temelli segmentasyon modeli ile çalışır. Bu API, müşterilerin davranışlarına göre anlamlı gruplara ayrılmasını sağlar.

---

## 🧾 Gönderilecek JSON (Request Body)

```json
{
  "total_spent": 2500,
  "num_orders": 8,
  "avg_order_value": 312.5,
  "num_products": 5,
  "recency": 15
}
```

| Alan Adı        | Tipi    | Açıklama                            |
|-----------------|---------|-------------------------------------|
| total_spent     | float   | Müşterinin toplam harcaması         |
| num_orders      | int     | Toplam sipariş sayısı               |
| avg_order_value | float   | Ortalama sipariş tutarı             |
| num_products    | int     | Toplam alınan ürün sayısı           |
| recency         | float   | Son siparişten bu yana geçen gün    |

---

## ✅ Başarılı Yanıt (Response)

```json
{
  "segment_id": 3,
  "segment_name": "Regulars"
}
```

---

## ⚠️ Hatalı Yanıt (Örnek)

```json
{
  "detail": "Tahmin yapılamadı: some error message"
}
```

---

## 📊 Segment Açıklamaları

| Segment ID | Segment İsmi        | Açıklama                                                                 |
|------------|---------------------|--------------------------------------------------------------------------|
| 0          | Unengaged           | Düşük harcama, eski siparişler. Etkileşimi düşük, kampanyaya uygun.     |
| 1          | Potential Loyalists | Orta-üst seviye harcama, sadık hale getirilebilecek potansiyel müşteriler.|
| 2          | Champions           | En yüksek değerli müşteriler. Sık alışveriş, yüksek harcama.            |
| 3          | Regulars            | Orta düzey alışveriş yapan düzenli müşteriler.                          |

---

## 🧪 Test İçin Örnek Değerler (Swagger / Postman)

```json
{
  "total_spent": 52000,
  "num_orders": 32,
  "avg_order_value": 650,
  "num_products": 40,
  "recency": 5
}
```

Beklenen segment: `Champions`

---

## 💡 Ekstra
- Model: `KMeans` (4 segmentli)
- Doğrulama: `MinMaxScaler` ile normalize edildi
- Skor: Silhouette Score ≈ `0.44`

---

## ✅ Validasyon & Hata Yönetimi

### Örnek Hatalı İstek:

```json
{
  "product_id": "abc",
  "year": 2024,
  "month": 13,
  "day": 32
}
```

**Dönüş**:

```json
{
  "detail": [
    {
      "loc": ["body", "product_id"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

---

## 🔬 Postman Test Örnekleri

- **URL**: `http://127.0.0.1:8000/predict`
- **Method**: `POST`
- **Body → raw → JSON**:

```json
{
  "product_id": 11,
  "year": 2024,
  "month": 4,
  "day": 1
}
```

---




