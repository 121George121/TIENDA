# ==============================================================================
# CU20 - GESTIONAR BITACORA Y AUDITORIA -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicacion: backend/app/views/cu20_gestionar_bitacora/bitacora_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Request, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
from app.schemas.cu20_gestionar_bitacora.bitacora_schema import (
    BitacoraCreate, BitacoraResponse, BitacoraListResponse, BitacoraStatsResponse
)

router = APIRouter(prefix="/bitacora", tags=["CU20 - Bitácora y Auditoría del Sistema (Web)"])


@router.get("", response_model=BitacoraListResponse, summary="Listar registros de auditoría")
def listar_bitacora(
    fecha_inicio: Optional[datetime] = Query(None, description="Fecha de inicio (ISO 8601)"),
    fecha_fin: Optional[datetime] = Query(None, description="Fecha de fin (ISO 8601)"),
    modulo: Optional[str] = Query(None, description="Filtrar por módulo"),
    accion: Optional[str] = Query(None, description="Filtrar por acción"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    search: Optional[str] = Query(None, description="Búsqueda por texto (detalle, IP, usuario)"),
    limit: int = Query(50, ge=1, le=200, description="Cantidad de registros por página"),
    offset: int = Query(0, ge=0, description="Desplazamiento / paginación"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """
    Retorna el historial paginado de bitácora con capacidades de filtrado multicriterio.
    """
    return BitacoraController.listar(
        db=db,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        modulo=modulo,
        accion=accion,
        usuario_id=usuario_id,
        search=search,
        limit=limit,
        offset=offset
    )


@router.get("/estadisticas", response_model=BitacoraStatsResponse, summary="Obtener KPIs y métricas de auditoría")
def obtener_estadisticas_bitacora(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """
    Retorna indicadores clave: eventos de hoy, semana, mes y distribución por módulo y acción.
    """
    return BitacoraController.obtener_estadisticas(db=db)


@router.get("/exportar", summary="Exportar registros filtrados a archivo CSV")
def exportar_bitacora_csv(
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    modulo: Optional[str] = Query(None),
    accion: Optional[str] = Query(None),
    usuario_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """
    Genera y descarga un archivo CSV con los registros de auditoría coincidentes con los filtros aplicados.
    """
    csv_data = BitacoraController.exportar_csv(
        db=db,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        modulo=modulo,
        accion=accion,
        usuario_id=usuario_id,
        search=search
    )

    filename = f"bitacora_auditoria_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        content=csv_data,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.post("", status_code=status.HTTP_201_CREATED, summary="Registrar evento manual en bitácora")
def crear_evento_bitacora(
    evento: BitacoraCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """
    Permite registrar un evento de auditoría originado desde el cliente web o servicios asociados.
    """
    ip_cliente = evento.ip or request.client.host if request.client else None
    usuario_efectivo = evento.usuarioid if evento.usuarioid is not None else current_user.id

    nuevo = BitacoraController.registrar_evento(
        db=db,
        accion=evento.accion,
        modulo=evento.modulo,
        usuario_id=usuario_efectivo,
        detalle=evento.detalle,
        ip=ip_cliente,
        datos_previos=evento.datosprevios,
        datos_nuevos=evento.datosnuevos
    )

    if not nuevo:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo registrar el evento en la bitácora"
        )

    return {
        "mensaje": "Evento registrado con éxito",
        "id": nuevo.id
    }
