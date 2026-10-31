# ==============================================================================
# CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> VISTAS (MVC - VIEW / ROUTER)
# Ubicación: backend/app/views/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento_reserva_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu24_gestionar_cancelacion_vencimiento_reservas.vencimiento_reserva_controller import VencimientoReservaController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.schemas.cu24_gestionar_cancelacion_vencimiento_reservas.vencimiento_reserva_schema import (
    CancelarReservaRequest,
    EjecutarPurgaRequest,
    PurgaVencimientoResponse,
    ReservaExpiracionItemResponse,
    VencimientoReservaKpisResponse
)

router = APIRouter(prefix="/vencimiento-reservas", tags=["CU24 - Vencimiento y Cancelación de Reservas"])


@router.post(
    "/cancelar-vencidas",
    response_model=PurgaVencimientoResponse,
    summary="Ejecutar auditoría y purga de reservas vencidas (>48h) liberando stock a tienda"
)
def ejecutar_cancelacion_vencidas(
    req: EjecutarPurgaRequest = EjecutarPurgaRequest(),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Evalúa todas las reservas en estado PENDIENTE del tenant. Aquellas cuya antigüedad supere
    las horas límite (48h por defecto) son marcadas como VENCIDAS, sus prendas son liberadas
    en Inventario (disminuyendo stockreservado), se emite movimiento en Kardex, se notifica
    al cliente y se audita en Bitácora (CU26).
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    try:
        resultado = VencimientoReservaController.purgar_reservas_vencidas(
            db=db,
            tenant_id=tenant_id,
            horas_limite=req.horas_limite,
            sucursal_id=req.sucursal_id,
            usuario_ejecutor_id=current_user.id
        )
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la purga de reservas vencidas: {str(e)}"
        )


@router.post(
    "/{reserva_id}/cancelar-manual",
    summary="Cancelar manualmente una reserva activa y retornar prendas a stock"
)
def cancelar_reserva_manual(
    reserva_id: int,
    req: CancelarReservaRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Permite cancelar una reserva activa ingresando el motivo de la cancelación.
    Libera de inmediato las unidades comprometidas en el inventario de la sucursal.
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    reserva = VencimientoReservaController.cancelar_reserva(
        db=db,
        reserva_id=reserva_id,
        tenant_id=tenant_id,
        motivo=req.motivo,
        usuario_id=current_user.id
    )
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo cancelar la reserva especificada (no existe o ya no está pendiente)"
        )
    return {
        "exito": True,
        "mensaje": f"Reserva #{reserva.codigoreserva} cancelada y stock restituido a la sucursal exitosamente."
    }


@router.get(
    "/kpis",
    response_model=VencimientoReservaKpisResponse,
    summary="Obtener métricas de reservas activas, en riesgo y prendas reintegradas"
)
def obtener_kpis_vencimiento(
    horas_politica: int = Query(48, ge=1, le=720),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Retorna métricas ejecutivas: reservas activas, reservas a punto de vencer (<12h),
    total de prendas recuperadas y valor económico reintegrado.
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return VencimientoReservaController.obtener_kpis(
        db=db,
        tenant_id=tenant_id,
        horas_politica=horas_politica
    )


@router.get(
    "/reservas-activas",
    response_model=List[ReservaExpiracionItemResponse],
    summary="Listar reservas activas con cálculo de tiempo restante y alerta de proximidad"
)
def listar_reservas_activas(
    sucursal_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    horas_politica: int = Query(48, ge=1, le=720),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Retorna el listado completo de reservas pendientes de recogida con cuenta regresiva,
    alertas de vencimiento inminente y detalle de prendas.
    """
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return VencimientoReservaController.listar_reservas_activas(
        db=db,
        tenant_id=tenant_id,
        sucursal_id=sucursal_id,
        horas_politica=horas_politica
    )
