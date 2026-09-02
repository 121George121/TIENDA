# ==============================================================================
# SCHEMAS DE VALIDACIÓN (PYDANTIC DTOs)
# Definen la forma de los datos que entran y salen de la API REST
# ==============================================================================

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- USUARIO ---
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse

# --- PRODUCTO ---
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria_id: Optional[int] = None
    imagen_url: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

# --- CATEGORIA ---
class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

# --- ORDEN DETALLE ---
class OrdenDetalleCreate(BaseModel):
    producto_id: int
    cantidad: int

class OrdenDetalleResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True

# --- ORDEN ---
class OrdenCreate(BaseModel):
    direccion_envio: str
    items: List[OrdenDetalleCreate]

class OrdenResponse(BaseModel):
    id: int
    usuario_id: int
    total: float
    estado: str
    direccion_envio: str
    created_at: datetime
    detalles: List[OrdenDetalleResponse]

    class Config:
        from_attributes = True
