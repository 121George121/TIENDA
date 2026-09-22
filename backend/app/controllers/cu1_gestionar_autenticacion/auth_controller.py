# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU1 - Gestionar Autenticación
# Ubicación: backend/app/controllers/cu1_gestionar_autenticacion/auth_controller.py
# Autenticación, Registro de Usuarios, OTP Cifrado y Hashing de contraseñas
# ==============================================================================

import random
import secrets
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import UsuarioModel, RolModel
from app.schemas.schemas import UsuarioCreate
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, create_reset_token
from app.core.email import send_recovery_email, send_otp_email
from fastapi import HTTPException, status

class AuthController:

    @staticmethod
    def register_user(db: Session, user_data: UsuarioCreate):
        """Registra un nuevo usuario cifrando el código OTP en la base de datos PostgreSQL"""
        clean_email = user_data.email.strip().lower()

        # Buscar usuario existente insensible a mayúsculas/minúsculas
        usuario_existente = db.query(UsuarioModel).filter(func.lower(UsuarioModel.email) == clean_email).first()
        
        if usuario_existente:
            if usuario_existente.verificado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo ya está registrado y verificado. Por favor inicia sesión."
                )
            else:
                # Si el usuario existe pero NO está verificado aún: reenviar nuevo código OTP cifrado
                otp_code = str(random.randint(100000, 999999))
                hashed_otp = get_password_hash(otp_code)
                expiracion = datetime.utcnow() + timedelta(minutes=15)
                
                usuario_existente.nombre = user_data.nombre
                usuario_existente.apellido = user_data.apellido
                usuario_existente.telefono = user_data.telefono
                usuario_existente.passwordhash = get_password_hash(user_data.password)
                usuario_existente.codigoverificacion = hashed_otp
                usuario_existente.codigoexpiracion = expiracion
                
                db.commit()
                db.refresh(usuario_existente)

                print("\n=======================================================")
                print(f"[RE-SEND OTP CODE] Email: {clean_email} | Código (Enviado al mail): {otp_code} | Hash DB: {hashed_otp[:20]}...")
                print("=======================================================\n")

                send_otp_email(email_to=clean_email, otp_code=otp_code)

                return {
                    "id": usuario_existente.id,
                    "nombre": usuario_existente.nombre,
                    "apellido": usuario_existente.apellido,
                    "email": usuario_existente.email,
                    "telefono": usuario_existente.telefono,
                    "activo": usuario_existente.activo,
                    "verificado": usuario_existente.verificado,
                    "mensaje": f"Nuevo código de verificación enviado a {clean_email}"
                }

        # Buscar el rol Cliente
        rol_cliente = db.query(RolModel).filter(RolModel.nombre == "Cliente").first()
        if not rol_cliente:
            rol_cliente = RolModel(nombre="Cliente", descripcion="Compra en tienda, visualiza catálogo")
            db.add(rol_cliente)
            db.commit()
            db.refresh(rol_cliente)

        # Generar código OTP de 6 dígitos cifrado
        otp_code = str(random.randint(100000, 999999))
        hashed_otp = get_password_hash(otp_code)
        expiracion = datetime.utcnow() + timedelta(minutes=15)

        print("\n=======================================================")
        print(f"[OTP VERIFICATION CODE] Email: {clean_email} | Código (Enviado al mail): {otp_code} | Hash DB: {hashed_otp[:20]}...")
        print("=======================================================\n")

        # Intentar enviar el correo real vía SMTP con el código plano
        send_otp_email(email_to=clean_email, otp_code=otp_code)

        hashed_pwd = get_password_hash(user_data.password)
        nuevo_usuario = UsuarioModel(
            nombre=user_data.nombre,
            apellido=user_data.apellido,
            email=clean_email,
            telefono=user_data.telefono,
            passwordhash=hashed_pwd,
            rolid=rol_cliente.id,
            verificado=True, # Auto-verificado por requerimiento
            codigoverificacion=None,
            codigoexpiracion=None,
            activo=True
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "apellido": nuevo_usuario.apellido,
            "email": nuevo_usuario.email,
            "telefono": nuevo_usuario.telefono,
            "activo": nuevo_usuario.activo,
            "verificado": nuevo_usuario.verificado,
            "mensaje": f"Código de verificación de 6 dígitos enviado a {clean_email}"
        }

    @staticmethod
    def verify_otp_code(db: Session, email: str, codigo: str):
        """Verifica el código OTP comparando el hash cifrado e inicia sesión automáticamente"""
        clean_email = email.strip().lower()
        usuario = db.query(UsuarioModel).filter(func.lower(UsuarioModel.email) == clean_email).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        if not usuario.codigoverificacion or not verify_password(codigo, usuario.codigoverificacion):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Código de verificación incorrecto")

        if usuario.codigoexpiracion and usuario.codigoexpiracion < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de verificación ha expirado")

        # Marcar como verificado y limpiar código OTP
        usuario.verificado = True
        usuario.codigoverificacion = None
        usuario.codigoexpiracion = None
        db.commit()
        db.refresh(usuario)

        access_token = create_access_token(subject=usuario.email)
        refresh_token = create_refresh_token(subject=usuario.email)

        return {
            "mensaje": "¡Cuenta verificada e iniciada exitosamente!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "usuario": usuario
        }

    @staticmethod
    def login_user(db: Session, email: str, password: str):
        """Valida credenciales y retorna los tokens"""
        clean_email = email.strip().lower()
        usuario = db.query(UsuarioModel).filter(func.lower(UsuarioModel.email) == clean_email).first()
        
        if not usuario or not verify_password(password, usuario.passwordhash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
        
        if not usuario.activo:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El usuario se encuentra inactivo")

        # Eliminado bloqueo de cuenta no verificada por requerimiento: auto-verificar
        if not usuario.verificado:
            usuario.verificado = True
            db.commit()
            db.refresh(usuario)
        
        access_token = create_access_token(subject=usuario.email)
        refresh_token = create_refresh_token(subject=usuario.email)
        
        rol_nombre = None
        if usuario.rolid:
            rol_model = db.query(RolModel).filter(RolModel.id == usuario.rolid).first()
            if rol_model:
                rol_nombre = rol_model.nombre
                
        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="LOGIN",
                modulo="AUTENTICACION",
                usuario_id=usuario.id,
                detalle=f"Inicio de sesión exitoso de {usuario.nombre} ({usuario.email})",
                datos_nuevos={"rol": rol_nombre}
            )
        except Exception:
            pass

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "rol": rol_nombre,
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "telefono": usuario.telefono,
                "rol": rol_nombre,
                "activo": usuario.activo,
                "verificado": usuario.verificado
            }
        }

    @staticmethod
    def request_password_recovery(db: Session, email: str):
        """Genera un token de recuperación, lo guarda cifrado (reutilizando codigoverificacion) y lo envía por correo"""
        clean_email = email.strip().lower()
        usuario = db.query(UsuarioModel).filter(func.lower(UsuarioModel.email) == clean_email).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe una cuenta con ese correo")

        reset_token = create_reset_token(clean_email)
        usuario.codigoverificacion = get_password_hash(reset_token)
        usuario.codigoexpiracion = datetime.utcnow() + timedelta(minutes=15)
        db.commit()

        print("\n=======================================================")
        print(f"[PASSWORD RECOVERY TOKEN] Email: {clean_email} | Token (enviado al mail): {reset_token}")
        print("=======================================================\n")

        send_recovery_email(email_to=clean_email, token=reset_token)

        return {"mensaje": f"Se envió un enlace de recuperación a {clean_email}"}

    @staticmethod
    def reset_password(db: Session, token: str, new_password: str):
        """Busca al usuario de forma segura y eficiente O(1) y actualiza su contraseña"""
        usuario = None
        # 1. Intentar decodificar el token JWT firmado de recuperación
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") == "password_reset":
                token_email = payload.get("sub")
                if token_email:
                    usuario = db.query(UsuarioModel).filter(func.lower(UsuarioModel.email) == token_email.strip().lower()).first()
        except JWTError:
            pass

        # 2. Si se resolvió por JWT, validar hash almacenado y expiración
        if usuario:
            if not usuario.codigoverificacion or not verify_password(token, usuario.codigoverificacion):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El enlace de recuperación ya fue utilizado o es inválido")
            if usuario.codigoexpiracion and usuario.codigoexpiracion < datetime.utcnow():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El enlace de recuperación ha expirado")
        else:
            # Fallback seguro para tokens antiguos generados previamente (acotado a 15 candidatos)
            candidatos = db.query(UsuarioModel).filter(
                UsuarioModel.codigoverificacion.isnot(None),
                UsuarioModel.codigoexpiracion.isnot(None),
                UsuarioModel.codigoexpiracion >= datetime.utcnow()
            ).limit(15).all()

            usuario = next((u for u in candidatos if verify_password(token, u.codigoverificacion)), None)
            if not usuario:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El enlace de recuperación es inválido o ha expirado")

        usuario.passwordhash = get_password_hash(new_password)
        usuario.codigoverificacion = None
        usuario.codigoexpiracion = None
        db.commit()

        return {"mensaje": "Contraseña restablecida exitosamente. Ya puedes iniciar sesión."}
