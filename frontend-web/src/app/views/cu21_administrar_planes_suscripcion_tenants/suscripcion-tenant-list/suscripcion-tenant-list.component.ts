// ==============================================================================
// CU21 - ADMINISTRAR PLANES DE SUSCRIPCIÓN Y TENANTS -> COMPONENTE VISTA
// Ubicación: frontend-web/src/app/views/cu21_administrar_planes_suscripcion_tenants/suscripcion-tenant-list/suscripcion-tenant-list.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import { SuscripcionTenantController } from '../../../controllers/cu21_administrar_planes_suscripcion_tenants/suscripcion-tenant.controller';
import {
  NuevoTenantRequest,
  PlanSuscripcionCreateDTO,
  TenantDTO
} from '../../../models/cu21_administrar_planes_suscripcion_tenants/suscripcion-tenant.model';

@Component({
  selector: 'app-suscripcion-tenant-list',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIconModule],
  templateUrl: './suscripcion-tenant-list.component.html',
  styleUrls: ['./suscripcion-tenant-list.component.css']
})
export class SuscripcionTenantListComponent implements OnInit {

  // Formulario Nuevo Tenant
  nuevoTenantForm: NuevoTenantRequest = {
    nombre: '',
    slug: '',
    nit_ruc: '',
    email_contacto: '',
    telefono_contacto: '',
    direccion_fiscal: '',
    plan_id: 1,
    meses_suscripcion: 12
  };

  // Formulario Cambio de Plan
  cambioPlanNuevoId: number = 1;
  cambioPlanMotivo: string = '';

  // Formulario Renovación
  renovacionMeses: number = 12;
  renovacionMetodo: string = 'TRANSFERENCIA_BANCARIA';

  // Formulario Plan
  planForm: PlanSuscripcionCreateDTO = {
    nombre: '',
    descripcion: '',
    precio_mensual: 150.00,
    limite_sucursales: 2,
    limite_usuarios: 5,
    limite_productos: 300,
    habilitar_vestidor_ia: false,
    activo: true
  };

  constructor(public ctrl: SuscripcionTenantController) {}

  ngOnInit(): void {
    this.ctrl.cargarDatos();
  }

  actualizarFiltro(event: Event): void {
    const valor = (event.target as HTMLInputElement).value;
    this.ctrl.filtroTexto.set(valor);
  }

  autoGenerarSlug(): void {
    if (!this.nuevoTenantForm.nombre) return;
    this.nuevoTenantForm.slug = this.nuevoTenantForm.nombre
      .toLowerCase()
      .trim()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]/g, '-')
      .replace(/-+/g, '-');
  }

  guardarNuevoTenant(): void {
    this.ctrl.crearTenant(this.nuevoTenantForm, () => {
      // Reset formulario
      this.nuevoTenantForm = {
        nombre: '',
        slug: '',
        nit_ruc: '',
        email_contacto: '',
        telefono_contacto: '',
        direccion_fiscal: '',
        plan_id: this.ctrl.planes()[0]?.id || 1,
        meses_suscripcion: 12
      };
    });
  }

  confirmarCambioPlan(): void {
    this.ctrl.ejecutarCambioPlan(this.cambioPlanNuevoId, this.cambioPlanMotivo);
  }

  confirmarRenovacion(): void {
    this.ctrl.ejecutarRenovacion(this.renovacionMeses, this.renovacionMetodo);
  }

  confirmarGuardarPlan(): void {
    const planSel = this.ctrl.planSeleccionado();
    this.ctrl.guardarPlan(this.planForm, planSel?.id);
  }
}
