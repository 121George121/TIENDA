# ==============================================================================
# CU20 - GENERAR REPORTES Y DASHBOARDS -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu20_generar_reportes_dashboards/reporte_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from app.services.cu20_generar_reportes_dashboards.reporte_service import ReporteService


class ReporteController:

    @staticmethod
    def obtener_kpis(
        db: Session,
        dias: Optional[int] = None,
        tenant_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """CU20: Retorna los KPIs ejecutivos calculados directamente de las tablas de PostgreSQL."""
        return ReporteService.obtener_kpis(db=db, dias=dias, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_por_sucursal(
        db: Session,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU20: Retorna distribución de ingresos y transacciones por sucursal física."""
        return ReporteService.obtener_ventas_por_sucursal(db=db, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_por_canal(
        db: Session,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU20: Retorna proporción entre ventas Digitales (App/Web) vs Presenciales (Caja/POS)."""
        return ReporteService.obtener_ventas_por_canal(db=db, tenant_id=tenant_id)

    @staticmethod
    def obtener_ventas_por_metodo_pago(
        db: Session,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU20: Desglose de ingresos por método de pago (PayPal, QR, Efectivo, Tarjeta)."""
        return ReporteService.obtener_ventas_por_metodo_pago(db=db, tenant_id=tenant_id)

    @staticmethod
    def obtener_top_prendas(
        db: Session,
        limite: int = 5,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """CU20: Top 5 de poleras más vendidas con ingresos generados."""
        return ReporteService.obtener_top_prendas(db=db, limite=limite, tenant_id=tenant_id)

    @staticmethod
    def exportar_ventas_csv(
        db: Session,
        tenant_id: Optional[int] = None
    ) -> str:
        """CU20: Genera archivo CSV descargable con todas las transacciones del sistema."""
        return ReporteService.exportar_ventas_csv(db=db, tenant_id=tenant_id)

