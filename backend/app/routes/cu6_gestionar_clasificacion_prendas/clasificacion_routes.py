# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTERS)
# Módulo: Clasificación de Prendas (CU06 - Categorías, Temporadas, Colecciones)
# Ubicación: backend/app/routes/clasificacion_routes.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.schemas.clasificacion_schema import (
    CategoriaCreate, CategoriaUpdate, CategoriaResponse,
    TemporadaCreate, TemporadaUpdate, TemporadaResponse,
    ColeccionCreate, ColeccionUpdate, ColeccionResponse
)
from app.controllers.cu6_gestionar_clasificacion_prendas.clasificacion_controller import ClasificacionController

router = APIRouter(
    tags=["Clasificación de Prendas (CU06)"],
    dependencies=[Depends(get_current_active_user)],
)

# ------------------------------------------------------------------------------
# ENDPOINTS DE CATEGORÍAS
# ------------------------------------------------------------------------------
@router.get("/categorias", response_model=List[CategoriaResponse])
def listar_categorias(
    search: Optional[str] = Query(None),
    activo: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    return ClasificacionController.listar_categorias(db=db, search=search, activo=activo)

@router.post("/categorias", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(data: CategoriaCreate, db: Session = Depends(get_db)):
    return ClasificacionController.crear_categoria(db=db, data=data)

@router.put("/categorias/{id}", response_model=CategoriaResponse)
def actualizar_categoria(id: int, data: CategoriaUpdate, db: Session = Depends(get_db)):
    return ClasificacionController.actualizar_categoria(db=db, id=id, data=data)

@router.delete("/categorias/{id}")
def baja_categoria(id: int, db: Session = Depends(get_db)):
    return ClasificacionController.baja_categoria(db=db, id=id)

# ------------------------------------------------------------------------------
# ENDPOINTS DE TEMPORADAS
# ------------------------------------------------------------------------------
@router.get("/temporadas", response_model=List[TemporadaResponse])
def listar_temporadas(
    search: Optional[str] = Query(None),
    activo: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    return ClasificacionController.listar_temporadas(db=db, search=search, activo=activo)

@router.post("/temporadas", response_model=TemporadaResponse, status_code=status.HTTP_201_CREATED)
def crear_temporada(data: TemporadaCreate, db: Session = Depends(get_db)):
    return ClasificacionController.crear_temporada(db=db, data=data)

@router.put("/temporadas/{id}", response_model=TemporadaResponse)
def actualizar_temporada(id: int, data: TemporadaUpdate, db: Session = Depends(get_db)):
    return ClasificacionController.actualizar_temporada(db=db, id=id, data=data)

@router.delete("/temporadas/{id}")
def baja_temporada(id: int, db: Session = Depends(get_db)):
    return ClasificacionController.baja_temporada(db=db, id=id)

# ------------------------------------------------------------------------------
# ENDPOINTS DE COLECCIONES
# ------------------------------------------------------------------------------
@router.get("/colecciones", response_model=List[ColeccionResponse])
def listar_colecciones(
    search: Optional[str] = Query(None),
    activo: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    return ClasificacionController.listar_colecciones(db=db, search=search, activo=activo)

@router.post("/colecciones", response_model=ColeccionResponse, status_code=status.HTTP_201_CREATED)
def crear_coleccion(data: ColeccionCreate, db: Session = Depends(get_db)):
    return ClasificacionController.crear_coleccion(db=db, data=data)

@router.put("/colecciones/{id}", response_model=ColeccionResponse)
def actualizar_coleccion(id: int, data: ColeccionUpdate, db: Session = Depends(get_db)):
    return ClasificacionController.actualizar_coleccion(db=db, id=id, data=data)

@router.delete("/colecciones/{id}")
def baja_coleccion(id: int, db: Session = Depends(get_db)):
    return ClasificacionController.baja_coleccion(db=db, id=id)
