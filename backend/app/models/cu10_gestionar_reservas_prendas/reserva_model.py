# ==============================================================================
# CU10 - GESTIONAR RESERVAS DE PRENDAS -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu10_gestionar_reservas_prendas/reserva_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ReservaModel(Base):
    __tablename__ = "reserva"

    id = Column(Integer, primary_key=True, index=True)
    codigoreserva = Column(String(100), unique=True, nullable=False, index=True)
    fechareserva = Column(DateTime, default=datetime.utcnow, nullable=False)
    estado = Column(String(50), default="PENDIENTE", nullable=False)  # PENDIENTE, CONFIRMADA, ENTREGADA, CANCELADA, EXPIRADA
    observaciones = Column(Text, nullable=True)
    sucursalid = Column(Integer, ForeignKey("sucursal.id", ondelete="RESTRICT"), nullable=False, index=True)
    clienteid = Column(Integer, ForeignKey("cliente.id", ondelete="RESTRICT"), nullable=False, index=True)

    sucursal = relationship("SucursalModel", backref="reservas")
    cliente = relationship("ClienteModel", backref="reservas")
    detalles = relationship("ReservaDetalleModel", back_populates="reserva", cascade="all, delete-orphan")


class ReservaDetalleModel(Base):
    __tablename__ = "reserva_detalle"

    varianteid = Column(Integer, ForeignKey("variante_producto.id", ondelete="RESTRICT"), primary_key=True)
    reservaid = Column(Integer, ForeignKey("reserva.id", ondelete="CASCADE"), primary_key=True)
    cantidad = Column(Integer, nullable=False)

    reserva = relationship("ReservaModel", back_populates="detalles")
    variante = relationship("VarianteProductoModel")
