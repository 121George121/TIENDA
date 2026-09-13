// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU11 - Atender Reservas en Sucursal
// Ubicación: frontend-web/src/app/controllers/cu11_atender_reservas_sucursal/reservation-admin.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize, tap } from 'rxjs';
import { Reserva } from '../../models/cu10_gestionar_reservas_prendas/reservation.model';
import { ReservationAdminService } from '../../services/cu11_atender_reservas_sucursal/reservation-admin.service';

@Injectable({
  providedIn: 'root'
})
export class ReservationAdminController {
  private reservasSubject = new BehaviorSubject<Reserva[]>([]);
  public reservas$: Observable<Reserva[]> = this.reservasSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private adminService: ReservationAdminService) {}

  public get reservas(): Reserva[] {
    return this.reservasSubject.value;
  }

  cargarReservas(sucursalId?: number | null, estado?: string | null): void {
    this.loadingSubject.next(true);
    this.adminService.getReservasAdmin(sucursalId, estado)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (reservas) => this.reservasSubject.next(reservas),
        error: (err) => console.error('Error al cargar reservas admin:', err)
      });
  }

  buscarPorCodigo(codigo: string): Observable<Reserva> {
    return this.adminService.buscarPorCodigo(codigo);
  }

  atenderReserva(reservaId: number, accion: 'ENTREGAR' | 'CANCELAR', observaciones?: string): Observable<Reserva> {
    this.loadingSubject.next(true);
    return this.adminService.atenderReserva(reservaId, accion, observaciones).pipe(
      tap((actualizada) => {
        const current = this.reservasSubject.value;
        const index = current.findIndex(r => r.id === reservaId);
        if (index !== -1) {
          const updated = [...current];
          updated[index] = actualizada;
          this.reservasSubject.next(updated);
        }
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }
}
