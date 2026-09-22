import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MetodoPago, VentaCompleta, VentaDetallada, VentaPresencialCreateDTO } from '../../models/cu14_registrar_ventas_presenciales/venta.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class VentaService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getVentas(tipo?: string, sucursalId?: number, skip: number = 0, limit: number = 100): Observable<VentaCompleta[]> {
    let params = new HttpParams();
    if (tipo) params = params.set('tipo', tipo);
    if (sucursalId) params = params.set('sucursal_id', sucursalId.toString());
    params = params.set('skip', skip.toString());
    params = params.set('limit', limit.toString());

    return this.http.get<VentaCompleta[]>(`${this.apiUrl}/ventas`, { params });
  }

  getVentaById(id: number): Observable<VentaDetallada> {
    return this.http.get<VentaDetallada>(`${this.apiUrl}/ventas/${id}`);
  }

  registrarVentaPresencial(dto: VentaPresencialCreateDTO): Observable<VentaCompleta> {
    return this.http.post<VentaCompleta>(`${this.apiUrl}/ventas/presencial`, dto);
  }

  getMetodosPago(): Observable<MetodoPago[]> {
    return this.http.get<MetodoPago[]>(`${this.apiUrl}/metodos-pago`);
  }
}
