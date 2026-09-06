# ==============================================================================
# CU5 - GESTIONAR PRODUCTOS -> CAPA MODELO
# Producto, Color, Talla y sus Variantes (combinacion color+talla)
# Ubicacion: backend/app/models/cu5_gestionar_productos/producto_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ProductoModel(Base):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    marca = Column(String(100), nullable=True)
    genero = Column(String(50), nullable=True)
    grupoedad = Column(String(50), nullable=True)
    preciobase = Column(Numeric(10, 2), nullable=False, default=0.00)
    imagenprincipal = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)
    fechaactualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    categoriaid = Column(Integer, ForeignKey("categoria.id"), nullable=True)

    categoria = relationship("CategoriaModel", back_populates="productos")
    variantes = relationship("VarianteProductoModel", back_populates="producto")

class ColorModel(Base):
    __tablename__ = "color"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    codigohex = Column(String(10), nullable=True)
    activo = Column(Boolean, default=True)

class TallaModel(Base):
    __tablename__ = "talla"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), nullable=False)
    grupoedad = Column(String(50), nullable=True)
    orden = Column(Integer, default=0)
    activo = Column(Boolean, default=True)

class VarianteProductoModel(Base):
    __tablename__ = "variante_producto"

    id = Column(Integer, primary_key=True, index=True)
    productoid = Column(Integer, ForeignKey("producto.id"), nullable=False)
    colorid = Column(Integer, ForeignKey("color.id"), nullable=True)
    tallaid = Column(Integer, ForeignKey("talla.id"), nullable=True)
    sku = Column(String(50), nullable=True)
    codigobarra = Column(String(100), nullable=True)
    imagenurl = Column(Text, nullable=True)
    precioventa = Column(Numeric(10, 2), nullable=True)
    activo = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)

    producto = relationship("ProductoModel", back_populates="variantes")
    color = relationship("ColorModel")
    talla = relationship("TallaModel")
