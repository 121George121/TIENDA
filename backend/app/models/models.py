# ==============================================================================
# CAPA MODELO (MVC - MODEL)
# Punto unico de importacion de todas las entidades del backend.
#
# Cada entidad vive fisicamente en la carpeta de su caso de uso:
#   CU1 - Gestionar Autenticacion              -> models/cu1_gestionar_autenticacion/
#   CU3 - Gestionar Clientes                   -> models/cu3_gestionar_clientes/
#   CU4 - Gestionar Sucursales                 -> models/cu4_gestionar_sucursales/
#   CU5 - Gestionar Productos                  -> models/cu5_gestionar_productos/
#   CU6 - Gestionar Clasificacion de Prendas   -> models/cu6_gestionar_clasificacion_prendas/
#   CU7 - Gestionar Proveedores y Productos    -> models/cu7_gestionar_proveedores_productos_suministrados/
#
# Este archivo solo re-exporta, para que el resto del backend (CU2, core,
# dependencias) pueda seguir escribiendo `from app.models.models import X`
# sin que le importe en que carpeta vive cada clase.
# ==============================================================================

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


