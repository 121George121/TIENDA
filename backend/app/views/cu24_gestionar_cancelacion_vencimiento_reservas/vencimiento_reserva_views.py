# ==============================================================================
# CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento_reserva_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu24_gestionar_cancelacion_vencimiento_reservas.vencimiento_reserva_controller import VencimientoReservaController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel

router = APIRouter(prefix="/vencimiento-reservas", tags=["CU24 - Vencimiento y Cancelación de Reservas"])


class CancelarReservaRequest(BaseModel):
    reserva_id: int
    motivo: str


@router.post("/cancelar-vencidas", summary="Ejecutar proceso de auditoría y liberación de stock de reservas vencidas (>48h)")
def ejecutar_cancelacion_vencidas(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    resultado = VencimientoReservaController.purgar_reservas_vencidas(db, tenant_id)
    return {"exito": True, "resultado": resultado}


@router.post("/cancelar-manual", summary="Cancelar reserva y retornar prendas al inventario")
def cancelar_reserva_manual(
    req: CancelarReservaRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    reserva = VencimientoReservaController.cancelar_reserva(db, req.reserva_id, tenant_id, req.motivo)
    if not reserva:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo cancelar la reserva especificada")
    return {"exito": True, "mensaje": "Reserva cancelada y stock liberado correctamente"}
