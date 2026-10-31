// CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> CONTROLLER
import { Injectable, signal } from '@angular/core';
import { VencimientoReservaService } from '../../services/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.service';
import { PurgaVencimientoResultado } from '../../models/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.model';

@Injectable({
  providedIn: 'root'
})
export class VencimientoReservaController {
  cargando = signal<boolean>(false);
  ultimoResultado = signal<PurgaVencimientoResultado | null>(null);

  constructor(private service: VencimientoReservaService) {}

  ejecutarPurga(): void {
    this.cargando.set(true);
    this.service.cancelarVencidas().subscribe({
      next: (res) => {
        this.cargando.set(false);
        if (res.exito) this.ultimoResultado.set(res.resultado);
      },
      error: () => this.cargando.set(false)
    });
  }
}
