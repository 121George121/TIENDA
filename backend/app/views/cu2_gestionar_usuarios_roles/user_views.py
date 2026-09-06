# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Router de Gestión de Usuarios
# ==============================================================================

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.schemas import UsuarioResponse, UsuarioAdminCreate, UsuarioUpdate, UsuarioEstadoUpdate, UsuarioRolUpdate
from app.controllers.cu2_gestionar_usuarios_roles.user_controller import UserController
from app.core.dependencies import get_current_active_user
from app.models.models import UsuarioModel

router = APIRouter(prefix="/usuarios", tags=["Usuarios (Vista API)"])

@router.get("/", response_model=List[UsuarioResponse], summary="Listar y filtrar usuarios")
def listar_usuarios(
    search: Optional[str] = Query(None, description="Búsqueda por nombre, apellido o email"),
    rol_id: Optional[int] = Query(None, description="Filtrar por ID de rol"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Listar usuarios con opciones de búsqueda y filtrado"""
    return UserController.get_all(db=db, search=search, rol_id=rol_id, activo=activo, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UsuarioResponse, summary="Obtener usuario por ID")
def obtener_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Obtener detalle de usuario por ID"""
    return UserController.get_by_id(db=db, user_id=user_id)

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
def crear_usuario(
    user_data: UsuarioAdminCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Crear un nuevo usuario desde el panel administrativo"""
    return UserController.create(db=db, user_data=user_data)

@router.put("/{user_id}", response_model=UsuarioResponse, summary="Editar usuario")
def editar_usuario(
    user_id: int,
    user_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Editar información de un usuario existente"""
    return UserController.update(db=db, user_id=user_id, user_data=user_data)

@router.patch("/{user_id}/estado", response_model=UsuarioResponse, summary="Activar/Desactivar usuario")
def cambiar_estado_usuario(
    user_id: int,
    estado_data: UsuarioEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Activar o desactivar el acceso de un usuario"""
    return UserController.toggle_status(db=db, user_id=user_id, activo=estado_data.activo)

@router.patch("/{user_id}/rol", response_model=UsuarioResponse, summary="Asignar rol a usuario")
def asignar_rol_usuario(
    user_id: int,
    rol_data: UsuarioRolUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Asignar o cambiar el rol de un usuario"""
    return UserController.assign_role(db=db, user_id=user_id, rol_id=rol_data.rol_id)

@router.delete("/{user_id}", summary="Eliminar usuario")
def eliminar_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Eliminar definitivamente un usuario de la base de datos"""
    return UserController.delete(db=db, user_id=user_id)

