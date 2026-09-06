# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: Clientes (CU03)
# Ubicación: backend/app/controllers/cliente_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from app.services.cu3_gestionar_clientes.cliente_service import ClienteService
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate

class ClienteController:

    @staticmethod
    def listar_clientes(
        db: Session, 
        search: Optional[str] = None, 
        activo: Optional[bool] = None, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Dict]:
        return ClienteService.get_all(db=db, search=search, activo=activo, skip=skip, limit=limit)

    @staticmethod
    def obtener_cliente(db: Session, cliente_id: int) -> Dict:
        return ClienteService.get_by_id(db=db, cliente_id=cliente_id)

    @staticmethod
    def crear_cliente(db: Session, cliente_data: ClienteCreate):
        return ClienteService.create(db=db, cliente_data=cliente_data)

    @staticmethod
    def actualizar_cliente(db: Session, cliente_id: int, cliente_data: ClienteUpdate):
        return ClienteService.update(db=db, cliente_id=cliente_id, cliente_data=cliente_data)

    @staticmethod
    def cambiar_estado(db: Session, cliente_id: int, activo: bool):
        return ClienteService.toggle_status(db=db, cliente_id=cliente_id, activo=activo)

    @staticmethod
    def baja_logica(db: Session, cliente_id: int):
        return ClienteService.logical_delete(db=db, cliente_id=cliente_id)

    @staticmethod
    def obtener_compras(db: Session, cliente_id: int):
        return ClienteService.get_historial_compras(db=db, cliente_id=cliente_id)

    @staticmethod
    def obtener_reservas(db: Session, cliente_id: int):
        return ClienteService.get_historial_reservas(db=db, cliente_id=cliente_id)
