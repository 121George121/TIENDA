# ==============================================================================
# CAPA MODELO (MVC - MODEL)
# Punto único de importación de todas las entidades del backend.
# Cada entidad vive modularmente en la carpeta de su caso de uso.
# ==============================================================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

from app.models.cu1_gestionar_autenticacion.usuario_rol_model import RolModel, UsuarioModel
from app.models.cu3_gestionar_clientes.cliente_model import ClienteModel
from app.models.cu4_gestionar_sucursales.sucursal_model import SucursalModel
from app.models.cu5_gestionar_productos.producto_model import (
    ProductoModel, ColorModel, TallaModel, VarianteProductoModel
)
from app.models.cu6_gestionar_clasificacion_prendas.clasificacion_model import (
    CategoriaModel, TemporadaModel, ColeccionModel
)
from app.models.cu7_gestionar_proveedores_productos_suministrados.proveedor_model import (
    ProveedorModel, ProductoProveedorModel
)
from app.models.cu14_registrar_ventas_presenciales.venta_presencial_model import (
    VentaModel, DetalleVentaModel, MetodoPagoModel, PagoModel, ReciboModel
)
from app.models.cu15_realizar_compras_digitales.compra_digital_model import (
    CarritoModel, CarritoItemModel
)
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import (
    InventarioModel, MovimientoInventarioModel
)

# Alias de compatibilidad: CU08-CU11 usan InventarioSucursalModel mapeado a la tabla inventario
InventarioSucursalModel = InventarioModel


# CU10 & CU11 - Modelos de Reserva de Prendas
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
