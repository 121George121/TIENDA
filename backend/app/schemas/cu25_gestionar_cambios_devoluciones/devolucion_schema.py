# ==============================================================================
# CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> ESQUEMAS PYDANTIC (MVC)
# Ubicación: backend/app/schemas/cu25_gestionar_cambios_devoluciones/devolucion_schema.py
# ==============================================================================

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ItemDevolucionRequest(BaseModel):
    variante_devuelta_id: int = Field(..., description="ID de la variante que el cliente regresa")
    variante_nueva_id: Optional[int] = Field(None, description="ID de la variante nueva en caso de cambio de talla/modelo")
    cantidad: int = Field(1, ge=1, description="Cantidad de prendas devueltas")
    precio_unitario: float = Field(0.0, ge=0, description="Precio unitario original")
    subtotal: float = Field(0.0, ge=0, description="Subtotal de la prenda devuelta")
    estado_prenda: str = Field("PERFECTO_ESTADO", description="PERFECTO_ESTADO, DEFECTUOSO_FABRICA, DAÑADO")


class SolicitudDevolucionRequest(BaseModel):
    venta_id: int = Field(..., description="ID de la venta original")
    sucursal_id: int = Field(..., description="Sucursal donde se realiza el cambio/devolución")
    cliente_id: Optional[int] = Field(None, description="ID del cliente")
    tipo_devolucion: str = Field(
        "CAMBIO_TALLA",
        description="CAMBIO_TALLA, CAMBIO_PRENDA, REEMBOLSO_TOTAL, NOTA_CREDITO"
    )
    motivo: str = Field(..., min_length=3, max_length=500, description="Justificación detallada")
    monto_reembolso: float = Field(0.0, ge=0, description="Monto en efectivo o nota de crédito a devolver")
    items: List[ItemDevolucionRequest] = Field(..., min_items=1, description="Lista de prendas devueltas o cambiadas")


class ValidarVentaDevolucionResponse(BaseModel):
    venta_valida: bool
    venta_id: int
    codigoventa: str
    fecha_venta: datetime
    dias_transcurridos: int
    dentro_de_plazo: bool
    plazo_maximo_dias: int
    cliente_nombre: str
    sucursal_nombre: str
    total_venta: float
    items_comprados: List[Dict[str, Any]]
    mensaje: Optional[str] = None


class DetalleDevolucionItemResponse(BaseModel):
    id: int
    variante_devuelta_id: int
    variante_devuelta_sku: Optional[str] = None
    producto_devuelto_nombre: str
    talla_devuelta: Optional[str] = None
    color_devuelto: Optional[str] = None
    variante_nueva_id: Optional[int] = None
    variante_nueva_sku: Optional[str] = None
    producto_nuevo_nombre: Optional[str] = None
    talla_nueva: Optional[str] = None
    color_nuevo: Optional[str] = None
    cantidad: int
    precio_unitario: float
    subtotal: float
    estado_prenda: str

    class Config:
        from_attributes = True


class DevolucionResponse(BaseModel):
    id: int
    codigo_devolucion: str
    tenant_id: int
    venta_id: int
    codigoventa: Optional[str] = None
    cliente_id: Optional[int] = None
    cliente_nombre: Optional[str] = None
    usuario_id: Optional[int] = None
    usuario_nombre: Optional[str] = None
    sucursal_id: int
    sucursal_nombre: Optional[str] = None
    tipo_devolucion: str
    motivo: str
    estado: str
    monto_reembolso: float
    reingreso_inventario: bool
    fecha_solicitud: datetime
    fecha_resolucion: Optional[datetime] = None
    detalles: List[DetalleDevolucionItemResponse] = []

    class Config:
        from_attributes = True


class DevolucionKpisResponse(BaseModel):
    total_operaciones: int
    cambios_talla_prenda: int
    reembolsos_notas_credito: int
    prendas_aptas_reincorporadas: int
    prendas_baja_defecto: int
    monto_total_reembolsado_bob: float
    plazo_garantia_dias: int
