# ==============================================================================
# CU15 - REALIZAR COMPRAS DIGITALES -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu15_realizar_compras_digitales/compra_digital_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class CarritoModel(Base):
    __tablename__ = "carrito"

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(50), nullable=False, default="Activo")
    fechacreacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fechaactualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    clienteid = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    sucursalid = Column(Integer, ForeignKey("sucursal.id"), nullable=True)

    items = relationship("CarritoItemModel", back_populates="carrito", cascade="all, delete-orphan")
    cliente = relationship("app.models.cu3_gestionar_clientes.cliente_model.ClienteModel")


class CarritoItemModel(Base):
    __tablename__ = "carrito_item"

    carritoid = Column(Integer, ForeignKey("carrito.id"), primary_key=True)
    varianteid = Column(Integer, ForeignKey("variante_producto.id"), primary_key=True)
    cantidad = Column(Integer, nullable=False, default=1)
    preciounitario = Column(Numeric(12, 2), nullable=False)
    fechaagregado = Column(DateTime, default=datetime.utcnow)

    carrito = relationship("CarritoModel", back_populates="items")
    variante = relationship("app.models.cu5_gestionar_productos.producto_model.VarianteProductoModel")
