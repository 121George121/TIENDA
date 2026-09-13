// ==============================================================================
// CAPA VISTA / CONTROLADOR (MVC - VIEW & CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU11 - Atender Reservas en Sucursal
// Ubicación: frontend-web/src/app/views/admin/reservas/admin-reservas.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';

import { ReservationService } from '../../../services/cu10_gestionar_reservas_prendas/reservation.service';
import { InventoryService } from '../../../services/cu8_consultar_catalogo_disponibilidad/inventory.service';
import { Reserva } from '../../../models/cu10_gestionar_reservas_prendas/reservation.model';
import { SucursalItem } from '../../../models/cu8_consultar_catalogo_disponibilidad/inventory.model';

@Component({
  selector: 'app-admin-reservas',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatTooltipModule
  ],
  templateUrl: './admin-reservas.component.html',
  styleUrls: ['./admin-reservas.component.css']
})
export class AdminReservasComponent implements OnInit {
  reservas: Reserva[] = [];
  sucursales: SucursalItem[] = [];

  // Filtros
  sucursalIdFiltro: number | null = null;
  estadoFiltro: string = 'TODAS';
  codigoBusqueda: string = '';

  // Estados de carga
  loading = true;
  buscando = false;
  procesandoAccion = false;

  // Modal de Atención
  reservaSeleccionada: Reserva | null = null;
  mostrarModalAtencion = false;
  notasAtencion = '';

  constructor(
    private reservationService: ReservationService,
    private inventoryService: InventoryService
  ) {}

  ngOnInit(): void {
    this.cargarSucursales();
    this.cargarReservas();
  }

  cargarSucursales(): void {
    this.inventoryService.getSucursales().subscribe({
      next: (data) => this.sucursales = data,
      error: (err) => console.error('Error al cargar sucursales:', err)
    });
  }

  cargarReservas(): void {
    this.loading = true;
    this.reservationService.getReservasAdmin(this.sucursalIdFiltro, this.estadoFiltro).subscribe({
      next: (data) => {
        this.reservas = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar reservas:', err);
        this.loading = false;
      }
    });
  }

  buscarPorCodigo(): void {
    const code = this.codigoBusqueda.trim().toUpperCase();
    if (!code) {
      this.cargarReservas();
      return;
    }

    this.buscando = true;
    this.reservationService.buscarPorCodigo(code).subscribe({
      next: (reserva) => {
        this.buscando = false;
        // Abrir directamente el modal de atención con la reserva encontrada
        this.abrirAtencion(reserva);
      },
      error: (err) => {
        this.buscando = false;
        alert(err.error?.detail || `No se encontró reserva con código "${code}"`);
      }
    });
  }

  abrirAtencion(reserva: Reserva): void {
    this.reservaSeleccionada = reserva;
    this.notasAtencion = '';
    this.mostrarModalAtencion = true;
  }

  cerrarModal(): void {
    if (this.procesandoAccion) return;
    this.mostrarModalAtencion = false;
    this.reservaSeleccionada = null;
  }

  procesarEntrega(accion: 'ENTREGAR' | 'CANCELAR'): void {
    if (!this.reservaSeleccionada) return;

    const accionTexto = accion === 'ENTREGAR' ? 'CONFIRMAR ENTREGA Y COBRO' : 'CANCELAR RESERVA';
    const confirmMsg = accion === 'ENTREGAR'
      ? `¿Confirmar entrega y cobro de Bs. ${this.reservaSeleccionada.total_estimado.toFixed(2)} para la reserva ${this.reservaSeleccionada.codigo_reserva}?\n\n(Se descontará el stock físico definitivamente).`
      : `¿Cancelar la reserva ${this.reservaSeleccionada.codigo_reserva}?\n\n(El stock reservado será liberado para venta).`;

    if (!confirm(confirmMsg)) return;

    this.procesandoAccion = true;
    this.reservationService.atenderReserva(
      this.reservaSeleccionada.id,
      accion,
      this.notasAtencion.trim() || undefined
    ).subscribe({
      next: (reservaActualizada) => {
        this.procesandoAccion = false;
        this.mostrarModalAtencion = false;
        this.reservaSeleccionada = null;

        const resultado = accion === 'ENTREGAR'
          ? `¡Reserva ${reservaActualizada.codigo_reserva} ENTREGADA con éxito! Stock físico descontado.`
          : `Reserva ${reservaActualizada.codigo_reserva} CANCELADA. Stock reservado liberado.`;
        alert(resultado);

        this.cargarReservas();
      },
      error: (err) => {
        this.procesandoAccion = false;
        alert(err.error?.detail || 'Error al procesar la reserva');
      }
    });
  }
}
