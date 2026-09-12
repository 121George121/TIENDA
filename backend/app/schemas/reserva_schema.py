from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ReservaDetalleResponse(BaseModel):
    variante_id: int
    producto_nombre: str
    talla: Optional[str] = None
    color: Optional[str] = None
    codigo_hex: Optional[str] = None
    imagen_url: Optional[str] = None
    precio_unitario: float
    cantidad: int
    subtotal: float

    class Config:
        from_attributes = True


class ReservaSucursalResponse(BaseModel):
    id: int
    nombre: str
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None

    class Config:
        from_attributes = True


class ReservaResponse(BaseModel):
    id: int
    codigo_reserva: str
    fecha_reserva: datetime
    estado: str
    observaciones: Optional[str] = None
    sucursal: Optional[ReservaSucursalResponse] = None
    detalles: List[ReservaDetalleResponse] = []
    total_items: int = 0
    total_estimado: float = 0.0

    class Config:
        from_attributes = True


class ReservaCreate(BaseModel):
    sucursal_id: Optional[int] = None
    observaciones: Optional[str] = None


class CancelarReservaRequest(BaseModel):
    motivo: Optional[str] = None
