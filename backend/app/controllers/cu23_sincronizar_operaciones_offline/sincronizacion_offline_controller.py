# ==============================================================================
# CU23 - SINCRONIZAR OPERACIONES OFFLINE -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu23_sincronizar_operaciones_offline/sincronizacion_offline_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.services.cu23_sincronizar_operaciones_offline.sincronizacion_offline_service import SincronizacionOfflineService


class SincronizacionOfflineController:

    @staticmethod
    def sincronizar_lote(
        db: Session,
        tenant_id: int,
        usuario_id: Optional[int],
        sucursal_id: int,
        operaciones: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return SincronizacionOfflineService.sincronizar_lote(
            db=db,
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            sucursal_id=sucursal_id,
            operaciones=operaciones
        )

    @staticmethod
    def listar_historial(db: Session, tenant_id: int, limite: int = 50) -> List[Any]:
        return SincronizacionOfflineService.listar_historial_sincronizaciones(db, tenant_id, limite)
