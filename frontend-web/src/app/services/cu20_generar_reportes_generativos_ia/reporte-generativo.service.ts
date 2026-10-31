// ==============================================================================
// CU20 - GENERAR REPORTES GENERATIVOS CON IA -> SERVICIO ANGULAR (MVC - SERVICE)
// Ubicación: frontend-web/src/app/services/cu20_generar_reportes_generativos_ia/reporte-generativo.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  ReporteGenerativoData,
  ConsultaIAPrompt,
  ConsultaSugerida,
  HistorialReporteItem
} from '../../models/cu20_generar_reportes_generativos_ia/reporte-generativo.model';

@Injectable({
  providedIn: 'root'
})
export class ReporteGenerativoService {
  private readonly apiUrl = `${environment.apiUrl}/reportes-ia`;

  constructor(private http: HttpClient) {}

  consultarReporteIA(payload: ConsultaIAPrompt): Observable<{ exito: boolean; datos: ReporteGenerativoData }> {
    return this.http.post<{ exito: boolean; datos: ReporteGenerativoData }>(`${this.apiUrl}/consultar`, payload);
  }

  obtenerHistorial(limite: number = 20): Observable<{ exito: boolean; historial: HistorialReporteItem[] }> {
    return this.http.get<{ exito: boolean; historial: HistorialReporteItem[] }>(`${this.apiUrl}/historial?limite=${limite}`);
  }

  obtenerConsultasSugeridas(): Observable<{ exito: boolean; sugerencias: ConsultaSugerida[] }> {
    return this.http.get<{ exito: boolean; sugerencias: ConsultaSugerida[] }>(`${this.apiUrl}/consultas-sugeridas`);
  }

  obtenerDetalleReporte(reporteId: number): Observable<{ exito: boolean; datos: ReporteGenerativoData }> {
    return this.http.get<{ exito: boolean; datos: ReporteGenerativoData }>(`${this.apiUrl}/${reporteId}`);
  }

  alternarFavorito(reporteId: number): Observable<{ exito: boolean; resultado: { reporte_id: number; es_favorito: boolean } }> {
    return this.http.post<{ exito: boolean; resultado: { reporte_id: number; es_favorito: boolean } }>(`${this.apiUrl}/${reporteId}/favorito`, {});
  }
}
