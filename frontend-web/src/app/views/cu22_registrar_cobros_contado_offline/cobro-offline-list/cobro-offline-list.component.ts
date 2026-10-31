import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CobroOfflineController } from '../../../controllers/cu22_registrar_cobros_contado_offline/cobro-offline.controller';

@Component({
  selector: 'app-cobro-offline-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="p-6 bg-slate-900 text-slate-100 min-h-screen">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold">CU22: Registro de Cobros de Contado Offline</h1>
          <p class="text-slate-400 text-sm">Persistencia local para cobros en efectivo con recibo provisional.</p>
        </div>
      </div>

      <div class="bg-slate-800 rounded-lg p-5 border border-slate-700">
        <h2 class="text-lg font-bold mb-4">Cobros Offline Pendientes de Sincronización</h2>
        <div *ngIf="ctrl.pendientes().length === 0" class="text-slate-400 text-sm py-4">
          No hay cobros de contingencia pendientes de sincronizar.
        </div>
        <table *ngIf="ctrl.pendientes().length > 0" class="w-full text-left text-sm">
          <thead class="text-slate-400 border-b border-slate-700">
            <tr>
              <th class="p-2">Recibo</th>
              <th class="p-2">Cliente</th>
              <th class="p-2">Monto</th>
              <th class="p-2">Fecha</th>
              <th class="p-2">Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let c of ctrl.pendientes()" class="border-b border-slate-700/50">
              <td class="p-2 font-mono text-amber-400">{{ c.nro_recibo_provisional }}</td>
              <td class="p-2">{{ c.cliente_nombre || 'Cliente Ocasional' }}</td>
              <td class="p-2 font-bold">{{ c.monto }} Bs.</td>
              <td class="p-2 text-xs text-slate-400">{{ c.fecha_cobro | date:'short' }}</td>
              <td class="p-2"><span class="bg-amber-900/60 text-amber-300 text-xs px-2 py-0.5 rounded">PENDIENTE SYNC</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `
})
export class CobroOfflineListComponent implements OnInit {
  constructor(public ctrl: CobroOfflineController) {}

  ngOnInit(): void {
    this.ctrl.cargarPendientes();
  }
}
