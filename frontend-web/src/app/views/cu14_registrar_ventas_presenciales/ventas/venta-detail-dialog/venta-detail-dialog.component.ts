import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatDividerModule } from '@angular/material/divider';
import { VentaDetallada } from '../../../../models/cu14_registrar_ventas_presenciales/venta.model';
import { VentaService } from '../../../../services/cu14_registrar_ventas_presenciales/venta.service';

export interface VentaDetailDialogData {
  ventaId: number;
}

@Component({
  selector: 'app-venta-detail-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatDividerModule
  ],
  templateUrl: './venta-detail-dialog.component.html',
  styleUrls: ['./venta-detail-dialog.component.css']
})
export class VentaDetailDialogComponent implements OnInit {
  venta?: VentaDetallada;
  loading = true;
  displayedColumns: string[] = ['producto', 'variante', 'cantidad', 'precio', 'subtotal'];

  constructor(
    public dialogRef: MatDialogRef<VentaDetailDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: VentaDetailDialogData,
    private ventaService: VentaService
  ) {}

  ngOnInit(): void {
    this.cargarDetalle();
  }

  cargarDetalle(): void {
    this.loading = true;
    this.ventaService.getVentaById(this.data.ventaId).subscribe({
      next: (data) => {
        this.venta = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar detalle de venta:', err);
        this.loading = false;
      }
    });
  }

  imprimir(): void {
    window.print();
  }

  onClose(): void {
    this.dialogRef.close();
  }
}
