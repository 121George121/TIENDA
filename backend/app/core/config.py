import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Shopyn Golden Store API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # URL directa de base de datos (Supabase / Railway)
    DATABASE_URL_ENV: str = os.getenv("DATABASE_URL", "")

    # PostgreSQL Configuration
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "ecommerce_db")
    
    @property
    def DATABASE_URL(self) -> str:
        # Priorizar DATABASE_URL inyectada por Supabase o Railway
        direct_url = os.getenv("DATABASE_URL") or self.DATABASE_URL_ENV
        if direct_url:
            # Normalizar prefijo postgres:// a postgresql:// para compatibilidad con SQLAlchemy
            if direct_url.startswith("postgres://"):
                direct_url = direct_url.replace("postgres://", "postgresql://", 1)
            return direct_url
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_key_change_me_in_production_12345")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 horas
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 dias

    # SMTP Configuration
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 465))

    # Google Gemini AI Configuration (CU18)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Decart AI Lucy VTON Configuration (CU12)
    DECART_API_KEY: str = os.getenv("DECART_API_KEY", "")

settings = Settings()
