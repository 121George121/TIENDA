# ==============================================================================
# CU20 - GENERAR REPORTES Y DASHBOARDS -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu20_generar_reportes_dashboards/reporte_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.controllers.cu20_generar_reportes_dashboards.reporte_controller import ReporteController

router = APIRouter(prefix="/reportes", tags=["CU20 - Generar Reportes y Dashboards (Web)"])


@router.get("/kpis", summary="Obtener KPIs ejecutivos para dashboard administrativo")
def obtener_kpis(
    dias: Optional[int] = Query(None, description="Filtrar por días (7, 30, etc.)"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU20: Retorna ingresos totales, ticket promedio, prendas vendidas y stock crítico."""
    return ReporteController.obtener_kpis(db=db, dias=dias)


@router.get("/ventas-por-sucursal", summary="Ventas e ingresos por sucursal física")
def obtener_ventas_sucursal(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU20: Retorna facturación y transacciones por cada sucursal."""
    return ReporteController.obtener_ventas_por_sucursal(db=db)


@router.get("/ventas-por-canal", summary="Ventas Digitales vs Presenciales")
def obtener_ventas_canal(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU20: Distribución de ventas online (Web/Móvil) vs ventas en tienda (POS)."""
    return ReporteController.obtener_ventas_por_canal(db=db)


@router.get("/ventas-por-metodo-pago", summary="Ingresos desglosados por método de pago")
def obtener_ventas_metodo_pago(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU20: Total recaudado a través de PayPal, QR BCP, Efectivo y Tarjetas."""
    return ReporteController.obtener_ventas_por_metodo_pago(db=db)


@router.get("/top-prendas", summary="Top 5 poleras más vendidas")
def obtener_top_prendas(
    limite: int = Query(5, description="Cantidad de prendas en el ranking"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU20: Ranking de productos con mayores ventas y recaudación en Bs."""
    return ReporteController.obtener_top_prendas(db=db, limite=limite)


@router.get("/exportar-csv", summary="Descargar reporte completo de ventas en formato CSV")
def exportar_csv(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU20: Genera y descarga el archivo CSV con todas las ventas del ERP."""
    csv_data = ReporteController.exportar_ventas_csv(db=db)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=reporte_ventas_boutique.csv"
        }
    )
