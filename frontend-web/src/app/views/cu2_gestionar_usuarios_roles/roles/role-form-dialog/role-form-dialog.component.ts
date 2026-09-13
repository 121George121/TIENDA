import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Rol } from '../../../../models/cu2_gestionar_usuarios_roles/role.model';

export interface RoleFormDialogData {
  rol?: Rol;
  isEdit: boolean;
}

@Component({
  selector: 'app-role-form-dialog',
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
  templateUrl: './role-form-dialog.component.html',
  styleUrls: ['./role-form-dialog.component.css']
})
export class RoleFormDialogComponent implements OnInit {
  roleForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<RoleFormDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: RoleFormDialogData
  ) {}

  ngOnInit(): void {
    const r = this.data.rol;
    this.roleForm = this.fb.group({
      nombre: [r?.nombre || '', [Validators.required, Validators.minLength(3)]],
      descripcion: [r?.descripcion || '']
    });
  }

  onSubmit(): void {
    if (this.roleForm.invalid) {
      this.roleForm.markAllAsTouched();
      return;
    }
    this.dialogRef.close(this.roleForm.value);
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
