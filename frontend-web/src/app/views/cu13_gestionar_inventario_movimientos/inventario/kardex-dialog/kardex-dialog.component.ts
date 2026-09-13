import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatChipsModule } from '@angular/material/chips';
import { InventarioItem, MovimientoInventarioItem } from '../../../../models/cu13_gestionar_inventario_movimientos/inventario.model';
import { InventarioService } from '../../../../services/cu13_gestionar_inventario_movimientos/inventario.service';

export interface KardexDialogData {
  item: InventarioItem;
}

@Component({
  selector: 'app-kardex-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatChipsModule
  ],
  templateUrl: './kardex-dialog.component.html',
  styleUrls: ['./kardex-dialog.component.css']
})
export class KardexDialogComponent implements OnInit {
  item: InventarioItem;
  movimientos: MovimientoInventarioItem[] = [];
  loading = true;
  displayedColumns: string[] = ['fecha', 'tipo', 'cantidad', 'stock_resultante', 'motivo', 'referencia'];

  constructor(
    public dialogRef: MatDialogRef<KardexDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: KardexDialogData,
    private inventarioService: InventarioService
  ) {
    this.item = data.item;
  }

  ngOnInit(): void {
    this.cargarKardex();
  }

  cargarKardex(): void {
    this.loading = true;
    this.inventarioService.getKardex(this.item.id).subscribe({
      next: (data) => {
        this.movimientos = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar kardex:', err);
        this.loading = false;
      }
    });
  }

  getBadgeClass(tipo: string): string {
    const t = tipo.toLowerCase();
    if (t.includes('entrada') || t.includes('ingreso') || t.includes('reabastecimiento')) return 'badge-entrada';
    if (t.includes('salida') || t.includes('merma') || t.includes('baja')) return 'badge-salida';
    if (t.includes('venta')) return 'badge-venta';
    return 'badge-ajuste';
  }

  onClose(): void {
    this.dialogRef.close();
  }
}
