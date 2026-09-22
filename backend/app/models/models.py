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


# CU10 & CU11 - Modelos de Reserva de Prendas (modularizados)
from app.models.cu10_gestionar_reservas_prendas.reserva_model import (
    ReservaModel,
    ReservaDetalleModel,
)
from app.models.cu19_gestionar_notificaciones.notificacion_model import NotificacionModel
from app.models.cu20_gestionar_bitacora.bitacora_model import BitacoraModel

