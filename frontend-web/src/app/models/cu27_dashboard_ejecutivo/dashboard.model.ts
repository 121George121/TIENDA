// ==============================================================================
// CU27 - DASHBOARD EJECUTIVO Y ANALÍTICA GLOBAL MULTITENANT -> MODELOS
// Ubicación: frontend-web/src/app/models/cu27_dashboard_ejecutivo/dashboard.model.ts
// ==============================================================================

export interface DashboardKPIs {
  total_ingresos_bs: number;
  ingresos_totales: number;
  ingresos_netos_bs: number;
  total_transacciones: number;
  ticket_promedio_bs: number;
  prendas_vendidas: number;
  reservas_activas: number;
  articulos_stock_critico: number;
  stock_total_fisico: number;
  total_devoluciones: number;
  monto_devoluciones_bs: number;
  operaciones_offline_sincronizadas: number;
  fecha_calculo: string;
}

export interface VentaPorCanal {
  canal: string;
  total_bs: number;
  transacciones: number;
  porcentaje: number;
}

export interface VentaPorSucursal {
  sucursal_id: number;
  sucursal_nombre: string;
  ciudad: string;
  total_bs: number;
  transacciones: number;
  porcentaje: number;
}

export interface VentaPorMetodoPago {
  metodo_id: number;
  metodo_nombre: string;
  total_bs: number;
  cantidad_pagos: number;
  porcentaje: number;
}

export interface TopPrenda {
  variante_id: number;
  sku: string;
  nombre_producto: string;
  precio_unitario: number;
  unidades_vendidas: number;
  recaudacion_bs: number;
}

export interface TenantSaaSResumen {
  tenant_id: number;
  tenant_nombre: string;
  plan_nombre: string;
  sucursales_activas: number;
  limite_sucursales: number;
  usuarios_activos: number;
  limite_usuarios: number;
  vestidor_ia_habilitado: boolean;
  suscripcion_estado: string;
  moneda_simbolo: string;
}

export interface DashboardConsolidado {
  periodo: string;
  kpis: DashboardKPIs;
  ventas_canal: VentaPorCanal[];
  ventas_sucursal: VentaPorSucursal[];
  ventas_metodo: VentaPorMetodoPago[];
  top_prendas: TopPrenda[];
  saas_tenant: TenantSaaSResumen;
}

export type TipoPeriodo = 'HOY' | '7D' | 'MES' | 'ANO' | 'TODO';
