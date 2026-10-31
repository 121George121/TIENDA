# ==============================================================================
# CU19 - GESTIONAR NOTIFICACIONES -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu19_gestionar_notificaciones/notificacion_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.services.cu19_gestionar_notificaciones.notificacion_service import NotificacionService


class NotificacionController:

    @staticmethod
    def listar_notificaciones(
        db: Session,
        current_user: UsuarioModel,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU19: Retorna la lista de notificaciones activas para el usuario conectado."""
        return NotificacionService.listar_notificaciones(db=db, current_user=current_user, tenant_id=tenant_id)

    @staticmethod
    def contar_no_leidas(
        db: Session,
        current_user: UsuarioModel,
        tenant_id: Optional[int] = None
    ) -> int:
        """CU19: Retorna la cantidad de notificaciones pendientes de lectura."""
        return NotificacionService.contar_no_leidas(db=db, current_user=current_user, tenant_id=tenant_id)

    @staticmethod
    def marcar_como_leida(
        db: Session,
        current_user: UsuarioModel,
        notificacion_id: int,
        tenant_id: Optional[int] = None
    ) -> bool:
        """CU19: Marca una notificación específica como leída."""
        return NotificacionService.marcar_como_leida(db=db, current_user=current_user, notificacion_id=notificacion_id, tenant_id=tenant_id)

    @staticmethod
    def marcar_todas_leidas(
        db: Session,
        current_user: UsuarioModel,
        tenant_id: Optional[int] = None
    ) -> bool:
        """CU19: Marca todas las notificaciones pendientes como leídas."""
        return NotificacionService.marcar_todas_leidas(db=db, current_user=current_user, tenant_id=tenant_id)

