# ==============================================================================
# CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu22_registrar_cobros_contado_offline/cobro_offline_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Optional, Any, Dict

from app.services.cu22_registrar_cobros_contado_offline.cobro_offline_service import CobroOfflineService
from app.schemas.cu22_registrar_cobros_contado_offline.cobro_offline_schema import CobroOfflineCreate


class CobroOfflineController:
    """
    Controlador de negocio para el registro de cobros de contado en contingencia offline (CU22).
    """

    @staticmethod
    def registrar_cobro(
        db: Session,
        tenant_id: int,
        cajero_id: Optional[int],
        data: CobroOfflineCreate
    ) -> Dict[str, Any]:
        return CobroOfflineService.registrar_cobro_offline(
            db=db,
            tenant_id=tenant_id,
            cajero_id=cajero_id,
            data=data
        )

    @staticmethod
    def listar_cobros(
        db: Session,
        tenant_id: int,
        sucursal_id: Optional[int] = None,
        solo_pendientes: bool = False
    ) -> List[Dict[str, Any]]:
        return CobroOfflineService.listar_cobros(
            db=db,
            tenant_id=tenant_id,
            sucursal_id=sucursal_id,
            solo_pendientes=solo_pendientes
        )

    @staticmethod
    def listar_pendientes(
        db: Session,
        tenant_id: int,
        sucursal_id: Optional[int] = None
    ) -> List[Any]:
        return CobroOfflineService.listar_pendientes(db, tenant_id, sucursal_id)

    @staticmethod
    def obtener_cobro(
        db: Session,
        cobro_id: int,
        tenant_id: int
    ) -> Optional[Dict[str, Any]]:
        return CobroOfflineService.obtener_cobro_por_id(db, cobro_id, tenant_id)

    @staticmethod
    def registrar_lote(
        db: Session,
        tenant_id: int,
        cajero_id: Optional[int],
        lote: List[CobroOfflineCreate]
    ) -> List[Dict[str, Any]]:
        return CobroOfflineService.registrar_lote_offline(db, tenant_id, cajero_id, lote)

    @staticmethod
    def obtener_kpis(
        db: Session,
        tenant_id: int,
        sucursal_id: Optional[int] = None
    ) -> Dict[str, Any]:
        return CobroOfflineService.obtener_kpis(db, tenant_id, sucursal_id)

    @staticmethod
    def marcar_sincronizado(
        db: Session,
        cobro_id: int,
        venta_id: Optional[int] = None
    ) -> Any:
        return CobroOfflineService.marcar_sincronizado(db, cobro_id, venta_id)
