# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: Proveedores y Productos Suministrados (CU07)
# Ubicación: backend/app/services/proveedor_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import ProveedorModel, ProductoProveedorModel
from app.schemas.proveedor_schema import ProveedorCreate, ProveedorUpdate, ProductoProveedorCreate
from fastapi import HTTPException, status
from typing import Optional, List

class ProveedorService:

    @staticmethod
    def get_all(
        db: Session,
        search: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[ProveedorModel]:
        query = db.query(ProveedorModel)

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                (ProveedorModel.nombre.ilike(pattern)) |
                (ProveedorModel.razonsocial.ilike(pattern)) |
                (ProveedorModel.nit.ilike(pattern)) |
                (ProveedorModel.contacto.ilike(pattern))
            )

        if activo is not None:
            query = query.filter(ProveedorModel.activo == activo)

        return query.order_by(ProveedorModel.id.desc()).all()

    @staticmethod
    def get_by_id(db: Session, id: int) -> ProveedorModel:
        prov = db.query(ProveedorModel).filter(ProveedorModel.id == id).first()
        if not prov:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
        return prov

    @staticmethod
    def create(db: Session, data: ProveedorCreate) -> ProveedorModel:
        nuevo = ProveedorModel(
            nombre=data.nombre,
            razonsocial=data.razonsocial,
            nit=data.nit,
            contacto=data.contacto,
            telefono=data.telefono,
            email=data.email,
            direccion=data.direccion,
            activo=data.activo if data.activo is not None else True
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    @staticmethod
    def update(db: Session, id: int, data: ProveedorUpdate) -> ProveedorModel:
        prov = db.query(ProveedorModel).filter(ProveedorModel.id == id).first()
        if not prov:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")

        for key, value in data.dict(exclude_unset=True).items():
            setattr(prov, key, value)

        db.commit()
        db.refresh(prov)
        return prov

    @staticmethod
    def delete(db: Session, id: int) -> dict:
        prov = db.query(ProveedorModel).filter(ProveedorModel.id == id).first()
        if not prov:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
        prov.activo = False
        db.commit()
        return {"message": f"Proveedor '{prov.nombre}' deshabilitado correctamente", "id": id}

    # PRODUCTOS SUMINISTRADOS BY PROVEEDOR
    @staticmethod
    def vincular_producto(db: Session, data: ProductoProveedorCreate) -> ProductoProveedorModel:
        rel = db.query(ProductoProveedorModel).filter(
            ProductoProveedorModel.idproducto == data.idproducto,
            ProductoProveedorModel.idproveedor == data.idproveedor
        ).first()

        if rel:
            rel.costocompra = data.costocompra
            rel.cantidad = data.cantidad
        else:
            rel = ProductoProveedorModel(**data.dict())
            db.add(rel)

        db.commit()
        db.refresh(rel)
        return rel
