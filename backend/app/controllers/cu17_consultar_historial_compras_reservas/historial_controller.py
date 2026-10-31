# ==============================================================================
# CU17 - CONSULTAR HISTORIAL DE COMPRAS Y RESERVAS -> CAPA CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu17_consultar_historial_compras_reservas/historial_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.services.cu17_consultar_historial_compras_reservas.historial_service import HistorialService


class HistorialController:

    @staticmethod
    def obtener_resumen_cliente(
        db: Session,
        current_user: UsuarioModel,
        tenant_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """CU17: Retorna indicadores clave del cliente para su panel de compras y reservas."""
        return HistorialService.obtener_resumen_cliente(db=db, current_user=current_user, tenant_id=tenant_id)

    @staticmethod
    def listar_compras_cliente(
        db: Session,
        current_user: UsuarioModel,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU17: Retorna el historial completo de compras con detalles, items y estado de entrega."""
        return HistorialService.listar_compras_cliente(db=db, current_user=current_user, tenant_id=tenant_id)

    @staticmethod
    def listar_reservas_cliente(
        db: Session,
        current_user: UsuarioModel,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU17: Retorna el historial de reservas de prendas con QR para retiro en tienda y tiempo restante."""
        return HistorialService.listar_reservas_cliente(db=db, current_user=current_user, tenant_id=tenant_id)
