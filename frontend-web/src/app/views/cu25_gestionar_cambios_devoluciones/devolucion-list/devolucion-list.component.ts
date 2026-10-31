// ==============================================================================
// CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> COMPONENTE VISTA (MVC - VIEW)
// Ubicación: frontend-web/src/app/views/cu25_gestionar_cambios_devoluciones/devolucion-list/devolucion-list.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';

import { DevolucionController } from '../../../controllers/cu25_gestionar_cambios_devoluciones/devolucion.controller';

@Component({
  selector: 'app-devolucion-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatDividerModule
  ],
  templateUrl: './devolucion-list.component.html',
  styleUrls: ['./devolucion-list.component.css']
})
export class DevolucionListComponent implements OnInit {
  constructor(public ctrl: DevolucionController) {}

  ngOnInit(): void {
    this.ctrl.cargarTodo();
  }
}
