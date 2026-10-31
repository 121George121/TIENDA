# ==============================================================================
# CU27 - DASHBOARD EJECUTIVO Y REPORTES -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu27_dashboard_ejecutivo/dashboard_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu27_dashboard_ejecutivo.dashboard_controller import DashboardController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.schemas.cu27_dashboard_ejecutivo.dashboard_schema import (
    DashboardKpiDTO,
    VentaPorCanalDTO,
    VentaPorSucursalDTO,
    VentaPorMetodoPagoDTO,
    TopPrendaDTO,
    TenantSaaSResumenDTO,
    DashboardConsolidadoResponse
)

router = APIRouter(prefix="/dashboard-ejecutivo", tags=["CU27 - Dashboard Ejecutivo y Analítica Global"])


@router.get("/resumen", response_model=DashboardConsolidadoResponse, summary="Obtener resumen consolidado completo para el dashboard ejecutivo")
def obtener_resumen_consolidado(
    dias: Optional[int] = Query(None, description="Filtro temporal en días (1=Hoy, 7=Semana, 30=Mes, 365=Año, None=Todo)"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_dashboard_completo(db=db, dias=dias, tenant_id=tenant_id)


@router.get("/kpis", response_model=DashboardKpiDTO, summary="Obtener KPIs primarios y secundarios consolidados")
def obtener_kpis(
    dias: Optional[int] = Query(None, description="Filtro de días"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_kpis(db=db, dias=dias, tenant_id=tenant_id)


@router.get("/ventas-sucursal", response_model=List[VentaPorSucursalDTO], summary="Ventas consolidadas y participación por sucursal física")
def obtener_ventas_sucursal(
    dias: Optional[int] = Query(None, description="Filtro de días"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_ventas_sucursal(db=db, dias=dias, tenant_id=tenant_id)


@router.get("/ventas-canal", response_model=List[VentaPorCanalDTO], summary="Distribución omnicanal (Digital vs Presencial vs Offline)")
def obtener_ventas_canal(
    dias: Optional[int] = Query(None, description="Filtro de días"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_ventas_canal(db=db, dias=dias, tenant_id=tenant_id)


@router.get("/ventas-metodo", response_model=List[VentaPorMetodoPagoDTO], summary="Desglose por método y pasarela de pago")
def obtener_ventas_metodo(
    dias: Optional[int] = Query(None, description="Filtro de días"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_ventas_metodo_pago(db=db, dias=dias, tenant_id=tenant_id)


@router.get("/top-productos", response_model=List[TopPrendaDTO], summary="Top 5 prendas boutique más vendidas")
def obtener_top_productos(
    limite: int = Query(5, ge=1, le=20),
    dias: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_top_productos(db=db, limite=limite, dias=dias, tenant_id=tenant_id)


@router.get("/saas-resumen", response_model=TenantSaaSResumenDTO, summary="Métricas de suscripción y límites del Tenant SaaS")
def obtener_saas_resumen(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    return DashboardController.obtener_resumen_saas_tenant(db=db, tenant_id=tenant_id)


@router.get("/exportar-csv", summary="Descargar informe ejecutivo en formato CSV")
def exportar_csv(
    dias: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    csv_content = DashboardController.exportar_resumen_csv(db=db, dias=dias, tenant_id=tenant_id)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=informe_ejecutivo_multitenant.csv"}
    )
