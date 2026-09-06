# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: Sucursales (CU04)
# Ubicación: backend/app/controllers/sucursal_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List
from app.services.cu4_gestionar_sucursales.sucursal_service import SucursalService
from app.schemas.sucursal_schema import SucursalCreate, SucursalUpdate
from app.models.models import SucursalModel

class SucursalController:

    @staticmethod
    def listar_sucursales(
        db: Session, 
        search: Optional[str] = None, 
        ciudad: Optional[str] = None, 
        activo: Optional[bool] = None, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SucursalModel]:
        return SucursalService.get_all(db=db, search=search, ciudad=ciudad, activo=activo, skip=skip, limit=limit)

    @staticmethod
    def obtener_sucursal(db: Session, sucursal_id: int) -> SucursalModel:
        return SucursalService.get_by_id(db=db, sucursal_id=sucursal_id)

    @staticmethod
    def crear_sucursal(db: Session, sucursal_data: SucursalCreate) -> SucursalModel:
        return SucursalService.create(db=db, sucursal_data=sucursal_data)

    @staticmethod
    def actualizar_sucursal(db: Session, sucursal_id: int, sucursal_data: SucursalUpdate) -> SucursalModel:
        return SucursalService.update(db=db, sucursal_id=sucursal_id, sucursal_data=sucursal_data)

    @staticmethod
    def cambiar_estado(db: Session, sucursal_id: int, activo: bool) -> SucursalModel:
        return SucursalService.toggle_status(db=db, sucursal_id=sucursal_id, activo=activo)

    @staticmethod
    def baja_logica(db: Session, sucursal_id: int) -> dict:
        return SucursalService.logical_delete(db=db, sucursal_id=sucursal_id)
