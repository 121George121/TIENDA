// CU21 - ADMINISTRAR PLANES DE SUSCRIPCIÓN Y TENANTS -> CONTROLLER
import { Injectable, signal } from '@angular/core';
import { SuscripcionTenantService } from '../../services/cu21_administrar_planes_suscripcion_tenants/suscripcion-tenant.service';
import { PlanSuscripcionDTO, TenantDTO, NuevoTenantRequest } from '../../models/cu21_administrar_planes_suscripcion_tenants/suscripcion-tenant.model';

@Injectable({
  providedIn: 'root'
})
export class SuscripcionTenantController {
  planes = signal<PlanSuscripcionDTO[]>([]);
  tenants = signal<TenantDTO[]>([]);
  cargando = signal<boolean>(false);
  error = signal<string | null>(null);

  constructor(private service: SuscripcionTenantService) {}

  cargarDatos(): void {
    this.cargando.set(true);
    this.service.listarPlanes().subscribe({
      next: (res) => {
        if (res.exito) this.planes.set(res.planes);
      }
    });

    this.service.listarTenants().subscribe({
      next: (res) => {
        this.cargando.set(false);
        if (res.exito) this.tenants.set(res.tenants);
      },
      error: (err) => {
        this.cargando.set(false);
        this.error.set('Error al cargar tenants');
      }
    });
  }

  crearTenant(payload: NuevoTenantRequest, onComplete: () => void): void {
    this.cargando.set(true);
    this.service.registrarTenant(payload).subscribe({
      next: (res) => {
        this.cargando.set(false);
        this.cargarDatos();
        onComplete();
      },
      error: (err) => {
        this.cargando.set(false);
        this.error.set('No se pudo crear el tenant');
      }
    });
  }
}
