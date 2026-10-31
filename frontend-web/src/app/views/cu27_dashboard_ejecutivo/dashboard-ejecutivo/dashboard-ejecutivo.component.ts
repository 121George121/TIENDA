// ==============================================================================
// CU27 - DASHBOARD EJECUTIVO Y REPORTES -> VISTA (ANGULAR 18 STANDALONE)
// Ubicación: frontend-web/src/app/views/cu27_dashboard_ejecutivo/dashboard-ejecutivo/dashboard-ejecutivo.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatProgressBarModule } from '@angular/material/progress-bar';

import { DashboardController } from '../../../controllers/cu27_dashboard_ejecutivo/dashboard.controller';
import { TipoPeriodo } from '../../../models/cu27_dashboard_ejecutivo/dashboard.model';

@Component({
  selector: 'app-cu27-dashboard-ejecutivo',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatTooltipModule,
    MatProgressBarModule
  ],
  templateUrl: './dashboard-ejecutivo.component.html',
  styleUrls: ['./dashboard-ejecutivo.component.css']
})
export class DashboardEjecutivoComponent implements OnInit {

  constructor(public controller: DashboardController) {}

  ngOnInit(): void {
    this.controller.cargarDashboard('TODO');
  }

  // Proxies para signals del controlador
  get consolidado() { return this.controller.consolidado; }
  get kpis() { return this.controller.kpis; }
  get saas() { return this.controller.saas; }
  get ventasCanal() { return this.controller.ventasCanal; }
  get ventasSucursal() { return this.controller.ventasSucursal; }
  get ventasMetodo() { return this.controller.ventasMetodo; }
  get topPrendas() { return this.controller.topPrendas; }
  get cargando() { return this.controller.cargando; }
  get filtroActivo() { return this.controller.filtroActivo; }
  get error() { return this.controller.error; }

  cambiarPeriodo(periodo: TipoPeriodo): void {
    this.controller.cargarDashboard(periodo);
  }

  recargar(): void {
    this.controller.cargarDashboard(this.controller.filtroActivo());
  }

  exportarCSV(): void {
    this.controller.exportarCSV();
  }

  imprimirReporte(): void {
    this.controller.imprimirReporte();
  }

  calcularPorcentaje(actual: number, maximo: number): number {
    if (!maximo || maximo <= 0) return 0;
    return Math.min(100, Math.round((actual / maximo) * 100));
  }
}
