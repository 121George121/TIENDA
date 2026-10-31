# ==============================================================================
# CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento_reserva_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.services.cu24_gestionar_cancelacion_vencimiento_reservas.vencimiento_reserva_service import VencimientoReservaService


class VencimientoReservaController:

    @staticmethod
    def purgar_reservas_vencidas(db: Session, tenant_id: int) -> Dict[str, Any]:
        return VencimientoReservaService.cancelar_reservas_vencidas(db, tenant_id)

    @staticmethod
    def cancelar_reserva(db: Session, reserva_id: int, tenant_id: int, motivo: str) -> Optional[Any]:
        return VencimientoReservaService.cancelar_reserva_manual(db, reserva_id, tenant_id, motivo)
