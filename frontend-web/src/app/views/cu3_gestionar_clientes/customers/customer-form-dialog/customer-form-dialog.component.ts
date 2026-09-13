import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { Cliente } from '../../../../models/cu3_gestionar_clientes/customer.model';

export interface CustomerFormDialogData {
  cliente?: Cliente;
  isEdit: boolean;
}

@Component({
  selector: 'app-customer-form-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSlideToggleModule
  ],
  templateUrl: './customer-form-dialog.component.html',
  styleUrls: ['./customer-form-dialog.component.css']
})
export class CustomerFormDialogComponent implements OnInit {
  form!: FormGroup;
  isEdit: boolean;
  cliente?: Cliente;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<CustomerFormDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: CustomerFormDialogData
  ) {
    this.isEdit = data.isEdit;
    this.cliente = data.cliente;
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      nombre: [this.cliente?.nombre || '', [Validators.required, Validators.minLength(2)]],
      apellido: [this.cliente?.apellido || ''],
      email: [this.cliente?.email || '', [Validators.required, Validators.email]],
      telefono: [this.cliente?.telefono || ''],
      password: ['', this.isEdit ? [] : [Validators.required, Validators.minLength(6)]]
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    const formValue = { ...this.form.value };
    if (this.isEdit && !formValue.password) {
      delete formValue.password;
    }
    this.dialogRef.close(formValue);
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}
