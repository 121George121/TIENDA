# ==============================================================================
# CU26 - GESTIONAR BITÁCORA Y AUDITORÍA -> SERVICIO (MVC - SERVICE)
# Ubicación: backend/app/services/cu26_gestionar_bitacora/bitacora_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from app.models.cu26_gestionar_bitacora.bitacora_model import BitacoraModel
from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController as LegacyBitacoraController


class BitacoraService:
    """
    Servicio de auditoría del sistema: registro de eventos, consultas multi-criterio y exportación.
    """

    @staticmethod
    def registrar_evento(
        db: Session,
        usuario_id: Optional[int],
        accion: str,
        tabla: str,
        registro_id: Optional[int] = None,
        valores_anteriores: Optional[Any] = None,
        valores_nuevos: Optional[Any] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        tenant_id: int = 1
    ) -> BitacoraModel:
        return LegacyBitacoraController.registrar_evento(
            db=db,
            usuario_id=usuario_id,
            accion=accion,
            tabla=tabla,
            registro_id=registro_id,
            valores_anteriores=valores_anteriores,
            valores_nuevos=valores_nuevos,
            ip_address=ip_address,
            user_agent=user_agent,
            tenant_id=tenant_id
        )

    @staticmethod
    def listar_bitacora(
        db: Session,
        tenant_id: int,
        limite: int = 50,
        offset: int = 0,
        modulo: Optional[str] = None,
        accion: Optional[str] = None
    ) -> Dict[str, Any]:
        return LegacyBitacoraController.listar(
            db=db,
            limit=limite,
            offset=offset,
            modulo=modulo,
            accion=accion,
            tenant_id=tenant_id
        )

