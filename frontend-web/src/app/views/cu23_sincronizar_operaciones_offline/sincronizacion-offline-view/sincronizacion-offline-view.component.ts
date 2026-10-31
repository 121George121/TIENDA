import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SincronizacionOfflineController } from '../../../controllers/cu23_sincronizar_operaciones_offline/sincronizacion-offline.controller';

@Component({
  selector: 'app-sincronizacion-offline-view',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="p-6 bg-slate-900 text-slate-100 min-h-screen">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold">CU23: Sincronización Offline y Resolución de Conflictos</h1>
          <p class="text-slate-400 text-sm">Monitoreo de colas de envío, prevención de duplicados e idempotencia.</p>
        </div>
      </div>

      <div class="bg-slate-800 rounded-lg p-5 border border-slate-700">
        <h2 class="text-lg font-bold mb-4">Registro de Lotes Sincronizados</h2>
        <div *ngIf="ctrl.logs().length === 0" class="text-slate-400 text-sm py-4">
          No hay registros de conflictos ni lotes en cola. Todo el inventario se encuentra consistente.
        </div>
        <table *ngIf="ctrl.logs().length > 0" class="w-full text-left text-sm">
          <thead class="text-slate-400 border-b border-slate-700">
            <tr>
              <th class="p-2">Operación</th>
              <th class="p-2">UUID Idempotencia</th>
              <th class="p-2">Resolución Conflicto</th>
              <th class="p-2">Fecha</th>
              <th class="p-2">Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let l of ctrl.logs()" class="border-b border-slate-700/50">
              <td class="p-2 font-bold">{{ l.tipo_operacion }}</td>
              <td class="p-2 font-mono text-xs text-indigo-400">{{ l.uuid_operacion }}</td>
              <td class="p-2 text-xs text-slate-300">{{ l.estrategia_conflicto || 'LAST_WRITE_WINS' }}</td>
              <td class="p-2 text-xs text-slate-400">{{ l.fecha_recibido | date:'short' }}</td>
              <td class="p-2"><span class="bg-emerald-900/60 text-emerald-300 text-xs px-2 py-0.5 rounded">{{ l.estado }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `
})
export class SincronizacionOfflineViewComponent implements OnInit {
  constructor(public ctrl: SincronizacionOfflineController) {}

  ngOnInit(): void {
    this.ctrl.cargarHistorial();
  }
}
