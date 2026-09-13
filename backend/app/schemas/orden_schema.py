# ==============================================================================
# CU14 - GESTIONAR ORDENES Y VENTAS -> CAPA ESQUEMA (MVC - SCHEMA / DTO)
# Ubicación: backend/app/schemas/orden_schema.py
# ==============================================================================

from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime


class OrdenItemCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(default=1, ge=1)
    variante_id: Optional[int] = None


class OrdenCreate(BaseModel):
    direccion_envio: Optional[str] = "Dirección de entrega"
    sucursal_id: Optional[int] = None
    items: List[OrdenItemCreate]


class DetalleVentaResponse(BaseModel):
    varianteid: int
    cantidad: int
    preciounitario: Decimal
    descuento: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class OrdenResponse(BaseModel):
    id: int
    codigoventa: str
    estado: str
    tipoventa: str
    subtotal: Decimal
    descuento: Decimal
    total: Decimal
    fecha: Optional[datetime] = None
    mensaje: str = "¡Orden procesada y registrada exitosamente!"

    class Config:
        from_attributes = True


class VentaPresencialCreate(BaseModel):
    sucursal_id: int = Field(..., description="ID de la sucursal donde se efectúa la venta")
    cliente_id: Optional[int] = Field(None, description="ID del cliente (opcional si es venta rápida)")
    cliente_nombre: Optional[str] = Field("Consumidor Final", description="Nombre del cliente para la factura/recibo")
    metodo_pago_id: int = Field(..., description="ID del método de pago (Efectivo, Tarjeta, QR)")
    monto_recibido: Optional[Decimal] = Field(None, description="Monto entregado en efectivo para cálculo de cambio")
    items: List[OrdenItemCreate]


class MetodoPagoResponse(BaseModel):
    id: int
    nombre: str
    estado: bool

    class Config:
        from_attributes = True


class VentaCompletaResponse(BaseModel):
    id: int
    codigoventa: str
    tipoventa: str
    estado: str
    subtotal: Decimal
    descuento: Decimal
    total: Decimal
    fecha: Optional[datetime] = None
    sucursalid: int
    sucursal_nombre: Optional[str] = None
    cliente_nombre: Optional[str] = None
    metodo_pago_nombre: Optional[str] = None
    cambio: Optional[Decimal] = Decimal("0.00")

    class Config:
        from_attributes = True


class VentaDetalleItemResponse(BaseModel):
    variante_id: int
    producto_nombre: str
    talla: Optional[str] = None
    color: Optional[str] = None
    cantidad: int
    preciounitario: Decimal
    descuento: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True

class VentaDetalladaResponse(VentaCompletaResponse):
    detalles: List[VentaDetalleItemResponse] = []

