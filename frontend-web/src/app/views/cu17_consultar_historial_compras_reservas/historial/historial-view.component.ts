import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatChipsModule } from '@angular/material/chips';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDividerModule } from '@angular/material/divider';
import { HistorialController } from '../../../controllers/cu17_consultar_historial_compras_reservas/historial.controller';

@Component({
  selector: 'app-historial-view',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatChipsModule,
    MatTabsModule,
    MatDividerModule
  ],
  templateUrl: './historial-view.component.html',
  styleUrls: ['./historial-view.component.css']
})
export class HistorialViewComponent implements OnInit {
  constructor(public controller: HistorialController) {}

  ngOnInit(): void {
    this.controller.cargarHistorial();
  }

  descargarComprobante(codigo: string): void {
    alert(`Descargando comprobante fiscal en PDF para el pedido ${codigo}...`);
  }
}
