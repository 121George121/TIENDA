# ==============================================================================
# CU27 - DASHBOARD EJECUTIVO Y REPORTES -> SERVICIO (MVC - SERVICE)
# Ubicación: backend/app/services/cu27_dashboard_ejecutivo/dashboard_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from app.controllers.cu20_generar_reportes_dashboards.reporte_controller import ReporteController as LegacyReporteController


class DashboardService:
    """
    Servicio para consolidar métricas, KPIs ejecutivos, gráficos de rendimiento y reportes de la tienda.
    """

    @staticmethod
    def obtener_kpis(db: Session, dias: Optional[int] = None, tenant_id: int = 1) -> Dict[str, Any]:
        return LegacyReporteController.obtener_kpis(db=db, dias=dias, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_sucursal(db: Session, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return LegacyReporteController.obtener_ventas_por_sucursal(db=db, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_canal(db: Session, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return LegacyReporteController.obtener_ventas_por_canal(db=db, tenant_id=tenant_id)

    @staticmethod
    def obtener_top_productos(db: Session, limite: int = 5, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return LegacyReporteController.obtener_productos_mas_vendidos(db=db, limite=limite, tenant_id=tenant_id)
