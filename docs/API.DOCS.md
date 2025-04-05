# 📘 ML Based Sales Prediction API Dokümantasyonu

## ⚖️ API Başlatma Komutu
```bash
uvicorn api.main:app --reload --app-dir src
```

---

## 🔧 Genel Bilgiler

| Alan        | Açıklama                           |
|-------------|------------------------------------|
| Base URL    | `http://127.0.0.1:8000`            |
| Framework   | FastAPI                           |
| Swagger UI  | `http://127.0.0.1:8000/docs`       |
| ReDoc       | `http://127.0.0.1:8000/redoc`      |

---

## 📌 Endpoint Rehberi

### 1. `/health` ✅
- **Method**: `GET`
- **Amaç**: API'nin çalışıp çalışmadığını test eder.
- **Response**:
```json
{
  "status": "API is running smoothly!"
}
```

---

### 2. `/products` 📦
- **Method**: `GET`
- **Amaç**: Veritabanındaki ürün listesini döner.
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

### 3. `/predict` 🔮 – Satış Tahmini
- **Method**: `POST`
- **Amaç**: Belirli bir ürün ve tarih için satış miktarı tahminler.

#### 🔸 Request Body – `PredictRequest`
| Alan       | Tip     | Açıklama                        |
|------------|---------|---------------------------------|
| product_id | int     | Ürünün ID’si                    |
| year       | int     | Tahmin yapılacak yıl            |
| month      | int     | Tahmin yapılacak ay (1-12)      |
| day        | int     | Tahmin yapılacak gün (1-31)     |

```json
{
  "product_id": 11,
  "year": 2024,
  "month": 4,
  "day": 1
}
```

#### 🔹 Response – `PredictResponse`
| Alan               | Tip     | Açıklama                    |
|--------------------|---------|-----------------------------|
| product_id         | int     | Ürün ID'si                 |
| predicted_quantity | float   | Tahmin edilen satış miktarı|

```json
{
  "product_id": 11,
  "predicted_quantity": 12.35
}
```

---

### 4. `/sales_summary` 📈
- **Method**: `GET`
- **Amaç**: Ürün bazlı toplam satış özetini döner.
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

---

### 5. `/predict-segment` 👥 – Müşteri Segment Tahmini
- **Method**: `POST`
- **Amaç**: Müşteri özelliklerine göre segment belirler.

#### 🔸 Request Body – `CustomerSegmentRequest`
| Alan             | Tip    | Açıklama                             |
|------------------|--------|--------------------------------------|
| total_spent      | float  | Müşterinin toplam harcaması          |
| num_orders       | int    | Toplam sipariş sayısı                |
| avg_order_value  | float  | Ortalama sipariş tutarı              |
| num_products     | int    | Alınan toplam ürün sayısı            |
| recency          | float  | Son siparişten bu yana geçen gün     |

```json
{
  "total_spent": 52000,
  "num_orders": 32,
  "avg_order_value": 650,
  "num_products": 40,
  "recency": 5
}
```

#### 🔹 Response – `CustomerSegmentResponse`
| Alan         | Tip     | Açıklama                     |
|--------------|---------|------------------------------|
| segment_id   | int     | Segmentin ID’si              |
| segment_name | string  | Açıklayıcı segment ismi      |

```json
{
  "segment_id": 2,
  "segment_name": "Champions"
}
```

---

## 📊 Segment Açıklamaları

| Segment ID | Segment İsmi        | Açıklama                                                                  |
|------------|---------------------|---------------------------------------------------------------------------|
| 0          | Unengaged           | Düşük harcama, eski siparişler, kampanya hedefli kullanıcı                 |
| 1          | Potential Loyalists | Sadık müşteriye dönüşebilecek potansiyel müşteriler                        |
| 2          | Champions           | En iyi müşteriler – sık alışveriş, yüksek harcama                          |
| 3          | Regulars            | Ortalama seviyede düzenli alışveriş yapanlar                              |

---

## ⚠️ Hatalı İstek & Validasyon Mesajları

### 🔸 Genel Hata Formatı
```json
{
  "detail": "Tahmin yapılamadı: some error message"
}
```

### 🔹 Validasyon Hataları (Örnek)
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

## 📬 Genel Response Yapısı

| Alan      | Tip     | Açıklama                                         |
|-----------|---------|--------------------------------------------------|
| success   | boolean | İşlem başarılı mı (`true`/`false`)               |
| code      | int     | `0`: başarılı, diğerleri: hata kodları           |
| message   | string  | Açıklayıcı mesaj                                 |
| data      | object  | İlgili endpoint’in döndürdüğü veri               |

