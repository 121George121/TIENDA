# ==============================================================================
# CU19 - GESTIONAR NOTIFICACIONES -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu19_gestionar_notificaciones/notificacion_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.controllers.cu19_gestionar_notificaciones.notificacion_controller import NotificacionController

router = APIRouter(prefix="/notificaciones", tags=["CU19 - Gestionar Notificaciones (Web y Móvil)"])


@router.get("", summary="Listar notificaciones del usuario (con detección de vencimientos y stock)")
def listar_notificaciones(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU19: Retorna lista de notificaciones activas para el usuario conectado."""
    return NotificacionController.listar_notificaciones(db=db, current_user=current_user)


@router.get("/contador", summary="Contar notificaciones no leídas para insignia/badge")
def contar_no_leidas(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU19: Retorna la cantidad de alertas no leídas."""
    conteo = NotificacionController.contar_no_leidas(db=db, current_user=current_user)
    return {"no_leidas": conteo}


@router.patch("/{notificacion_id}/leer", summary="Marcar una notificación como leída")
def marcar_leida(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU19: Actualiza el estado a leído = True."""
    ok = NotificacionController.marcar_como_leida(db=db, current_user=current_user, notificacion_id=notificacion_id)
    return {"exito": ok}


@router.post("/marcar-todas-leidas", summary="Marcar todas las notificaciones como leídas")
def marcar_todas(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU19: Marca todas las notificaciones pendientes como leídas."""
    ok = NotificacionController.marcar_todas_leidas(db=db, current_user=current_user)
    return {"exito": ok}
