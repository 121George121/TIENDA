# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: Proveedores y Productos Suministrados (CU07)
# Ubicación: backend/app/controllers/proveedor_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List
from app.services.cu7_gestionar_proveedores_productos_suministrados.proveedor_service import ProveedorService
from app.schemas.proveedor_schema import ProveedorCreate, ProveedorUpdate, ProductoProveedorCreate
from app.models.models import ProveedorModel, ProductoProveedorModel

class ProveedorController:

    @staticmethod
    def listar_proveedores(db: Session, search: Optional[str] = None, activo: Optional[bool] = None) -> List[ProveedorModel]:
        return ProveedorService.get_all(db=db, search=search, activo=activo)

    @staticmethod
    def obtener_proveedor(db: Session, id: int) -> ProveedorModel:
        return ProveedorService.get_by_id(db=db, id=id)

    @staticmethod
    def crear_proveedor(db: Session, data: ProveedorCreate) -> ProveedorModel:
        return ProveedorService.create(db=db, data=data)

    @staticmethod
    def actualizar_proveedor(db: Session, id: int, data: ProveedorUpdate) -> ProveedorModel:
        return ProveedorService.update(db=db, id=id, data=data)

    @staticmethod
    def baja_proveedor(db: Session, id: int) -> dict:
        return ProveedorService.delete(db=db, id=id)

    @staticmethod
    def vincular_producto(db: Session, data: ProductoProveedorCreate) -> ProductoProveedorModel:
        return ProveedorService.vincular_producto(db=db, data=data)
