# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Módulo: CU6 - Gestionar Clasificación de Prendas (Categorías, Temporadas, Colecciones)
# Arquitectura: Multi-Tenant SaaS con Roles RBAC
# Ubicación: backend/app/views/cu6_gestionar_clasificacion_prendas/clasificacion_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Header, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import require_staff, require_admin
from app.models.models import Usuario
from app.schemas.clasificacion_schema import (
    CategoriaCreate, CategoriaUpdate, CategoriaResponse,
    TemporadaCreate, TemporadaUpdate, TemporadaResponse,
    ColeccionCreate, ColeccionUpdate, ColeccionResponse
)
from app.controllers.cu6_gestionar_clasificacion_prendas.clasificacion_controller import ClasificacionController

router = APIRouter(
    tags=["Clasificación de Prendas (CU06 - Vista API)"],
)


# ==============================================================================
# ENDPOINTS DE CATEGORÍAS
# ==============================================================================
@router.get("/categorias", response_model=List[CategoriaResponse], summary="Listar categorías de prendas")
def listar_categorias(
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """Listar categorías adaptadas al tenant (Público / Catálogo)"""
    tenant_id = x_tenant_id or 1
    return ClasificacionController.listar_categorias(
        db=db,
        tenant_id=tenant_id,
        search=search,
        activo=activo
    )


@router.get("/categorias/{id}", response_model=CategoriaResponse, summary="Obtener detalle de categoría")
def obtener_categoria(
    id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """Obtener detalle de categoría por ID"""
    tenant_id = x_tenant_id or 1
    return ClasificacionController.obtener_categoria_por_id(db=db, id=id, tenant_id=tenant_id)


@router.post("/categorias", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED, summary="Crear categoría")
def crear_categoria(
    data: CategoriaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Crear categoría nueva (Solo Personal / Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.crear_categoria(
        db=db,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.put("/categorias/{id}", response_model=CategoriaResponse, summary="Actualizar categoría")
def actualizar_categoria(
    id: int, 
    data: CategoriaUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Actualizar datos de la categoría (Solo Personal / Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.actualizar_categoria(
        db=db,
        id=id,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.patch("/categorias/{id}/estado", response_model=CategoriaResponse, summary="Activar / Desactivar categoría")
def cambiar_estado_categoria(
    id: int,
    activo: bool = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Cambiar estado activo/inactivo de categoría"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.cambiar_estado_categoria(
        db=db,
        id=id,
        activo=activo,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.delete("/categorias/{id}", summary="Eliminar categoría")
def baja_categoria(
    id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Eliminar categoría definitivamente o desactivar si tiene productos (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.eliminar_categoria(
        db=db,
        id=id,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


# ==============================================================================
# ENDPOINTS DE TEMPORADAS
# ==============================================================================
@router.get("/temporadas", response_model=List[TemporadaResponse], summary="Listar temporadas comerciales")
def listar_temporadas(
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """Listar temporadas adaptadas al tenant (Público / Catálogo)"""
    tenant_id = x_tenant_id or 1
    return ClasificacionController.listar_temporadas(
        db=db,
        tenant_id=tenant_id,
        search=search,
        activo=activo
    )


@router.get("/temporadas/{id}", response_model=TemporadaResponse, summary="Obtener detalle de temporada")
def obtener_temporada(
    id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """Obtener temporada por ID"""
    tenant_id = x_tenant_id or 1
    return ClasificacionController.obtener_temporada_por_id(db=db, id=id, tenant_id=tenant_id)


@router.post("/temporadas", response_model=TemporadaResponse, status_code=status.HTTP_201_CREATED, summary="Crear temporada")
def crear_temporada(
    data: TemporadaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Crear nueva temporada comercial (Solo Personal / Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.crear_temporada(
        db=db,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.put("/temporadas/{id}", response_model=TemporadaResponse, summary="Actualizar temporada")
def actualizar_temporada(
    id: int, 
    data: TemporadaUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Actualizar datos de la temporada (Solo Personal / Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.actualizar_temporada(
        db=db,
        id=id,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.patch("/temporadas/{id}/estado", response_model=TemporadaResponse, summary="Activar / Desactivar temporada")
def cambiar_estado_temporada(
    id: int,
    activo: bool = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Cambiar estado activo/inactivo de temporada"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.cambiar_estado_temporada(
        db=db,
        id=id,
        activo=activo,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.delete("/temporadas/{id}", summary="Eliminar temporada")
def baja_temporada(
    id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Eliminar definitivamente o desactivar si posee colecciones (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.eliminar_temporada(
        db=db,
        id=id,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


# ==============================================================================
# ENDPOINTS DE COLECCIONES
# ==============================================================================
@router.get("/colecciones", response_model=List[ColeccionResponse], summary="Listar colecciones de moda")
def listar_colecciones(
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    temporada_id: Optional[int] = Query(None, description="Filtrar por temporada"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """Listar colecciones adaptadas al tenant (Público / Catálogo)"""
    tenant_id = x_tenant_id or 1
    return ClasificacionController.listar_colecciones(
        db=db,
        tenant_id=tenant_id,
        search=search,
        temporada_id=temporada_id,
        activo=activo
    )


@router.get("/colecciones/{id}", response_model=ColeccionResponse, summary="Obtener detalle de colección")
def obtener_coleccion(
    id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """Obtener colección por ID"""
    tenant_id = x_tenant_id or 1
    return ClasificacionController.obtener_coleccion_por_id(db=db, id=id, tenant_id=tenant_id)


@router.post("/colecciones", response_model=ColeccionResponse, status_code=status.HTTP_201_CREATED, summary="Crear colección")
def crear_coleccion(
    data: ColeccionCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Crear nueva colección de prendas (Solo Personal / Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.crear_coleccion(
        db=db,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.put("/colecciones/{id}", response_model=ColeccionResponse, summary="Actualizar colección")
def actualizar_coleccion(
    id: int, 
    data: ColeccionUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Actualizar datos de la colección (Solo Personal / Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.actualizar_coleccion(
        db=db,
        id=id,
        data=data,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.patch("/colecciones/{id}/estado", response_model=ColeccionResponse, summary="Activar / Desactivar colección")
def cambiar_estado_coleccion(
    id: int,
    activo: bool = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_staff)
):
    """Cambiar estado activo/inactivo de colección"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.cambiar_estado_coleccion(
        db=db,
        id=id,
        activo=activo,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )


@router.delete("/colecciones/{id}", summary="Eliminar colección")
def baja_coleccion(
    id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Eliminar colección definitivamente (Solo Administrador)"""
    tenant_id = getattr(current_user, "tenant_id", None) or 1
    return ClasificacionController.eliminar_coleccion(
        db=db,
        id=id,
        tenant_id=tenant_id,
        usuario_id=current_user.id
    )
