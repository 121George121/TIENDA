# ==============================================================================
# CU27 - DASHBOARD EJECUTIVO Y REPORTES -> CONTROLADOR (MVC - CONTROLLER)
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
    def obtener_ventas_sucursal(db: Session, dias: Optional[int] = None, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return DashboardService.obtener_ventas_sucursal(db=db, dias=dias, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_canal(db: Session, dias: Optional[int] = None, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return DashboardService.obtener_ventas_canal(db=db, dias=dias, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_metodo_pago(db: Session, dias: Optional[int] = None, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return DashboardService.obtener_ventas_metodo_pago(db=db, dias=dias, tenant_id=tenant_id)

    @staticmethod
    def obtener_top_productos(db: Session, limite: int = 5, dias: Optional[int] = None, tenant_id: int = 1) -> List[Dict[str, Any]]:
        return DashboardService.obtener_top_productos(db=db, limite=limite, dias=dias, tenant_id=tenant_id)

    @staticmethod
    def obtener_resumen_saas_tenant(db: Session, tenant_id: int = 1) -> Dict[str, Any]:
        return DashboardService.obtener_resumen_saas_tenant(db=db, tenant_id=tenant_id)

    @staticmethod
    def obtener_dashboard_completo(db: Session, dias: Optional[int] = None, tenant_id: int = 1) -> Dict[str, Any]:
        return DashboardService.obtener_dashboard_completo(db=db, dias=dias, tenant_id=tenant_id)

    @staticmethod
    def exportar_resumen_csv(db: Session, dias: Optional[int] = None, tenant_id: int = 1) -> str:
        return DashboardService.exportar_resumen_csv(db=db, dias=dias, tenant_id=tenant_id)
