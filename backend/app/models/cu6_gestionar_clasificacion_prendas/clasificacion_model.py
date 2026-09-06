# ==============================================================================
# CU6 - GESTIONAR CLASIFICACION DE PRENDAS -> CAPA MODELO
# Categorias, Temporadas y Colecciones
# Ubicacion: backend/app/models/cu6_gestionar_clasificacion_prendas/clasificacion_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class CategoriaModel(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    productos = relationship("ProductoModel", back_populates="categoria")

class TemporadaModel(Base):
    __tablename__ = "temporada"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fechainicio = Column(Date, nullable=True)
    fechafin = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)

    colecciones = relationship("ColeccionModel", back_populates="temporada")

class ColeccionModel(Base):
    __tablename__ = "coleccion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagenurl = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    temporadaid = Column(Integer, ForeignKey("temporada.id"), nullable=True)

    temporada = relationship("TemporadaModel", back_populates="colecciones")
