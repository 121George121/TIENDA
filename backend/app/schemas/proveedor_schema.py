# ==============================================================================
# CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Módulo: Proveedores y Productos Suministrados (CU07)
# Ubicación: backend/app/schemas/proveedor_schema.py
# ==============================================================================

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.schemas.producto_schema import ProductoResponse

class ProveedorBase(BaseModel):
    nombre: str
    razonsocial: Optional[str] = None
    nit: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = True

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = None
    razonsocial: Optional[str] = None
    nit: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = None

class ProductoProveedorBase(BaseModel):
    idproducto: int
    idproveedor: int
    costocompra: Optional[Decimal] = 0.00
    cantidad: Optional[int] = 0

class ProductoProveedorCreate(ProductoProveedorBase):
    pass

class ProductoProveedorResponse(ProductoProveedorBase):
    producto: Optional[ProductoResponse] = None

    class Config:
        from_attributes = True

class ProveedorResponse(ProveedorBase):
    id: int
    fechacreacion: Optional[datetime] = None
    productos_suministrados: Optional[List[ProductoProveedorResponse]] = []

    class Config:
        from_attributes = True
