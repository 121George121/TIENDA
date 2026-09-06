# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: Clasificación de Prendas (CU06 - Categorías, Temporadas, Colecciones)
# Ubicación: backend/app/controllers/clasificacion_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List
from app.services.cu6_gestionar_clasificacion_prendas.clasificacion_service import CategoriaService, TemporadaService, ColeccionService
from app.schemas.clasificacion_schema import (
    CategoriaCreate, CategoriaUpdate,
    TemporadaCreate, TemporadaUpdate,
    ColeccionCreate, ColeccionUpdate
)

class ClasificacionController:

    # CATEGORÍAS
    @staticmethod
    def listar_categorias(db: Session, search: Optional[str] = None, activo: Optional[bool] = None):
        return CategoriaService.get_all(db=db, search=search, activo=activo)

    @staticmethod
    def crear_categoria(db: Session, data: CategoriaCreate):
        return CategoriaService.create(db=db, data=data)

    @staticmethod
    def actualizar_categoria(db: Session, id: int, data: CategoriaUpdate):
        return CategoriaService.update(db=db, id=id, data=data)

    @staticmethod
    def baja_categoria(db: Session, id: int):
        return CategoriaService.delete(db=db, id=id)

    # TEMPORADAS
    @staticmethod
    def listar_temporadas(db: Session, search: Optional[str] = None, activo: Optional[bool] = None):
        return TemporadaService.get_all(db=db, search=search, activo=activo)

    @staticmethod
    def crear_temporada(db: Session, data: TemporadaCreate):
        return TemporadaService.create(db=db, data=data)

    @staticmethod
    def actualizar_temporada(db: Session, id: int, data: TemporadaUpdate):
        return TemporadaService.update(db=db, id=id, data=data)

    @staticmethod
    def baja_temporada(db: Session, id: int):
        return TemporadaService.delete(db=db, id=id)

    # COLECCIONES
    @staticmethod
    def listar_colecciones(db: Session, search: Optional[str] = None, activo: Optional[bool] = None):
        return ColeccionService.get_all(db=db, search=search, activo=activo)

    @staticmethod
    def crear_coleccion(db: Session, data: ColeccionCreate):
        return ColeccionService.create(db=db, data=data)

    @staticmethod
    def actualizar_coleccion(db: Session, id: int, data: ColeccionUpdate):
        return ColeccionService.update(db=db, id=id, data=data)

    @staticmethod
    def baja_coleccion(db: Session, id: int):
        return ColeccionService.delete(db=db, id=id)
