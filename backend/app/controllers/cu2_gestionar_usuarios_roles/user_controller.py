# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Gestión de Usuarios (CRUD, Cambio de Estado, Asignación de Rol)
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import (
    UsuarioModel, RolModel, ClienteModel, VentaModel, 
    MovimientoInventarioModel, ReservaModel, ReservaDetalleModel, 
    CarritoModel, CarritoItemModel, NotificacionModel
)
from app.schemas.schemas import UsuarioAdminCreate, UsuarioUpdate
from app.core.security import get_password_hash
from fastapi import HTTPException, status
from typing import Optional

class UserController:

    @staticmethod
    def get_all(db: Session, search: Optional[str] = None, rol_id: Optional[int] = None, activo: Optional[bool] = None, skip: int = 0, limit: int = 100):
        query = db.query(UsuarioModel)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (UsuarioModel.nombre.ilike(search_pattern)) |
                (UsuarioModel.apellido.ilike(search_pattern)) |
                (UsuarioModel.email.ilike(search_pattern))
            )
        
        if rol_id is not None:
            query = query.filter(UsuarioModel.rolid == rol_id)
            
        if activo is not None:
            query = query.filter(UsuarioModel.activo == activo)

        return query.order_by(UsuarioModel.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return user

    @staticmethod
    def create(db: Session, user_data: UsuarioAdminCreate, operador_id: Optional[int] = None):
        existente = db.query(UsuarioModel).filter(UsuarioModel.email == user_data.email).first()
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")

        password_plano = user_data.password.strip() if (user_data.password and user_data.password.strip()) else "usuario123."
        hashed_pwd = get_password_hash(password_plano)
        nuevo_usuario = UsuarioModel(
            nombre=user_data.nombre,
            apellido=user_data.apellido,
            email=user_data.email,
            passwordhash=hashed_pwd,
            telefono=user_data.telefono,
            rolid=user_data.rol_id,
            activo=user_data.activo if user_data.activo is not None else True
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR",
                modulo="USUARIOS",
                usuario_id=operador_id or nuevo_usuario.id,
                detalle=f"Creación de usuario: {nuevo_usuario.nombre} ({nuevo_usuario.email})",
                datos_nuevos={"nombre": nuevo_usuario.nombre, "email": nuevo_usuario.email, "rol_id": nuevo_usuario.rolid}
            )
        except Exception:
            pass

        # Nota: No se envía ningún correo de restablecimiento de contraseña al crear el usuario.
        return nuevo_usuario

    @staticmethod
    def update(db: Session, user_id: int, user_data: UsuarioUpdate, operador_id: Optional[int] = None):
        user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        if user_data.email and user_data.email != user.email:
            existente = db.query(UsuarioModel).filter(UsuarioModel.email == user_data.email).first()
            if existente:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado por otro usuario")
            user.email = user_data.email

        if user_data.nombre is not None:
            user.nombre = user_data.nombre
        if user_data.apellido is not None:
            user.apellido = user_data.apellido
        if user_data.telefono is not None:
            user.telefono = user_data.telefono
        if user_data.rol_id is not None:
            user.rolid = user_data.rol_id
        if user_data.activo is not None:
            user.activo = user_data.activo

        db.commit()
        db.refresh(user)

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="MODIFICAR",
                modulo="USUARIOS",
                usuario_id=operador_id or user.id,
                detalle=f"Actualización de datos del usuario: {user.nombre} ({user.email})",
                datos_nuevos={"nombre": user.nombre, "email": user.email, "rol_id": user.rolid, "activo": user.activo}
            )
        except Exception:
            pass

        return user

    @staticmethod
    def toggle_status(db: Session, user_id: int, activo: bool, operador_id: Optional[int] = None):
        user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        user.activo = activo
        db.commit()
        db.refresh(user)

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO",
                modulo="USUARIOS",
                usuario_id=operador_id or user.id,
                detalle=f"Cambio de estado del usuario {user.email} a {'Activo' if activo else 'Inactivo'}",
                datos_nuevos={"activo": activo}
            )
        except Exception:
            pass

        return user

    @staticmethod
    def assign_role(db: Session, user_id: int, rol_id: int, operador_id: Optional[int] = None):
        user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        rol = db.query(RolModel).filter(RolModel.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")

        user.rolid = rol_id
        db.commit()
        db.refresh(user)

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ROL",
                modulo="USUARIOS",
                usuario_id=operador_id or user.id,
                detalle=f"Asignación de nuevo rol {rol.nombre} al usuario {user.email}",
                datos_nuevos={"rol_id": rol_id, "rol_nombre": rol.nombre}
            )
        except Exception:
            pass

        return user

    @staticmethod
    def delete(db: Session, user_id: int):
        user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        # 1. Verificar si tiene ventas como vendedor/cajero o como cliente
        cliente = db.query(ClienteModel).filter(ClienteModel.usuarioid == user_id).first()
        cliente_id = cliente.id if cliente else -1

        ventas_count = db.query(VentaModel).filter(
            (VentaModel.usuarioid == user_id) | (VentaModel.clienteid == cliente_id)
        ).count()
        if ventas_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar permanentemente este usuario porque tiene ventas o compras registradas. Se recomienda desactivar su acceso en su lugar."
            )

        # 2. Verificar si tiene movimientos de inventario registrados para auditoría
        movs_count = db.query(MovimientoInventarioModel).filter(MovimientoInventarioModel.usuarioid == user_id).count()
        if movs_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar este usuario porque tiene movimientos de inventario registrados. Se recomienda desactivar su acceso en su lugar."
            )

        # 3. Eliminar reservas asociadas (y sus detalles)
        reservas = db.query(ReservaModel).filter(
            (ReservaModel.clienteid == user_id) | ((ReservaModel.clienteid == cliente_id) if cliente else False)
        ).all()
        for res in reservas:
            db.query(ReservaDetalleModel).filter(ReservaDetalleModel.reservaid == res.id).delete()
            db.delete(res)

        # 4. Eliminar carritos y sus items
        carritos = db.query(CarritoModel).filter(CarritoModel.clienteid == user_id).all()
        for car in carritos:
            db.query(CarritoItemModel).filter(CarritoItemModel.carritoid == car.id).delete()
            db.delete(car)

        # 5. Eliminar notificaciones
        db.query(NotificacionModel).filter(NotificacionModel.usuario_id == user_id).delete()

        # 6. Eliminar perfil en tabla cliente
        if cliente:
            db.delete(cliente)

        # 7. Eliminar usuario definitivamente
        db.delete(user)
        db.commit()
        return {"message": "Usuario eliminado correctamente"}

