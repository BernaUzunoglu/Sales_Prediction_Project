## 📁 Proje Yapısı
```bash
📁 Sales_Prediction_Project/
├── 📄 .env.example                      → Örnek çevre değişkenleri şablonu  
├── 📄 .gitignore                       → Git için ignore dosyası  
├── 📄 README.md                        → Proje açıklamaları  
├── 📄 requirements.txt                 → Proje bağımlılıkları  

├── 📁 tests/                           → Unit ve integration testleri  
│   ├── 🧪 test_api.py  
│   └── 🧪 test_models.py  

├── 📁 docs/                            → Dokümantasyon klasörü  
│   ├── 📄 API_DOCS.md  
│   ├── 📄 DATA_DICTIONARY.md           → Veri yapısı dokümantasyonu  
│   └── 📄 ARCHITECTURE.md              → Sistem mimarisi  

├── 📁 research/                        → Keşifçi Veri Analizi (EDA) - AR-GE çalışmaları  
│   └── 📓 EDA.ipynb  

├── 📁 src/                             → Ana kaynak kod klasörü  
│   ├── 📄 __init__.py  

│   ├── 📁 api/                         → API ile ilgili tüm kodlar  
│   │   ├── 📄 __init__.py  
│   │   ├── 🚀 main.py                  → Ana FastAPI dosyası  
│   │   ├── 📁 routes/                  → API endpointleri  
│   │   │   ├── 📄 __init__.py  
│   │   │   ├── 📄 predict.py                  → Tahmin endpoint’i  
│   │   │   ├── 📄 retrain.py                  → Model eğitimi endpoint’i (opsiyonel)  
│   │   │   ├── 📄 health.py                   → Sağlık kontrolü endpoint’i  
│   │   │   ├── 📄 products.py                 → Ürün listesini dönen endpoint  
│   │   │   ├── 📄 sales_summary.py            → Satış özeti endpoint’i  
│   │   │   └── 📄 customer_segment_predict.py → Müşteri segmentasyonu endpoint’i  
│   │   ├── 📁 models/                → API Pydantic modelleri  
│   │   │   ├── 📄 __init__.py  
│   │   │   ├── 📄 request_models.py  
│   │   │   └── 📄 customer_segment_request_model.py  
│   │   └── 📁 utils/                 → Yardımcı fonksiyonlar  
│   │       ├── 📄 __init__.py  
│   │       ├── 📄 errors.py                → Özel hata mesajları  
│   │       └── 📄 model_loader.py         → Model yükleyici fonksiyon  

│   ├── 📁 models/                      → Eğitimli model ve ilgili kodlar  
│   │   ├── 📁 model_reports/           → Model raporları (.pkl)  
│   │   │   └── 📁 graphics/            → Rapor grafik dosyaları (.png)  
│   │   ├── 📁 model_result/            → Model sonuçları (.csv, .json)  
│   │   ├── 📁 saved_models/            → Eğitilmiş model dosyaları (.pkl)  
│   │   ├── 📄 __init__.py  
│   │   ├── 📄 customer_segm_kneighborsclass.py  
│   │   ├── 📄 customer_segmentation_kmeans.py  
│   │   ├── 📄 customer_segmentation_kneighborsclassifier.py  
│   │   ├── 📄 feature_engineering.py  
│   │   ├── 📄 sales_forecasting_product.py  
│   │   ├── 📄 sales_forecasting_product_id.py  
│   │   └── 📄 sales_forecasting_product_pipeline.py  

│   ├── 📁 data/                        → Veri ve veritabanı işlemleri  
│   │   ├── 📁 models/                  → SQLAlchemy ORM modelleri  
│   │   ├── 📁 processed/               → İşlenmiş veriler (.csv)  
│   │   ├── 📄 __init__.py  
│   │   ├── 📄 category_revenue_data_preprocessing.py  
│   │   ├── 📄 create_customer_features.py  
│   │   ├── 📄 database.py  
│   │   ├── 📄 extract_customer_transactions.py  
│   │   ├── 📄 preprocessing.py  
│   │   ├── 📄 preprocessing_data1.py  
│   │   └── 📄 sales_forecasting_preprocessing.py  

│   └── 📄 config.py                   → Proje konfigürasyon dosyası  

└── 📁 legacy_models/                  → Eski model dosyaları (.pkl)  
```
