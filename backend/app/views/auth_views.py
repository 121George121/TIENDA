# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Router de Autenticación y Registro
# ==============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import UsuarioCreate, UsuarioResponse, TokenResponse
from app.controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["Autenticacion (Vista API)"])

@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Registrar usuario")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Endpoint de registro de cliente"""
    return AuthController.register_user(db=db, user_data=usuario)

@router.post("/login", response_model=TokenResponse, summary="Iniciar sesion")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Endpoint de login de usuario"""
    usuario = AuthController.login_user(db=db, email=email, password=password)
    return {
        "access_token": f"mock_token_for_user_{usuario.id}",
        "token_type": "bearer",
        "usuario": usuario
    }
