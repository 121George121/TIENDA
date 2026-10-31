// ==============================================================================
// CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> CONTROLADOR REACTIVO (MVC - SIGNALS)
// Ubicación: frontend-web/src/app/controllers/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.controller.ts
// ==============================================================================

import { Injectable, signal, computed } from '@angular/core';
import { VencimientoReservaService } from '../../services/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.service';
import {
  ReservaExpiracionItem,
  VencimientoReservaKpisDTO,
  PurgaVencimientoResultado
} from '../../models/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.model';

@Injectable({
  providedIn: 'root'
})
export class VencimientoReservaController {
  // Estado Reactivo Principal
  reservas = signal<ReservaExpiracionItem[]>([]);
  kpis = signal<VencimientoReservaKpisDTO | null>(null);
  cargando = signal<boolean>(false);
  purgando = signal<boolean>(false);

  // Parámetros de Política y Filtros
  horasPolitica = signal<number>(48);
  filtroRiesgo = signal<string>('TODAS'); // TODAS, EN_RIESGO, EXPIRADAS, VIGENTES
  filtroBusqueda = signal<string>('');

  // Modales y Selección
  reservaSeleccionada = signal<ReservaExpiracionItem | null>(null);
  modalDetalleAbierto = signal<boolean>(false);
  modalCancelarAbierto = signal<boolean>(false);
  modalPurgaAbierto = signal<boolean>(false);
  motivoCancelacion = signal<string>('');

  // Resultados y Notificaciones
  ultimoResultadoPurga = signal<PurgaVencimientoResultado | null>(null);
  mensajeToast = signal<{ tipo: 'success' | 'error' | 'info'; texto: string } | null>(null);

  // Reservas Filtradas (Computed)
  reservasFiltradas = computed(() => {
    let items = this.reservas();
    const riesgo = this.filtroRiesgo();
    const query = this.filtroBusqueda().trim().toLowerCase();

    if (riesgo === 'EN_RIESGO') {
      items = items.filter(r => r.en_riesgo && !r.es_expirada);
    } else if (riesgo === 'EXPIRADAS') {
      items = items.filter(r => r.es_expirada);
    } else if (riesgo === 'VIGENTES') {
      items = items.filter(r => !r.en_riesgo && !r.es_expirada);
    }

    if (query) {
      items = items.filter(r =>
        r.codigoreserva.toLowerCase().includes(query) ||
        r.cliente_nombre.toLowerCase().includes(query) ||
        (r.cliente_email && r.cliente_email.toLowerCase().includes(query)) ||
        r.sucursal_nombre.toLowerCase().includes(query)
      );
    }

    return items;
  });

  constructor(private service: VencimientoReservaService) {}

  cargarTodo(): void {
    this.cargando.set(true);
    const horas = this.horasPolitica();

    // 1. Cargar KPIs
    this.service.obtenerKpis(horas).subscribe({
      next: (data) => this.kpis.set(data),
      error: (err) => console.error('Error cargando KPIs CU24:', err)
    });

    // 2. Cargar Reservas Activas
    this.service.listarReservasActivas(undefined, horas).subscribe({
      next: (list) => {
        this.reservas.set(list);
        this.cargando.set(false);
      },
      error: (err) => {
        this.cargando.set(false);
        this.mostrarToast('error', 'No se pudieron cargar las reservas activas.');
        console.error('Error cargando reservas activas CU24:', err);
      }
    });
  }

  ejecutarPurga(): void {
    this.purgando.set(true);
    const horas = this.horasPolitica();

    this.service.cancelarVencidas(horas).subscribe({
      next: (res) => {
        this.purgando.set(false);
        this.ultimoResultadoPurga.set(res);
        this.modalPurgaAbierto.set(true);

        if (res.reservas_vencidas_canceladas === 0) {
          this.mostrarToast('info', 'No se encontraron reservas vencidas pendientes de purga.');
        } else {
          this.mostrarToast(
            'success',
            `Auditoría 48h completada: ${res.reservas_vencidas_canceladas} reservas vencidas canceladas y ${res.prendas_liberadas_al_stock} prendas reintegradas a stock.`
          );
        }
        this.cargarTodo();
      },
      error: (err) => {
        this.purgando.set(false);
        this.mostrarToast('error', `Error ejecutando auditoría de reservas: ${err.message || 'Error de red'}`);
      }
    });
  }

  abrirModalCancelar(reserva: ReservaExpiracionItem): void {
    this.reservaSeleccionada.set(reserva);
    this.motivoCancelacion.set('');
    this.modalCancelarAbierto.set(true);
  }

  cerrarModalCancelar(): void {
    this.modalCancelarAbierto.set(false);
    this.reservaSeleccionada.set(null);
  }

  confirmarCancelacionManual(): void {
    const res = this.reservaSeleccionada();
    const motivo = this.motivoCancelacion().trim();

    if (!res) return;
    if (!motivo) {
      this.mostrarToast('error', 'Por favor especifique el motivo de la cancelación.');
      return;
    }

    this.cargando.set(true);
    this.service.cancelarReservaManual(res.id, motivo).subscribe({
      next: (data) => {
        this.cargando.set(false);
        this.cerrarModalCancelar();
        this.mostrarToast('success', data.mensaje || 'Reserva cancelada y stock liberado correctamente.');
        this.cargarTodo();
      },
      error: (err) => {
        this.cargando.set(false);
        this.mostrarToast('error', `Error cancelando reserva: ${err.error?.detail || err.message}`);
      }
    });
  }

  abrirDetalle(reserva: ReservaExpiracionItem): void {
    this.reservaSeleccionada.set(reserva);
    this.modalDetalleAbierto.set(true);
  }

  cerrarDetalle(): void {
    this.modalDetalleAbierto.set(false);
    this.reservaSeleccionada.set(null);
  }

  cerrarModalPurga(): void {
    this.modalPurgaAbierto.set(false);
  }

  setHorasPolitica(horas: number): void {
    this.horasPolitica.set(horas);
    this.cargarTodo();
  }

  setFiltroRiesgo(filtro: string): void {
    this.filtroRiesgo.set(filtro);
  }

  setBusqueda(val: string): void {
    this.filtroBusqueda.set(val);
  }

  mostrarToast(tipo: 'success' | 'error' | 'info', texto: string): void {
    this.mensajeToast.set({ tipo, texto });
    setTimeout(() => {
      if (this.mensajeToast()?.texto === texto) {
        this.mensajeToast.set(null);
      }
    }, 6000);
  }

  limpiarToast(): void {
    this.mensajeToast.set(null);
  }
}
