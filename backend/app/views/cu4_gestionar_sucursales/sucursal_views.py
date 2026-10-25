# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Módulo: CU4 - Gestionar Sucursales (Multi-Tenant SaaS)
# Ubicación: backend/app/views/cu4_gestionar_sucursales/sucursal_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin
from app.models.models import Usuario, UsuarioModel
from app.schemas.sucursal_schema import SucursalCreate, SucursalUpdate, SucursalResponse
from app.controllers.cu4_gestionar_sucursales.sucursal_controller import SucursalController

router = APIRouter(
    prefix="/sucursales",
    tags=["Sucursales (CU04 - Vista API)"],
)


@router.get("", response_model=List[SucursalResponse], summary="Listar sucursales de la tienda")
@router.get("/", response_model=List[SucursalResponse], include_in_schema=False)
def listar_sucursales(
    search: Optional[str] = Query(None, description="Buscar por nombre, ciudad o dirección"),
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Consulta pública o administrativa de sucursales con aislamiento por Tenant"""
    tenant_id = x_tenant_id or 1
    return SucursalController.listar_sucursales(
        db=db,
        tenant_id=tenant_id,
        search=search,
        ciudad=ciudad,
        activo=activo,
        skip=skip,
        limit=limit
    )


@router.get("/{sucursal_id}", response_model=SucursalResponse, summary="Obtener sucursal por ID")
def obtener_sucursal(
    sucursal_id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """Detalle de una sucursal específica verificando su tenant"""
    tenant_id = x_tenant_id or 1
    return SucursalController.obtener_sucursal_por_id(db=db, sucursal_id=sucursal_id, tenant_id=tenant_id)


@router.post("", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED, summary="Crear sucursal")
@router.post("/", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def crear_sucursal(
    sucursal_data: SucursalCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Crear sucursal validando límite estipulado por el Plan de Suscripción (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return SucursalController.crear_sucursal(
        db=db,
        sucursal_data=sucursal_data,
        tenant_id=tenant_id,
        operador_id=current_user.id
    )


@router.put("/{sucursal_id}", response_model=SucursalResponse, summary="Actualizar sucursal")
def actualizar_sucursal(
    sucursal_id: int,
    sucursal_data: SucursalUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Actualizar datos de una sucursal física (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return SucursalController.actualizar_sucursal(
        db=db,
        sucursal_id=sucursal_id,
        sucursal_data=sucursal_data,
        tenant_id=tenant_id,
        operador_id=current_user.id
    )


@router.patch("/{sucursal_id}/estado", response_model=SucursalResponse, summary="Activar / Desactivar sucursal")
def cambiar_estado_sucursal(
    sucursal_id: int,
    activo: bool = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Activar o desactivar sucursal validando límites (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return SucursalController.cambiar_estado_sucursal(
        db=db,
        sucursal_id=sucursal_id,
        activo=activo,
        tenant_id=tenant_id,
        operador_id=current_user.id
    )


@router.delete("/{sucursal_id}", summary="Baja lógica de sucursal")
def baja_logica_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Baja lógica de sucursal preservando integridad referencial (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return SucursalController.dar_baja_logica_sucursal(
        db=db,
        sucursal_id=sucursal_id,
        tenant_id=tenant_id,
        operador_id=current_user.id
    )
