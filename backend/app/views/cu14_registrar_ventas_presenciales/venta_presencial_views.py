# ==============================================================================
# CU14 - REGISTRAR VENTAS PRESENCIALES -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu14_registrar_ventas_presenciales/venta_presencial_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Header, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import require_staff
from app.models.models import UsuarioModel
from app.schemas.orden_schema import (
    VentaPresencialCreate,
    VentaCompletaResponse,
    VentaDetalladaResponse,
    MetodoPagoResponse,
)
from app.controllers.cu14_registrar_ventas_presenciales.venta_presencial_controller import (
    VentaPresencialController,
)

router = APIRouter(tags=["CU14 - Registrar Ventas Presenciales (POS)"])


def _resolver_tenant_id(
    x_tenant_id: Optional[int], current_user: Optional[UsuarioModel]
) -> int:
    if x_tenant_id is not None:
        return x_tenant_id
    if current_user and getattr(current_user, "tenant_id", None):
        return current_user.tenant_id
    return 1


@router.post(
    "/ventas/presencial",
    response_model=VentaCompletaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar venta presencial en mostrador (POS)",
)
def registrar_venta_presencial(
    data: VentaPresencialCreate,
    request: Request,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff),
):
    """
    CU14: Permite al personal de mostrador / cajero registrar una venta física (POS),
    descontando stock disponible libre de reservas y registrando el comprobante en caja.
    """
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    ip_origen = request.client.host if request.client else "127.0.0.1"
    return VentaPresencialController.registrar_venta_presencial(
        db=db,
        current_user=current_user,
        data=data,
        tenant_id=tenant_id,
        ip_origen=ip_origen,
    )


@router.get(
    "/ventas",
    response_model=List[VentaCompletaResponse],
    summary="Listar todas las ventas (Presenciales y Digitales)",
)
def listar_ventas(
    tipo: Optional[str] = Query(None, description="Filtrar por 'Presencial' o 'Digital'"),
    sucursal_id: Optional[int] = Query(None, description="Filtrar por ID de sucursal"),
    skip: int = 0,
    limit: int = 100,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff),
):
    """Listado de ventas para auditoría en el panel administrativo con aislamiento multi-tenant"""
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    return VentaPresencialController.listar_todas_ventas(
        db=db,
        tipoventa=tipo,
        sucursal_id=sucursal_id,
        skip=skip,
        limit=limit,
        tenant_id=tenant_id,
    )


@router.get(
    "/ventas/{venta_id}",
    response_model=VentaDetalladaResponse,
    summary="Obtener comprobante desglosado de una venta",
)
def obtener_venta_por_id(
    venta_id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff),
):
    """Permite al cajero o administrador consultar el detalle completo de un comprobante/recibo"""
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    return VentaPresencialController.obtener_venta_por_id(
        db=db,
        venta_id=venta_id,
        tenant_id=tenant_id,
    )


@router.get(
    "/metodos-pago",
    response_model=List[MetodoPagoResponse],
    summary="Listar métodos de pago disponibles",
)
def listar_metodos_pago(db: Session = Depends(get_db)):
    """Consulta de formas de pago activas (Efectivo, Tarjeta, QR, etc.)"""
    return VentaPresencialController.listar_metodos_pago(db=db)
