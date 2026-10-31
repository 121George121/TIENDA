# ==============================================================================
# CU25 - ESQUEMAS PACKAGE INIT
# ==============================================================================

from .devolucion_schema import (
    ItemDevolucionRequest,
    SolicitudDevolucionRequest,
    ValidarVentaDevolucionResponse,
    DetalleDevolucionItemResponse,
    DevolucionResponse,
    DevolucionKpisResponse
)

__all__ = [
    "ItemDevolucionRequest",
    "SolicitudDevolucionRequest",
    "ValidarVentaDevolucionResponse",
    "DetalleDevolucionItemResponse",
    "DevolucionResponse",
    "DevolucionKpisResponse"
]
