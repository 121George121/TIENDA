# ==============================================================================
# CU11 - ATENDER RESERVAS EN SUCURSAL -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu11_atender_reservas_sucursal/atender_reserva_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.models import UsuarioModel
from app.models.saas_tenant.tenant_model import Tenant
from app.schemas.reserva_schema import (
    ReservaResponse,
    AtenderReservaRequest,
)
from app.controllers.cu11_atender_reservas_sucursal.atender_reserva_controller import (
    AtenderReservaController,
)

router = APIRouter(prefix="/reservas", tags=["CU11 - Atender Reservas en Sucursal"])


def get_current_staff_user(
    authorization: Optional[str] = Header(None),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
) -> int:
    """Extrae el ID del usuario del token JWT respetando el tenant; o retorna el staff por defecto del tenant"""
    tenant_id = x_tenant_id or 1

    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant con ID {tenant_id} no existe en la plataforma SaaS",
        )

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        email = verify_token(token)
        if email:
            user = (
                db.query(UsuarioModel)
                .filter(
                    UsuarioModel.email == email,
                    UsuarioModel.tenant_id == tenant_id,
                )
                .first()
            )
            if user:
                return user.id

    # Fallback: primer usuario staff activo del tenant
    staff_user = (
        db.query(UsuarioModel)
        .filter(
            UsuarioModel.tenant_id == tenant_id,
            UsuarioModel.activo == True,
            UsuarioModel.rolid.in_([1, 2, 3]),
        )
        .first()
    )
    if staff_user:
        return staff_user.id

    primer_usuario = (
        db.query(UsuarioModel)
        .filter(
            UsuarioModel.tenant_id == tenant_id,
            UsuarioModel.activo == True,
        )
        .first()
    )
    return primer_usuario.id if primer_usuario else 1


@router.get(
    "/admin/listado",
    response_model=List[ReservaResponse],
    summary="Listado general de reservas para sucursal/admin",
)
def listar_reservas_admin(
    sucursal_id: Optional[int] = None,
    estado: Optional[str] = None,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
):
    """
    CU11: Retorna todas las reservas filtradas por sucursal física y/o estado para el personal de tienda.
    Aislado estrictamente por Tenant ID.
    """
    tenant_id = x_tenant_id or 1
    return AtenderReservaController.listar_reservas_admin(
        db=db,
        sucursal_id=sucursal_id,
        estado=estado,
        tenant_id=tenant_id,
    )


@router.get(
    "/admin/buscar/{codigo}",
    response_model=ReservaResponse,
    summary="Búsqueda rápida por código de reserva",
)
def buscar_por_codigo(
    codigo: str,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
):
    """
    CU11: Permite al cajero buscar inmediatamente una reserva por su código alfanumérico (ej: RES-NWDTBO).
    """
    tenant_id = x_tenant_id or 1
    return AtenderReservaController.buscar_reserva_codigo(
        db=db,
        codigo=codigo,
        tenant_id=tenant_id,
    )


@router.post(
    "/{reserva_id}/atender",
    response_model=ReservaResponse,
    summary="Atender y entregar o cancelar reserva en tienda",
)
def atender_reserva(
    reserva_id: int,
    datos: AtenderReservaRequest,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_staff_user),
):
    """
    CU11: Atender reserva en caja/mostrador.
    - ENTREGAR: Marca como ENTREGADA, libera el stock reservado y descuenta definitivamente el stock físico.
    - CANCELAR: Marca como CANCELADA y libera el stock reservado para venta general.
    """
    tenant_id = x_tenant_id or 1
    return AtenderReservaController.atender_reserva_sucursal(
        db=db,
        reserva_id=reserva_id,
        datos=datos,
        usuario_staff_id=usuario_id,
        tenant_id=tenant_id,
    )
