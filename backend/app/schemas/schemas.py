# ==============================================================================
# SCHEMAS DE VALIDACIÓN (PYDANTIC DTOs)
# Definen la forma de los datos que entran y salen de la API REST
# ==============================================================================

import re
from pydantic import BaseModel, EmailStr, field_validator, Field, AliasChoices, ConfigDict
from typing import Optional, List
from datetime import datetime

def validate_password_complexity(v: str) -> str:
    if len(v) < 8:
        raise ValueError('La contraseña debe tener al menos 8 caracteres')
    if not re.search(r'[A-Z]', v):
        raise ValueError('La contraseña debe tener al menos una mayúscula')
    if not re.search(r'[a-z]', v):
        raise ValueError('La contraseña debe tener al menos una minúscula')
    if not re.search(r'[0-9]', v):
        raise ValueError('La contraseña debe tener al menos un número')
    if not re.search(r'[\W_]', v):
        raise ValueError('La contraseña debe tener al menos un carácter especial')
    return v

# --- USUARIO ---
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str
    apellido: Optional[str] = None
    telefono: Optional[str] = None

    @field_validator('password')
    @classmethod
    def password_strong(cls, v):
        return validate_password_complexity(v)

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    rol_id: Optional[int] = Field(default=None, validation_alias=AliasChoices('rol_id', 'rolid'))
    activo: Optional[bool] = None

class UsuarioEstadoUpdate(BaseModel):
    activo: bool

class UsuarioRolUpdate(BaseModel):
    rol_id: int

class UsuarioAdminCreate(BaseModel):
    nombre: str
    apellido: Optional[str] = None
    email: EmailStr
    password: Optional[str] = "usuario123."
    telefono: Optional[str] = None
    rol_id: Optional[int] = Field(default=None, validation_alias=AliasChoices('rol_id', 'rolid'))
    activo: Optional[bool] = True

    @field_validator('password')
    @classmethod
    def password_strong(cls, v):
        if not v or not v.strip() or v == "usuario123.":
            return "usuario123."
        return validate_password_complexity(v)

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    permisos: Optional[List[str]] = []

class RolResponse(RolBase):
    id: int
    permisos: Optional[List[str]] = []

    model_config = ConfigDict(from_attributes=True)

class PermisosUpdate(BaseModel):
    permisos: List[str]

from typing import Optional, List, Any, Union

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    created_at: Optional[datetime] = Field(default=None, validation_alias=AliasChoices('created_at', 'fechacreacion'))
    fechacreacion: Optional[datetime] = Field(default=None, validation_alias=AliasChoices('fechacreacion', 'created_at'))
    rol_id: Optional[int] = Field(default=None, validation_alias=AliasChoices('rol_id', 'rolid'))
    rolid: Optional[int] = Field(default=None, validation_alias=AliasChoices('rolid', 'rol_id'))
    rol: Optional[Union[RolResponse, str]] = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
    rol: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PasswordRecoveryRequest(BaseModel):
    email: EmailStr

class PasswordRecoveryReset(BaseModel):
    token: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def password_strong(cls, v):
        return validate_password_complexity(v)

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    codigo: str

class VerifyOtpResponse(BaseModel):
    mensaje: str
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse

