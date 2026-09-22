import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatIconModule } from '@angular/material/icon';
import { Usuario } from '../../../../models/cu2_gestionar_usuarios_roles/user.model';
import { Rol } from '../../../../models/cu2_gestionar_usuarios_roles/role.model';

export interface UserFormDialogData {
  usuario?: Usuario;
  roles: Rol[];
  isEdit: boolean;
}

@Component({
  selector: 'app-user-form-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatSlideToggleModule,
    MatIconModule
  ],
  templateUrl: './user-form-dialog.component.html',
  styleUrls: ['./user-form-dialog.component.css']
})
export class UserFormDialogComponent implements OnInit {
  userForm!: FormGroup;
  hidePassword = true;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<UserFormDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: UserFormDialogData
  ) {}

  ngOnInit(): void {
    const u = this.data.usuario;

    this.userForm = this.fb.group({
      nombre: [u?.nombre || '', [Validators.required, Validators.minLength(2)]],
      apellido: [u?.apellido || ''],
      email: [u?.email || '', [Validators.required, Validators.email]],
      password: [this.data.isEdit ? '' : 'usuario123.'],
      telefono: [u?.telefono || ''],
      rol_id: [u?.rol_id || u?.rolid || (this.data.roles.length > 0 ? this.data.roles[0].id : null), [Validators.required]],
      activo: [u !== undefined ? u.activo : true]
    });
  }

  onSubmit(): void {
    if (this.userForm.invalid) {
      this.userForm.markAllAsTouched();
      return;
    }

    const formValue = { ...this.userForm.value };
    if (!this.data.isEdit && (!formValue.password || !formValue.password.trim())) {
      formValue.password = 'usuario123.';
    }
    if (this.data.isEdit && !formValue.password) {
      delete formValue.password;
    }

    this.dialogRef.close(formValue);
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
