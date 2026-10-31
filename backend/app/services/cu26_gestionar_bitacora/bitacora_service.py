# ==============================================================================
# CU26 - GESTIONAR BITACORA Y AUDITORIA -> CAPA SERVICIO (MVC - SERVICE)
# Ubicación: backend/app/services/cu26_gestionar_bitacora/bitacora_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.models.cu26_gestionar_bitacora.bitacora_model import BitacoraModel
from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController


class BitacoraService:
    """
    Servicio de auditoría del sistema para el registro y consulta de eventos (CU26).
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
    ) -> Optional[BitacoraModel]:
        return BitacoraController.registrar_evento(
            db=db,
            accion=accion,
            modulo=tabla,
            usuario_id=usuario_id,
            detalle=f"Registro ID: {registro_id}" if registro_id else None,
            ip=ip_address,
            datos_previos=valores_anteriores,
            datos_nuevos=valores_nuevos,
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
        return BitacoraController.listar(
            db=db,
            limit=limite,
            offset=offset,
            modulo=modulo,
            accion=accion,
            tenant_id=tenant_id
        )
