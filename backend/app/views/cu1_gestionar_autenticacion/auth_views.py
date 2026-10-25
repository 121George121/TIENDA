# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Módulo: CU1 - Gestionar Autenticación
# Ubicación: backend/app/views/cu1_gestionar_autenticacion/auth_views.py
# Router de Autenticación, Registro y Verificación OTP en Español
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
from app.models.models import UsuarioModel, TenantModel

router = APIRouter(prefix="/auth", tags=["CU01 - Gestionar Autenticacion (Vista API)"])

@router.post("/registro", status_code=status.HTTP_201_CREATED, summary="Registrar usuario con código OTP")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Endpoint de registro de cliente (Genera código OTP de 6 dígitos)"""
    return AuthController.registrar_usuario(db=db, user_data=usuario)

@router.post("/verificar-codigo", summary="Verificar código OTP de 6 dígitos")
def verificar_codigo(req: VerifyOtpRequest, db: Session = Depends(get_db)):
    """Endpoint de validación de código de 6 dígitos enviado por correo/demostración"""
    return AuthController.verificar_codigo_otp(db=db, email=req.email, codigo=req.codigo)

@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión (OAuth2 Form)")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint de login de usuario en formato OAuth2"""
    return AuthController.iniciar_sesion(db=db, email=form_data.username, password=form_data.password)

@router.post("/login/json", response_model=TokenResponse, summary="Iniciar sesión vía JSON con ámbito de Tenant")
def login_json(usuario: LoginRequest, db: Session = Depends(get_db)):
    """Endpoint alternativo de login recibiendo JSON con soporte para tenant_slug"""
    return AuthController.iniciar_sesion(
        db=db,
        email=usuario.email,
        password=usuario.password,
        tenant_slug=usuario.tenant_slug
    )

@router.post("/recuperar-password", summary="Solicitar recuperación de contraseña")
def solicitar_recuperacion(req: PasswordRecoveryRequest, db: Session = Depends(get_db)):
    """Genera token de recuperación de contraseña"""
    return AuthController.solicitar_recuperacion_contrasenia(db=db, email=req.email)

@router.post("/reset-password", summary="Restablecer contraseña")
def restablecer_password(req: PasswordRecoveryReset, db: Session = Depends(get_db)):
    """Cambia la contraseña usando el token temporal"""
    return AuthController.restablecer_contrasenia(db=db, token=req.token, new_password=req.new_password)

@router.get("/me", response_model=UsuarioResponse, summary="Obtener usuario actual autenticado")
def get_me(current_user: UsuarioModel = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Devuelve los datos del usuario logueado actualmente con información del tenant."""
    # Enriquecer respuesta con datos del tenant
    tenant = db.query(TenantModel).filter(TenantModel.id == current_user.tenant_id).first()
    if tenant:
        current_user.tenant_slug = tenant.slug
        current_user.tenant_nombre = tenant.nombre
    return current_user
