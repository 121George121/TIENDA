# ==============================================================================
# CAPA ESQUEMA (PYDANTIC SCHEMAS)
# Módulo: Clientes (CU03)
# Ubicación: backend/app/schemas/cliente_schema.py
# ==============================================================================

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- DETALLES DE COMPRAS / ORDENES ---
class OrdenDetalleItem(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True

class HistorialCompraResponse(BaseModel):
    id: int
    usuario_id: int
    total: Decimal
    estado: str
    direccion_envio: str
    created_at: datetime
    detalles: List[OrdenDetalleItem] = []

    class Config:
        from_attributes = True

class HistorialReservaResponse(BaseModel):
    id: int
    cliente_id: int
    codigo_reserva: str
    fecha_reserva: datetime
    estado: str
    total_estimado: Decimal
    notas: Optional[str] = None

# --- CLIENTE CRUD SCHEMAS ---
class ClienteCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del cliente")
    apellido: Optional[str] = Field(None, max_length=100, description="Apellido del cliente")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=6, description="Contraseña de acceso")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None

class ClienteEstadoUpdate(BaseModel):
    activo: bool = Field(..., description="Estado activo (True) o desactivado/baja lógica (False)")

class ClientePerfilResponse(BaseModel):
    id: int
    nombre: str
    apellido: Optional[str] = None
    email: str
    telefono: Optional[str] = None
    activo: bool
    rol_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: Optional[str] = None
    email: str
    telefono: Optional[str] = None
    activo: bool
    rol_id: Optional[int] = None
    created_at: Optional[datetime] = None
    total_ordenes: int = 0
    total_gastado: Decimal = Decimal('0.00')

    class Config:
        from_attributes = True
