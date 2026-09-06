# ==============================================================================
# CU7 - GESTIONAR PROVEEDORES Y PRODUCTOS SUMINISTRADOS -> CAPA MODELO
# Ubicacion: backend/app/models/cu7_gestionar_proveedores_productos_suministrados/proveedor_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ProveedorModel(Base):
    __tablename__ = "proveedor"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    razonsocial = Column(String(150), nullable=True)
    nit = Column(String(50), nullable=True)
    contacto = Column(String(100), nullable=True)
    telefono = Column(String(30), nullable=True)
    email = Column(String(150), nullable=True)
    direccion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)

    productos_suministrados = relationship("ProductoProveedorModel", back_populates="proveedor")

class ProductoProveedorModel(Base):
    __tablename__ = "producto_proveedor"

    idproducto = Column(Integer, ForeignKey("producto.id"), primary_key=True)
    idproveedor = Column(Integer, ForeignKey("proveedor.id"), primary_key=True)
    costocompra = Column(Numeric(10, 2), nullable=True)
    cantidad = Column(Integer, default=0)

    proveedor = relationship("ProveedorModel", back_populates="productos_suministrados")
    producto = relationship("ProductoModel")
