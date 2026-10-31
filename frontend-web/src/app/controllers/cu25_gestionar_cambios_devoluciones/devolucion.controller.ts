// CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> CONTROLLER
import { Injectable, signal } from '@angular/core';
import { DevolucionService } from '../../services/cu25_gestionar_cambios_devoluciones/devolucion.service';
import { DevolucionDTO } from '../../models/cu25_gestionar_cambios_devoluciones/devolucion.model';

@Injectable({
  providedIn: 'root'
})
export class DevolucionController {
  devoluciones = signal<DevolucionDTO[]>([]);
  cargando = signal<boolean>(false);

  constructor(private service: DevolucionService) {}

  cargarDevoluciones(): void {
    this.cargando.set(true);
    this.service.listarDevoluciones().subscribe({
      next: (res) => {
        this.cargando.set(false);
        if (res.exito) this.devoluciones.set(res.devoluciones);
      },
      error: () => this.cargando.set(false)
    });
  }
}
