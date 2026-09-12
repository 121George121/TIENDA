# ==============================================================================
# CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Módulo: CU09 - Gestionar Carrito de Compras
# Ubicación: backend/app/schemas/carrito_schema.py
# ==============================================================================

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class CarritoItemResponse(BaseModel):
    variante_id: int
    producto_id: int
    producto_nombre: str
    imagen_url: Optional[str] = None
    sku: Optional[str] = None
    talla: Optional[str] = None
    color: Optional[str] = None
    codigohex: Optional[str] = None
    precio_unitario: Decimal
    cantidad: int
    subtotal: Decimal
    stock_disponible: int
    stock_suficiente: bool

    class Config:
        from_attributes = True

class CarritoResponse(BaseModel):
    id: int
    estado: str
    cliente_id: int
    sucursal_id: Optional[int] = None
    sucursal_nombre: Optional[str] = None
    items: List[CarritoItemResponse] = []
    total_items: int
    total_precio: Decimal
    tiene_alertas_stock: bool
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgregarItemCarritoRequest(BaseModel):
    variante_id: int
    cantidad: int = 1
    sucursal_id: Optional[int] = None

class ActualizarCantidadItemRequest(BaseModel):
    cantidad: int

class AsignarSucursalCarritoRequest(BaseModel):
    sucursal_id: int
