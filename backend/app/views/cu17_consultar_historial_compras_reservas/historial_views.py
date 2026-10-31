# ==============================================================================
# CU17 - CONSULTAR HISTORIAL DE COMPRAS Y RESERVAS -> CAPA VISTA / RUTAS API (MVC)
# Ubicación: backend/app/views/cu17_consultar_historial_compras_reservas/historial_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.core.dependencies import get_current_tenant_user
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.controllers.cu17_consultar_historial_compras_reservas.historial_controller import HistorialController

router = APIRouter(prefix="/historial", tags=["CU17 - Consultar Historial de Compras y Reservas (Web y Móvil)"])


@router.get("/resumen", summary="Resumen de actividad del cliente (compras, reservas, total invertido)")
def obtener_resumen(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_tenant_user)
):
    """CU17: Retorna el resumen consolidado de compras y reservas del cliente."""
    tenant_id = getattr(current_user, 'tenant_id', 1) or 1
    return HistorialController.obtener_resumen_cliente(db=db, current_user=current_user, tenant_id=tenant_id)


@router.get("/compras", summary="Historial de compras del cliente con tracking de entrega y comprobante")
def listar_compras(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_tenant_user)
):
    """CU17: Retorna la lista de pedidos con timeline de estado logístico y acceso al comprobante con QR."""
    tenant_id = getattr(current_user, 'tenant_id', 1) or 1
    return HistorialController.listar_compras_cliente(db=db, current_user=current_user, tenant_id=tenant_id)


@router.get("/reservas", summary="Historial de reservas de prendas con QR de retiro en tienda y tiempo restante")
def listar_reservas(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_tenant_user)
):
    """CU17: Retorna las reservas del cliente con QR de retiro físico y horas restantes de la ventana de 48 horas."""
    tenant_id = getattr(current_user, 'tenant_id', 1) or 1
    return HistorialController.listar_reservas_cliente(db=db, current_user=current_user, tenant_id=tenant_id)

