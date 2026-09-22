// ==============================================================================
// CAPA SERVICIO (MVC - SERVICE EN FRONTEND ANGULAR)
// Módulo: CU11 - Atender Reservas en Sucursal
// Ubicación: frontend-web/src/app/services/cu11_atender_reservas_sucursal/reservation-admin.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reserva, AtenderReservaDTO } from '../../models/cu10_gestionar_reservas_prendas/reservation.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ReservationAdminService {
  private apiUrl = `${environment.apiUrl}/reservas`;

  constructor(private http: HttpClient) {}

  /** CU11: Listado general de reservas para administración y encargados de sucursal */
  getReservasAdmin(sucursalId?: number | null, estado?: string | null): Observable<Reserva[]> {
    let params: any = {};
    if (sucursalId) params.sucursal_id = sucursalId;
    if (estado && estado !== 'TODAS') params.estado = estado;
    return this.http.get<Reserva[]>(`${this.apiUrl}/admin/listado`, { params });
  }

  /** CU11: Búsqueda rápida por código alfanumérico para el punto de atención */
  buscarPorCodigo(codigo: string): Observable<Reserva> {
    const codigoLimpio = codigo.trim().toUpperCase();
    return this.http.get<Reserva>(`${this.apiUrl}/admin/buscar/${codigoLimpio}`);
  }

  /** CU11: Atender reserva en caja/mostrador (Entregar y cobrar o Cancelar) */
  atenderReserva(reservaId: number, accion: 'ENTREGAR' | 'CANCELAR', observaciones?: string): Observable<Reserva> {
    const payload: AtenderReservaDTO = {
      accion: accion,
      observaciones: observaciones
    };
    return this.http.post<Reserva>(`${this.apiUrl}/${reservaId}/atender`, payload);
  }
}
