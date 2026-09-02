# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# FastAPI Routers que exponen los endpoints JSON recibidos por Angular y Flutter
# ==============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.schemas import ProductoResponse, ProductoCreate
from app.controllers.product_controller import ProductoController

router = APIRouter(prefix="/productos", tags=["Productos (Vista API)"])

@router.get("/", response_model=List[ProductoResponse], summary="Obtener catálogo de productos")
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Vista pública para consultar productos disponibles"""
    return ProductoController.get_all(db=db, skip=skip, limit=limit)

@router.get("/{producto_id}", response_model=ProductoResponse, summary="Obtener detalle de un producto")
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """Vista detallada de un producto por ID"""
    return ProductoController.get_by_id(db=db, producto_id=producto_id)

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED, summary="Crear producto")
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Vista administrativa para registrar un nuevo producto"""
    return ProductoController.create(db=db, producto_data=producto)

@router.put("/{producto_id}", response_model=ProductoResponse, summary="Actualizar producto")
def actualizar_producto(producto_id: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    """Vista administrativa para actualizar un producto"""
    return ProductoController.update(db=db, producto_id=producto_id, producto_data=producto)

@router.delete("/{producto_id}", summary="Eliminar producto")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """Vista administrativa para desactivar un producto"""
    return ProductoController.delete(db=db, producto_id=producto_id)
