# ==============================================================================
# CU26 - GESTIONAR BITACORA Y AUDITORIA -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu26_gestionar_bitacora/bitacora_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database import Base


def get_bolivia_now():
    """Retorna la fecha y hora actual en la zona horaria de Bolivia (BOT, UTC-4)"""
    return datetime.now(timezone(timedelta(hours=-4))).replace(tzinfo=None)


class Bitacora(Base):
    """
    Entidad de persistencia para el registro inmutable de auditoría (Bitácora - CU26).
    Registra operaciones críticas, cambios de estado, accesos e información contextual.
    """
    __tablename__ = "bitacora"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, default=1, index=True)
    usuarioid = Column(Integer, ForeignKey("usuario.id", ondelete="SET NULL"), nullable=True, index=True)
    accion = Column(String(50), nullable=False, index=True)  # LOGIN, LOGOUT, CREAR, MODIFICAR, ELIMINAR, etc.
    modulo = Column(String(50), nullable=False, index=True)  # AUTENTICACION, USUARIOS, ROLES, PRODUCTOS, etc.
    detalle = Column(Text, nullable=True)
    ip = Column(String(45), nullable=True)
    fechahora = Column(DateTime, default=get_bolivia_now, nullable=False, index=True)
    datosprevios = Column(Text, nullable=True)   # JSON string snapshot previo
    datosnuevos = Column(Text, nullable=True)    # JSON string snapshot nuevo

    # Relación con Usuario (permite obtener nombre, email y rol del operador)
    usuario = relationship("Usuario", foreign_keys=[usuarioid])

    __table_args__ = (
        Index("ix_bitacora_modulo_fechahora", "modulo", "fechahora"),
        Index("ix_bitacora_accion_fechahora", "accion", "fechahora"),
    )


BitacoraModel = Bitacora
bitacora = Bitacora

__all__ = ["Bitacora", "BitacoraModel", "bitacora", "get_bolivia_now"]
