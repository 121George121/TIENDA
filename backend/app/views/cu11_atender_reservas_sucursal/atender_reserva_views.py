# ==============================================================================
# CU11 - ATENDER RESERVAS EN SUCURSAL -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu11_atender_reservas_sucursal/atender_reserva_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.models import UsuarioModel, ClienteModel
from app.schemas.reserva_schema import (
    ReservaResponse,
    AtenderReservaRequest,
)
from app.controllers.cu11_atender_reservas_sucursal.atender_reserva_controller import (
    AtenderReservaController,
)

router = APIRouter(prefix="/reservas", tags=["CU11 - Atender Reservas en Sucursal"])


def get_current_user_id(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> int:
    """Extrae el ID del cliente o staff del token JWT; si es invitado o demo, asocia el demo predeterminado"""
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        email = verify_token(token)
        if email:
            user = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
            if user:
                cli = db.query(ClienteModel).filter(ClienteModel.usuarioid == user.id).first()
                if not cli:
                    cli = db.query(ClienteModel).filter(ClienteModel.email == user.email).first()
                if cli:
                    return cli.id
                cli = ClienteModel(nombre=user.nombre, apellido=user.apellido or "", email=user.email, usuarioid=user.id)
                db.add(cli)
                db.commit()
                db.refresh(cli)
                return cli.id

    default_cli = db.query(ClienteModel).first()
    return default_cli.id if default_cli else 1


@router.get("/admin/listado", response_model=List[ReservaResponse], summary="Listado general de reservas para sucursal/admin")
def listar_reservas_admin(
    sucursal_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    CU11: Retorna todas las reservas filtradas por sucursal física y/o estado para el personal de tienda.
    """
    return AtenderReservaController.listar_reservas_admin(db=db, sucursal_id=sucursal_id, estado=estado)


@router.get("/admin/buscar/{codigo}", response_model=ReservaResponse, summary="Búsqueda rápida por código de reserva")
def buscar_por_codigo(
    codigo: str,
    db: Session = Depends(get_db),
):
    """
    CU11: Permite al cajero buscar inmediatamente una reserva por su código alfanumérico (ej: RES-NWDTBO).
    """
    return AtenderReservaController.buscar_reserva_codigo(db=db, codigo=codigo)


@router.post("/{reserva_id}/atender", response_model=ReservaResponse, summary="Atender y entregar o cancelar reserva en tienda")
def atender_reserva(
    reserva_id: int,
    datos: AtenderReservaRequest,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id),
):
    """
    CU11: Atender reserva en caja/mostrador.
    - ENTREGAR: Marca como ENTREGADA, libera el stock reservado y descuenta definitivamente el stock físico.
    - CANCELAR: Marca como CANCELADA y libera el stock reservado para venta general.
    """
    return AtenderReservaController.atender_reserva_sucursal(
        db=db, reserva_id=reserva_id, datos=datos, usuario_staff_id=usuario_id
    )
