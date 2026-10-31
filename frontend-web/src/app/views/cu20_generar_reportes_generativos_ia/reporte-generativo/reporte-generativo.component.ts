// ==============================================================================
// CU20 - GENERAR REPORTES GENERATIVOS CON IA -> VISTA COMPONENTE (MVC - VIEW)
// Ubicación: frontend-web/src/app/views/cu20_generar_reportes_generativos_ia/reporte-generativo/reporte-generativo.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReporteGenerativoController } from '../../../controllers/cu20_generar_reportes_generativos_ia/reporte-generativo.controller';

@Component({
  selector: 'app-reporte-generativo',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reporte-generativo.component.html',
  styleUrls: ['./reporte-generativo.component.css']
})
export class ReporteGenerativoComponent implements OnInit {
  promptInput: string = '';

  constructor(public ctrl: ReporteGenerativoController) {}

  ngOnInit(): void {
    this.ctrl.cargarSugerenciasEHistorial();
  }

  enviarConsulta(): void {
    if (this.promptInput.trim()) {
      this.ctrl.ejecutarConsulta(this.promptInput);
    }
  }

  aplicarSugerencia(prompt: string): void {
    this.promptInput = prompt;
    this.ctrl.ejecutarConsulta(prompt);
  }

  cambiarFiltro(filtro: string): void {
    this.ctrl.filtroActual.set(filtro);
  }
}
