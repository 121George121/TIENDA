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
import { Sucursal } from '../../../../models/cu4_gestionar_sucursales/sucursal.model';

export interface TrasladoDialogData {
  item: InventarioItem;
  sucursales: Sucursal[];
}

@Component({
  selector: 'app-traslado-dialog',
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
  templateUrl: './traslado-dialog.component.html',
  styleUrls: ['./traslado-dialog.component.css']
})
export class TrasladoDialogComponent implements OnInit {
  form!: FormGroup;
  item: InventarioItem;
  sucursalesDisponibles: Sucursal[] = [];

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<TrasladoDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: TrasladoDialogData
  ) {
    this.item = data.item;
    // Solo permitir trasladar a otras sucursales distintas de la actual
    this.sucursalesDisponibles = (data.sucursales || []).filter(s => s.id !== this.item.sucursal_id);
  }

  get stockDisponible(): number {
    if (this.item.stockdisponible !== undefined) {
      return this.item.stockdisponible;
    }
    return Math.max(0, this.item.stockfisico - (this.item.stockreservado || 0));
  }

  ngOnInit(): void {
    const primerDestino = this.sucursalesDisponibles.length > 0 ? this.sucursalesDisponibles[0].id : null;

    this.form = this.fb.group({
      sucursal_destino_id: [primerDestino, [Validators.required]],
      cantidad: [1, [Validators.required, Validators.min(1), Validators.max(this.stockDisponible)]],
      motivo: ['Reabastecimiento de existencias', [Validators.required, Validators.minLength(3)]],
      referencia: ['']
    });
  }

  get stockOrigenProyectado(): number {
    const cant = Number(this.form?.get('cantidad')?.value || 0);
    return Math.max(0, this.item.stockfisico - cant);
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const cant = Number(this.form.value.cantidad);
    if (cant > this.stockDisponible) {
      alert(`No puede transferir ${cant} unidades. El stock disponible no comprometido es de ${this.stockDisponible}.`);
      return;
    }

    this.dialogRef.close({
      sucursal_destino_id: Number(this.form.value.sucursal_destino_id),
      cantidad: cant,
      motivo: this.form.value.motivo,
      referencia: this.form.value.referencia || `TRF-${this.item.sucursal_id}-TO-${this.form.value.sucursal_destino_id}`
    });
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}
