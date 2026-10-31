# ==============================================================================
# CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu22_registrar_cobros_contado_offline/cobro_offline_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu22_registrar_cobros_contado_offline.cobro_offline_controller import CobroOfflineController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.schemas.cu22_registrar_cobros_contado_offline.cobro_offline_schema import (
    CobroOfflineCreate, CobroOfflineResponse, BatchCobrosOfflineRequest, CobroOfflineKpis
)

router = APIRouter(prefix="/cobros-offline", tags=["CU22 - Cobros Contado Offline"])


@router.post("/registrar", summary="Registrar cobro de contado generado en modo sin conexión")
def registrar_cobro_offline(
    req: CobroOfflineCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Registra un pago en efectivo capturado localmente durante una contingencia de red.
    Garantiza idempotencia mediante UUID y emite folio de auditoría.
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    try:
        cobro = CobroOfflineController.registrar_cobro(
            db=db,
            tenant_id=tenant_id,
            cajero_id=current_user.id,
            data=req
        )
        return {"exito": True, "cobro_offline": cobro}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar cobro de contingencia: {str(e)}"
        )


@router.get("", summary="Listar todos los cobros offline con filtros")
def listar_cobros(
    sucursal_id: Optional[int] = Query(None, description="Filtrar por ID de sucursal"),
    solo_pendientes: bool = Query(False, description="Listar únicamente los no sincronizados"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Retorna la lista de cobros offline detallados con información de prendas y cajero."""
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    cobros = CobroOfflineController.listar_cobros(
        db=db,
        tenant_id=tenant_id,
        sucursal_id=sucursal_id,
        solo_pendientes=solo_pendientes
    )
    return {"exito": True, "cobros": cobros}


@router.get("/pendientes", summary="Listar cobros de contado pendientes de sincronización")
def listar_cobros_pendientes(
    sucursal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Retorna los cobros de contingencia que aún no han sido sincronizados hacia ventas."""
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    pendientes = CobroOfflineController.listar_cobros(
        db=db,
        tenant_id=tenant_id,
        sucursal_id=sucursal_id,
        solo_pendientes=True
    )
    return {"exito": True, "pendientes": pendientes}


@router.get("/kpis", summary="Obtener KPIs de cobros de contingencia offline")
def obtener_kpis(
    sucursal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Retorna total recaudado offline, pendientes, montos en caja y sincronizados."""
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    kpis = CobroOfflineController.obtener_kpis(
        db=db,
        tenant_id=tenant_id,
        sucursal_id=sucursal_id
    )
    return {"exito": True, "kpis": kpis}


@router.get("/{cobro_id}", summary="Obtener detalle y datos para recibo térmico de contingencia")
def obtener_detalle_recibo(
    cobro_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Retorna los datos completos de un recibo provisional para vista/impresión de ticket."""
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    cobro = CobroOfflineController.obtener_cobro(db=db, cobro_id=cobro_id, tenant_id=tenant_id)
    if not cobro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cobro offline no encontrado.")
    return {"exito": True, "recibo": cobro}


@router.post("/lote", summary="Subida por lote de cobros acumulados en terminal offline")
def registrar_lote_offline(
    req: BatchCobrosOfflineRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Procesa e inserta un lote de cobros generado en LocalStorage durante desconexión prolongada."""
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    try:
        registrados = CobroOfflineController.registrar_lote(
            db=db,
            tenant_id=tenant_id,
            cajero_id=current_user.id,
            lote=req.cobros
        )
        return {"exito": True, "procesados": len(registrados), "cobros": registrados}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar lote de cobros offline: {str(e)}"
        )
