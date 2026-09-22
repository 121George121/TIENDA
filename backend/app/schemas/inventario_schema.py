# ==============================================================================
# CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Módulos: CU08 (Catálogo y Disponibilidad) y CU13 (Inventario y Movimientos Kardex)
# Ubicación: backend/app/schemas/inventario_schema.py
# ==============================================================================

from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


# --- CU08: Catálogo y Disponibilidad Multitienda ---

class DisponibilidadVarianteResponse(BaseModel):
    variante_id: int
    sku: Optional[str] = None
    talla: Optional[str] = None
    color: Optional[str] = None
    codigohex: Optional[str] = None
    precio: Decimal
    stock: int
    disponible: bool

    class Config:
        from_attributes = True


class DisponibilidadSucursalDetalle(BaseModel):
    sucursal_id: int
    sucursal_nombre: str
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    stock_total: int
    variantes: List[DisponibilidadVarianteResponse] = []


class DisponibilidadProductoResponse(BaseModel):
    producto_id: int
    producto_nombre: str
    marca: Optional[str] = None
    preciobase: Decimal
    imagenprincipal: Optional[str] = None
    sucursales: List[DisponibilidadSucursalDetalle] = []


class ProductoCatalogoItem(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    genero: Optional[str] = None
    preciobase: Decimal
    imagenprincipal: Optional[str] = None
    categoria_id: Optional[int] = None
    categoria_nombre: Optional[str] = None
    stock_sucursal: int
    stock_total: int
    disponible: bool
    variantes: List[DisponibilidadVarianteResponse] = []

    class Config:
        from_attributes = True


class ActualizarStockRequest(BaseModel):
    variante_id: int
    sucursal_id: int
    cantidad: int
    stock_minimo: Optional[int] = 5


# --- CU13: Gestión de Inventario Físico y Movimientos Kardex ---

class MovimientoInventarioCreate(BaseModel):
    tipomovimiento: str = Field(..., description="Tipo: Entrada, Salida o Ajuste")
    cantidad: int = Field(..., ge=1, description="Cantidad de unidades del movimiento")
    motivo: Optional[str] = Field(None, max_length=200, description="Motivo de la operación")
    referencia: Optional[str] = Field(None, max_length=100, description="Nro de factura, guía o código de orden")


class StockMinimoUpdate(BaseModel):
    stockminimo: int = Field(..., ge=0, description="Nuevo nivel de stock mínimo de seguridad")


class MovimientoInventarioResponse(BaseModel):
    id: int
    tipomovimiento: str
    cantidad: int
    motivo: Optional[str] = None
    referencia: Optional[str] = None
    fecha: Optional[datetime] = None
    usuario_nombre: Optional[str] = None

    class Config:
        from_attributes = True


class InventarioResponse(BaseModel):
    id: int
    sucursal_id: int
    sucursal_nombre: str
    variante_id: int
    producto_id: int
    producto_nombre: str
    producto_marca: Optional[str] = None
    producto_precio: Decimal
    color_nombre: Optional[str] = None
    color_hex: Optional[str] = None
    talla_nombre: Optional[str] = None
    sku: Optional[str] = None
    stockfisico: int
    stockreservado: int
    stockminimo: int
    estado_stock: str  # 'NORMAL', 'BAJO_STOCK', 'AGOTADO'
    imagen_url: Optional[str] = None
    fechaactualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
