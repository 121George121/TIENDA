# ==============================================================================
# CU23 - SINCRONIZAR OPERACIONES OFFLINE -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu23_sincronizar_operaciones_offline/sincronizacion_offline_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu23_sincronizar_operaciones_offline.sincronizacion_offline_controller import SincronizacionOfflineController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel

router = APIRouter(prefix="/sincronizacion-offline", tags=["CU23 - Sincronización Offline"])


class SyncLoteRequest(BaseModel):
    sucursal_id: int
    operaciones: List[Dict[str, Any]]


@router.post("/lote", summary="Enviar lote de operaciones generadas offline para sincronización")
def sincronizar_lote(
    req: SyncLoteRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    resultado = SincronizacionOfflineController.sincronizar_lote(
        db=db,
        tenant_id=tenant_id,
        usuario_id=current_user.id,
        sucursal_id=req.sucursal_id,
        operaciones=req.operaciones
    )
    return {"exito": True, "resultado": resultado}


@router.get("/historial", summary="Consultar log de sincronizaciones y resolución de conflictos")
def listar_historial_sync(
    limite: int = 50,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    logs = SincronizacionOfflineController.listar_historial(db, tenant_id, limite)
    return {"exito": True, "logs": logs}
