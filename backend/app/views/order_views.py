# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW)
# Router de FastAPI para Pedidos / Órdenes
# ==============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.schemas import OrdenResponse, OrdenCreate
from app.controllers.order_controller import OrderController

router = APIRouter(prefix="/ordenes", tags=["Ordenes (Vista API)"])

@router.post("/", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo pedido")
def crear_orden(orden: OrdenCreate, usuario_id: int = 1, db: Session = Depends(get_db)):
    """Vista para procesar una nueva compra desde Angular o Flutter"""
    return OrderController.create_order(db=db, usuario_id=usuario_id, orden_data=orden)

@router.get("/mis-ordenes/{usuario_id}", response_model=List[OrdenResponse], summary="Listar pedidos del usuario")
def listar_mis_ordenes(usuario_id: int, db: Session = Depends(get_db)):
    """Vista para consultar el historial de pedidos de un cliente"""
    return OrderController.get_user_orders(db=db, usuario_id=usuario_id)
