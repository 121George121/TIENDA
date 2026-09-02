# ==============================================================================
# CAPA MODELO (MVC - MODEL)
# Define las entidades y estructuras de tablas de la Base de Datos PostgreSQL
# ==============================================================================

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class RolModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    usuarios = relationship("UsuarioModel", back_populates="rol")

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    rol = relationship("RolModel", back_populates="usuarios")
    ordenes = relationship("OrdenModel", back_populates="usuario")

class CategoriaModel(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String(255), nullable=True)

    productos = relationship("ProductoModel", back_populates="categoria")

class ProductoModel(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    imagen_url = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)

    categoria = relationship("CategoriaModel", back_populates="productos")

class OrdenModel(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(50), default="PENDIENTE")
    direccion_envio = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("UsuarioModel", back_populates="ordenes")
    detalles = relationship("OrdenDetalleModel", back_populates="orden", cascade="all, delete-orphan")

class OrdenDetalleModel(Base):
    __tablename__ = "orden_detalles"

    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    orden = relationship("OrdenModel", back_populates="detalles")
    producto = relationship("ProductoModel")
