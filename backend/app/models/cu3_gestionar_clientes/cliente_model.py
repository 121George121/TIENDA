# ==============================================================================
# CU3 - GESTIONAR CLIENTES -> CAPA MODELO
# Ubicacion: backend/app/models/cu3_gestionar_clientes/cliente_model.py
# ==============================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, event, select, insert
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel, RolModel


class ClienteModel(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=True)
    email = Column(String(150), nullable=True)
    telefono = Column(String(20), nullable=True)
    fechanac = Column(Date, nullable=True)
    genero = Column(String(30), nullable=True)
    activo = Column(Boolean, default=True)
    fecharegistro = Column(DateTime, default=datetime.utcnow)
    usuarioid = Column(Integer, ForeignKey("usuario.id"), nullable=True)

    usuario = relationship("UsuarioModel")


@event.listens_for(UsuarioModel, "after_insert")
def _crear_perfil_cliente(mapper, connection, target):
    """
    CU3: cada vez que se crea un usuario con rol "Cliente" -ya sea por
    auto-registro (CU1 - auth_controller.register_user) o alta desde el
    panel admin (CU3 - cliente_service.create)- se crea automáticamente su
    fila en la tabla `cliente` (perfil extendido: fechanac, genero). El
    cliente completa esos campos faltantes despues via PUT /clientes/me.
    """
    rol_nombre = connection.execute(
        select(RolModel.nombre).where(RolModel.id == target.rolid)
    ).scalar()

    if not rol_nombre or rol_nombre.strip().lower() != "cliente":
        return

    ya_existe = connection.execute(
        select(ClienteModel.id).where(ClienteModel.usuarioid == target.id)
    ).first()
    if ya_existe:
        return

    connection.execute(
        insert(ClienteModel).values(
            nombre=target.nombre,
            apellido=target.apellido,
            email=target.email,
            telefono=target.telefono,
            usuarioid=target.id,
            activo=True,
        )
    )
