// CU27 - DASHBOARD EJECUTIVO Y REPORTES -> CONTROLLER
import { Injectable, signal } from '@angular/core';
import { DashboardService } from '../../services/cu27_dashboard_ejecutivo/dashboard.service';

@Injectable({
  providedIn: 'root'
})
export class DashboardController {
  kpis = signal<any>(null);
  cargando = signal<boolean>(false);

  constructor(private service: DashboardService) {}

  cargarKPIs(): void {
    this.cargando.set(true);
    this.service.obtenerKPIs().subscribe({
      next: (data) => {
        this.cargando.set(false);
        this.kpis.set(data);
      },
      error: () => this.cargando.set(false)
    });
  }
}
