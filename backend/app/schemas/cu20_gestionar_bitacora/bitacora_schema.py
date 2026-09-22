# ==============================================================================
# CU20 - GESTIONAR BITACORA Y AUDITORIA -> CAPA ESQUEMAS (MVC - SCHEMA)
# Ubicacion: backend/app/schemas/cu20_gestionar_bitacora/bitacora_schema.py
# ==============================================================================

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class BitacoraBase(BaseModel):
    accion: str
    modulo: str
    detalle: Optional[str] = None
    ip: Optional[str] = None
    datosprevios: Optional[str] = None
    datosnuevos: Optional[str] = None


class BitacoraCreate(BitacoraBase):
    usuarioid: Optional[int] = None


class BitacoraUsuarioInfo(BaseModel):
    id: int
    nombre: str
    apellido: Optional[str] = None
    email: str
    rol_nombre: Optional[str] = None

    class Config:
        from_attributes = True


class BitacoraResponse(BitacoraBase):
    id: int
    usuarioid: Optional[int] = None
    fechahora: datetime
    usuario: Optional[BitacoraUsuarioInfo] = None

    class Config:
        from_attributes = True


class BitacoraListResponse(BaseModel):
    total: int
    items: List[BitacoraResponse]
    limit: int
    offset: int


class BitacoraStatsResponse(BaseModel):
    total_hoy: int
    total_semana: int
    total_mes: int
    acciones_distribucion: Dict[str, int]
    modulos_distribucion: Dict[str, int]
