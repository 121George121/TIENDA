// ==============================================================================
// CU20 - GESTIONAR BITACORA Y AUDITORIA -> CAPA SERVICIO (FRONTEND)
// Ubicacion: frontend-web/src/app/services/cu20_gestionar_bitacora/bitacora.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { BitacoraListResponse, BitacoraStats, BitacoraFilter } from '../../models/cu20_gestionar_bitacora/bitacora.model';

@Injectable({
  providedIn: 'root'
})
export class BitacoraService {
  private apiUrl = `${environment.apiUrl}/bitacora`;

  constructor(private http: HttpClient) {}

  getLogs(filter: BitacoraFilter = {}): Observable<BitacoraListResponse> {
    let params = new HttpParams();

    if (filter.fecha_inicio) {
      params = params.set('fecha_inicio', filter.fecha_inicio);
    }
    if (filter.fecha_fin) {
      params = params.set('fecha_fin', filter.fecha_fin);
    }
    if (filter.modulo && filter.modulo !== 'TODOS') {
      params = params.set('modulo', filter.modulo);
    }
    if (filter.accion && filter.accion !== 'TODAS') {
      params = params.set('accion', filter.accion);
    }
    if (filter.usuario_id) {
      params = params.set('usuario_id', filter.usuario_id.toString());
    }
    if (filter.search && filter.search.trim()) {
      params = params.set('search', filter.search.trim());
    }
    if (filter.limit !== undefined) {
      params = params.set('limit', filter.limit.toString());
    }
    if (filter.offset !== undefined) {
      params = params.set('offset', filter.offset.toString());
    }

    return this.http.get<BitacoraListResponse>(this.apiUrl, { params });
  }

  getStats(): Observable<BitacoraStats> {
    return this.http.get<BitacoraStats>(`${this.apiUrl}/estadisticas`);
  }

  exportCsv(filter: BitacoraFilter = {}): Observable<Blob> {
    let params = new HttpParams();

    if (filter.fecha_inicio) {
      params = params.set('fecha_inicio', filter.fecha_inicio);
    }
    if (filter.fecha_fin) {
      params = params.set('fecha_fin', filter.fecha_fin);
    }
    if (filter.modulo && filter.modulo !== 'TODOS') {
      params = params.set('modulo', filter.modulo);
    }
    if (filter.accion && filter.accion !== 'TODAS') {
      params = params.set('accion', filter.accion);
    }
    if (filter.usuario_id) {
      params = params.set('usuario_id', filter.usuario_id.toString());
    }
    if (filter.search && filter.search.trim()) {
      params = params.set('search', filter.search.trim());
    }

    return this.http.get(`${this.apiUrl}/exportar`, {
      params,
      responseType: 'blob'
    });
  }
}
