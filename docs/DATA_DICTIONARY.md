# 📊 Data Dictionary

Bu doküman, projede kullanılan **veri yapılarının tanımını**, **alan isimlerinin açıklamalarını** ve **veri tiplerini** içerir. Hem Northwind veritabanındaki tablolar hem de API için kullanılan CSV dosyaları kapsam dahilindedir.

---

## 🗄️ Northwind Veritabanı Tabloları

### 📦 Products
| Kolon Adı      | Veri Tipi   | Açıklama                          |
|----------------|-------------|-----------------------------------|
| ProductID      | int         | Ürün benzersiz kimliği            |
| ProductName    | string      | Ürün adı                          |
| SupplierID     | int         | Ürünü sağlayan tedarikçi ID'si    |
| CategoryID     | int         | Ürünün ait olduğu kategori ID     |
| QuantityPerUnit| string      | Paketleme bilgisi (ör: 10 boxes)  |
| UnitPrice      | float       | Birim fiyat                       |
| UnitsInStock   | int         | Mevcut stok adedi                 |
| UnitsOnOrder   | int         | Sipariş edilmiş fakat gelmemiş    |
| ReorderLevel   | int         | Yeniden sipariş seviyesi          |
| Discontinued   | boolean     | Satışı durdurulmuş mu?            |

### 🧾 Orders
| Kolon Adı     | Veri Tipi | Açıklama                             |
|---------------|-----------|--------------------------------------|
| OrderID       | int       | Sipariş kimliği                      |
| CustomerID    | string    | Siparişi veren müşteri ID'si         |
| EmployeeID    | int       | Siparişi alan çalışan ID             |
| OrderDate     | date      | Sipariş tarihi                       |
| RequiredDate  | date      | Teslim edilmesi gereken tarih        |
| ShippedDate   | date      | Gerçek teslim tarihi                 |
| ShipVia       | int       | Nakliye şirketi ID'si                |
| Freight       | float     | Kargo ücreti                         |
| ShipName      | string    | Teslimat şirket ismi                 |
| ShipAddress   | string    | Teslimat adresi                      |
| ShipCity      | string    | Teslimat şehri                       |
| ShipRegion    | string    | Teslimat bölgesi (varsa)            |
| ShipPostalCode| string    | Teslimat posta kodu                 |
| ShipCountry   | string    | Teslimat ülkesi                     |

### 🧮 OrderDetails
| Kolon Adı   | Veri Tipi | Açıklama                      |
|-------------|-----------|-------------------------------|
| OrderID     | int       | İlgili sipariş ID             |
| ProductID   | int       | Siparişteki ürün ID'si        |
| UnitPrice   | float     | Sipariş sırasındaki fiyat     |
| Quantity    | int       | Sipariş edilen ürün adedi     |
| Discount    | float     | Uygulanan indirim (0.0 - 1.0) |

### 👤 Customers
| Kolon Adı     | Veri Tipi | Açıklama                          |
|---------------|-----------|-----------------------------------|
| CustomerID    | string    | Müşteri kimliği (primary key)     |
| CompanyName   | string    | Firma adı                         |
| ContactName   | string    | Yetkili kişi adı                  |
| ContactTitle  | string    | Yetkili pozisyonu                |
| Address       | string    | Adres                             |
| City          | string    | Şehir                             |
| Region        | string    | Bölge                             |
| PostalCode    | string    | Posta kodu                        |
| Country       | string    | Ülke                              |
| Phone         | string    | Telefon numarası                  |
| Fax           | string    | Faks numarası                     |

### 🗃️ Categories
| Kolon Adı     | Veri Tipi | Açıklama                          |
|---------------|-----------|-----------------------------------|
| CategoryID    | int       | Kategori kimliği (primary key)    |
| CategoryName  | string    | Kategori adı                      |
| Description   | string    | Açıklama                          |
| Picture       | binary    | Kategoriye ait resim (varsa)      |


## İlişkisel Yapı Analizi
 * Orders - Order_Details: One-to-Many (Bir siparişin birden çok detayı olabilir)

 * Products - Order_Details: One-to-Many (Bir ürün birden çok sipariş detayında yer alabilir)

 * Customers - Orders: One-to-Many (Bir müşteri birden çok sipariş verebilir)

 * Categories - Products: One-to-Many (Bir kategoride birden çok ürün olabilir)

---

## 📁 API Tahmin Modeli Kaynak CSV Dosyaları

### 📈 sales_forecasting_data.csv
| Kolon Adı     | Veri Tipi | Açıklama                                  |
|---------------|-----------|-------------------------------------------|
| order_date    | object    | Sipariş tarihi (modelde yıl, ay, gün çıkarılır) |
| product_id    | int       | Ürün kimliği                              |
| quantity      | int       | Satış adedi                               |
| total_sales   | float     | Satış tutarı (fiyat × adet gibi)          |

#### 🛠️ Feature Engineering Sonrası Kullanılan Alanlar
| Kolon Adı           | Veri Tipi | Açıklama                                            |
|---------------------|-----------|-----------------------------------------------------|
| product_id          | int       | Ürün ID (girdi olarak kalır)                       |
| year                | int       | Satış yılı                                          |
| month               | int       | Satış ayı                                           |
| day                 | int       | Satış günü                                          |
| dayofweek           | int       | Haftanın günü (0=Mon, 6=Sun)                       |
| dayofyear           | int       | Yılın kaçıncı günü                                  |
| lag_1 - lag_14      | float     | Önceki 14 güne ait geçmiş satışlar                 |
| moving_avg_7        | float     | Son 7 günün hareketli ortalaması                   |
| moving_avg_14       | float     | Son 14 günün hareketli ortalaması                  |
| exp_moving_avg_7    | float     | Üssel ağırlıklı hareketli ortalama (7 gün)         |
| cumulative_sales    | float     | O güne kadar kümülatif satış miktarı               |
| avg_sales_per_day   | float     | Günlük ortalama satış miktarı                      |

### 👥 customer_features.csv
| Kolon Adı          | Veri Tipi | Açıklama                                  |
|--------------------|-----------|-------------------------------------------|
| customer_id        | string    | Müşteri kimliği                           |
| total_spent        | float     | Müşterinin toplam harcaması               |
| num_orders         | int       | Toplam sipariş sayısı                     |
| avg_order_value    | float     | Ortalama sipariş tutarı                   |
| num_products       | int       | Toplam satın alınan ürün sayısı           |
| recency            | float     | Son siparişten bu yana geçen gün sayısı   |
| segment_id         | int       | Segment sınıf ID’si (etiket)              |

---

## 📡 API Endpoint Çıktı Alanları

### 🔮 `/predict` (POST) – Satış Tahmini
| Alan Adı           | Veri Tipi | Açıklama                               |
|--------------------|-----------|----------------------------------------|
| product_id         | int       | Tahmini yapılan ürünün ID’si           |
| predicted_quantity | float     | Modelin tahmin ettiği satış miktarı    |

### 👥 `/predict-segment` (POST) – Müşteri Segmentasyonu
| Alan Adı      | Veri Tipi | Açıklama                                 |
|---------------|-----------|------------------------------------------|
| segment_id    | int       | Segment ID’si (etiket olarak)            |
| segment_name  | string    | Segmentin açıklayıcı ismi                |

### 📦 `/products` (GET) – Ürün Listesi
| Alan Adı   | Veri Tipi | Açıklama           |
|------------|-----------|--------------------|
| id         | int       | Ürün ID’si         |
| name       | string    | Ürün adı           |

### 📈 `/sales_summary` (GET) – Satış Özeti
| Alan Adı       | Veri Tipi | Açıklama                 |
|----------------|-----------|--------------------------|
| product_name   | string    | Ürün adı                 |
| total_quantity | int       | Toplam satış miktarı     |

### 🔄 `/health` (GET) – API Durumu
| Alan Adı | Veri Tipi | Açıklama                     |
|----------|-----------|------------------------------|
| status   | string    | API çalışma durumu mesajı    |

---

## 🎯 Model Girdileri ve Hedef Değişkenler

### 🔮 Satış Tahmin Modeli (Regression)
#### 🎯 Hedef Değişken:
- `quantity`: Tahmin edilmek istenen satış miktarı (int)

#### 🔢 Kullanılan Özellikler (Features):
- `product_id`
- `year`, `month`, `day`
- `dayofweek`, `dayofyear`
- `lag_1` – `lag_14`
- `moving_avg_7`, `moving_avg_14`, `exp_moving_avg_7`
- `cumulative_sales`, `avg_sales_per_day`

### 👥 Müşteri Segmentasyon Modeli (Classification)
#### 🎯 Hedef Değişken:
- `segment_id`: Müşterinin ait olduğu segment sınıfı (int)

#### 🔢 Kullanılan Özellikler (Features):
- `total_spent`
- `num_orders`
- `avg_order_value`
- `num_products`
- `recency`

---

## 📌 Notlar
- Tüm tarih alanları `YYYY-MM-DD` formatındadır.
- CSV dosyaları API tarafından model tahmini ve segmentasyon için kullanılır.
- Northwind veritabanı, demo veri seti olarak kullanılmıştır.
- GET endpoint’lerinin yanıtları doğrudan arayüz veri sunumlarında kullanılır.
