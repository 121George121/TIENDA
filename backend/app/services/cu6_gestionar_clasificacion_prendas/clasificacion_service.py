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
        try:
            db.delete(cat)
            db.commit()
            return {"message": "Categoría eliminada correctamente", "id": id}
        except Exception:
            db.rollback()
            cat.activo = False
            db.commit()
            return {"message": "Categoría desactivada porque tiene productos asociados", "id": id}

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
        try:
            db.delete(temp)
            db.commit()
            return {"message": "Temporada eliminada correctamente", "id": id}
        except Exception:
            db.rollback()
            temp.activo = False
            db.commit()
            return {"message": "Temporada desactivada porque tiene colecciones asociadas", "id": id}

class ColeccionService:

    @staticmethod
    def get_all(db: Session, search: Optional[str] = None, activo: Optional[bool] = None) -> List[ColeccionModel]:
        query = db.query(ColeccionModel).options(joinedload(ColeccionModel.temporada))
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
        try:
            db.delete(col)
            db.commit()
            return {"message": "Colección eliminada correctamente", "id": id}
        except Exception:
            db.rollback()
            col.activo = False
            db.commit()
            return {"message": "Colección desactivada correctamente", "id": id}
