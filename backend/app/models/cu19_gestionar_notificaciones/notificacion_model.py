# ==============================================================================
# CU19 - GESTIONAR NOTIFICACIONES -> CAPA MODELO (MVC - MODEL)
# Ubicación: backend/app/models/cu19_gestionar_notificaciones/notificacion_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base


class NotificacionModel(Base):
    __tablename__ = "notificacion"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=True, index=True)
    titulo = Column(String(150), nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50), default="INFO")  # RESERVA_EXPIRANDO, PAGO_EXITOSO, STOCK_CRITICO, INFO
    leido = Column(Boolean, default=False)
    enlace = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
