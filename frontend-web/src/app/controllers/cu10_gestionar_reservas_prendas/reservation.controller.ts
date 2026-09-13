// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU10 - Gestionar Reservas de Prendas
// Ubicación: frontend-web/src/app/controllers/cu10_gestionar_reservas_prendas/reservation.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize, tap } from 'rxjs';
import {
  Reserva,
  CrearReservaDTO
} from '../../models/cu10_gestionar_reservas_prendas/reservation.model';
import { ReservationService } from '../../services/cu10_gestionar_reservas_prendas/reservation.service';

@Injectable({
  providedIn: 'root'
})
export class ReservationController {
  private misReservasSubject = new BehaviorSubject<Reserva[]>([]);
  public misReservas$: Observable<Reserva[]> = this.misReservasSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private reservationService: ReservationService) {}

  public get misReservas(): Reserva[] {
    return this.misReservasSubject.value;
  }

  cargarMisReservas(): void {
    this.loadingSubject.next(true);
    this.reservationService.getMisReservas()
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (reservas) => this.misReservasSubject.next(reservas),
        error: (err) => console.error('Error al cargar mis reservas:', err)
      });
  }

  crearReserva(datos: CrearReservaDTO): Observable<Reserva> {
    this.loadingSubject.next(true);
    return this.reservationService.crearReserva(datos).pipe(
      tap((nueva) => {
        const current = this.misReservasSubject.value;
        this.misReservasSubject.next([nueva, ...current]);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  cancelarReserva(reservaId: number, motivo?: string): Observable<Reserva> {
    this.loadingSubject.next(true);
    return this.reservationService.cancelarReserva(reservaId, motivo).pipe(
      tap((actualizada) => {
        const current = this.misReservasSubject.value;
        const index = current.findIndex(r => r.id === reservaId);
        if (index !== -1) {
          const updated = [...current];
          updated[index] = actualizada;
          this.misReservasSubject.next(updated);
        }
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  obtenerReserva(idOCodigo: string | number): Observable<Reserva> {
    return this.reservationService.getReserva(idOCodigo);
  }
}
