# ==============================================================================
# CU15 - REALIZAR COMPRAS DIGITALES -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu15_realizar_compras_digitales/compra_digital_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.models import UsuarioModel
from app.schemas.orden_schema import (
    OrdenCreate,
    OrdenResponse
)
from app.controllers.cu15_realizar_compras_digitales.compra_digital_controller import CompraDigitalController

router = APIRouter(tags=["CU15 - Realizar Compras Digitales (Web y Móvil)"])


@router.post("/ordenes", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED, summary="Procesar compra digital (App Móvil / Web)")
@router.post("/ordenes/", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def crear_orden_digital(
    data: OrdenCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """
    CU15: Procesa la compra online, genera la venta digital, registra el pago
    y descuenta automáticamente el stock en el inventario físico de la tienda.
    """
    return CompraDigitalController.procesar_orden_digital(db=db, current_user=current_user, data=data)


@router.get("/ordenes/me", response_model=List[OrdenResponse], summary="Historial de pedidos del cliente autenticado")
def consultar_mis_ordenes(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU15: Permite al cliente autenticado ver sus pedidos pasados desde la app móvil o web"""
    return CompraDigitalController.listar_mis_ordenes(db=db, current_user=current_user)
