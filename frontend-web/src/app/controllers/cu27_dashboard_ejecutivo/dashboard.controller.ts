// ==============================================================================
// CU27 - DASHBOARD EJECUTIVO Y REPORTES -> CONTROLADOR (MVC - CONTROLLER)
// Ubicación: frontend-web/src/app/controllers/cu27_dashboard_ejecutivo/dashboard.controller.ts
// ==============================================================================

import { Injectable, signal, computed } from '@angular/core';
import { DashboardService } from '../../services/cu27_dashboard_ejecutivo/dashboard.service';
import {
  DashboardConsolidado,
  TipoPeriodo
} from '../../models/cu27_dashboard_ejecutivo/dashboard.model';

@Injectable({
  providedIn: 'root'
})
export class DashboardController {
  // Estado Reactivo con Signals
  readonly consolidado = signal<DashboardConsolidado | null>(null);
  readonly cargando = signal<boolean>(false);
  readonly filtroActivo = signal<TipoPeriodo>('TODO');
  readonly diasActivo = signal<number | undefined>(undefined);
  readonly error = signal<string | null>(null);

  // Computeds convenientes para la vista
  readonly kpis = computed(() => this.consolidado()?.kpis ?? null);
  readonly saas = computed(() => this.consolidado()?.saas_tenant ?? null);
  readonly ventasCanal = computed(() => this.consolidado()?.ventas_canal ?? []);
  readonly ventasSucursal = computed(() => this.consolidado()?.ventas_sucursal ?? []);
  readonly ventasMetodo = computed(() => this.consolidado()?.ventas_metodo ?? []);
  readonly topPrendas = computed(() => this.consolidado()?.top_prendas ?? []);

  constructor(private service: DashboardService) {}

  cargarDashboard(periodo: TipoPeriodo = 'TODO'): void {
    this.cargando.set(true);
    this.filtroActivo.set(periodo);
    this.error.set(null);

    let dias: number | undefined = undefined;
    switch (periodo) {
      case 'HOY':
        dias = 1;
        break;
      case '7D':
        dias = 7;
        break;
      case 'MES':
        dias = 30;
        break;
      case 'ANO':
        dias = 365;
        break;
      case 'TODO':
      default:
        dias = undefined;
        break;
    }

    this.diasActivo.set(dias);

    this.service.obtenerResumenConsolidado(dias).subscribe({
      next: (data) => {
        this.consolidado.set(data);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error('Error al cargar dashboard consolidado:', err);
        this.error.set('No se pudo sincronizar la analítica ejecutiva del tenant.');
        this.cargando.set(false);
      }
    });
  }

  exportarCSV(): void {
    this.service.descargarCSV(this.diasActivo());
  }

  imprimirReporte(): void {
    window.print();
  }
}
