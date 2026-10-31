# ==============================================================================
# CU27 - DASHBOARD EJECUTIVO Y REPORTES -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu27_dashboard_ejecutivo/dashboard_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from app.services.cu27_dashboard_ejecutivo.dashboard_service import DashboardService


class DashboardController:

    @staticmethod
    def obtener_kpis(db: Session, dias: Optional[int] = None, tenant_id: int = 1) -> Dict[str, Any]:
        return DashboardService.obtener_kpis(db=db, dias=dias, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_sucursal(db: Session, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return DashboardService.obtener_ventas_sucursal(db=db, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_canal(db: Session, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return DashboardService.obtener_ventas_canal(db=db, tenant_id=tenant_id)

    @staticmethod
    def obtener_top_productos(db: Session, limite: int = 5, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return DashboardService.obtener_top_productos(db=db, limite=limite, tenant_id=tenant_id)
