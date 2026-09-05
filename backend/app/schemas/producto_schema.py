# ==============================================================================
# CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Módulo: Productos y Catálogo Retail (CU05)
# Ubicación: backend/app/schemas/producto_schema.py
# ==============================================================================

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.schemas.clasificacion_schema import CategoriaResponse

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    genero: Optional[str] = None
    grupoedad: Optional[str] = None
    preciobase: Decimal
    imagenprincipal: Optional[str] = None
    categoriaid: Optional[int] = None
    activo: Optional[bool] = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    genero: Optional[str] = None
    grupoedad: Optional[str] = None
    preciobase: Optional[Decimal] = None
    imagenprincipal: Optional[str] = None
    categoriaid: Optional[int] = None
    activo: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id: int
    fechacreacion: Optional[datetime] = None
    fechaactualizacion: Optional[datetime] = None
    categoria: Optional[CategoriaResponse] = None

    class Config:
        from_attributes = True
