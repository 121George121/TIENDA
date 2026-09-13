# ==============================================================================
# CU11 - ATENDER RESERVAS EN SUCURSAL -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu11_atender_reservas_sucursal/atencion_reserva_model.py
# ==============================================================================

from app.models.cu10_gestionar_reservas_prendas.reserva_model import (
    ReservaModel,
    ReservaDetalleModel,
)

__all__ = ["ReservaModel", "ReservaDetalleModel"]
