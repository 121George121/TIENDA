# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Autenticación, Registro de Usuarios y Hashing de contraseñas
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import UsuarioModel
from app.schemas.schemas import UsuarioCreate
from fastapi import HTTPException, status
import hashlib

class AuthController:

    @staticmethod
    def _hash_password(password: str) -> str:
        """Genera un hash SHA256 simple para propósitos académicos"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(db: Session, user_data: UsuarioCreate):
        """Registra un nuevo usuario en el sistema"""
        usuario_existente = db.query(UsuarioModel).filter(UsuarioModel.email == user_data.email).first()
        if usuario_existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")

        hashed_pwd = AuthController._hash_password(user_data.password)
        nuevo_usuario = UsuarioModel(
            nombre=user_data.nombre,
            email=user_data.email,
            password_hash=hashed_pwd
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def login_user(db: Session, email: str, password: str):
        """Valida credenciales y retorna el usuario autenticado"""
        hashed_pwd = AuthController._hash_password(password)
        usuario = db.query(UsuarioModel).filter(
            UsuarioModel.email == email,
            UsuarioModel.password_hash == hashed_pwd,
            UsuarioModel.activo == True
        ).first()

        if not usuario:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
        
        return usuario
