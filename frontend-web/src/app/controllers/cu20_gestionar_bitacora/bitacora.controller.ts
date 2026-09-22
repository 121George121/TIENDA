// ==============================================================================
// CU20 - GESTIONAR BITACORA Y AUDITORIA -> CAPA CONTROLADOR (FRONTEND MVC)
// Ubicacion: frontend-web/src/app/controllers/cu20_gestionar_bitacora/bitacora.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { BitacoraService } from '../../services/cu20_gestionar_bitacora/bitacora.service';
import { BitacoraEntry, BitacoraStats, BitacoraFilter } from '../../models/cu20_gestionar_bitacora/bitacora.model';

@Injectable({
  providedIn: 'root'
})
export class BitacoraController {
  private logsSubject = new BehaviorSubject<BitacoraEntry[]>([]);
  public logs$: Observable<BitacoraEntry[]> = this.logsSubject.asObservable();

  private totalSubject = new BehaviorSubject<number>(0);
  public total$: Observable<number> = this.totalSubject.asObservable();

  private statsSubject = new BehaviorSubject<BitacoraStats | null>(null);
  public stats$: Observable<BitacoraStats | null> = this.statsSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  private exportingSubject = new BehaviorSubject<boolean>(false);
  public exporting$: Observable<boolean> = this.exportingSubject.asObservable();

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private bitacoraService: BitacoraService) {}

  loadLogs(filter: BitacoraFilter = {}): void {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    this.bitacoraService.getLogs(filter).subscribe({
      next: (response) => {
        this.logsSubject.next(response.items);
        this.totalSubject.next(response.total);
        this.loadingSubject.next(false);
      },
      error: (err) => {
        console.error('Error al cargar la bitácora:', err);
        this.errorSubject.next(err?.error?.detail || 'No se pudo obtener el historial de bitácora.');
        this.loadingSubject.next(false);
      }
    });
  }

  loadStats(): void {
    this.bitacoraService.getStats().subscribe({
      next: (stats) => {
        this.statsSubject.next(stats);
      },
      error: (err) => {
        console.warn('Advertencia al cargar estadísticas de bitácora:', err);
      }
    });
  }

  exportCsv(filter: BitacoraFilter = {}): void {
    this.exportingSubject.next(true);

    this.bitacoraService.exportCsv(filter).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        const fechaStr = new Date().toISOString().slice(0, 10);
        a.href = url;
        a.download = `bitacora_auditoria_${fechaStr}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        this.exportingSubject.next(false);
      },
      error: (err) => {
        console.error('Error al exportar CSV:', err);
        this.errorSubject.next('Error al generar la descarga del archivo CSV.');
        this.exportingSubject.next(false);
      }
    });
  }
}
