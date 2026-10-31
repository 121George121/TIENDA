# ==============================================================================
# CU26 - GESTIONAR BITÁCORA Y AUDITORÍA -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu26_gestionar_bitacora/bitacora_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel

router = APIRouter(prefix="/bitacora-audit", tags=["CU26 - Bitácora y Auditoría"])


@router.get("/", summary="Consultar registros de la bitácora de auditoría")
def consultar_bitacora(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    modulo: Optional[str] = None,
    accion: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return BitacoraController.consultar_bitacora(
        db=db,
        tenant_id=tenant_id,
        limite=limit,
        offset=offset,
        modulo=modulo,
        accion=accion
    )
