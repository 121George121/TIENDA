# ==============================================================================
# CU14 - REGISTRAR VENTAS PRESENCIALES -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu14_registrar_ventas_presenciales/venta_presencial_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import require_staff
from app.models.models import UsuarioModel
from app.schemas.orden_schema import (
    VentaPresencialCreate,
    VentaCompletaResponse,
    VentaDetalladaResponse,
    MetodoPagoResponse
)
from app.controllers.cu14_registrar_ventas_presenciales.venta_presencial_controller import VentaPresencialController

router = APIRouter(tags=["CU14 - Registrar Ventas Presenciales (POS)"])


@router.post("/ventas/presencial", response_model=VentaCompletaResponse, status_code=status.HTTP_201_CREATED, summary="Registrar venta presencial en mostrador (POS)")
def registrar_venta_presencial(
    data: VentaPresencialCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff)
):
    """
    CU14: Permite al personal de mostrador / cajero registrar una venta física (POS),
    descontando stock de la sucursal y registrando el pago correspondiente.
    """
    return VentaPresencialController.registrar_venta_presencial(db=db, current_user=current_user, data=data)


@router.get("/ventas", response_model=List[VentaCompletaResponse], summary="Listar todas las ventas (Presenciales y Digitales)")
def listar_ventas(
    tipo: Optional[str] = Query(None, description="Filtrar por 'Presencial' o 'Digital'"),
    sucursal_id: Optional[int] = Query(None, description="Filtrar por ID de sucursal"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff)
):
    """Listado general de ventas para auditoría en el panel administrativo ERP"""
    return VentaPresencialController.listar_todas_ventas(db=db, tipoventa=tipo, sucursal_id=sucursal_id, skip=skip, limit=limit)


@router.get("/ventas/{venta_id}", response_model=VentaDetalladaResponse, summary="Obtener comprobante desglosado de una venta")
def obtener_venta_por_id(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff)
):
    """Permite al cajero o administrador consultar el detalle completo de un comprobante/recibo"""
    return VentaPresencialController.obtener_venta_por_id(db=db, venta_id=venta_id)


@router.get("/metodos-pago", response_model=List[MetodoPagoResponse], summary="Listar métodos de pago disponibles")
def listar_metodos_pago(db: Session = Depends(get_db)):
    """Consulta de formas de pago activas (Efectivo, Tarjeta, QR, etc.)"""
    return VentaPresencialController.listar_metodos_pago(db=db)
