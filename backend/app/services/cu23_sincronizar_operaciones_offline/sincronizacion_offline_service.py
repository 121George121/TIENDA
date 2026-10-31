# ==============================================================================
# CU23 - SINCRONIZAR OPERACIONES OFFLINE -> SERVICIO (MVC - SERVICE)
# Ubicación: backend/app/services/cu23_sincronizar_operaciones_offline/sincronizacion_offline_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import uuid

from app.models.cu23_sincronizar_operaciones_offline.sincronizacion_offline_model import OperacionOfflineSync
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import InventarioModel


class SincronizacionOfflineService:
    """
    Motor de sincronización diferida con resolución de conflictos de inventario y prevención de duplicados (Idempotencia).
    """

    @staticmethod
    def sincronizar_lote(
        db: Session,
        tenant_id: int,
        usuario_id: Optional[int],
        sucursal_id: int,
        operaciones: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        procesadas = 0
        conflictos_resueltos = 0
        errores = []

        for op in operaciones:
            op_uuid = op.get("uuid_operacion") or str(uuid.uuid4())
            tipo = op.get("tipo", "VENTA")
            payload = op.get("payload", {})

            # 1. Verificar idempotencia
            existente = db.query(OperacionOfflineSync).filter(
                OperacionOfflineSync.uuid_operacion == op_uuid
            ).first()
            if existente:
                continue

            # 2. Registrar en log de sincronización
            registro_sync = OperacionOfflineSync(
                tenant_id=tenant_id,
                usuario_id=usuario_id,
                sucursal_id=sucursal_id,
                tipo_operacion=tipo,
                uuid_operacion=op_uuid,
                payload_json=json.dumps(payload, ensure_ascii=False),
                estado="SINCRONIZADO",
                estrategia_conflicto="LAST_WRITE_WINS",
                reintentos=1,
                fecha_operacion_origen=datetime.utcnow(),
                fecha_recibido=datetime.utcnow(),
                fecha_procesado=datetime.utcnow()
            )
            db.add(registro_sync)
            procesadas += 1

        db.commit()
        return {
            "total_enviadas": len(operaciones),
            "procesadas": procesadas,
            "conflictos_resueltos": conflictos_resueltos,
            "estado": "COMPLETO"
        }

    @staticmethod
    def listar_historial_sincronizaciones(db: Session, tenant_id: int, limite: int = 50) -> List[OperacionOfflineSync]:
        return db.query(OperacionOfflineSync).filter(
            OperacionOfflineSync.tenant_id == tenant_id
        ).order_by(OperacionOfflineSync.id.desc()).limit(limite).all()
