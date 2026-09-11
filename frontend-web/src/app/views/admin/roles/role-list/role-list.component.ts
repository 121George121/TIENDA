import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTooltipModule } from '@angular/material/tooltip';

import { Subject, Observable } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { Rol } from '../../../../models/role.model';
import { RoleController } from '../../../../controllers/role.controller';
import { RoleFormDialogComponent } from '../role-form-dialog/role-form-dialog.component';
import { RolePermissionsDialogComponent } from '../role-permissions-dialog/role-permissions-dialog.component';
import { ConfirmDialogComponent } from '../../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-role-list',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatCardModule,
    MatDialogModule,
    MatSnackBarModule,
    MatProgressBarModule,
    MatTooltipModule
  ],
  templateUrl: './role-list.component.html',
  styleUrls: ['./role-list.component.css']
})
export class RoleListComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['id', 'nombre', 'descripcion', 'estado', 'permisos', 'acciones'];
  dataSource = new MatTableDataSource<Rol>([]);

  loading$!: Observable<boolean>;
  private destroy$ = new Subject<void>();

  // KPIs
  totalRoles = 0;
  totalPermisosAsignados = 0;

  constructor(
    public roleController: RoleController,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loading$ = this.roleController.loading$;

    this.roleController.roles$.pipe(takeUntil(this.destroy$)).subscribe(roles => {
      this.dataSource.data = roles;
      this.calculateKpis(roles);
    });

    this.roleController.loadRoles();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculateKpis(roles: Rol[]): void {
    this.totalRoles = roles.length;
    this.totalPermisosAsignados = roles.reduce((acc, r) => acc + (r.permisos ? r.permisos.length : 0), 0);
  }

  getRoleIcon(nombre: string): string {
    const n = nombre ? nombre.toUpperCase() : '';
    if (n.includes('ADMIN')) return 'shield';
    if (n.includes('SUPERVISOR')) return 'manage_accounts';
    if (n.includes('CAJERO') || n.includes('VENDEDOR')) return 'point_of_sale';
    if (n.includes('CLIENTE')) return 'shopping_bag';
    return 'security';
  }

  getRoleCardClass(nombre: string): string {
    const n = nombre ? nombre.toUpperCase() : '';
    if (n.includes('ADMIN')) return 'admin';
    if (n.includes('SUPERVISOR')) return 'supervisor';
    if (n.includes('CAJERO') || n.includes('VENDEDOR')) return 'cajero';
    if (n.includes('CLIENTE')) return 'cliente';
    return 'admin';
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(RoleFormDialogComponent, {
      width: '520px',
      data: { isEdit: false }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.roleController.createRole(result).subscribe({
          next: () => {
            this.snackBar.open('Rol registrado exitosamente', 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

  openEditDialog(rol: Rol): void {
    const dialogRef = this.dialog.open(RoleFormDialogComponent, {
      width: '520px',
      data: { rol, isEdit: true }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.roleController.updateRole(rol.id, result).subscribe({
          next: () => {
            this.snackBar.open('Rol actualizado correctamente', 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

  openPermissionsDialog(rol: Rol): void {
    const dialogRef = this.dialog.open(RolePermissionsDialogComponent, {
      width: '680px',
      data: { rol }
    });

    dialogRef.afterClosed().subscribe(permisos => {
      if (permisos && Array.isArray(permisos)) {
        this.roleController.updatePermissions(rol.id, permisos).subscribe({
          next: () => {
            this.snackBar.open(`Permisos del rol ${rol.nombre} guardados exitosamente`, 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

  onDeleteRole(rol: Rol): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '420px',
      data: {
        title: '¿Eliminar Rol?',
        message: `¿Estás seguro de eliminar el rol "${rol.nombre}"? Los usuarios asociados perderán esta asignación.`,
        confirmText: 'Sí, Eliminar Rol',
        cancelText: 'Cancelar',
        color: 'warn',
        icon: 'security'
      }
    });

    dialogRef.afterClosed().subscribe(confirmed => {
      if (confirmed) {
        this.roleController.deleteRole(rol.id).subscribe({
          next: () => {
            this.snackBar.open(`Rol ${rol.nombre} eliminado de la base de datos`, 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error al eliminar: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }
}
