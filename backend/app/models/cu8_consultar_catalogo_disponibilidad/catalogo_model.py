# ==============================================================================
# CU08 - CONSULTAR CATÁLOGO Y DISPONIBILIDAD -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu8_consultar_catalogo_disponibilidad/catalogo_model.py
# ==============================================================================

from app.models.cu5_gestionar_productos.producto_model import (
    Producto, Color, Talla, VarianteProducto,
    ProductoModel, ColorModel, TallaModel, VarianteProductoModel
)
from app.models.cu6_gestionar_clasificacion_prendas.clasificacion_model import (
    Categoria, Temporada, Coleccion,
    CategoriaModel, TemporadaModel, ColeccionModel
)
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import (
    Inventario, InventarioModel
)
from app.models.cu4_gestionar_sucursales.sucursal_model import (
    Sucursal, SucursalModel
)

# Aliases canónicos para disponibilidad en sucursales
InventarioSucursal = Inventario
InventarioSucursalModel = InventarioModel

__all__ = [
    "Producto", "VarianteProducto", "Color", "Talla",
    "Categoria", "Temporada", "Coleccion",
    "Sucursal", "Inventario", "InventarioSucursal",
    "ProductoModel", "VarianteProductoModel", "ColorModel", "TallaModel",
    "CategoriaModel", "TemporadaModel", "ColeccionModel",
    "SucursalModel", "InventarioModel", "InventarioSucursalModel"
]
