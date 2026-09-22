import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { MatBadgeModule } from '@angular/material/badge';
import { NotificacionController } from '../../../controllers/cu19_gestionar_notificaciones/notificacion.controller';

@Component({
  selector: 'app-notificaciones-view',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatDividerModule,
    MatBadgeModule
  ],
  templateUrl: './notificaciones-view.component.html',
  styleUrls: ['./notificaciones-view.component.css']
})
export class NotificacionesViewComponent implements OnInit {
  filtroActual: string = 'todas';

  constructor(public controller: NotificacionController) {}

  ngOnInit(): void {
    this.controller.cargarNotificaciones();
  }

  cambiarFiltro(filtro: string): void {
    this.filtroActual = filtro;
  }
}
