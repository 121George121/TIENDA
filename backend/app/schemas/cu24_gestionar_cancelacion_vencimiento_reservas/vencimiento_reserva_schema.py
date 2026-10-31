# ==============================================================================
# CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> ESQUEMAS PYDANTIC (MVC)
# Ubicación: backend/app/schemas/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento_reserva_schema.py
# ==============================================================================

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CancelarReservaRequest(BaseModel):
    motivo: str = Field(..., min_length=3, max_length=250, description="Motivo de la cancelación de la reserva")


class EjecutarPurgaRequest(BaseModel):
    horas_limite: int = Field(48, ge=1, le=720, description="Plazo máximo de tolerancia en horas (por defecto 48h)")
    sucursal_id: Optional[int] = Field(None, description="Filtrar por sucursal específica")


class PurgaVencimientoResponse(BaseModel):
    reservas_vencidas_canceladas: int
    prendas_liberadas_al_stock: int
    valor_monetario_liberado_bob: float
    fecha_ejecucion: str
    detalles: Optional[List[Dict[str, Any]]] = None


class ReservaPrendaDetalleDTO(BaseModel):
    variante_id: int
    sku: Optional[str] = None
    producto_nombre: str
    talla: Optional[str] = None
    color: Optional[str] = None
    cantidad: int
    precio_unitario: float
    subtotal: float


class ReservaExpiracionItemResponse(BaseModel):
    id: int
    codigoreserva: str
    fechareserva: datetime
    fecha_expiracion: datetime
    horas_restantes: float
    en_riesgo: bool  # True si quedan menos de 12 horas
    es_expirada: bool
    estado: str
    observaciones: Optional[str] = None
    sucursalid: int
    sucursal_nombre: str
    clienteid: int
    cliente_nombre: str
    cliente_email: Optional[str] = None
    total_prendas: int
    monto_total_estimado: float
    detalles: List[ReservaPrendaDetalleDTO]

    class Config:
        from_attributes = True


class VencimientoReservaKpisResponse(BaseModel):
    total_reservas_activas: int
    reservas_en_riesgo: int  # < 12 horas para expirar
    reservas_vencidas_historicas: int
    reservas_canceladas_manual: int
    total_prendas_reintegradas: int
    valor_total_liberado_bob: float
    horas_politica_defecto: int
