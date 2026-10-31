// ==============================================================================
// CU27 - DASHBOARD EJECUTIVO Y REPORTES -> SERVICIO HTTP (ANGULAR 18)
// Ubicación: frontend-web/src/app/services/cu27_dashboard_ejecutivo/dashboard.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  DashboardConsolidado,
  DashboardKPIs,
  VentaPorCanal,
  VentaPorSucursal,
  VentaPorMetodoPago,
  TopPrenda,
  TenantSaaSResumen
} from '../../models/cu27_dashboard_ejecutivo/dashboard.model';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private readonly apiUrl = `${environment.apiUrl}/dashboard-ejecutivo`;

  constructor(private http: HttpClient) {}

  obtenerResumenConsolidado(dias?: number): Observable<DashboardConsolidado> {
    let params = new HttpParams();
    if (dias !== undefined && dias !== null) {
      params = params.set('dias', dias.toString());
    }
    return this.http.get<DashboardConsolidado>(`${this.apiUrl}/resumen`, { params });
  }

  obtenerKPIs(dias?: number): Observable<DashboardKPIs> {
    let params = new HttpParams();
    if (dias !== undefined && dias !== null) {
      params = params.set('dias', dias.toString());
    }
    return this.http.get<DashboardKPIs>(`${this.apiUrl}/kpis`, { params });
  }

  obtenerVentasSucursal(dias?: number): Observable<VentaPorSucursal[]> {
    let params = new HttpParams();
    if (dias !== undefined && dias !== null) {
      params = params.set('dias', dias.toString());
    }
    return this.http.get<VentaPorSucursal[]>(`${this.apiUrl}/ventas-sucursal`, { params });
  }

  obtenerVentasCanal(dias?: number): Observable<VentaPorCanal[]> {
    let params = new HttpParams();
    if (dias !== undefined && dias !== null) {
      params = params.set('dias', dias.toString());
    }
    return this.http.get<VentaPorCanal[]>(`${this.apiUrl}/ventas-canal`, { params });
  }

  obtenerVentasMetodo(dias?: number): Observable<VentaPorMetodoPago[]> {
    let params = new HttpParams();
    if (dias !== undefined && dias !== null) {
      params = params.set('dias', dias.toString());
    }
    return this.http.get<VentaPorMetodoPago[]>(`${this.apiUrl}/ventas-metodo`, { params });
  }

  obtenerTopPrendas(limite: number = 5, dias?: number): Observable<TopPrenda[]> {
    let params = new HttpParams().set('limite', limite.toString());
    if (dias !== undefined && dias !== null) {
      params = params.set('dias', dias.toString());
    }
    return this.http.get<TopPrenda[]>(`${this.apiUrl}/top-productos`, { params });
  }

  obtenerSaaSResumen(): Observable<TenantSaaSResumen> {
    return this.http.get<TenantSaaSResumen>(`${this.apiUrl}/saas-resumen`);
  }

  descargarCSV(dias?: number): void {
    let params = new HttpParams();
    if (dias !== undefined && dias !== null) {
      params = params.set('dias', dias.toString());
    }

    this.http.get(`${this.apiUrl}/exportar-csv`, {
      params,
      responseType: 'blob'
    }).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const sufijo = dias ? `_${dias}dias` : '_historico';
        a.download = `informe_ejecutivo_boutique${sufijo}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      },
      error: (err) => console.error('Error al descargar reporte ejecutivo CSV:', err)
    });
  }
}
