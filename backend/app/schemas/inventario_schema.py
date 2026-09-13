# ==============================================================================
# CU13 - GESTIONAR INVENTARIO Y MOVIMIENTOS -> CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Ubicación: backend/app/schemas/inventario_schema.py
# ==============================================================================

from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


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
    estado_stock: str # 'NORMAL', 'BAJO_STOCK', 'AGOTADO'
    fechaactualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
