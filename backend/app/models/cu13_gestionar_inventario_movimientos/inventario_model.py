# ==============================================================================
# CU13 - GESTIONAR INVENTARIO Y MOVIMIENTOS -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu13_gestionar_inventario_movimientos/inventario_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, synonym
from datetime import datetime
from app.core.database import Base


class InventarioModel(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    stockfisico = Column(Integer, default=0, nullable=False)
    stockreservado = Column(Integer, default=0, nullable=False)
    stockminimo = Column(Integer, default=5, nullable=False)
    fechaactualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sucursalid = Column(Integer, ForeignKey("sucursal.id"), nullable=False)
    varianteid = Column(Integer, ForeignKey("variante_producto.id"), nullable=False)

    # Alias de compatibilidad: CU08-CU11 usan .cantidad para referirse al stock físico
    cantidad = synonym("stockfisico")

    sucursal = relationship("app.models.cu4_gestionar_sucursales.sucursal_model.SucursalModel")
    variante = relationship("app.models.cu5_gestionar_productos.producto_model.VarianteProductoModel")
    movimientos = relationship("MovimientoInventarioModel", back_populates="inventario", cascade="all, delete-orphan")



class MovimientoInventarioModel(Base):
    __tablename__ = "movimiento_inventario"

    id = Column(Integer, primary_key=True, index=True)
    tipomovimiento = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    motivo = Column(String(200), nullable=True)
    referencia = Column(String(100), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    inventarioid = Column(Integer, ForeignKey("inventario.id"), nullable=False)
    usuarioid = Column(Integer, ForeignKey("usuario.id"), nullable=False)

    inventario = relationship("InventarioModel", back_populates="movimientos")
    usuario = relationship("app.models.cu1_gestionar_autenticacion.usuario_rol_model.UsuarioModel")
