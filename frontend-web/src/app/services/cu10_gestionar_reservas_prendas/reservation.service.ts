// ==============================================================================
// CAPA SERVICIO (MVC - SERVICE EN FRONTEND ANGULAR)
// Módulo: CU10 - Gestionar Reservas de Prendas
// Ubicación: frontend-web/src/app/services/cu10_gestionar_reservas_prendas/reservation.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { Reserva, CrearReservaDTO, CancelarReservaDTO } from '../../models/cu10_gestionar_reservas_prendas/reservation.model';
import { CartService } from '../cu9_gestionar_carrito_compras/cart.service';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  private apiUrl = `${environment.apiUrl}/reservas`;

  constructor(
    private http: HttpClient,
    private cartService: CartService
  ) {}

  /** CU10: Convierte el carrito en una reserva en sucursal física */
  crearReserva(datos: CrearReservaDTO): Observable<Reserva> {
    return this.http.post<Reserva>(this.apiUrl, datos).pipe(
      // Actualizar el estado del carrito tras ser convertido
      tap(() => this.cartService.cargarCarrito().subscribe())
    );
  }

  /** CU10: Consulta el listado de reservas del cliente actual */
  getMisReservas(): Observable<Reserva[]> {
    return this.http.get<Reserva[]>(`${this.apiUrl}/mis-reservas`);
  }

  /** CU10: Consulta una reserva específica por ID o código único */
  getReserva(idOCodigo: string | number): Observable<Reserva> {
    return this.http.get<Reserva>(`${this.apiUrl}/${idOCodigo}`);
  }

  /** CU10: Cancela una reserva pendiente y libera el stock reservado */
  cancelarReserva(reservaId: number, motivo?: string): Observable<Reserva> {
    const payload: CancelarReservaDTO = { motivo };
    return this.http.patch<Reserva>(`${this.apiUrl}/${reservaId}/cancelar`, payload);
  }

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
    const payload = {
      accion: accion,
      observaciones: observaciones
    };
    return this.http.post<Reserva>(`${this.apiUrl}/${reservaId}/atender`, payload);
  }
}
