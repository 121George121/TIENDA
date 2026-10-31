# ==============================================================================
# CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu22_registrar_cobros_contado_offline/cobro_offline_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Optional, Any

from app.services.cu22_registrar_cobros_contado_offline.cobro_offline_service import CobroOfflineService


class CobroOfflineController:

    @staticmethod
    def registrar_cobro(
        db: Session,
        tenant_id: int,
        cajero_id: Optional[int],
        sucursal_id: int,
        monto: float,
        nro_recibo_provisional: str,
        uuid_operacion: Optional[str] = None,
        cliente_nombre: Optional[str] = None,
        cliente_nit: Optional[str] = None,
        observaciones: Optional[str] = None
    ) -> Any:
        return CobroOfflineService.registrar_cobro_offline(
            db=db,
            tenant_id=tenant_id,
            cajero_id=cajero_id,
            sucursal_id=sucursal_id,
            monto=monto,
            nro_recibo_provisional=nro_recibo_provisional,
            uuid_operacion=uuid_operacion,
            cliente_nombre=cliente_nombre,
            cliente_nit=cliente_nit,
            observaciones=observaciones
        )

    @staticmethod
    def listar_pendientes(db: Session, tenant_id: int, sucursal_id: Optional[int] = None) -> List[Any]:
        return CobroOfflineService.listar_pendientes(db, tenant_id, sucursal_id)
