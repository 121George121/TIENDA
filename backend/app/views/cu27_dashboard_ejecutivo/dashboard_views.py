# ==============================================================================
# CU27 - DASHBOARD EJECUTIVO Y REPORTES -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu27_dashboard_ejecutivo/dashboard_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu27_dashboard_ejecutivo.dashboard_controller import DashboardController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel

router = APIRouter(prefix="/dashboard-ejecutivo", tags=["CU27 - Dashboard Ejecutivo y KPIs"])


@router.get("/kpis", summary="Obtener KPIs consolidados para el dashboard directivo")
def obtener_kpis(
    dias: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_kpis(db=db, dias=dias, tenant_id=tenant_id)


@router.get("/ventas-sucursal", summary="Ventas consolidadas por sucursal")
def obtener_ventas_sucursal(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_ventas_sucursal(db=db, tenant_id=tenant_id)


@router.get("/ventas-canal", summary="Comparativa de canales Digital vs Presencial POS")
def obtener_ventas_canal(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_ventas_canal(db=db, tenant_id=tenant_id)
