// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU12 - Utilizar Vestidor Virtual mediante IA
// Ubicación: frontend-web/src/app/controllers/cu12_vestidor_virtual_ia/vestidor.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize, tap } from 'rxjs';
import { AnalisisFisonomiaResponse, TryOnResponse } from '../../models/cu12_vestidor_virtual_ia/vestidor.model';
import { VestidorService } from '../../services/cu12_vestidor_virtual_ia/vestidor.service';

@Injectable({
  providedIn: 'root'
})
export class VestidorController {
  private analisisSubject = new BehaviorSubject<AnalisisFisonomiaResponse | null>(null);
  public analisis$: Observable<AnalisisFisonomiaResponse | null> = this.analisisSubject.asObservable();

  private tryonSubject = new BehaviorSubject<TryOnResponse | null>(null);
  public tryon$: Observable<TryOnResponse | null> = this.tryonSubject.asObservable();

  private loadingAnalisisSubject = new BehaviorSubject<boolean>(false);
  public loadingAnalisis$: Observable<boolean> = this.loadingAnalisisSubject.asObservable();

  private loadingTryonSubject = new BehaviorSubject<boolean>(false);
  public loadingTryon$: Observable<boolean> = this.loadingTryonSubject.asObservable();

  constructor(private vestidorService: VestidorService) {}

  public get analisisActual(): AnalisisFisonomiaResponse | null {
    return this.analisisSubject.value;
  }

  public get tryonActual(): TryOnResponse | null {
    return this.tryonSubject.value;
  }

  analizarFisonomia(
    productoNombre: string,
    talla: string,
    color: string,
    imagen?: File
  ): Observable<AnalisisFisonomiaResponse> {
    this.loadingAnalisisSubject.next(true);
    return this.vestidorService.analizarFisonomia(productoNombre, talla, color, imagen).pipe(
      tap((res) => this.analisisSubject.next(res)),
      finalize(() => this.loadingAnalisisSubject.next(false))
    );
  }

  generarTryOn(
    prendaUrl: string,
    productoNombre: string,
    talla: string,
    color: string,
    imagenUsuario: File
  ): Observable<TryOnResponse> {
    this.loadingTryonSubject.next(true);
    return this.vestidorService.generarTryOn(prendaUrl, productoNombre, talla, color, imagenUsuario).pipe(
      tap((res) => this.tryonSubject.next(res)),
      finalize(() => this.loadingTryonSubject.next(false))
    );
  }

  limpiarEstado(): void {
    this.analisisSubject.next(null);
    this.tryonSubject.next(null);
  }
}
