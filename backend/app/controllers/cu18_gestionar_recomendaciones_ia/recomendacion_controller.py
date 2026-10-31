# ==============================================================================
# CU18 - GESTIONAR RECOMENDACIONES MEDIANTE IA -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu18_gestionar_recomendaciones_ia/recomendacion_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.services.cu18_gestionar_recomendaciones_ia.recomendacion_service import RecomendacionService


class RecomendacionController:

    @staticmethod
    def recomendar_outfit(
        db: Session,
        producto_id: Optional[int] = None,
        carrito_ids: Optional[List[int]] = None,
        limite: int = 3,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU18: Genera recomendaciones de outfit combinando prendas del catálogo."""
        return RecomendacionService.recomendar_outfit(
            db=db,
            producto_id=producto_id,
            carrito_ids=carrito_ids,
            limite=limite,
            tenant_id=tenant_id
        )

    @staticmethod
    def obtener_tendencias(
        db: Session,
        limite: int = 4,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU18: Retorna productos destacados en tendencia."""
        return RecomendacionService.obtener_tendencias(db=db, limite=limite, tenant_id=tenant_id)

    @staticmethod
    def recomendar_personalizado(
        db: Session,
        current_user: UsuarioModel,
        limite: int = 4,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU18: Genera recomendaciones a medida según el historial del cliente."""
        return RecomendacionService.recomendar_personalizado_cliente(
            db=db,
            current_user=current_user,
            limite=limite,
            tenant_id=tenant_id
        )

