import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatTabsModule } from '@angular/material/tabs';
import { MatProgressBarModule } from '@angular/material/progress-bar';

import { Cliente, HistorialCompra, HistorialReserva } from '../../../../models/customer.model';
import { CustomerService } from '../../../../services/customer.service';

@Component({
  selector: 'app-customer-detail-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatTabsModule,
    MatProgressBarModule
  ],
  templateUrl: './customer-detail-dialog.component.html',
  styleUrls: ['./customer-detail-dialog.component.css']
})
export class CustomerDetailDialogComponent implements OnInit {
  cliente: Cliente;
  compras: HistorialCompra[] = [];
  reservas: HistorialReserva[] = [];
  loading = true;

  constructor(
    public dialogRef: MatDialogRef<CustomerDetailDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { cliente: Cliente },
    private customerService: CustomerService
  ) {
    this.cliente = data.cliente;
  }

  ngOnInit(): void {
    this.customerService.getHistorialCompras(this.cliente.id).subscribe({
      next: (res) => {
        this.compras = res || [];
        this.checkLoading();
      },
      error: () => this.checkLoading()
    });

    this.customerService.getHistorialReservas(this.cliente.id).subscribe({
      next: (res) => {
        this.reservas = res || [];
        this.checkLoading();
      },
      error: () => this.checkLoading()
    });
  }

  checkLoading(): void {
    this.loading = false;
  }

  onClose(): void {
    this.dialogRef.close();
  }
}
