// CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> CONTROLLER
import { Injectable, signal } from '@angular/core';
import { CobroOfflineService } from '../../services/cu22_registrar_cobros_contado_offline/cobro-offline.service';
import { CobroOfflineDTO, RegistroCobroOfflineRequest } from '../../models/cu22_registrar_cobros_contado_offline/cobro-offline.model';

@Injectable({
  providedIn: 'root'
})
export class CobroOfflineController {
  pendientes = signal<CobroOfflineDTO[]>([]);
  cargando = signal<boolean>(false);
  mensaje = signal<string | null>(null);

  constructor(private service: CobroOfflineService) {}

  cargarPendientes(): void {
    this.cargando.set(true);
    this.service.listarPendientes().subscribe({
      next: (res) => {
        this.cargando.set(false);
        if (res.exito) this.pendientes.set(res.pendientes);
      },
      error: () => this.cargando.set(false)
    });
  }

  registrarCobro(req: RegistroCobroOfflineRequest, onDone: () => void): void {
    this.cargando.set(true);
    this.service.registrarCobro(req).subscribe({
      next: (res) => {
        this.cargando.set(false);
        this.mensaje.set('Cobro offline registrado con folio provisional exitosamente.');
        this.cargarPendientes();
        onDone();
      },
      error: () => this.cargando.set(false)
    });
  }
}
