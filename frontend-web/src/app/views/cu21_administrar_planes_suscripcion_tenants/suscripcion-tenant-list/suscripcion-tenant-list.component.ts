import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SuscripcionTenantController } from '../../../controllers/cu21_administrar_planes_suscripcion_tenants/suscripcion-tenant.controller';

@Component({
  selector: 'app-suscripcion-tenant-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="p-6 bg-slate-900 text-slate-100 min-h-screen">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold">CU21: Administración de Planes y Tenants</h1>
          <p class="text-slate-400 text-sm">Gestión de empresas SaaS, planes de suscripción y límites de sucursales.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div *ngFor="let plan of ctrl.planes()" class="bg-slate-800 p-5 rounded-lg border border-slate-700">
          <span class="text-xs bg-indigo-900 text-indigo-300 font-bold px-2 py-1 rounded">PLAN {{ plan.nombre }}</span>
          <div class="text-2xl font-extrabold text-white mt-3">{{ plan.precio_mensual }} Bs. <span class="text-xs font-normal text-slate-400">/mes</span></div>
          <p class="text-sm text-slate-400 mt-2">{{ plan.descripcion || 'Plan integral para boutiques multitienda' }}</p>
          <ul class="text-xs text-slate-300 mt-4 space-y-1">
            <li>✔ Hasta {{ plan.limite_sucursales }} sucursales físicas</li>
            <li>✔ Hasta {{ plan.limite_usuarios }} colaboradores</li>
            <li>✔ Catálogo y catálogo ilimitado</li>
          </ul>
        </div>
      </div>

      <div class="bg-slate-800 rounded-lg p-5 border border-slate-700">
        <h2 class="text-lg font-bold mb-4">Tenants / Empresas Activas</h2>
        <table class="w-full text-left text-sm">
          <thead class="text-slate-400 border-b border-slate-700">
            <tr>
              <th class="p-2">ID</th>
              <th class="p-2">Empresa</th>
              <th class="p-2">Slug Dominio</th>
              <th class="p-2">Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let t of ctrl.tenants()" class="border-b border-slate-700/50">
              <td class="p-2">{{ t.id }}</td>
              <td class="p-2 font-semibold text-white">{{ t.nombre }}</td>
              <td class="p-2 text-indigo-400">{{ t.slug }}</td>
              <td class="p-2"><span class="bg-emerald-900/60 text-emerald-300 px-2 py-0.5 rounded text-xs">ACTIVO</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `
})
export class SuscripcionTenantListComponent implements OnInit {
  constructor(public ctrl: SuscripcionTenantController) {}

  ngOnInit(): void {
    this.ctrl.cargarDatos();
  }
}
