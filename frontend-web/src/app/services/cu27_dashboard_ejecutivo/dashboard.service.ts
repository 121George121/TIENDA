// CU27 - DASHBOARD EJECUTIVO Y REPORTES -> SERVICE
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private readonly apiUrl = `${environment.apiUrl}/dashboard-ejecutivo`;

  constructor(private http: HttpClient) {}

  obtenerKPIs(dias?: number): Observable<any> {
    const url = dias ? `${this.apiUrl}/kpis?dias=${dias}` : `${this.apiUrl}/kpis`;
    return this.http.get<any>(url);
  }

  obtenerVentasSucursal(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/ventas-sucursal`);
  }

  obtenerVentasCanal(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/ventas-canal`);
  }
}
