// ==============================================================================
// CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> SERVICIO HTTP (FRONTEND)
// Ubicación: frontend-web/src/app/services/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  PurgaVencimientoResultado,
  ReservaExpiracionItem,
  VencimientoReservaKpisDTO,
  CancelarReservaRequest,
  EjecutarPurgaRequest
} from '../../models/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.model';

@Injectable({
  providedIn: 'root'
})
export class VencimientoReservaService {
  private readonly apiUrl = `${environment.apiUrl}/vencimiento-reservas`;

  constructor(private http: HttpClient) {}

  /**
   * Ejecuta el proceso de auditoría y cancelación de reservas que hayan superado las 48 horas.
   */
  cancelarVencidas(horasLimite: number = 48, sucursalId?: number): Observable<PurgaVencimientoResultado> {
    const body: EjecutarPurgaRequest = {
      horas_limite: horasLimite,
      sucursal_id: sucursalId
    };
    return this.http.post<PurgaVencimientoResultado>(`${this.apiUrl}/cancelar-vencidas`, body);
  }

  /**
   * Cancela manualmente una reserva activa ingresando el motivo de la cancelación.
   */
  cancelarReservaManual(reservaId: number, motivo: string): Observable<{ exito: boolean; mensaje: string }> {
    const body: CancelarReservaRequest = { motivo };
    return this.http.post<{ exito: boolean; mensaje: string }>(
      `${this.apiUrl}/${reservaId}/cancelar-manual`,
      body
    );
  }

  /**
   * Obtiene las métricas consolidadas del motor de reservas y vencimientos.
   */
  obtenerKpis(horasPolitica: number = 48): Observable<VencimientoReservaKpisDTO> {
    const params = new HttpParams().set('horas_politica', horasPolitica.toString());
    return this.http.get<VencimientoReservaKpisDTO>(`${this.apiUrl}/kpis`, { params });
  }

  /**
   * Recupera todas las reservas pendientes con el cálculo de cuenta regresiva y proximidad.
   */
  listarReservasActivas(sucursalId?: number, horasPolitica: number = 48): Observable<ReservaExpiracionItem[]> {
    let params = new HttpParams().set('horas_politica', horasPolitica.toString());
    if (sucursalId) {
      params = params.set('sucursal_id', sucursalId.toString());
    }
    return this.http.get<ReservaExpiracionItem[]>(`${this.apiUrl}/reservas-activas`, { params });
  }
}
