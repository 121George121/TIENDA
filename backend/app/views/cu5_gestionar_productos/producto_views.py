# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Módulo: Productos y Catálogo Retail (CU05)
# Ubicación: backend/app/views/cu5_gestionar_productos/producto_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import require_staff, require_admin
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoResponse
from app.controllers.cu5_gestionar_productos.producto_controller import ProductoController

router = APIRouter(prefix="/productos", tags=["Productos y Catálogo Retail (CU05 - Vista API)"])

# Lectura pública: la app móvil y el catálogo web muestran productos sin requerir login
@router.get("", response_model=List[ProductoResponse])
def listar_productos(
    search: Optional[str] = Query(None, description="Buscar por nombre, marca o descripción"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    genero: Optional[str] = Query(None, description="Filtrar por género (Damas, Caballeros, Unisex)"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar catálogo de productos (Público / Móvil / Web)"""
    return ProductoController.listar_productos(
        db=db, search=search, categoria_id=categoria_id, genero=genero, activo=activo, skip=skip, limit=limit
    )

@router.get("/{id}", response_model=ProductoResponse)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    """Obtener detalle de producto por ID (Público)"""
    return ProductoController.obtener_producto(db=db, id=id)

# Mutaciones: protegidas para Administradores y Staff
@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    data: ProductoCreate, 
    db: Session = Depends(get_db), 
    current_user=Depends(require_staff)
):
    """Crear producto nuevo (Solo Personal / Administrador)"""
    return ProductoController.crear_producto(db=db, data=data)

@router.put("/{id}", response_model=ProductoResponse)
def actualizar_producto(
    id: int, 
    data: ProductoUpdate, 
    db: Session = Depends(get_db), 
    current_user=Depends(require_staff)
):
    """Actualizar producto (Solo Personal / Administrador)"""
    return ProductoController.actualizar_producto(db=db, id=id, data=data)

@router.patch("/{id}/estado", response_model=ProductoResponse)
def cambiar_estado_producto(
    id: int, 
    activo: bool = Query(...), 
    db: Session = Depends(get_db), 
    current_user=Depends(require_admin)
):
    """Activar / Desactivar producto del catálogo (Solo Administrador)"""
    return ProductoController.cambiar_estado(db=db, id=id, activo=activo)

@router.delete("/{id}")
def eliminar_producto(
    id: int, 
    db: Session = Depends(get_db), 
    current_user=Depends(require_admin)
):
    """Eliminar definitivamente un producto de la base de datos (Solo Administrador)"""
    return ProductoController.eliminar_producto(db=db, id=id)
