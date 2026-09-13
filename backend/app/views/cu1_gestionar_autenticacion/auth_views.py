# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Módulo: CU1 - Gestionar Autenticación
# Ubicación: backend/app/views/cu1_gestionar_autenticacion/auth_views.py
# Router de Autenticación, Registro y Verificación OTP
# ==============================================================================

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import (
    UsuarioCreate, UsuarioResponse, TokenResponse,
    LoginRequest,
    PasswordRecoveryRequest, PasswordRecoveryReset,
    VerifyOtpRequest, VerifyOtpResponse
)
from app.controllers.cu1_gestionar_autenticacion.auth_controller import AuthController
from app.core.dependencies import get_current_active_user
from app.models.models import UsuarioModel

router = APIRouter(prefix="/auth", tags=["Autenticacion (Vista API)"])

@router.post("/registro", status_code=status.HTTP_201_CREATED, summary="Registrar usuario con código OTP")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Endpoint de registro de cliente (Genera código OTP de 6 dígitos)"""
    return AuthController.register_user(db=db, user_data=usuario)

@router.post("/verificar-codigo", summary="Verificar código OTP de 6 dígitos")
def verificar_codigo(req: VerifyOtpRequest, db: Session = Depends(get_db)):
    """Endpoint de validación de código de 6 dígitos enviado por correo/demostración"""
    return AuthController.verify_otp_code(db=db, email=req.email, codigo=req.codigo)

@router.post("/login", response_model=TokenResponse, summary="Iniciar sesion")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint de login de usuario en formato OAuth2"""
    return AuthController.login_user(db=db, email=form_data.username, password=form_data.password)

@router.post("/login/json", response_model=TokenResponse, summary="Iniciar sesion vía JSON")
def login_json(usuario: LoginRequest, db: Session = Depends(get_db)):
    """Endpoint alternativo de login recibiendo JSON"""
    return AuthController.login_user(db=db, email=usuario.email, password=usuario.password)

@router.post("/recuperar-password", summary="Solicitar recuperación de contraseña")
def solicitar_recuperacion(req: PasswordRecoveryRequest, db: Session = Depends(get_db)):
    """Genera token de recuperación de contraseña"""
    return AuthController.request_password_recovery(db=db, email=req.email)

@router.post("/reset-password", summary="Restablecer contraseña")
def restablecer_password(req: PasswordRecoveryReset, db: Session = Depends(get_db)):
    """Cambia la contraseña usando el token temporal"""
    return AuthController.reset_password(db=db, token=req.token, new_password=req.new_password)

@router.get("/me", response_model=UsuarioResponse, summary="Obtener usuario actual")
def get_me(current_user: UsuarioModel = Depends(get_current_active_user)):
    """Devuelve los datos del usuario logueado actualmente. Protegido por JWT."""
    return current_user
