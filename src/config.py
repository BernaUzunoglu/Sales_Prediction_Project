import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını yükle

class Config:
    PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/default/path")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")  # Varsayılan PostgreSQL portu 5432
    DB_NAME = os.getenv("DB_NAME")

    # SQLAlchemy için bağlantı URL'si
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"