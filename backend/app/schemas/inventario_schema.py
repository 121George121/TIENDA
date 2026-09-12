# ==============================================================================
# CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
# Ubicación: backend/app/schemas/inventario_schema.py
# ==============================================================================

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

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
