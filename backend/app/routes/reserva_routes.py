# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTER)
# Módulo: CU10 - Gestionar Reservas de Prendas
# Ubicación: backend/app/routes/reserva_routes.py
# ==============================================================================

from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.models import UsuarioModel
from app.schemas.reserva_schema import (
    ReservaResponse,
    ReservaCreate,
    CancelarReservaRequest,
)
from app.controllers.reserva_controller import ReservaController

router = APIRouter(prefix="/reservas", tags=["CU10 - Reservas de Prendas"])


def get_current_user_id(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> int:
    """Extrae el ID del usuario del token JWT; si es cliente invitado o demo, obtiene el cliente predeterminado"""
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        email = verify_token(token)
        if email:
            user = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
            if user:
                return user.id

    default_user = (
        db.query(UsuarioModel)
        .filter(UsuarioModel.email == "cliente@tienda.com")
        .first()
        or db.query(UsuarioModel).first()
    )
    return default_user.id if default_user else 1


@router.post("", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED, summary="Crear reserva desde el carrito")
def crear_reserva(
    datos: ReservaCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    """
    CU10: Convierte los ítems del carrito activo en una Reserva física en sucursal.
    Genera un código único de reserva (ej: RES-XXXXXX) y bloquea el stock en la sucursal física.
    """
    return ReservaController.crear_reserva_desde_carrito(db=db, usuario_id=usuario_id, datos=datos)


@router.get("/mis-reservas", response_model=List[ReservaResponse], summary="Listar reservas del cliente autenticado")
def listar_mis_reservas(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    """
    CU10: Retorna el historial y estado de todas las reservas efectuadas por el cliente.
    """
    return ReservaController.listar_reservas_usuario(db=db, usuario_id=usuario_id)


@router.get("/{id_o_codigo}", response_model=ReservaResponse, summary="Obtener detalle de reserva por ID o código")
def obtener_reserva(
    id_o_codigo: str,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    """
    CU10: Consulta la información completa de una reserva usando su ID o su código alfanumérico.
    """
    return ReservaController.obtener_reserva_por_id_o_codigo(db=db, id_o_codigo=id_o_codigo, usuario_id=usuario_id)


@router.patch("/{reserva_id}/cancelar", response_model=ReservaResponse, summary="Cancelar reserva pendiente")
def cancelar_reserva(
    reserva_id: int,
    datos: Optional[CancelarReservaRequest] = None,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    """
    CU10: Cancela una reserva que se encuentre en estado PENDIENTE y libera el stock reservado en la sucursal.
    """
    motivo = datos.motivo if datos else None
    return ReservaController.cancelar_reserva_cliente(
        db=db, reserva_id=reserva_id, usuario_id=usuario_id, motivo=motivo
    )
