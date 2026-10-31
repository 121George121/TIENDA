# ==============================================================================
# CU20 - GENERAR REPORTES GENERATIVOS CON IA -> VISTAS / RUTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu20_generar_reportes_generativos_ia/reporte_generativo_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu20_generar_reportes_generativos_ia.reporte_generativo_controller import ReporteGenerativoController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel

router = APIRouter(prefix="/reportes-ia", tags=["CU20 - Reportes Generativos con IA"])


class ConsultaIARequest(BaseModel):
    prompt: str
    filtros: Optional[str] = None


@router.post("/consultar", summary="Generar reporte analítico mediante consulta en lenguaje natural con IA")
def consultar_reporte_ia(
    req: ConsultaIARequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    usuario_id = current_user.id
    try:
        reporte = ReporteGenerativoController.generar_reporte(
            db=db,
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            prompt=req.prompt,
            filtros=req.filtros
        )
        return {"exito": True, "datos": reporte}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al sintetizar el reporte analítico: {str(e)}"
        )


@router.get("/historial", summary="Obtener el historial de reportes generados")
def listar_historial(
    limite: int = 20,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    historial = ReporteGenerativoController.listar_historial(db=db, tenant_id=tenant_id, limite=limite)
    return {"exito": True, "historial": historial}


@router.get("/consultas-sugeridas", summary="Obtener plantillas de consultas en lenguaje natural listas para usar")
def obtener_sugerencias():
    sugerencias = ReporteGenerativoController.obtener_consultas_sugeridas()
    return {"exito": True, "sugerencias": sugerencias}


@router.get("/{reporte_id}", summary="Obtener el detalle de un reporte por su ID")
def obtener_detalle_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    reporte = ReporteGenerativoController.obtener_reporte(db=db, reporte_id=reporte_id, tenant_id=tenant_id)
    if not reporte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado")
    return {"exito": True, "datos": reporte}


@router.post("/{reporte_id}/favorito", summary="Marcar o desmarcar reporte como favorito")
def alternar_favorito(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    res = ReporteGenerativoController.alternar_favorito(db=db, reporte_id=reporte_id, tenant_id=tenant_id)
    return {"exito": True, "resultado": res}
