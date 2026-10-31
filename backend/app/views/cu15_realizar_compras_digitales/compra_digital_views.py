# ==============================================================================
# CU15 - REALIZAR COMPRAS DIGITALES -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu15_realizar_compras_digitales/compra_digital_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_current_tenant_user
from app.models.models import UsuarioModel
from app.schemas.orden_schema import (
    OrdenCreate,
    OrdenResponse,
    OrdenTrackingResponse,
    ActualizarEstadoOrdenRequest
)
from app.controllers.cu15_realizar_compras_digitales.compra_digital_controller import CompraDigitalController

router = APIRouter(tags=["CU15 - Realizar Compras Digitales (Web y Móvil)"])


@router.post("/ordenes", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED, summary="Procesar compra digital (App Móvil / Web)")
@router.post("/ordenes/", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/compras/procesar", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED, summary="Alias para procesar compra digital")
def crear_orden_digital(
    data: OrdenCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_tenant_user)
):
    """
    CU15: Procesa la compra online, valida stock disponible, genera la venta digital,
    emite recibo fiscal, registra el pago, vacía el carrito y asienta en Kardex y Bitácora.
    """
    tenant_id = getattr(current_user, 'tenant_id', 1) or 1
    return CompraDigitalController.procesar_orden_digital(
        db=db,
        current_user=current_user,
        data=data,
        tenant_id=tenant_id
    )


@router.get("/ordenes/me", response_model=List[OrdenResponse], summary="Historial de compras y pedidos del cliente autenticado")
def consultar_mis_ordenes(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_tenant_user)
):
    """
    CU15: Permite al cliente autenticado ver sus compras digitales pasadas y el estado de entrega.
    """
    tenant_id = getattr(current_user, 'tenant_id', 1) or 1
    return CompraDigitalController.listar_mis_ordenes(
        db=db,
        current_user=current_user,
        tenant_id=tenant_id
    )


@router.get("/ordenes/{orden_id}/tracking", response_model=OrdenTrackingResponse, summary="Consultar tracking y timeline de entrega de una orden")
def consultar_tracking(
    orden_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_tenant_user)
):
    """
    CU15: Consulta las etapas de despacho de la orden (Confirmado -> Preparación -> En Camino -> Entregado).
    """
    tenant_id = getattr(current_user, 'tenant_id', 1) or 1
    return CompraDigitalController.consultar_tracking(
        db=db,
        orden_id=orden_id,
        current_user=current_user,
        tenant_id=tenant_id
    )


@router.put("/ordenes/{orden_id}/estado", summary="Actualizar estado logístico de la orden (Admin/Personal)")
def actualizar_estado_orden(
    orden_id: int,
    req: ActualizarEstadoOrdenRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_tenant_user)
):
    """
    CU15: Permite al encargado/administrador avanzar el estado logístico de un pedido online.
    """
    tenant_id = getattr(current_user, 'tenant_id', 1) or 1
    return CompraDigitalController.actualizar_estado_orden(
        db=db,
        orden_id=orden_id,
        req=req,
        usuario_actual=current_user,
        tenant_id=tenant_id
    )
