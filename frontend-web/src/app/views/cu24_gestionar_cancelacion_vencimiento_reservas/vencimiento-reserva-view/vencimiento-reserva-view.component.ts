import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VencimientoReservaController } from '../../../controllers/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.controller';

@Component({
  selector: 'app-vencimiento-reserva-view',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="p-6 bg-slate-900 text-slate-100 min-h-screen">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold">CU24: Cancelación y Vencimiento Automático de Reservas</h1>
          <p class="text-slate-400 text-sm">Auditoría del plazo de recogida de 48 horas y reintegración de prendas al stock.</p>
        </div>
        <button
          (click)="ctrl.ejecutarPurga()"
          [disabled]="ctrl.cargando()"
          class="bg-rose-600 hover:bg-rose-500 font-bold px-4 py-2 rounded text-sm transition"
        >
          <span *ngIf="!ctrl.cargando()">Ejecutar Auditoría 48h ⚡</span>
          <span *ngIf="ctrl.cargando()">Purgando vencidas...</span>
        </button>
      </div>

      <div *ngIf="ctrl.ultimoResultado()" class="bg-slate-800 rounded-lg p-5 border border-rose-500/30">
        <h2 class="text-lg font-bold text-white mb-2">Resultado de la Auditoría</h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-slate-900 p-4 rounded border border-slate-700">
            <span class="text-xs text-slate-400">Reservas Vencidas Canceladas</span>
            <div class="text-2xl font-black text-rose-400">{{ ctrl.ultimoResultado()?.reservas_vencidas_canceladas }}</div>
          </div>
          <div class="bg-slate-900 p-4 rounded border border-slate-700">
            <span class="text-xs text-slate-400">Prendas Reintegradas a Stock</span>
            <div class="text-2xl font-black text-emerald-400">{{ ctrl.ultimoResultado()?.prendas_liberadas_al_stock }}</div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class VencimientoReservaViewComponent {
  constructor(public ctrl: VencimientoReservaController) {}
}
