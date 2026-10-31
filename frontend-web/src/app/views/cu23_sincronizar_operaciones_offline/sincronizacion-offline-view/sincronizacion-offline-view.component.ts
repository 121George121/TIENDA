// ==============================================================================
// CU23 - SINCRONIZAR OPERACIONES OFFLINE -> COMPONENTE VISTA (MVC - VIEW)
// Ubicación: frontend-web/src/app/views/cu23_sincronizar_operaciones_offline/sincronizacion-offline-view/sincronizacion-offline-view.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';

import { SincronizacionOfflineController } from '../../../controllers/cu23_sincronizar_operaciones_offline/sincronizacion-offline.controller';

@Component({
  selector: 'app-sincronizacion-offline-view',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatDividerModule
  ],
  templateUrl: './sincronizacion-offline-view.component.html',
  styleUrls: ['./sincronizacion-offline-view.component.css']
})
export class SincronizacionOfflineViewComponent implements OnInit {
  constructor(public ctrl: SincronizacionOfflineController) {}

  ngOnInit(): void {
    this.ctrl.cargarTodo();
  }
}
