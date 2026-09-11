import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { Sucursal } from '../../../../models/sucursal.model';

export interface SucursalFormDialogData {
  sucursal?: Sucursal;
  isEdit: boolean;
}

@Component({
  selector: 'app-sucursal-form-dialog',
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
  templateUrl: './sucursal-form-dialog.component.html',
  styleUrls: ['./sucursal-form-dialog.component.css']
})
export class SucursalFormDialogComponent implements OnInit {
  form!: FormGroup;
  isEdit: boolean;
  sucursal?: Sucursal;

  ciudadesDisponibles: string[] = ['Santa Cruz', 'La Paz', 'Cochabamba', 'Tarija', 'Sucre', 'Oruro', 'Potosí', 'Beni', 'Pando'];

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<SucursalFormDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: SucursalFormDialogData
  ) {
    this.isEdit = data.isEdit;
    this.sucursal = data.sucursal;
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      nombre: [this.sucursal?.nombre || '', [Validators.required, Validators.minLength(3)]],
      ciudad: [this.sucursal?.ciudad || 'Santa Cruz', [Validators.required]],
      direccion: [this.sucursal?.direccion || '', [Validators.required]],
      telefono: [this.sucursal?.telefono || ''],
      latitud: [this.sucursal?.latitud || null],
      longitud: [this.sucursal?.longitud || null]
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.dialogRef.close(this.form.value);
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}
