// ==============================================================================
// CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> CONTROLADOR (MVC)
// Ubicación: frontend-web/src/app/controllers/cu22_registrar_cobros_contado_offline/cobro-offline.controller.ts
// ==============================================================================

import { Injectable, signal, computed } from '@angular/core';
import { CobroOfflineService } from '../../services/cu22_registrar_cobros_contado_offline/cobro-offline.service';
import {
  CobroOfflineDTO,
  RegistroCobroOfflineRequest,
  CobroOfflineKPIsDTO
} from '../../models/cu22_registrar_cobros_contado_offline/cobro-offline.model';

@Injectable({
  providedIn: 'root'
})
export class CobroOfflineController {
  // Estado Reactivo con Signals
  cobros = signal<CobroOfflineDTO[]>([]);
  kpis = signal<CobroOfflineKPIsDTO | null>(null);

  cargando = signal<boolean>(false);
  guardando = signal<boolean>(false);
  sincronizando = signal<boolean>(false);
  error = signal<string | null>(null);
  mensajeExito = signal<string | null>(null);

  // Modo de Contingencia y Simulación
  modoOfflineForzado = signal<boolean>(false);
  estadoConexionReal = signal<boolean>(navigator.onLine);

  // Computed: Determina si el sistema opera en modo offline (por hardware o por simulador)
  enModoOffline = computed(() => {
    return this.modoOfflineForzado() || !this.estadoConexionReal();
  });

  // Filtros de UI
  filtroTexto = signal<string>('');
  filtroSoloPendientes = signal<boolean>(false);

  // Modales
  modalNuevoCobro = signal<boolean>(false);
  modalTicket = signal<boolean>(false);
  reciboSeleccionado = signal<CobroOfflineDTO | null>(null);

  // Computed: Cobros filtrados
  cobrosFiltrados = computed(() => {
    const texto = this.filtroTexto().toLowerCase().trim();
    const soloPend = this.filtroSoloPendientes();
    let lista = this.cobros();

    if (soloPend) {
      lista = lista.filter(c => !c.sincronizado);
    }

    if (!texto) return lista;

    return lista.filter(c =>
      c.nro_recibo_provisional.toLowerCase().includes(texto) ||
      (c.cliente_nombre && c.cliente_nombre.toLowerCase().includes(texto)) ||
      (c.cliente_nit && c.cliente_nit.includes(texto)) ||
      (c.sucursal_nombre && c.sucursal_nombre.toLowerCase().includes(texto))
    );
  });

  constructor(private service: CobroOfflineService) {
    // Escuchar cambios de conectividad reales de la ventana
    window.addEventListener('online', () => {
      this.estadoConexionReal.set(true);
      this.sincronizarLoteLocal();
    });
    window.addEventListener('offline', () => {
      this.estadoConexionReal.set(false);
    });
  }

  cargarTodo(): void {
    this.cargando.set(true);
    this.error.set(null);

    // Cargar KPIs
    this.service.obtenerKpis().subscribe({
      next: (res) => {
        if (res.exito) this.kpis.set(res.kpis);
      },
      error: () => {}
    });

    // Cargar registros remotos de backend
    this.service.listarCobros().subscribe({
      next: (res) => {
        this.cargando.set(false);
        const remotos = res.exito ? res.cobros : [];
        // Combinar con los registros pendientes que estén en LocalStorage
        const locales = this.service.obtenerDeLocalStorage();
        const mapaUuids = new Set(remotos.map(r => r.uuid_operacion));
        const localesNoSubidos = locales.filter(l => !mapaUuids.has(l.uuid_operacion));

        this.cobros.set([...localesNoSubidos, ...remotos]);
      },
      error: (err) => {
        this.cargando.set(false);
        // Si no hay conexión al backend, cargar de LocalStorage
        const locales = this.service.obtenerDeLocalStorage();
        this.cobros.set(locales);
        if (!this.enModoOffline()) {
          this.error.set('Modo fuera de línea: Visualizando cobros guardados en el almacenamiento local del equipo.');
        }
      }
    });
  }

  toggleSimuladorOffline(): void {
    const nuevo = !this.modoOfflineForzado();
    this.modoOfflineForzado.set(nuevo);
    if (nuevo) {
      this.mostrarExito('⚠️ Simulador de Contingencia ACTIVADO: Las operaciones se guardarán localmente en este terminal.');
    } else {
      this.mostrarExito('🟢 Conexión reestablecida: Iniciando sincronización de cobros offline acumulados...');
      this.sincronizarLoteLocal();
    }
  }

  abrirModalNuevoCobro(): void {
    this.modalNuevoCobro.set(true);
    this.error.set(null);
  }

  cerrarModalNuevoCobro(): void {
    this.modalNuevoCobro.set(false);
  }

  registrarCobro(payload: RegistroCobroOfflineRequest, onSuccess?: (cobro: CobroOfflineDTO) => void): void {
    this.guardando.set(true);
    this.error.set(null);

    // Si estamos en modo offline (real o forzado por simulador)
    if (this.enModoOffline()) {
      const cobroLocal = this.service.guardarEnLocalStorage(payload);
      this.guardando.set(false);
      this.mostrarExito(`Cobro offline registrado en contingencia local: Folio ${cobroLocal.nro_recibo_provisional}.`);
      this.cerrarModalNuevoCobro();
      this.cargarTodo();
      if (onSuccess) onSuccess(cobroLocal);
      return;
    }

    // Si hay conexión, intentar persistencia inmediata en Backend
    this.service.registrarCobro(payload).subscribe({
      next: (res) => {
        this.guardando.set(false);
        this.mostrarExito(`Cobro registrado con éxito: Recibo ${res.cobro_offline.nro_recibo_provisional}.`);
        this.cerrarModalNuevoCobro();
        this.cargarTodo();
        if (onSuccess) onSuccess(res.cobro_offline);
      },
      error: (err) => {
        // En caso de fallo inesperado de red, fallback a LocalStorage
        const cobroLocal = this.service.guardarEnLocalStorage(payload);
        this.guardando.set(false);
        this.mostrarExito(`Conexión inestable. Cobro guardado en contingencia local: ${cobroLocal.nro_recibo_provisional}.`);
        this.cerrarModalNuevoCobro();
        this.cargarTodo();
        if (onSuccess) onSuccess(cobroLocal);
      }
    });
  }

  sincronizarLoteLocal(): void {
    const pendientesLocales = this.service.obtenerDeLocalStorage();
    if (pendientesLocales.length === 0) return;

    this.sincronizando.set(true);
    const payload = pendientesLocales.map(p => ({
      sucursal_id: p.sucursal_id,
      monto: p.monto,
      moneda: p.moneda,
      nro_recibo_provisional: p.nro_recibo_provisional,
      uuid_operacion: p.uuid_operacion,
      cliente_nombre: p.cliente_nombre,
      cliente_nit: p.cliente_nit,
      efectivo_recibido: p.efectivo_recibido,
      cambio: p.cambio,
      observaciones: p.observaciones,
      items: p.items
    }));

    this.service.subirLote(payload).subscribe({
      next: (res) => {
        this.sincronizando.set(false);
        this.service.limpiarLocalStorage();
        this.mostrarExito(`Sincronización completada: ${res.procesados} cobros de contingencia subidos al servidor central.`);
        this.cargarTodo();
      },
      error: (err) => {
        this.sincronizando.set(false);
        console.warn('No se pudo completar la sincronización automática:', err);
      }
    });
  }

  verTicket(cobro: CobroOfflineDTO): void {
    this.reciboSeleccionado.set(cobro);
    this.modalTicket.set(true);
  }

  cerrarModalTicket(): void {
    this.modalTicket.set(false);
    this.reciboSeleccionado.set(null);
  }

  imprimirTicket(): void {
    window.print();
  }

  private mostrarExito(msg: string): void {
    this.mensajeExito.set(msg);
    setTimeout(() => {
      this.mensajeExito.set(null);
    }, 4500);
  }
}
