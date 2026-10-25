# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Módulo: CU5 - Gestionar Productos y Catálogo Retail (Multi-Tenant SaaS)
# Ubicación: backend/app/views/cu5_gestionar_productos/producto_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Header, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import require_staff, require_admin
from app.models.models import Usuario, UsuarioModel
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoResponse
from app.controllers.cu5_gestionar_productos.producto_controller import ProductoController

router = APIRouter(prefix="/productos", tags=["Productos y Catálogo Retail (CU05 - Vista API)"])


@router.get("", response_model=List[ProductoResponse], summary="Listar catálogo de productos")
@router.get("/", response_model=List[ProductoResponse], include_in_schema=False)
def listar_productos(
    search: Optional[str] = Query(None, description="Buscar por nombre, marca o descripción"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    genero: Optional[str] = Query(None, description="Filtrar por género (Damas, Caballeros, Unisex)"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar catálogo de productos adaptado al tenant (Público / Móvil / Web)"""
    tenant_id = x_tenant_id or 1
    return ProductoController.listar_productos(
        db=db,
        tenant_id=tenant_id,
        search=search,
        categoria_id=categoria_id,
        genero=genero,
        activo=activo,
        skip=skip,
        limit=limit
    )


@router.get("/{id}", response_model=ProductoResponse, summary="Obtener detalle de producto")
def obtener_producto(
    id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """Obtener detalle de producto por ID verificando su tenant"""
    tenant_id = x_tenant_id or 1
    return ProductoController.obtener_producto_por_id(db=db, id=id, tenant_id=tenant_id)


@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED, summary="Crear producto")
@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def crear_producto(
    data: ProductoCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_staff)
):
    """Crear producto nuevo validando la cuota del catálogo según el Plan de Suscripción"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProductoController.crear_producto(
        db=db,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.put("/{id}", response_model=ProductoResponse, summary="Actualizar producto")
def actualizar_producto(
    id: int, 
    data: ProductoUpdate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_staff)
):
    """Actualizar datos del producto (Solo Personal / Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProductoController.actualizar_producto(
        db=db,
        id=id,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.patch("/{id}/estado", response_model=ProductoResponse, summary="Activar / Desactivar producto")
def cambiar_estado_producto(
    id: int, 
    activo: bool = Query(...), 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_admin)
):
    """Activar o desactivar producto del catálogo con validación de cuota (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProductoController.cambiar_estado_producto(
        db=db,
        id=id,
        activo=activo,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.delete("/{id}", summary="Eliminar producto")
def eliminar_producto(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(require_admin)
):
    """Eliminar definitivamente o desactivar si posee ventas registradas (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ProductoController.eliminar_producto(
        db=db,
        id=id,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )
