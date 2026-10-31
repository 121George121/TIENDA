# ==============================================================================
# CU23 - SINCRONIZAR OPERACIONES OFFLINE -> VISTAS (MVC - VIEW / ROUTER)
# Ubicación: backend/app/views/cu23_sincronizar_operaciones_offline/sincronizacion_offline_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.controllers.cu23_sincronizar_operaciones_offline.sincronizacion_offline_controller import SincronizacionOfflineController
from app.schemas.cu23_sincronizar_operaciones_offline.sincronizacion_offline_schema import (
    SyncLoteRequest,
    SincronizarPendientesRequest,
    SyncLoteResponse,
    SyncLogResponse,
    SyncKpisResponse,
    ResolverConflictoRequest
)

router = APIRouter(prefix="/sincronizacion-offline", tags=["CU23 - Sincronización Offline"])


@router.post(
    "/sincronizar-pendientes",
    response_model=SyncLoteResponse,
    summary="Consolidar todos los cobros offline pendientes del tenant"
)
def sincronizar_cobros_pendientes(
    req: SincronizarPendientesRequest = SincronizarPendientesRequest(),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Sincroniza todos los cobros en efectivo registrados en modo offline (CU22).
    Verifica stock en inventario, aplica la estrategia de resolución de discrepancias
    (por defecto PRIORIZAR_TIENDA_FISICA), crea las ventas/pagos oficiales y audita en Bitácora (CU26).
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    try:
        resultado = SincronizacionOfflineController.sincronizar_pendientes(
            db=db,
            tenant_id=tenant_id,
            usuario_id=current_user.id,
            sucursal_id=req.sucursal_id,
            estrategia_preferida=req.estrategia_preferida
        )
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al sincronizar cobros pendientes: {str(e)}"
        )


@router.post(
    "/lote",
    response_model=SyncLoteResponse,
    summary="Enviar lote de operaciones generadas offline desde cliente navegador"
)
def sincronizar_lote(
    req: SyncLoteRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Ingesta un lote de operaciones guardadas en IndexedDB/LocalStorage durante la pérdida de red.
    Garantiza idempotencia mediante UUID y resuelve discrepancias de stock.
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    try:
        resultado = SincronizacionOfflineController.sincronizar_lote(
            db=db,
            tenant_id=tenant_id,
            usuario_id=current_user.id,
            sucursal_id=req.sucursal_id,
            operaciones=req.operaciones,
            estrategia_preferida=req.estrategia_preferida
        )
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar lote offline: {str(e)}"
        )


@router.get(
    "/kpis",
    response_model=SyncKpisResponse,
    summary="Obtener métricas ejecutivas del motor de sincronización offline"
)
def obtener_kpis(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Retorna métricas del motor: operaciones sincronizadas, conflictos resueltos,
    errores y cobros offline pendientes con su monto total acumulado.
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return SincronizacionOfflineController.obtener_kpis(db=db, tenant_id=tenant_id)


@router.get(
    "/historial",
    response_model=List[SyncLogResponse],
    summary="Consultar log de sincronizaciones y resolución de conflictos"
)
def listar_historial_sync(
    limite: int = Query(50, ge=1, le=200),
    estado: Optional[str] = Query(None, description="Filtrar por estado: SINCRONIZADO, CONFLICTO_RESUELTO, ERROR, etc."),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Retorna el log detallado de transacciones offline procesadas y la política aplicada a cada una.
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return SincronizacionOfflineController.listar_historial(
        db=db,
        tenant_id=tenant_id,
        limite=limite,
        estado=estado
    )


@router.post(
    "/{sync_id}/resolver-conflicto",
    summary="Resolver manualmente una discrepancia o conflicto retenido"
)
def resolver_conflicto(
    sync_id: int,
    req: ResolverConflictoRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Permite al administrador o encargado aplicar una estrategia correctiva manual a un conflicto retenido.
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    try:
        resultado = SincronizacionOfflineController.resolver_conflicto_manual(
            db=db,
            tenant_id=tenant_id,
            usuario_id=current_user.id,
            sync_id=sync_id,
            estrategia=req.estrategia,
            notas=req.notas
        )
        return resultado
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al resolver conflicto: {str(e)}"
        )
