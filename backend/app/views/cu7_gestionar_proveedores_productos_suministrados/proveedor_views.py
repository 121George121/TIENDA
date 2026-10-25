# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Módulo: CU7 - Proveedores y Productos Suministrados (Multi-Tenant SaaS)
# Ubicación: backend/app/views/cu7_gestionar_proveedores_productos_suministrados/proveedor_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Header, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import require_staff, require_admin
from app.models.models import Usuario
from app.schemas.proveedor_schema import (
    ProveedorCreate, ProveedorUpdate, ProveedorResponse,
    ProductoProveedorCreate, ProductoProveedorResponse
)
from app.controllers.cu7_gestionar_proveedores_productos_suministrados.proveedor_controller import ProveedorController

router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores y Suministros (CU07 - Vista API)"],
)


@router.get("", response_model=List[ProveedorResponse], summary="Listar proveedores")
@router.get("/", response_model=List[ProveedorResponse], include_in_schema=False)
def listar_proveedores(
    search: Optional[str] = Query(None, description="Buscar por nombre, NIT, contacto, email..."),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Listar proveedores registrados para el tenant (Personal / Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or x_tenant_id or 1
    return ProveedorController.listar_proveedores(
        db=db,
        tenant_id=tenant_id,
        search=search,
        activo=activo,
        skip=skip,
        limit=limit
    )


@router.get("/{id}", response_model=ProveedorResponse, summary="Obtener detalle de proveedor")
def obtener_proveedor(
    id: int, 
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Obtener detalle de un proveedor por ID verificando su pertenencia al tenant"""
    tenant_id = getattr(current_user, "tenant_id", None) or x_tenant_id or 1
    return ProveedorController.obtener_proveedor_por_id(db=db, id=id, tenant_id=tenant_id)


@router.post("", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED, summary="Crear proveedor")
@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def crear_proveedor(
    data: ProveedorCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Registrar nuevo proveedor en el tenant"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProveedorController.crear_proveedor(
        db=db,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.put("/{id}", response_model=ProveedorResponse, summary="Actualizar proveedor")
def actualizar_proveedor(
    id: int, 
    data: ProveedorUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Actualizar datos del proveedor"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProveedorController.actualizar_proveedor(
        db=db,
        id=id,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.patch("/{id}/estado", response_model=ProveedorResponse, summary="Activar / Desactivar proveedor")
def cambiar_estado_proveedor(
    id: int,
    activo: bool = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Activar o desactivar proveedor"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProveedorController.cambiar_estado_proveedor(
        db=db,
        id=id,
        activo=activo,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.delete("/{id}", summary="Eliminar proveedor")
def baja_proveedor(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_admin)
):
    """Eliminar proveedor definitivamente o aplicar baja lógica si tiene suministros (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProveedorController.eliminar_proveedor(
        db=db,
        id=id,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.post("/suministro", response_model=ProductoProveedorResponse, summary="Vincular producto suministrado")
def vincular_producto(
    data: ProductoProveedorCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Vincular producto con un proveedor suministrador"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProveedorController.vincular_producto_suministrado(
        db=db,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.get("/{id}/suministros", response_model=List[ProductoProveedorResponse], summary="Listar productos suministrados")
def listar_suministros(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Listar productos suministrados por un proveedor"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProveedorController.listar_productos_suministrados(
        db=db,
        proveedor_id=id,
        tenant_id=tenant_id
    )
