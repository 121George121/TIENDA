# ==============================================================================
# CU15 - REALIZAR COMPRAS DIGITALES -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu15_realizar_compras_digitales/compra_digital_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Carrito(Base):
    __tablename__ = "carrito"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, default=1)
    estado = Column(String(50), nullable=False, default="Activo")
    fechacreacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fechaactualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    clienteid = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    sucursalid = Column(Integer, ForeignKey("sucursal.id"), nullable=True)

    items = relationship("CarritoItem", back_populates="carrito", cascade="all, delete-orphan")
    cliente = relationship("Usuario", foreign_keys=[clienteid])
    sucursal = relationship("Sucursal")


class CarritoItem(Base):
    __tablename__ = "carrito_item"

    carritoid = Column(Integer, ForeignKey("carrito.id"), primary_key=True)
    varianteid = Column(Integer, ForeignKey("variante_producto.id"), primary_key=True)
    cantidad = Column(Integer, nullable=False, default=1)
    preciounitario = Column(Numeric(12, 2), nullable=False)
    fechaagregado = Column(DateTime, default=datetime.utcnow)

    carrito = relationship("Carrito", back_populates="items")
    variante = relationship("VarianteProducto")


# ==============================================================================
# ALIASES DE COMPATIBILIDAD (DIAGRAMAS Y CODIGO EXISTENTE)
# ==============================================================================
CarritoModel = Carrito
CarritoItemModel = CarritoItem

carrito = Carrito
carrito_item = CarritoItem
