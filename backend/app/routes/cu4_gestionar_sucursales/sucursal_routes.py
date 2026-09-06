# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTER)
# Módulo: Sucursales (CU04)
# Ubicación: backend/app/routes/sucursal_routes.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.schemas.sucursal_schema import SucursalCreate, SucursalUpdate, SucursalResponse
from app.controllers.cu4_gestionar_sucursales.sucursal_controller import SucursalController

router = APIRouter(
    prefix="/sucursales",
    tags=["Sucursales (CU04)"],
    dependencies=[Depends(get_current_active_user)],
)

@router.get("", response_model=List[SucursalResponse])
def listar_sucursales(
    search: Optional[str] = Query(None, description="Buscar por nombre, ciudad o dirección"),
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    return SucursalController.listar_sucursales(
        db=db, search=search, ciudad=ciudad, activo=activo, skip=skip, limit=limit
    )

@router.get("/{sucursal_id}", response_model=SucursalResponse)
def obtener_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db)
):

    return SucursalController.obtener_sucursal(db=db, sucursal_id=sucursal_id)

@router.post("", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED)
def crear_sucursal(
    sucursal_data: SucursalCreate,
    db: Session = Depends(get_db)
):

    return SucursalController.crear_sucursal(db=db, sucursal_data=sucursal_data)

@router.put("/{sucursal_id}", response_model=SucursalResponse)
def actualizar_sucursal(
    sucursal_id: int,
    sucursal_data: SucursalUpdate,
    db: Session = Depends(get_db)
):

    return SucursalController.actualizar_sucursal(db=db, sucursal_id=sucursal_id, sucursal_data=sucursal_data)

@router.patch("/{sucursal_id}/estado", response_model=SucursalResponse)
def cambiar_estado_sucursal(
    sucursal_id: int,
    activo: bool = Query(..., description="Nuevo estado activo (true/false)"),
    db: Session = Depends(get_db)
):

    return SucursalController.cambiar_estado(db=db, sucursal_id=sucursal_id, activo=activo)

@router.delete("/{sucursal_id}")
def baja_logica_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db)
):

    return SucursalController.baja_logica(db=db, sucursal_id=sucursal_id)
