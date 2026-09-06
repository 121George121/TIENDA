# ==============================================================================
# CU1 - GESTIONAR AUTENTICACION -> CAPA MODELO
# Ubicacion: backend/app/models/cu1_gestionar_autenticacion/usuario_rol_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class RolModel(Base):
    __tablename__ = "rol"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    usuarios = relationship("UsuarioModel", back_populates="rol")


class UsuarioModel(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    passwordhash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    rolid = Column(Integer, ForeignKey("rol.id"), nullable=True)
    sucursalid = Column(Integer, ForeignKey("sucursal.id"), nullable=True)
    activo = Column(Boolean, default=True)
    verificado = Column(Boolean, default=False)
    codigoverificacion = Column(String(255), nullable=True)
    codigoexpiracion = Column(DateTime, nullable=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)

    rol = relationship("RolModel", back_populates="usuarios")
    sucursal = relationship("SucursalModel", back_populates="usuarios")

    @property
    def created_at(self):
        return self.fechacreacion

    @property
    def rol_id(self):
        return self.rolid
