import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Proveedor } from '../../../../models/proveedor.model';

export interface ProveedorFormDialogData {
  proveedor?: Proveedor;
  isEdit: boolean;
}

@Component({
  selector: 'app-proveedor-form-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './proveedor-form-dialog.component.html',
  styleUrls: ['./proveedor-form-dialog.component.css']
})
export class ProveedorFormDialogComponent implements OnInit {
  form!: FormGroup;
  isEdit: boolean;
  proveedor?: Proveedor;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<ProveedorFormDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ProveedorFormDialogData
  ) {
    this.isEdit = data.isEdit;
    this.proveedor = data.proveedor;
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      nombre: [this.proveedor?.nombre || '', [Validators.required, Validators.minLength(3)]],
      razonsocial: [this.proveedor?.razonsocial || ''],
      nit: [this.proveedor?.nit || ''],
      contacto: [this.proveedor?.contacto || '', [Validators.required]],
      telefono: [this.proveedor?.telefono || '', [Validators.required]],
      email: [this.proveedor?.email || '', [Validators.email]],
      direccion: [this.proveedor?.direccion || '']
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
