# ==============================================================================
# CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Módulo: Sucursales (CU04)
# Ubicación: backend/app/schemas/sucursal_schema.py
# ==============================================================================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class SucursalBase(BaseModel):
    nombre: str
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    activo: Optional[bool] = True

class SucursalCreate(SucursalBase):
    pass

class SucursalUpdate(BaseModel):
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    activo: Optional[bool] = None

class SucursalResponse(SucursalBase):
    id: int
    fechacreacion: Optional[datetime] = None

    class Config:
        from_attributes = True
