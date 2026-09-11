# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: Sucursales (CU04)
# Ubicación: backend/app/services/sucursal_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import SucursalModel
from app.schemas.sucursal_schema import SucursalCreate, SucursalUpdate
from fastapi import HTTPException, status
from typing import Optional, List

class SucursalService:

    @staticmethod
    def get_all(
        db: Session, 
        search: Optional[str] = None, 
        ciudad: Optional[str] = None, 
        activo: Optional[bool] = None, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SucursalModel]:
        query = db.query(SucursalModel)

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                (SucursalModel.nombre.ilike(pattern)) |
                (SucursalModel.direccion.ilike(pattern)) |
                (SucursalModel.ciudad.ilike(pattern))
            )

        if ciudad:
            query = query.filter(SucursalModel.ciudad.ilike(f"%{ciudad}%"))

        if activo is not None:
            query = query.filter(SucursalModel.activo == activo)

        return query.order_by(SucursalModel.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, sucursal_id: int) -> SucursalModel:
        sucursal = db.query(SucursalModel).filter(SucursalModel.id == sucursal_id).first()
        if not sucursal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")
        return sucursal

    @staticmethod
    def create(db: Session, sucursal_data: SucursalCreate) -> SucursalModel:
        nueva_sucursal = SucursalModel(
            nombre=sucursal_data.nombre,
            ciudad=sucursal_data.ciudad,
            direccion=sucursal_data.direccion,
            telefono=sucursal_data.telefono,
            latitud=sucursal_data.latitud,
            longitud=sucursal_data.longitud,
            activo=sucursal_data.activo if sucursal_data.activo is not None else True
        )
        db.add(nueva_sucursal)
        db.commit()
        db.refresh(nueva_sucursal)
        return nueva_sucursal

    @staticmethod
    def update(db: Session, sucursal_id: int, sucursal_data: SucursalUpdate) -> SucursalModel:
        sucursal = db.query(SucursalModel).filter(SucursalModel.id == sucursal_id).first()
        if not sucursal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")

        if sucursal_data.nombre is not None:
            sucursal.nombre = sucursal_data.nombre
        if sucursal_data.ciudad is not None:
            sucursal.ciudad = sucursal_data.ciudad
        if sucursal_data.direccion is not None:
            sucursal.direccion = sucursal_data.direccion
        if sucursal_data.telefono is not None:
            sucursal.telefono = sucursal_data.telefono
        if sucursal_data.latitud is not None:
            sucursal.latitud = sucursal_data.latitud
        if sucursal_data.longitud is not None:
            sucursal.longitud = sucursal_data.longitud
        if sucursal_data.activo is not None:
            sucursal.activo = sucursal_data.activo

        db.commit()
        db.refresh(sucursal)
        return sucursal

    @staticmethod
    def toggle_status(db: Session, sucursal_id: int, activo: bool) -> SucursalModel:
        sucursal = db.query(SucursalModel).filter(SucursalModel.id == sucursal_id).first()
        if not sucursal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")

        sucursal.activo = activo
        db.commit()
        db.refresh(sucursal)
        return sucursal

    @staticmethod
    def logical_delete(db: Session, sucursal_id: int) -> dict:
        sucursal = db.query(SucursalModel).filter(SucursalModel.id == sucursal_id).first()
        if not sucursal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")

        sucursal.activo = False
        db.commit()
        return {"message": f"Sucursal '{sucursal.nombre}' dada de baja lógicamente exitosamente", "id": sucursal_id}
