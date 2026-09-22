// ==============================================================================
// CU18 - GESTIONAR RECOMENDACIONES MEDIANTE IA -> CAPA CONTROLADOR (MVC)
// Ubicación: frontend-web/src/app/controllers/cu18_gestionar_recomendaciones_ia/recomendacion.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, catchError, finalize, of, tap } from 'rxjs';
import { RecomendacionService } from '../../services/cu18_gestionar_recomendaciones_ia/recomendacion.service';
import { RecomendacionOutfit, TendenciaModa } from '../../models/cu18_gestionar_recomendaciones_ia/recomendacion.model';

@Injectable({
  providedIn: 'root'
})
export class RecomendacionController {
  private outfitsSubject = new BehaviorSubject<RecomendacionOutfit[]>([]);
  public outfits$: Observable<RecomendacionOutfit[]> = this.outfitsSubject.asObservable();

  private tendenciasSubject = new BehaviorSubject<TendenciaModa[]>([]);
  public tendencias$: Observable<TendenciaModa[]> = this.tendenciasSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private service: RecomendacionService) {}

  public cargarTendencias(): void {
    this.loadingSubject.next(true);

    this.service.obtenerTendencias(4).pipe(
      tap((tendencias) => this.tendenciasSubject.next(tendencias)),
      catchError((err) => {
        console.warn('[RecomendacionController] Error cargando tendencias:', err);
        return of([]);
      }),
      finalize(() => this.loadingSubject.next(false))
    ).subscribe();
  }

  public generarRecomendacionOutfit(productoId?: number): void {
    this.loadingSubject.next(true);

    this.service.obtenerRecomendacionOutfit(productoId, [], 3).pipe(
      tap((outfits) => this.outfitsSubject.next(outfits)),
      catchError((err) => {
        console.warn('[RecomendacionController] Error generando outfit con IA:', err);
        return of([]);
      }),
      finalize(() => this.loadingSubject.next(false))
    ).subscribe();
  }
}
