# ==============================================================================
# CU4 - GESTIONAR SUCURSALES -> CAPA MODELO
# Ubicacion: backend/app/models/cu4_gestionar_sucursales/sucursal_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class SucursalModel(Base):
    __tablename__ = "sucursal"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=True)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    latitud = Column(Numeric(10, 8), nullable=True)
    longitud = Column(Numeric(11, 8), nullable=True)
    activo = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)

    usuarios = relationship("UsuarioModel", back_populates="sucursal")
