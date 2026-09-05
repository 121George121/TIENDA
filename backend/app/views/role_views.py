# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Router de Gestión de Roles y Permisos
# ==============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.schemas import RolResponse, RolCreate, PermisosUpdate
from app.controllers.role_controller import RoleController
from app.core.dependencies import get_current_active_user
from app.models.models import UsuarioModel

router = APIRouter(prefix="/roles", tags=["Roles (Vista API)"])

@router.get("/", response_model=List[RolResponse], summary="Listar todos los roles")
def listar_roles(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Obtener listado completo de roles con sus permisos"""
    return RoleController.get_all(db=db)

@router.get("/{rol_id}", response_model=RolResponse, summary="Obtener rol por ID")
def obtener_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Obtener detalle de un rol específico por ID"""
    return RoleController.get_by_id(db=db, rol_id=rol_id)

@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED, summary="Crear rol")
def crear_rol(
    rol_data: RolCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Crear un nuevo rol de usuario"""
    return RoleController.create(db=db, rol_data=rol_data)

@router.put("/{rol_id}", response_model=RolResponse, summary="Editar rol")
def editar_rol(
    rol_id: int,
    rol_data: RolCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Editar nombre y descripción de un rol"""
    return RoleController.update(db=db, rol_id=rol_id, rol_data=rol_data)

@router.put("/{rol_id}/permisos", response_model=RolResponse, summary="Gestionar permisos del rol")
def actualizar_permisos(
    rol_id: int,
    permisos_data: PermisosUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Actualizar el conjunto de permisos asignados a un rol"""
    return RoleController.update_permissions(db=db, rol_id=rol_id, permisos=permisos_data.permisos)

@router.delete("/{rol_id}", summary="Eliminar rol")
def eliminar_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Eliminar un rol de la base de datos"""
    return RoleController.delete(db=db, rol_id=rol_id)

