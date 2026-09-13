# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTER)
# Módulo: Productos y Catálogo Retail (CU05)
# Ubicación: backend/app/routes/producto_routes.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoResponse
from app.controllers.producto_controller import ProductoController

router = APIRouter(prefix="/productos", tags=["Productos y Catálogo Retail (CU05)"])

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
    return ProductoController.listar_productos(
        db=db, search=search, categoria_id=categoria_id, genero=genero, activo=activo, skip=skip, limit=limit
    )

@router.get("/{id}", response_model=ProductoResponse)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    return ProductoController.obtener_producto(db=db, id=id)

@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(data: ProductoCreate, db: Session = Depends(get_db)):
    return ProductoController.crear_producto(db=db, data=data)

@router.put("/{id}", response_model=ProductoResponse)
def actualizar_producto(id: int, data: ProductoUpdate, db: Session = Depends(get_db)):
    return ProductoController.actualizar_producto(db=db, id=id, data=data)

@router.patch("/{id}/estado", response_model=ProductoResponse)
def cambiar_estado_producto(id: int, activo: bool = Query(...), db: Session = Depends(get_db)):
    return ProductoController.cambiar_estado(db=db, id=id, activo=activo)

@router.delete("/{id}")
def baja_logica_producto(id: int, db: Session = Depends(get_db)):
    return ProductoController.baja_logica(db=db, id=id)
