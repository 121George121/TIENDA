# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: Productos y Catálogo Retail (CU05)
# Ubicación: backend/app/controllers/producto_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List
from app.services.producto_service import ProductoService
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate
from app.models.models import ProductoModel

class ProductoController:

    @staticmethod
    def listar_productos(
        db: Session,
        search: Optional[str] = None,
        categoria_id: Optional[int] = None,
        genero: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductoModel]:
        return ProductoService.get_all(
            db=db, search=search, categoria_id=categoria_id, genero=genero, activo=activo, skip=skip, limit=limit
        )

    @staticmethod
    def obtener_producto(db: Session, id: int) -> ProductoModel:
        return ProductoService.get_by_id(db=db, id=id)

    @staticmethod
    def crear_producto(db: Session, data: ProductoCreate) -> ProductoModel:
        return ProductoService.create(db=db, data=data)

    @staticmethod
    def actualizar_producto(db: Session, id: int, data: ProductoUpdate) -> ProductoModel:
        return ProductoService.update(db=db, id=id, data=data)

    @staticmethod
    def cambiar_estado(db: Session, id: int, activo: bool) -> ProductoModel:
        return ProductoService.toggle_status(db=db, id=id, activo=activo)

    @staticmethod
    def baja_logica(db: Session, id: int) -> dict:
        return ProductoService.logical_delete(db=db, id=id)
