// ==============================================================================
// CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> COMPONENTE VISTA (MVC - VIEW)
// Ubicación: frontend-web/src/app/views/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva-view/vencimiento-reserva-view.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';

import { VencimientoReservaController } from '../../../controllers/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.controller';

@Component({
  selector: 'app-vencimiento-reserva-view',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatDividerModule
  ],
  templateUrl: './vencimiento-reserva-view.component.html',
  styleUrls: ['./vencimiento-reserva-view.component.css']
})
export class VencimientoReservaViewComponent implements OnInit {
  constructor(public ctrl: VencimientoReservaController) {}

  ngOnInit(): void {
    this.ctrl.cargarTodo();
  }
}
