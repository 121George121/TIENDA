from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Engine de SQLAlchemy para conectar con PostgreSQL
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Creador de sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para la declaración de modelos ORM
Base = declarative_base()

# Inyección de dependencia para obtener sesión DB en los controladores
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
