# ==============================================================================
# CAPA MODELO (MVC - MODEL)
# Punto único de importación de todas las entidades del backend.
# Los modelos llevan el nombre exacto de las tablas de la Base de Datos para
# que coincidan 1 a 1 con los diagramas de clases, DER y UML.
# ==============================================================================

from app.core.database import Base

# CU01 - Autenticación
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import (
    Rol, Usuario, RolModel, UsuarioModel, rol, usuario
)

# CU03 - Clientes
from app.models.cu3_gestionar_clientes.cliente_model import (
    Cliente, ClienteModel, cliente
)

# CU04 - Sucursales
from app.models.cu4_gestionar_sucursales.sucursal_model import (
    Sucursal, SucursalModel, sucursal
)

# CU05 - Productos, Colores, Tallas y Variantes
from app.models.cu5_gestionar_productos.producto_model import (
    Producto, Color, Talla, VarianteProducto,
    ProductoModel, ColorModel, TallaModel, VarianteProductoModel,
    producto, color, talla, variante_producto
)

# CU06 - Clasificación de Prendas
from app.models.cu6_gestionar_clasificacion_prendas.clasificacion_model import (
    Categoria, Temporada, Coleccion,
    CategoriaModel, TemporadaModel, ColeccionModel,
    categoria, temporada, coleccion
)

# CU07 - Proveedores y Suministro
from app.models.cu7_gestionar_proveedores_productos_suministrados.proveedor_model import (
    Proveedor, ProductoProveedor,
    ProveedorModel, ProductoProveedorModel,
    proveedor, producto_proveedor
)

# CU13 - Inventario y Movimientos
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import (
    Inventario, MovimientoInventario,
    InventarioModel, MovimientoInventarioModel, InventarioSucursalModel,
    inventario, movimiento_inventario, inventario_sucursal
)

# CU14 - Ventas Presenciales, Pagos y Recibos
from app.models.cu14_registrar_ventas_presenciales.venta_presencial_model import (
    Venta, DetalleVenta, MetodoPago, Pago, Recibo,
    VentaModel, DetalleVentaModel, MetodoPagoModel, PagoModel, ReciboModel,
    venta, detalle_venta, metodo_pago, pago, recibo
)

# CU15 - Compras Digitales y Carrito
from app.models.cu15_realizar_compras_digitales.compra_digital_model import (
    Carrito, CarritoItem,
    CarritoModel, CarritoItemModel,
    carrito, carrito_item
)

# CU10 & CU11 - Reservas de Prendas
from app.models.cu10_gestionar_reservas_prendas.reserva_model import (
    Reserva, ReservaDetalle,
    ReservaModel, ReservaDetalleModel,
    reserva, reserva_detalle
)

# CU19 - Notificaciones
from app.models.cu19_gestionar_notificaciones.notificacion_model import (
    Notificacion, NotificacionModel, notificacion
)

# CU20 - Bitácora y Auditoría
from app.models.cu20_gestionar_bitacora.bitacora_model import (
    Bitacora, BitacoraModel, bitacora
)

# SaaS Multi-Tenant & Diagrama UML
from app.models.saas_tenant.tenant_model import (
    PlanSuscripcion, Tenant, TenantConfiguracion, TenantSuscripcion,
    DireccionCliente, EventoCliente, PruebaVirtual, ProductoColeccion,
    PlanSuscripcionModel, TenantModel, TenantConfiguracionModel, TenantSuscripcionModel,
    DireccionClienteModel, EventoClienteModel, PruebaVirtualModel, ProductoColeccionModel,
    plan_suscripcion, tenant, tenant_configuracion, tenant_suscripcion,
    direccioncliente, evento_cliente, prueba_virtual, producto_coleccion
)

# Registro de retrocompatibilidad en SQLAlchemy _class_registry para que tanto
# 'Usuario' como 'UsuarioModel' resuelvan automáticamente en cualquier relación por cadena
_MODEL_MAP = {
    "RolModel": Rol,
    "UsuarioModel": Usuario,
    "ClienteModel": Cliente,
    "SucursalModel": Sucursal,
    "ProductoModel": Producto,
    "ColorModel": Color,
    "TallaModel": Talla,
    "VarianteProductoModel": VarianteProducto,
    "CategoriaModel": Categoria,
    "TemporadaModel": Temporada,
    "ColeccionModel": Coleccion,
    "ProveedorModel": Proveedor,
    "ProductoProveedorModel": ProductoProveedor,
    "InventarioModel": Inventario,
    "InventarioSucursalModel": Inventario,
    "MovimientoInventarioModel": MovimientoInventario,
    "VentaModel": Venta,
    "DetalleVentaModel": DetalleVenta,
    "MetodoPagoModel": MetodoPago,
    "PagoModel": Pago,
    "ReciboModel": Recibo,
    "CarritoModel": Carrito,
    "CarritoItemModel": CarritoItem,
    "ReservaModel": Reserva,
    "ReservaDetalleModel": ReservaDetalle,
    "NotificacionModel": Notificacion,
    "BitacoraModel": Bitacora,
    "PlanSuscripcionModel": PlanSuscripcion,
    "TenantModel": Tenant,
    "TenantConfiguracionModel": TenantConfiguracion,
    "TenantSuscripcionModel": TenantSuscripcion,
    "DireccionClienteModel": DireccionCliente,
    "EventoClienteModel": EventoCliente,
    "PruebaVirtualModel": PruebaVirtual,
    "ProductoColeccionModel": ProductoColeccion,
}

if hasattr(Base, "registry") and hasattr(Base.registry, "_class_registry"):
    for alias_name, model_cls in _MODEL_MAP.items():
        Base.registry._class_registry[alias_name] = model_cls
