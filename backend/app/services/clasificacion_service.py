# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: Clasificación de Prendas (CU06 - Categorías, Temporadas, Colecciones)
# Ubicación: backend/app/services/clasificacion_service.py
# ==============================================================================

from sqlalchemy.orm import Session, joinedload
from app.models.models import CategoriaModel, TemporadaModel, ColeccionModel
from app.schemas.clasificacion_schema import (
    CategoriaCreate, CategoriaUpdate,
    TemporadaCreate, TemporadaUpdate,
    ColeccionCreate, ColeccionUpdate
)
from fastapi import HTTPException, status
from typing import Optional, List

class CategoriaService:

    @staticmethod
    def get_all(db: Session, search: Optional[str] = None, activo: Optional[bool] = None) -> List[CategoriaModel]:
        query = db.query(CategoriaModel)
        if search:
            query = query.filter(CategoriaModel.nombre.ilike(f"%{search}%"))
        if activo is not None:
            query = query.filter(CategoriaModel.activo == activo)
        return query.order_by(CategoriaModel.id.desc()).all()

    @staticmethod
    def create(db: Session, data: CategoriaCreate) -> CategoriaModel:
        nueva = CategoriaModel(**data.dict())
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def update(db: Session, id: int, data: CategoriaUpdate) -> CategoriaModel:
        cat = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(cat, key, value)
        db.commit()
        db.refresh(cat)
        return cat

    @staticmethod
    def delete(db: Session, id: int):
        cat = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        cat.activo = False
        db.commit()
        return {"message": "Categoría dada de baja correctamente", "id": id}

class TemporadaService:

    @staticmethod
    def get_all(db: Session, search: Optional[str] = None, activo: Optional[bool] = None) -> List[TemporadaModel]:
        query = db.query(TemporadaModel)
        if search:
            query = query.filter(TemporadaModel.nombre.ilike(f"%{search}%"))
        if activo is not None:
            query = query.filter(TemporadaModel.activo == activo)
        return query.order_by(TemporadaModel.id.desc()).all()

    @staticmethod
    def create(db: Session, data: TemporadaCreate) -> TemporadaModel:
        nueva = TemporadaModel(**data.dict())
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def update(db: Session, id: int, data: TemporadaUpdate) -> TemporadaModel:
        temp = db.query(TemporadaModel).filter(TemporadaModel.id == id).first()
        if not temp:
            raise HTTPException(status_code=404, detail="Temporada no encontrada")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(temp, key, value)
        db.commit()
        db.refresh(temp)
        return temp

    @staticmethod
    def delete(db: Session, id: int):
        temp = db.query(TemporadaModel).filter(TemporadaModel.id == id).first()
        if not temp:
            raise HTTPException(status_code=404, detail="Temporada no encontrada")
        temp.activo = False
        db.commit()
        return {"message": "Temporada dada de baja correctamente", "id": id}

class ColeccionService:

    @staticmethod
    def get_all(db: Session, search: Optional[str] = None, activo: Optional[bool] = None) -> List[ColeccionModel]:
        query = db.query(ColeccionModel)
        if search:
            query = query.filter(ColeccionModel.nombre.ilike(f"%{search}%"))
        if activo is not None:
            query = query.filter(ColeccionModel.activo == activo)
        return query.order_by(ColeccionModel.id.desc()).all()

    @staticmethod
    def create(db: Session, data: ColeccionCreate) -> ColeccionModel:
        nueva = ColeccionModel(**data.dict())
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def update(db: Session, id: int, data: ColeccionUpdate) -> ColeccionModel:
        col = db.query(ColeccionModel).filter(ColeccionModel.id == id).first()
        if not col:
            raise HTTPException(status_code=404, detail="Colección no encontrada")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(col, key, value)
        db.commit()
        db.refresh(col)
        return col

    @staticmethod
    def delete(db: Session, id: int):
        col = db.query(ColeccionModel).filter(ColeccionModel.id == id).first()
        if not col:
            raise HTTPException(status_code=404, detail="Colección no encontrada")
        col.activo = False
        db.commit()
        return {"message": "Colección dada de baja correctamente", "id": id}
