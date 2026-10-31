# ==============================================================================
# CU23 - SINCRONIZAR OPERACIONES OFFLINE -> ESQUEMAS PYDANTIC (MVC)
# Ubicación: backend/app/schemas/cu23_sincronizar_operaciones_offline/sincronizacion_offline_schema.py
# ==============================================================================

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SyncOperacionItem(BaseModel):
    uuid_operacion: str = Field(..., description="UUID único de la operación offline")
    tipo: str = Field("VENTA", description="Tipo de operación (VENTA, COBRO, AJUSTE_STOCK)")
    sucursal_id: int = Field(..., description="ID de la sucursal de origen")
    payload: Dict[str, Any] = Field(..., description="Datos de la transacción offline")
    fecha_operacion: Optional[datetime] = Field(None, description="Fecha de origen")


class SyncLoteRequest(BaseModel):
    sucursal_id: int = Field(..., description="ID de la sucursal de donde provienen las operaciones")
    estrategia_preferida: str = Field(
        "PRIORIZAR_TIENDA_FISICA",
        description="Estrategia en caso de conflicto de inventario (PRIORIZAR_TIENDA_FISICA, AJUSTE_KARDEX, BLOQUEAR)"
    )
    operaciones: List[SyncOperacionItem] = Field(..., description="Lista de transacciones en cola offline")


class SincronizarPendientesRequest(BaseModel):
    sucursal_id: Optional[int] = Field(None, description="Filtrar por sucursal específica o todas")
    estrategia_preferida: str = Field(
        "PRIORIZAR_TIENDA_FISICA",
        description="Política para resolver conflictos de stock (PRIORIZAR_TIENDA_FISICA, AJUSTE_KARDEX)"
    )


class SyncResultadoOperacion(BaseModel):
    uuid_operacion: str
    tipo: str
    estado: str  # SINCRONIZADO, CONFLICTO_RESUELTO, ERROR, DUPLICADO_IGNORADO
    mensaje: str
    venta_id: Optional[int] = None
    nro_recibo: Optional[str] = None
    conflicto_detectado: bool = False
    estrategia_aplicada: Optional[str] = None


class SyncLoteResponse(BaseModel):
    total: int
    procesadas: int
    sincronizadas: int
    conflictos_resueltos: int
    errores: int
    resultados: List[SyncResultadoOperacion]


class SyncLogResponse(BaseModel):
    id: int
    tenant_id: int
    usuario_id: Optional[int] = None
    usuario_nombre: Optional[str] = None
    sucursal_id: int
    sucursal_nombre: Optional[str] = None
    tipo_operacion: str
    uuid_operacion: str
    estado: str
    estrategia_conflicto: Optional[str] = None
    reintentos: int
    error_detalle: Optional[str] = None
    fecha_operacion_origen: datetime
    fecha_recibido: Optional[datetime] = None
    fecha_procesado: Optional[datetime] = None
    payload: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class SyncKpisResponse(BaseModel):
    total_operaciones: int
    sincronizadas: int
    conflictos_resueltos: int
    errores: int
    cobros_pendientes_en_cola: int
    monto_pendiente_en_cola: float
    estado_motor: str


class ResolverConflictoRequest(BaseModel):
    estrategia: str = Field(
        "PRIORIZAR_TIENDA_FISICA",
        description="Estrategia seleccionada (PRIORIZAR_TIENDA_FISICA, AJUSTE_KARDEX, DESCARTAR)"
    )
    notas: Optional[str] = Field(None, description="Justificación de la resolución de la discrepancia")
