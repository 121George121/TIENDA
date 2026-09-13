import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { VentaCompleta } from '../../../../models/cu14_registrar_ventas_presenciales/venta.model';

export interface ReceiptDialogData {
  venta: VentaCompleta;
  items: Array<{
    nombre: string;
    variante?: string;
    cantidad: number;
    precio: number;
    subtotal: number;
  }>;
  montoRecibido?: number;
  cambio?: number;
}

@Component({
  selector: 'app-receipt-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule
  ],
  templateUrl: './receipt-dialog.component.html',
  styleUrls: ['./receipt-dialog.component.css']
})
export class ReceiptDialogComponent {
  venta: VentaCompleta;
  items: ReceiptDialogData['items'];
  montoRecibido?: number;
  cambio?: number;

  constructor(
    public dialogRef: MatDialogRef<ReceiptDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ReceiptDialogData
  ) {
    this.venta = data.venta;
    this.items = data.items;
    this.montoRecibido = data.montoRecibido;
    this.cambio = data.cambio;
  }

  printReceipt(): void {
    window.print();
  }

  onClose(): void {
    this.dialogRef.close();
  }
}
