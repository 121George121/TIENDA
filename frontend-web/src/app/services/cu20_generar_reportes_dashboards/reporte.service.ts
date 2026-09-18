// ==============================================================================
// CU20 - GENERAR REPORTES Y DASHBOARDS -> SERVICIO ANGULAR
// Ubicación: frontend-web/src/app/services/cu20_generar_reportes_dashboards/reporte.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DashboardKPIs {
  total_ingresos_bs: number;
  total_transacciones: number;
  ticket_promedio_bs: number;
  prendas_vendidas: number;
  reservas_activas: number;
  stock_total_fisico: number;
  articulos_stock_critico: number;
  fecha_calculo: string;
}

export interface VentasPorSucursal {
  sucursal_id: number;
  sucursal_nombre: string;
  ciudad: string;
  total_bs: number;
  transacciones: number;
}

export interface VentasPorCanal {
  canal: string;
  total_bs: number;
  transacciones: number;
}

export interface VentasPorMetodoPago {
  metodo_id: number;
  metodo_nombre: string;
  total_bs: number;
  cantidad_pagos: number;
}

export interface TopPrenda {
  variante_id: number;
  sku: string;
  nombre_producto: string;
  precio_unitario: number;
  unidades_vendidas: number;
  recaudacion_bs: number;
}

@Injectable({
  providedIn: 'root'
})
export class ReporteService {
  private readonly apiUrl = 'http://localhost:8000/api/v1/reportes';

  constructor(private http: HttpClient) {}

  getKPIs(dias?: number): Observable<DashboardKPIs> {
    const params = dias ? `?dias=${dias}` : '';
    return this.http.get<DashboardKPIs>(`${this.apiUrl}/kpis${params}`);
  }

  getVentasPorSucursal(): Observable<VentasPorSucursal[]> {
    return this.http.get<VentasPorSucursal[]>(`${this.apiUrl}/ventas-por-sucursal`);
  }

  getVentasPorCanal(): Observable<VentasPorCanal[]> {
    return this.http.get<VentasPorCanal[]>(`${this.apiUrl}/ventas-por-canal`);
  }

  getVentasPorMetodoPago(): Observable<VentasPorMetodoPago[]> {
    return this.http.get<VentasPorMetodoPago[]>(`${this.apiUrl}/ventas-por-metodo-pago`);
  }

  getTopPrendas(limite: number = 5): Observable<TopPrenda[]> {
    return this.http.get<TopPrenda[]>(`${this.apiUrl}/top-prendas?limite=${limite}`);
  }

  descargarCSV(): void {
    window.open(`${this.apiUrl}/exportar-csv`, '_blank');
  }
}
