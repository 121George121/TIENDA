# ==============================================================================
# CU14 - REGISTRAR VENTAS PRESENCIALES -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu14_registrar_ventas_presenciales/venta_presencial_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class VentaModel(Base):
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True, index=True)
    codigoventa = Column(String(100), nullable=False, unique=True)
    tipoventa = Column(String(50), nullable=False, default="Presencial")
    estado = Column(String(50), nullable=False, default="Completada")
    subtotal = Column(Numeric(12, 2), nullable=False)
    descuento = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    sucursalid = Column(Integer, ForeignKey("sucursal.id"), nullable=False)
    clienteid = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    usuarioid = Column(Integer, ForeignKey("usuario.id"), nullable=False)

    detalles = relationship("DetalleVentaModel", back_populates="venta", cascade="all, delete-orphan")
    pagos = relationship("PagoModel", back_populates="venta", cascade="all, delete-orphan")
    sucursal = relationship("app.models.cu4_gestionar_sucursales.sucursal_model.SucursalModel")
    cliente = relationship("app.models.cu3_gestionar_clientes.cliente_model.ClienteModel")
    usuario = relationship("app.models.cu1_gestionar_autenticacion.usuario_rol_model.UsuarioModel")


class DetalleVentaModel(Base):
    __tablename__ = "detalle_venta"

    ventaid = Column(Integer, ForeignKey("venta.id"), primary_key=True)
    varianteid = Column(Integer, ForeignKey("variante_producto.id"), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    preciounitario = Column(Numeric(12, 2), nullable=False)
    descuento = Column(Numeric(12, 2), default=0)
    subtotal = Column(Numeric(12, 2), nullable=False)

    venta = relationship("VentaModel", back_populates="detalles")
    variante = relationship("app.models.cu5_gestionar_productos.producto_model.VarianteProductoModel")


class MetodoPagoModel(Base):
    __tablename__ = "metodo_pago"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)


class ReciboModel(Base):
    __tablename__ = "recibo"

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(50), nullable=False, default="Emitido")
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)


class PagoModel(Base):
    __tablename__ = "pago"

    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Numeric(12, 2), nullable=False)
    estado = Column(String(50), nullable=False, default="Aprobado")
    referencia = Column(String(150), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    ventaid = Column(Integer, ForeignKey("venta.id"), nullable=False)
    reciboid = Column(Integer, ForeignKey("recibo.id"), nullable=True)
    metodoid = Column(Integer, ForeignKey("metodo_pago.id"), nullable=False)

    venta = relationship("VentaModel", back_populates="pagos")
    metodo = relationship("MetodoPagoModel")
