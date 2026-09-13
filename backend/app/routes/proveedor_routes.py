# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTER)
# Módulo: Proveedores y Productos Suministrados (CU07)
# Ubicación: backend/app/routes/proveedor_routes.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.proveedor_schema import (
    ProveedorCreate, ProveedorUpdate, ProveedorResponse,
    ProductoProveedorCreate, ProductoProveedorResponse
)
from app.controllers.proveedor_controller import ProveedorController

router = APIRouter(prefix="/proveedores", tags=["Proveedores y Suministros (CU07)"])

@router.get("", response_model=List[ProveedorResponse])
def listar_proveedores(
    search: Optional[str] = Query(None, description="Buscar por nombre, NIT, contacto..."),
    activo: Optional[bool] = Query(None, description="Filtrar por activo"),
    db: Session = Depends(get_db)
):
    return ProveedorController.listar_proveedores(db=db, search=search, activo=activo)

@router.get("/{id}", response_model=ProveedorResponse)
def obtener_proveedor(id: int, db: Session = Depends(get_db)):
    return ProveedorController.obtener_proveedor(db=db, id=id)

@router.post("", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
def crear_proveedor(data: ProveedorCreate, db: Session = Depends(get_db)):
    return ProveedorController.crear_proveedor(db=db, data=data)

@router.put("/{id}", response_model=ProveedorResponse)
def actualizar_proveedor(id: int, data: ProveedorUpdate, db: Session = Depends(get_db)):
    return ProveedorController.actualizar_proveedor(db=db, id=id, data=data)

@router.delete("/{id}")
def baja_proveedor(id: int, db: Session = Depends(get_db)):
    return ProveedorController.baja_proveedor(db=db, id=id)

@router.post("/suministro", response_model=ProductoProveedorResponse)
def vincular_producto(data: ProductoProveedorCreate, db: Session = Depends(get_db)):
    return ProveedorController.vincular_producto(db=db, data=data)
