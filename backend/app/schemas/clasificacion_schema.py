# ==============================================================================
# CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Módulo: Clasificación de Prendas (CU06 - Categorías, Temporadas, Colecciones)
# Ubicación: backend/app/schemas/clasificacion_schema.py
# ==============================================================================

from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# CATEGORÍA DTOs
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: Optional[bool] = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

# TEMPORADA DTOs
class TemporadaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fechainicio: Optional[date] = None
    fechafin: Optional[date] = None
    activo: Optional[bool] = True

class TemporadaCreate(TemporadaBase):
    pass

class TemporadaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fechainicio: Optional[date] = None
    fechafin: Optional[date] = None
    activo: Optional[bool] = None

class TemporadaResponse(TemporadaBase):
    id: int

    class Config:
        from_attributes = True

# COLECCIÓN DTOs
class ColeccionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagenurl: Optional[str] = None
    temporadaid: Optional[int] = None
    activo: Optional[bool] = True

class ColeccionCreate(ColeccionBase):
    pass

class ColeccionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    imagenurl: Optional[str] = None
    temporadaid: Optional[int] = None
    activo: Optional[bool] = None

class ColeccionResponse(ColeccionBase):
    id: int
    temporada: Optional[TemporadaResponse] = None

    class Config:
        from_attributes = True
