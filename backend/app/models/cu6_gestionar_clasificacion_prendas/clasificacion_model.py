# ==============================================================================
# CU6 - GESTIONAR CLASIFICACION DE PRENDAS -> CAPA MODELO
# Categorias, Temporadas y Colecciones
# Ubicacion: backend/app/models/cu6_gestionar_clasificacion_prendas/clasificacion_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, default=1)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    productos = relationship("Producto", back_populates="categoria")


class Temporada(Base):
    __tablename__ = "temporada"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, default=1)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fechainicio = Column(Date, nullable=True)
    fechafin = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)

    colecciones = relationship("Coleccion", back_populates="temporada")


class Coleccion(Base):
    __tablename__ = "coleccion"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, default=1)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagenurl = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    temporadaid = Column(Integer, ForeignKey("temporada.id"), nullable=True)

    temporada = relationship("Temporada", back_populates="colecciones")


# ==============================================================================
# ALIASES DE COMPATIBILIDAD (DIAGRAMAS Y CODIGO EXISTENTE)
# ==============================================================================
CategoriaModel = Categoria
TemporadaModel = Temporada
ColeccionModel = Coleccion

categoria = Categoria
temporada = Temporada
coleccion = Coleccion
