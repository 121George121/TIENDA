# ==============================================================================
# CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu22_registrar_cobros_contado_offline/cobro_offline_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu22_registrar_cobros_contado_offline.cobro_offline_controller import CobroOfflineController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel

router = APIRouter(prefix="/cobros-offline", tags=["CU22 - Cobros Contado Offline"])


class CobroOfflineRequest(BaseModel):
    sucursal_id: int
    monto: float
    nro_recibo_provisional: str
    uuid_operacion: Optional[str] = None
    cliente_nombre: Optional[str] = None
    cliente_nit: Optional[str] = None
    observaciones: Optional[str] = None


@router.post("/registrar", summary="Registrar cobro de contado generado en modo sin conexión")
def registrar_cobro_offline(
    req: CobroOfflineRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    cobro = CobroOfflineController.registrar_cobro(
        db=db,
        tenant_id=tenant_id,
        cajero_id=current_user.id,
        sucursal_id=req.sucursal_id,
        monto=req.monto,
        nro_recibo_provisional=req.nro_recibo_provisional,
        uuid_operacion=req.uuid_operacion,
        cliente_nombre=req.cliente_nombre,
        cliente_nit=req.cliente_nit,
        observaciones=req.observaciones
    )
    return {"exito": True, "cobro_offline": cobro}


@router.get("/pendientes", summary="Listar cobros de contado pendientes de sincronización")
def listar_cobros_pendientes(
    sucursal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    pendientes = CobroOfflineController.listar_pendientes(db, tenant_id, sucursal_id)
    return {"exito": True, "pendientes": pendientes}
