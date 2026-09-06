# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Gestión de Usuarios (CRUD, Cambio de Estado, Asignación de Rol)
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import UsuarioModel, RolModel
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
    def create(db: Session, user_data: UsuarioAdminCreate):
        existente = db.query(UsuarioModel).filter(UsuarioModel.email == user_data.email).first()
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")

        hashed_pwd = get_password_hash(user_data.password)
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
        return nuevo_usuario

    @staticmethod
    def update(db: Session, user_id: int, user_data: UsuarioUpdate):
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
        return user

    @staticmethod
    def toggle_status(db: Session, user_id: int, activo: bool):
        user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        user.activo = activo
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def assign_role(db: Session, user_id: int, rol_id: int):
        user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        rol = db.query(RolModel).filter(RolModel.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")

        user.rolid = rol_id
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int):
        user = db.query(UsuarioModel).filter(UsuarioModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        db.delete(user)
        db.commit()
        return {"message": "Usuario eliminado correctamente"}

