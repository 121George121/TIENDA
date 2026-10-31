# ==============================================================================
# CU27 - DASHBOARD EJECUTIVO -> ESQUEMAS PYDANTIC (MVC - SCHEMA)
# Ubicación: backend/app/schemas/cu27_dashboard_ejecutivo/dashboard_schema.py
# ==============================================================================

from pydantic import BaseModel, Field
from typing import List, Optional


class DashboardKpiDTO(BaseModel):
    total_ingresos_bs: float = Field(..., description="Ingresos brutos acumulados en BOB")
    ingresos_totales: float = Field(..., description="Alias para retrocompatibilidad")
    ingresos_netos_bs: float = Field(..., description="Ingresos netos descontando devoluciones en BOB")
    total_transacciones: int = Field(..., description="Número total de transacciones completadas")
    ticket_promedio_bs: float = Field(..., description="Gasto promedio por transacción")
    prendas_vendidas: int = Field(..., description="Total de unidades físicas entregadas")
    reservas_activas: int = Field(..., description="Reservas pendientes o confirmadas vigentes")
    articulos_stock_critico: int = Field(..., description="Artículos con stock igual o menor al mínimo")
    stock_total_fisico: int = Field(..., description="Total de prendas físicas en existencias")
    total_devoluciones: int = Field(default=0, description="Cantidad de devoluciones/cambios procesados")
    monto_devoluciones_bs: float = Field(default=0.0, description="Monto total devuelto en efectivo/crédito")
    operaciones_offline_sincronizadas: int = Field(default=0, description="Operaciones sincronizadas desde contingencia")
    fecha_calculo: str = Field(..., description="Timestamp de generación del cálculo")


class VentaPorCanalDTO(BaseModel):
    canal: str
    total_bs: float
    transacciones: int
    porcentaje: float = 0.0


class VentaPorSucursalDTO(BaseModel):
    sucursal_id: int
    sucursal_nombre: str
    ciudad: str
    total_bs: float
    transacciones: int
    porcentaje: float = 0.0


class VentaPorMetodoPagoDTO(BaseModel):
    metodo_id: int
    metodo_nombre: str
    total_bs: float
    cantidad_pagos: int
    porcentaje: float = 0.0


class TopPrendaDTO(BaseModel):
    variante_id: int
    sku: str
    nombre_producto: str
    precio_unitario: float
    unidades_vendidas: int
    recaudacion_bs: float


class TenantSaaSResumenDTO(BaseModel):
    tenant_id: int
    tenant_nombre: str
    plan_nombre: str
    sucursales_activas: int
    limite_sucursales: int
    usuarios_activos: int
    limite_usuarios: int
    vestidor_ia_habilitado: bool
    suscripcion_estado: str
    moneda_simbolo: str = "Bs."


class DashboardConsolidadoResponse(BaseModel):
    periodo: str
    kpis: DashboardKpiDTO
    ventas_canal: List[VentaPorCanalDTO]
    ventas_sucursal: List[VentaPorSucursalDTO]
    ventas_metodo: List[VentaPorMetodoPagoDTO]
    top_prendas: List[TopPrendaDTO]
    saas_tenant: TenantSaaSResumenDTO
