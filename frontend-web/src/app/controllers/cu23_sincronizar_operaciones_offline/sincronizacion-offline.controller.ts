// ==============================================================================
// CU23 - SINCRONIZAR OPERACIONES OFFLINE -> CONTROLADOR REACTIVO (MVC - SIGNALS)
// Ubicación: frontend-web/src/app/controllers/cu23_sincronizar_operaciones_offline/sincronizacion-offline.controller.ts
// ==============================================================================

import { Injectable, signal, computed } from '@angular/core';
import { SincronizacionOfflineService } from '../../services/cu23_sincronizar_operaciones_offline/sincronizacion-offline.service';
import {
  SyncLogDTO,
  SyncKpisDTO,
  SyncLoteResponse
} from '../../models/cu23_sincronizar_operaciones_offline/sincronizacion-offline.model';

@Injectable({
  providedIn: 'root'
})
export class SincronizacionOfflineController {
  // Estado Reactivo Principal
  logs = signal<SyncLogDTO[]>([]);
  kpis = signal<SyncKpisDTO | null>(null);
  cargando = signal<boolean>(false);
  sincronizando = signal<boolean>(false);

  // Filtros y Preferencias
  filtroEstado = signal<string>('TODOS');
  filtroBusqueda = signal<string>('');
  estrategiaPreferida = signal<string>('PRIORIZAR_TIENDA_FISICA');

  // Estado Modal y Detalle
  logSeleccionado = signal<SyncLogDTO | null>(null);
  modalDetalleAbierto = signal<boolean>(false);
  modalResolucionAbierto = signal<boolean>(false);

  // Mensajes y Feedback
  ultimoResultado = signal<SyncLoteResponse | null>(null);
  mensajeToast = signal<{ tipo: 'success' | 'error' | 'info' | 'warning'; texto: string } | null>(null);

  // Cola Local Browser Cache
  colaLocalCount = signal<number>(0);

  // Logs Filtrados (Computed)
  logsFiltrados = computed(() => {
    let items = this.logs();
    const filtro = this.filtroEstado();
    const busqueda = this.filtroBusqueda().trim().toLowerCase();

    if (filtro !== 'TODOS') {
      items = items.filter(l => l.estado === filtro);
    }

    if (busqueda) {
      items = items.filter(l =>
        l.uuid_operacion.toLowerCase().includes(busqueda) ||
        (l.sucursal_nombre && l.sucursal_nombre.toLowerCase().includes(busqueda)) ||
        (l.usuario_nombre && l.usuario_nombre.toLowerCase().includes(busqueda)) ||
        l.tipo_operacion.toLowerCase().includes(busqueda) ||
        (l.estrategia_conflicto && l.estrategia_conflicto.toLowerCase().includes(busqueda))
      );
    }

    return items;
  });

  constructor(private service: SincronizacionOfflineService) {
    this.actualizarConteoColaLocal();
  }

  actualizarConteoColaLocal(): void {
    const cola = this.service.obtenerColaLocal();
    this.colaLocalCount.set(cola.length);
  }

  cargarTodo(): void {
    this.cargando.set(true);
    this.actualizarConteoColaLocal();

    // 1. Cargar KPIs
    this.service.obtenerKpis().subscribe({
      next: (k) => this.kpis.set(k),
      error: (err) => console.error('Error cargando KPIs CU23:', err)
    });

    // 2. Cargar Historial
    this.service.obtenerHistorial(100, this.filtroEstado()).subscribe({
      next: (data) => {
        this.logs.set(data);
        this.cargando.set(false);
      },
      error: (err) => {
        this.cargando.set(false);
        this.mostrarToast('error', 'No se pudo cargar el historial de sincronizaciones.');
        console.error('Error cargando historial CU23:', err);
      }
    });
  }

  sincronizarTodoAhora(): void {
    this.sincronizando.set(true);
    const estrategia = this.estrategiaPreferida();

    // 1. Enviar primero operaciones de la cola local si existen
    const colaLocal = this.service.obtenerColaLocal();
    if (colaLocal.length > 0) {
      const loteOps = colaLocal.map(c => ({
        uuid_operacion: c.uuid_operacion,
        tipo: 'COBRO_CONTINGENCIA',
        sucursal_id: c.sucursal_id || 1,
        payload: c,
        fecha_operacion: c.fecha_cobro
      }));

      this.service.enviarLote(1, loteOps, estrategia).subscribe({
        next: () => {
          this.service.limpiarColaLocal();
          this.actualizarConteoColaLocal();
          this.ejecutarSincronizacionServidor(estrategia);
        },
        error: () => {
          this.ejecutarSincronizacionServidor(estrategia);
        }
      });
    } else {
      this.ejecutarSincronizacionServidor(estrategia);
    }
  }

  private ejecutarSincronizacionServidor(estrategia: string): void {
    this.service.sincronizarPendientes(estrategia).subscribe({
      next: (res) => {
        this.sincronizando.set(false);
        this.ultimoResultado.set(res);

        if (res.procesadas === 0 && res.total === 0) {
          this.mostrarToast('info', 'Todo el inventario y cobros ya se encuentran sincronizados.');
        } else {
          this.mostrarToast(
            'success',
            `Sincronización completada: ${res.sincronizadas} sincronizadas, ${res.conflictos_resueltos} conflictos resueltos, ${res.errores} errores.`
          );
        }
        this.cargarTodo();
      },
      error: (err) => {
        this.sincronizando.set(false);
        this.mostrarToast('error', `Error durante la sincronización: ${err.message || 'Fallo de red'}`);
      }
    });
  }

  resolverConflictoManual(syncId: number, estrategia: string, notas?: string): void {
    this.cargando.set(true);
    this.service.resolverConflicto(syncId, estrategia, notas).subscribe({
      next: (res) => {
        this.cargando.set(false);
        this.modalResolucionAbierto.set(false);
        this.cerrarDetalle();
        this.mostrarToast('success', res.mensaje || 'Conflicto resuelto exitosamente.');
        this.cargarTodo();
      },
      error: (err) => {
        this.cargando.set(false);
        this.mostrarToast('error', `Error resolviendo conflicto: ${err.error?.detail || err.message}`);
      }
    });
  }

  abrirDetalle(log: SyncLogDTO): void {
    this.logSeleccionado.set(log);
    this.modalDetalleAbierto.set(true);
  }

  cerrarDetalle(): void {
    this.modalDetalleAbierto.set(false);
    this.logSeleccionado.set(null);
  }

  abrirResolucion(log: SyncLogDTO): void {
    this.logSeleccionado.set(log);
    this.modalResolucionAbierto.set(true);
  }

  cerrarResolucion(): void {
    this.modalResolucionAbierto.set(false);
  }

  setFiltroEstado(estado: string): void {
    this.filtroEstado.set(estado);
    this.cargarTodo();
  }

  setFiltroBusqueda(val: string): void {
    this.filtroBusqueda.set(val);
  }

  setEstrategiaPreferida(est: string): void {
    this.estrategiaPreferida.set(est);
  }

  mostrarToast(tipo: 'success' | 'error' | 'info' | 'warning', texto: string): void {
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
