import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { InventarioItem } from '../../../../models/cu13_gestionar_inventario_movimientos/inventario.model';

export interface MovimientoDialogData {
  item: InventarioItem;
}

@Component({
  selector: 'app-movimiento-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSelectModule
  ],
  templateUrl: './movimiento-dialog.component.html',
  styleUrls: ['./movimiento-dialog.component.css']
})
export class MovimientoDialogComponent implements OnInit {
  form!: FormGroup;
  item: InventarioItem;

  tiposMovimiento = [
    { value: 'Entrada', label: 'Entrada (Reabastecimiento / Compra)', icon: 'arrow_downward', color: '#10b981' },
    { value: 'Salida', label: 'Salida (Consumo / Merma / Baja)', icon: 'arrow_upward', color: '#ef4444' },
    { value: 'Ajuste', label: 'Ajuste de Auditoría (Fijar Stock Exacto)', icon: 'sync_alt', color: '#f59e0b' }
  ];

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<MovimientoDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: MovimientoDialogData
  ) {
    this.item = data.item;
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      tipo_movimiento: ['Entrada', [Validators.required]],
      cantidad: [1, [Validators.required, Validators.min(1)]],
      motivo: ['', [Validators.required, Validators.minLength(3)]],
      referencia: ['']
    });
  }

  get stockProyectado(): number {
    const tipo = this.form?.get('tipo_movimiento')?.value;
    const cant = Number(this.form?.get('cantidad')?.value || 0);
    const actual = this.item.stockfisico;

    if (tipo === 'Entrada') return actual + cant;
    if (tipo === 'Salida') return Math.max(0, actual - cant);
    if (tipo === 'Ajuste') return cant;
    return actual;
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const tipo = this.form.value.tipo_movimiento;
    const cant = Number(this.form.value.cantidad);
    if (tipo === 'Salida' && cant > this.item.stockfisico) {
      alert(`No puede realizar una salida de ${cant} unidades. El stock actual es ${this.item.stockfisico}.`);
      return;
    }

    this.dialogRef.close({
      tipo_movimiento: tipo,
      cantidad: cant,
      motivo: this.form.value.motivo,
      referencia: this.form.value.referencia || 'REG-MANUAL'
    });
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}
