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

## 🚀 Swagger UI Açıklama Geliştirme

```python
@router.post("/", summary="Tahmin yap", description="Ürün ve tarihe göre satış tahmini döner.")
```

---



