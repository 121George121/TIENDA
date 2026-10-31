# ==============================================================================
# CU26 - GESTIONAR BITÁCORA Y AUDITORÍA -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu26_gestionar_bitacora/bitacora_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from app.services.cu26_gestionar_bitacora.bitacora_service import BitacoraService


class BitacoraController:

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
    ) -> Any:
        return BitacoraService.registrar_evento(
            db, usuario_id, accion, tabla, registro_id,
            valores_anteriores, valores_nuevos, ip_address, user_agent, tenant_id
        )

    @staticmethod
    def consultar_bitacora(
        db: Session,
        tenant_id: int = 1,
        limite: int = 50,
        offset: int = 0,
        modulo: Optional[str] = None,
        accion: Optional[str] = None
    ) -> Dict[str, Any]:
        return BitacoraService.listar_bitacora(
            db=db,
            tenant_id=tenant_id,
            limite=limite,
            offset=offset,
            modulo=modulo,
            accion=accion
        )
