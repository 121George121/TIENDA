// ==============================================================================
// CAPA VISTA / CONTROLADOR (MVC - VIEW & CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU10 - Gestionar Reservas de Prendas
// Ubicación: frontend-web/src/app/views/reservations/my-reservations.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';

import { ReservationService } from '../../services/reservation.service';
import { Reserva } from '../../models/reservation.model';

@Component({
  selector: 'app-my-reservations',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatTooltipModule
  ],
  templateUrl: './my-reservations.component.html',
  styleUrls: ['./my-reservations.component.css']
})
export class MyReservationsComponent implements OnInit {
  reservas: Reserva[] = [];
  reservasFiltradas: Reserva[] = [];
  filtroActual: 'TODAS' | 'PENDIENTE' | 'ENTREGADA' | 'CANCELADA' = 'TODAS';
  loading = true;
  cancelandoId: number | null = null;
  copiadoId: number | null = null;

  constructor(private reservationService: ReservationService) {}

  ngOnInit(): void {
    this.cargarReservas();
  }

  cargarReservas(): void {
    this.loading = true;
    this.reservationService.getMisReservas().subscribe({
      next: (res) => {
        this.reservas = res;
        this.aplicarFiltro(this.filtroActual);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar reservas:', err);
        this.loading = false;
      }
    });
  }

  aplicarFiltro(filtro: 'TODAS' | 'PENDIENTE' | 'ENTREGADA' | 'CANCELADA'): void {
    this.filtroActual = filtro;
    if (filtro === 'TODAS') {
      this.reservasFiltradas = [...this.reservas];
    } else {
      this.reservasFiltradas = this.reservas.filter(r => r.estado === filtro);
    }
  }

  copiarCodigo(codigo: string, id: number): void {
    navigator.clipboard.writeText(codigo).then(() => {
      this.copiadoId = id;
      setTimeout(() => this.copiadoId = null, 2500);
    });
  }

  cancelar(reserva: Reserva): void {
    if (reserva.estado !== 'PENDIENTE') {
      alert('Solo se pueden cancelar reservas que se encuentren en estado PENDIENTE.');
      return;
    }

    const motivo = prompt('¿Por qué deseas cancelar esta reserva? (Opcional):', 'Cambio de planes');
    if (motivo === null) return; // Canceló el prompt

    this.cancelandoId = reserva.id;
    this.reservationService.cancelarReserva(reserva.id, motivo || 'Cancelada por cliente').subscribe({
      next: (actualizada) => {
        this.cancelandoId = null;
        alert(`La reserva ${actualizada.codigo_reserva} ha sido cancelada. El inventario ha sido liberado.`);
        this.cargarReservas();
      },
      error: (err) => {
        this.cancelandoId = null;
        alert(err.error?.detail || 'Error al cancelar la reserva');
      }
    });
  }

  get pendientesCount(): number {
    return this.reservas.filter(r => r.estado === 'PENDIENTE').length;
  }

  get entregadasCount(): number {
    return this.reservas.filter(r => r.estado === 'ENTREGADA').length;
  }
}
