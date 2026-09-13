# ==============================================================================
# CU08 - CONSULTAR CATÁLOGO Y DISPONIBILIDAD -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu8_consultar_catalogo_disponibilidad/catalogo_model.py
# ==============================================================================

from app.models.cu5_gestionar_productos.producto_model import (
    ProductoModel, ColorModel, TallaModel, VarianteProductoModel
)
from app.models.cu6_gestionar_clasificacion_prendas.clasificacion_model import (
    CategoriaModel, TemporadaModel, ColeccionModel
)
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import (
    InventarioModel
)
from app.models.cu4_gestionar_sucursales.sucursal_model import (
    SucursalModel
)

# Alias canónico para disponibilidad en sucursales
InventarioSucursalModel = InventarioModel
