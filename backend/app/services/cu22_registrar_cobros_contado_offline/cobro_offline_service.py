# ==============================================================================
# CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> SERVICIO (MVC - SERVICE)
# Ubicación: backend/app/services/cu22_registrar_cobros_contado_offline/cobro_offline_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from app.models.cu22_registrar_cobros_contado_offline.cobro_offline_model import CobroOffline


class CobroOfflineService:
    """
    Servicio de caja para cobros de contado en contingencia / offline.
    Maneja recibos provisionales y vinculación diferida con ventas.
    """

    @staticmethod
    def registrar_cobro_offline(
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
    ) -> CobroOffline:
        op_uuid = uuid_operacion or str(uuid.uuid4())
        # Verificar idempotencia
        existente = db.query(CobroOffline).filter(CobroOffline.uuid_operacion == op_uuid).first()
        if existente:
            return existente

        nuevo_cobro = CobroOffline(
            tenant_id=tenant_id,
            cajero_id=cajero_id,
            sucursal_id=sucursal_id,
            monto=monto,
            moneda="BOB",
            nro_recibo_provisional=nro_recibo_provisional,
            uuid_operacion=op_uuid,
            cliente_nombre=cliente_nombre,
            cliente_nit=cliente_nit,
            observaciones=observaciones,
            fecha_cobro=datetime.utcnow(),
            sincronizado=False
        )
        db.add(nuevo_cobro)
        db.commit()
        db.refresh(nuevo_cobro)
        return nuevo_cobro

    @staticmethod
    def listar_pendientes(db: Session, tenant_id: int, sucursal_id: Optional[int] = None) -> List[CobroOffline]:
        q = db.query(CobroOffline).filter(
            CobroOffline.tenant_id == tenant_id,
            CobroOffline.sincronizado == False
        )
        if sucursal_id:
            q = q.filter(CobroOffline.sucursal_id == sucursal_id)
        return q.order_by(CobroOffline.id.desc()).all()
