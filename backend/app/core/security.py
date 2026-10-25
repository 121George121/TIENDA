from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login" if hasattr(settings, 'API_V1_STR') else "/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Aliases en español
verificar_contrasenia = verify_password
obtener_hash_contrasenia = get_password_hash

def create_access_token(
    subject: Union[str, Any],
    claims_adicionales: Optional[dict] = None,
    extra_claims: Optional[dict] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Genera un token JWT de acceso con soporte para claims adicionales (tenant_id, rol, etc.)"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    claims = claims_adicionales or extra_claims
    if claims and isinstance(claims, dict):
        to_encode.update(claims)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

crear_token_acceso = create_access_token

def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

crear_token_refresco = create_refresh_token

def decodificar_token(token: str) -> Optional[dict]:
    """Decodifica un token JWT y retorna su payload como diccionario, o None si es inválido"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception:
        return None

decode_token = decodificar_token

def verify_token(token: str) -> Optional[str]:
    payload = decodificar_token(token)
    if payload:
        return payload.get("sub")
    return None

verificar_token = verify_token

def create_reset_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "password_reset"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

crear_token_recuperacion = create_reset_token


