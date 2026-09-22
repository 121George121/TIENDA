import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
import { PagoController } from '../../../controllers/cu16_gestionar_pagos_comprobantes/pago.controller';
import { MetodoPago } from '../../../models/cu16_gestionar_pagos_comprobantes/pago.model';

@Component({
  selector: 'app-pagos-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatChipsModule,
    MatProgressBarModule,
    MatDialogModule,
    MatDividerModule
  ],
  templateUrl: './pagos-list.component.html',
  styleUrls: ['./pagos-list.component.css']
})
export class PagosListComponent implements OnInit {
  displayedColumns: string[] = ['id', 'icono', 'nombre', 'descripcion', 'estado', 'acciones'];

  constructor(public controller: PagoController) {}

  ngOnInit(): void {
    this.controller.cargarMetodosPago();
  }

  simularComprobante(metodo: MetodoPago): void {
    alert(`Comprobante digital simulado para: ${metodo.nombre}\nEstado: Procesador activo en pasarela.`);
  }
}
