import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { Rol, LISTA_PERMISOS_SISTEMA, PermisoCategoria } from '../../../../models/cu2_gestionar_usuarios_roles/role.model';

export interface RolePermissionsDialogData {
  rol: Rol;
}

@Component({
  selector: 'app-role-permissions-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatCheckboxModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatExpansionModule
  ],
  templateUrl: './role-permissions-dialog.component.html',
  styleUrls: ['./role-permissions-dialog.component.css']
})
export class RolePermissionsDialogComponent implements OnInit {
  rol!: Rol;
  categoriasPermisos: PermisoCategoria[] = LISTA_PERMISOS_SISTEMA;
  selectedPermisos: Set<string> = new Set<string>();

  constructor(
    public dialogRef: MatDialogRef<RolePermissionsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: RolePermissionsDialogData
  ) {}

  ngOnInit(): void {
    this.rol = this.data.rol;
    if (this.rol.permisos && Array.isArray(this.rol.permisos)) {
      this.rol.permisos.forEach(p => this.selectedPermisos.add(p));
    }
  }

  isPermissionSelected(clave: string): boolean {
    return this.selectedPermisos.has(clave);
  }

  togglePermission(clave: string): void {
    if (this.selectedPermisos.has(clave)) {
      this.selectedPermisos.delete(clave);
    } else {
      this.selectedPermisos.add(clave);
    }
  }

  isCategoryAllSelected(cat: PermisoCategoria): boolean {
    return cat.permisos.every(p => this.selectedPermisos.has(p.clave));
  }

  isCategorySomeSelected(cat: PermisoCategoria): boolean {
    const count = cat.permisos.filter(p => this.selectedPermisos.has(p.clave)).length;
    return count > 0 && count < cat.permisos.length;
  }

  toggleCategory(cat: PermisoCategoria): void {
    const allSelected = this.isCategoryAllSelected(cat);
    if (allSelected) {
      cat.permisos.forEach(p => this.selectedPermisos.delete(p.clave));
    } else {
      cat.permisos.forEach(p => this.selectedPermisos.add(p.clave));
    }
  }

  onSubmit(): void {
    this.dialogRef.close(Array.from(this.selectedPermisos));
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
