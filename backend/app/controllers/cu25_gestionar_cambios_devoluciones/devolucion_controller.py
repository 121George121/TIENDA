# ==============================================================================
# CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu25_gestionar_cambios_devoluciones/devolucion_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.services.cu25_gestionar_cambios_devoluciones.devolucion_service import DevolucionService


class DevolucionController:

    @staticmethod
    def procesar_devolucion(
        db: Session,
        tenant_id: int,
        venta_id: int,
        cliente_id: Optional[int],
        usuario_id: Optional[int],
        sucursal_id: int,
        tipo_devolucion: str,
        motivo: str,
        monto_reembolso: float,
        items: List[Dict[str, Any]]
    ) -> Any:
        return DevolucionService.solicitar_devolucion(
            db=db,
            tenant_id=tenant_id,
            venta_id=venta_id,
            cliente_id=cliente_id,
            usuario_id=usuario_id,
            sucursal_id=sucursal_id,
            tipo_devolucion=tipo_devolucion,
            motivo=motivo,
            monto_reembolso=monto_reembolso,
            items=items
        )

    @staticmethod
    def listar_devoluciones(db: Session, tenant_id: int, sucursal_id: Optional[int] = None) -> List[Any]:
        return DevolucionService.listar_devoluciones(db, tenant_id, sucursal_id)
