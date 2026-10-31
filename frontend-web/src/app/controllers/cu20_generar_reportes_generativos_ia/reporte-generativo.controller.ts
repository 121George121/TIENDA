// ==============================================================================
// CU20 - GENERAR REPORTES GENERATIVOS CON IA -> CONTROLADOR ANGULAR (MVC - CONTROLLER)
// Ubicación: frontend-web/src/app/controllers/cu20_generar_reportes_generativos_ia/reporte-generativo.controller.ts
// ==============================================================================

import { Injectable, signal } from '@angular/core';
import { ReporteGenerativoService } from '../../services/cu20_generar_reportes_generativos_ia/reporte-generativo.service';
import {
  ReporteGenerativoData,
  ConsultaSugerida,
  HistorialReporteItem
} from '../../models/cu20_generar_reportes_generativos_ia/reporte-generativo.model';

@Injectable({
  providedIn: 'root'
})
export class ReporteGenerativoController {
  // Signals para reactividad Senior
  cargando = signal<boolean>(false);
  errorMensaje = signal<string | null>(null);
  reporteActual = signal<ReporteGenerativoData | null>(null);
  historial = signal<HistorialReporteItem[]>([]);
  sugerencias = signal<ConsultaSugerida[]>([]);
  filtroActual = signal<string>('General');

  constructor(private service: ReporteGenerativoService) {}

  cargarSugerenciasEHistorial(): void {
    this.service.obtenerConsultasSugeridas().subscribe({
      next: (res) => {
        if (res.exito && res.sugerencias) {
          this.sugerencias.set(res.sugerencias);
        }
      },
      error: (err) => console.warn('[CU20] Error al cargar sugerencias:', err)
    });

    this.cargarHistorial();
  }

  cargarHistorial(): void {
    this.service.obtenerHistorial().subscribe({
      next: (res) => {
        if (res.exito && res.historial) {
          this.historial.set(res.historial);
        }
      },
      error: (err) => console.warn('[CU20] Error al cargar historial:', err)
    });
  }

  ejecutarConsulta(promptTexto: string): void {
    if (!promptTexto || promptTexto.trim().length < 3) {
      this.errorMensaje.set('Ingresa una consulta de al menos 3 caracteres.');
      return;
    }

    this.cargando.set(true);
    this.errorMensaje.set(null);

    this.service.consultarReporteIA({
      prompt: promptTexto.trim(),
      filtros: this.filtroActual()
    }).subscribe({
      next: (res) => {
        this.cargando.set(false);
        if (res.exito && res.datos) {
          this.reporteActual.set(res.datos);
          this.cargarHistorial();
        }
      },
      error: (err) => {
        this.cargando.set(false);
        this.errorMensaje.set(err.error?.detail || 'Error al comunicarse con el motor de Inteligencia Artificial.');
      }
    });
  }

  seleccionarDeHistorial(reporteId: number): void {
    this.cargando.set(true);
    this.service.obtenerDetalleReporte(reporteId).subscribe({
      next: (res) => {
        this.cargando.set(false);
        if (res.exito && res.datos) {
          this.reporteActual.set(res.datos);
        }
      },
      error: (err) => {
        this.cargando.set(false);
        this.errorMensaje.set('No se pudo cargar el reporte del historial.');
      }
    });
  }

  alternarFavorito(): void {
    const rep = this.reporteActual();
    if (!rep || !rep.id) return;

    this.service.alternarFavorito(rep.id).subscribe({
      next: (res) => {
        if (res.exito) {
          this.reporteActual.set({
            ...rep,
            es_favorito: res.resultado.es_favorito
          });
          this.cargarHistorial();
        }
      }
    });
  }

  exportarCSV(): void {
    const rep = this.reporteActual();
    if (!rep || !rep.tabla_filas || rep.tabla_filas.length === 0) return;

    let csvContent = 'data:text/csv;charset=utf-8,\uFEFF';
    csvContent += rep.tabla_columnas.join(',') + '\r\n';

    rep.tabla_filas.forEach(row => {
      const escapedRow = row.map(cell => `"${(cell || '').replace(/"/g, '""')}"`);
      csvContent += escapedRow.join(',') + '\r\n';
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `reporte_ia_${rep.id || 'export'}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  imprimirPDF(): void {
    window.print();
  }
}
