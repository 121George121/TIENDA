// CU23 - SINCRONIZAR OPERACIONES OFFLINE -> CONTROLLER
import { Injectable, signal } from '@angular/core';
import { SincronizacionOfflineService } from '../../services/cu23_sincronizar_operaciones_offline/sincronizacion-offline.service';
import { SyncLogDTO } from '../../models/cu23_sincronizar_operaciones_offline/sincronizacion-offline.model';

@Injectable({
  providedIn: 'root'
})
export class SincronizacionOfflineController {
  logs = signal<SyncLogDTO[]>([]);
  cargando = signal<boolean>(false);
  estadoSync = signal<string>('En línea y sincronizado');

  constructor(private service: SincronizacionOfflineService) {}

  cargarHistorial(): void {
    this.cargando.set(true);
    this.service.obtenerHistorial().subscribe({
      next: (res) => {
        this.cargando.set(false);
        if (res.exito) this.logs.set(res.logs);
      },
      error: () => this.cargando.set(false)
    });
  }
}
