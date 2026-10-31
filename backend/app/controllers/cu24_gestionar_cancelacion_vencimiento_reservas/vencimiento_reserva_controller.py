# ==============================================================================
# CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento_reserva_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List

from app.services.cu24_gestionar_cancelacion_vencimiento_reservas.vencimiento_reserva_service import VencimientoReservaService


class VencimientoReservaController:
    """
    Controlador MVC para la gestión de auditoría de 48h, vencimiento automático y cancelación de reservas.
    """

    @staticmethod
    def purgar_reservas_vencidas(
        db: Session,
        tenant_id: int,
        horas_limite: int = 48,
        sucursal_id: Optional[int] = None,
        usuario_ejecutor_id: Optional[int] = None
    ) -> Dict[str, Any]:
        return VencimientoReservaService.cancelar_reservas_vencidas(
            db=db,
            tenant_id=tenant_id,
            horas_limite=horas_limite,
            sucursal_id=sucursal_id,
            usuario_ejecutor_id=usuario_ejecutor_id
        )

    @staticmethod
    def cancelar_reserva(
        db: Session,
        reserva_id: int,
        tenant_id: int,
        motivo: str,
        usuario_id: Optional[int] = None
    ) -> Optional[Any]:
        return VencimientoReservaService.cancelar_reserva_manual(
            db=db,
            reserva_id=reserva_id,
            tenant_id=tenant_id,
            motivo=motivo,
            usuario_id=usuario_id
        )

    @staticmethod
    def listar_reservas_activas(
        db: Session,
        tenant_id: int,
        sucursal_id: Optional[int] = None,
        horas_politica: int = 48
    ) -> List[Dict[str, Any]]:
        return VencimientoReservaService.listar_reservas_activas(
            db=db,
            tenant_id=tenant_id,
            sucursal_id=sucursal_id,
            horas_politica=horas_politica
        )

    @staticmethod
    def obtener_kpis(
        db: Session,
        tenant_id: int,
        horas_politica: int = 48
    ) -> Dict[str, Any]:
        return VencimientoReservaService.obtener_kpis(
            db=db,
            tenant_id=tenant_id,
            horas_politica=horas_politica
        )
