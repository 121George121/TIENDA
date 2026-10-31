# ==============================================================================
# CU23 - SINCRONIZAR OPERACIONES OFFLINE -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu23_sincronizar_operaciones_offline/sincronizacion_offline_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.services.cu23_sincronizar_operaciones_offline.sincronizacion_offline_service import SincronizacionOfflineService


class SincronizacionOfflineController:
    """
    Controlador MVC para el motor de sincronización offline y resolución de conflictos.
    """

    @staticmethod
    def sincronizar_pendientes(
        db: Session,
        tenant_id: int,
        usuario_id: Optional[int] = None,
        sucursal_id: Optional[int] = None,
        estrategia_preferida: str = "PRIORIZAR_TIENDA_FISICA"
    ) -> Dict[str, Any]:
        return SincronizacionOfflineService.sincronizar_cobros_offline_pendientes(
            db=db,
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            sucursal_id=sucursal_id,
            estrategia_preferida=estrategia_preferida
        )

    @staticmethod
    def sincronizar_lote(
        db: Session,
        tenant_id: int,
        usuario_id: Optional[int],
        sucursal_id: int,
        operaciones: List[Any],
        estrategia_preferida: str = "PRIORIZAR_TIENDA_FISICA"
    ) -> Dict[str, Any]:
        return SincronizacionOfflineService.sincronizar_lote(
            db=db,
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            sucursal_id=sucursal_id,
            operaciones=operaciones,
            estrategia_preferida=estrategia_preferida
        )

    @staticmethod
    def listar_historial(
        db: Session,
        tenant_id: int,
        limite: int = 50,
        estado: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return SincronizacionOfflineService.listar_historial_sincronizaciones(
            db=db,
            tenant_id=tenant_id,
            limite=limite,
            estado=estado
        )

    @staticmethod
    def obtener_kpis(db: Session, tenant_id: int) -> Dict[str, Any]:
        return SincronizacionOfflineService.obtener_kpis(db=db, tenant_id=tenant_id)

    @staticmethod
    def resolver_conflicto_manual(
        db: Session,
        tenant_id: int,
        usuario_id: int,
        sync_id: int,
        estrategia: str,
        notas: Optional[str] = None
    ) -> Dict[str, Any]:
        return SincronizacionOfflineService.resolver_conflicto_manual(
            db=db,
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            sync_id=sync_id,
            estrategia=estrategia,
            notas=notas
        )
