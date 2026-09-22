// ==============================================================================
// CU17 - CONSULTAR HISTORIAL DE COMPRAS Y RESERVAS -> CAPA CONTROLADOR (MVC)
// Ubicación: frontend-web/src/app/controllers/cu17_consultar_historial_compras_reservas/historial.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, catchError, finalize, of, tap } from 'rxjs';
import { HistorialService } from '../../services/cu17_consultar_historial_compras_reservas/historial.service';
import { CompraHistorial, ReservaHistorial, ResumenCliente } from '../../models/cu17_consultar_historial_compras_reservas/historial.model';

@Injectable({
  providedIn: 'root'
})
export class HistorialController {
  private comprasSubject = new BehaviorSubject<CompraHistorial[]>([]);
  public compras$: Observable<CompraHistorial[]> = this.comprasSubject.asObservable();

  private reservasSubject = new BehaviorSubject<ReservaHistorial[]>([]);
  public reservas$: Observable<ReservaHistorial[]> = this.reservasSubject.asObservable();

  private resumenSubject = new BehaviorSubject<ResumenCliente | null>(null);
  public resumen$: Observable<ResumenCliente | null> = this.resumenSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private service: HistorialService) {}

  public cargarHistorial(): void {
    this.loadingSubject.next(true);

    this.service.obtenerResumen().pipe(
      tap((resumen) => this.resumenSubject.next(resumen)),
      catchError((err) => {
        console.warn('[HistorialController] No se pudo cargar resumen:', err);
        return of(null);
      })
    ).subscribe();

    this.service.obtenerCompras().pipe(
      tap((compras) => this.comprasSubject.next(compras as CompraHistorial[])),
      catchError((err) => {
        console.warn('[HistorialController] Error al obtener compras:', err);
        return of([]);
      }),
      finalize(() => this.loadingSubject.next(false))
    ).subscribe();

    this.service.obtenerReservas().pipe(
      tap((reservas) => this.reservasSubject.next(reservas as ReservaHistorial[])),
      catchError((err) => {
        console.warn('[HistorialController] Error al obtener reservas:', err);
        return of([]);
      })
    ).subscribe();
  }
}
