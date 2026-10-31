import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DevolucionController } from '../../../controllers/cu25_gestionar_cambios_devoluciones/devolucion.controller';

@Component({
  selector: 'app-devolucion-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="p-6 bg-slate-900 text-slate-100 min-h-screen">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold">CU25: Cambios y Devoluciones de Prendas</h1>
          <p class="text-slate-400 text-sm">Validación de plazos, cambios de talla/modelo y reingreso a inventario.</p>
        </div>
      </div>

      <div class="bg-slate-800 rounded-lg p-5 border border-slate-700">
        <h2 class="text-lg font-bold mb-4">Historial de Solicitudes</h2>
        <div *ngIf="ctrl.devoluciones().length === 0" class="text-slate-400 text-sm py-4">
          No hay solicitudes de devolución registradas.
        </div>
        <table *ngIf="ctrl.devoluciones().length > 0" class="w-full text-left text-sm">
          <thead class="text-slate-400 border-b border-slate-700">
            <tr>
              <th class="p-2">Código</th>
              <th class="p-2">Tipo</th>
              <th class="p-2">Motivo</th>
              <th class="p-2">Reembolso</th>
              <th class="p-2">Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let d of ctrl.devoluciones()" class="border-b border-slate-700/50">
              <td class="p-2 font-mono text-indigo-400 font-bold">{{ d.codigo_devolucion }}</td>
              <td class="p-2 font-semibold">{{ d.tipo_devolucion }}</td>
              <td class="p-2 text-slate-300">{{ d.motivo }}</td>
              <td class="p-2">{{ d.monto_reembolso }} Bs.</td>
              <td class="p-2"><span class="bg-emerald-900/60 text-emerald-300 px-2 py-0.5 rounded text-xs">{{ d.estado }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `
})
export class DevolucionListComponent implements OnInit {
  constructor(public ctrl: DevolucionController) {}

  ngOnInit(): void {
    this.ctrl.cargarDevoluciones();
  }
}
