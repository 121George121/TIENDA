import { Component, OnInit, ViewChild, AfterViewInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormControl } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatChipsModule } from '@angular/material/chips';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatCardModule } from '@angular/material/card';
import { MatTooltipModule } from '@angular/material/tooltip';

import { Subject, Observable } from 'rxjs';
import { debounceTime, takeUntil } from 'rxjs/operators';

import { Usuario } from '../../../../models/cu2_gestionar_usuarios_roles/user.model';
import { Rol } from '../../../../models/cu2_gestionar_usuarios_roles/role.model';
import { UserController } from '../../../../controllers/cu2_gestionar_usuarios_roles/user.controller';
import { RoleController } from '../../../../controllers/cu2_gestionar_usuarios_roles/role.controller';
import { UserFormDialogComponent } from '../user-form-dialog/user-form-dialog.component';
import { UserDetailDialogComponent } from '../user-detail-dialog/user-detail-dialog.component';
import { ConfirmDialogComponent } from '../../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSelectModule,
    MatSlideToggleModule,
    MatChipsModule,
    MatDialogModule,
    MatSnackBarModule,
    MatProgressBarModule,
    MatCardModule,
    MatTooltipModule
  ],
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit, AfterViewInit, OnDestroy {
  displayedColumns: string[] = ['id', 'usuario', 'email', 'telefono', 'rol', 'activo', 'fecha', 'acciones'];
  dataSource = new MatTableDataSource<Usuario>([]);
  roles: Rol[] = [];

  searchControl = new FormControl('');
  rolFilterControl = new FormControl<number | null>(null);
  estadoFilterControl = new FormControl<boolean | null>(null);

  loading$!: Observable<boolean>;
  private destroy$ = new Subject<void>();

  // KPIs
  totalUsuarios = 0;
  usuariosActivos = 0;
  usuariosInactivos = 0;
  totalRoles = 0;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    public userController: UserController,
    public roleController: RoleController,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loading$ = this.userController.loading$;

    this.roleController.loadRoles();
    this.roleController.roles$.pipe(takeUntil(this.destroy$)).subscribe(r => {
      this.roles = r;
      this.totalRoles = r.length;
    });

    this.userController.users$.pipe(takeUntil(this.destroy$)).subscribe(users => {
      this.dataSource.data = users;
      this.calculateKpis(users);
    });

    this.userController.loadUsers();

    // Filtros reactivos
    this.searchControl.valueChanges
      .pipe(debounceTime(300), takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.rolFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.estadoFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculateKpis(users: Usuario[]): void {
    this.totalUsuarios = users.length;
    this.usuariosActivos = users.filter(u => u.activo).length;
    this.usuariosInactivos = users.filter(u => !u.activo).length;
  }

  applyFilters(): void {
    const search = this.searchControl.value || undefined;
    const rolId = this.rolFilterControl.value !== null ? this.rolFilterControl.value : undefined;
    const activo = this.estadoFilterControl.value !== null ? this.estadoFilterControl.value : undefined;

    this.userController.loadUsers(search, rolId, activo);
  }

  resetFilters(): void {
    this.searchControl.setValue('');
    this.rolFilterControl.setValue(null);
    this.estadoFilterControl.setValue(null);
    this.userController.loadUsers();
  }

  getRoleName(user: Usuario): string {
    if (user.rol && user.rol.nombre) return user.rol.nombre;
    const rId = user.rol_id || user.rolid;
    const r = this.roles.find(x => x.id === rId);
    return r ? r.nombre : 'Sin Rol';
  }

  openViewDialog(user: Usuario): void {
    this.dialog.open(UserDetailDialogComponent, {
      width: '520px',
      data: { usuario: user, rolNombre: this.getRoleName(user) }
    });
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(UserFormDialogComponent, {
      width: '580px',
      data: { roles: this.roles, isEdit: false }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.userController.createUser(result).subscribe({
          next: () => {
            this.snackBar.open('Usuario registrado exitosamente (Contraseña: usuario123.)', 'Cerrar', { duration: 4000 });
          },
          error: (err) => {
            const msg = typeof err === 'string' ? err : (err?.error?.detail || err?.message || 'Error al registrar usuario');
            this.snackBar.open(`Error: ${msg}`, 'Cerrar', { duration: 5000 });
          }
        });
      }
    });
  }

  openEditDialog(user: Usuario): void {
    const dialogRef = this.dialog.open(UserFormDialogComponent, {
      width: '580px',
      data: { usuario: user, roles: this.roles, isEdit: true }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.userController.updateUser(user.id, result).subscribe({
          next: () => {
            this.snackBar.open('Usuario actualizado correctamente', 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

  onToggleStatus(user: Usuario): void {
    this.userController.toggleStatus(user.id, user.activo).subscribe({
      next: (u) => {
        const estadoStr = u.activo ? 'activado' : 'desactivado';
        this.snackBar.open(`Acceso de ${user.nombre} ${estadoStr}`, 'Cerrar', { duration: 3000 });
      },
      error: (err) => {
        this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
        this.userController.loadUsers();
      }
    });
  }

  onDeleteUser(user: Usuario): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '420px',
      data: {
        title: '¿Eliminar Usuario?',
        message: `¿Estás seguro de que deseas eliminar permanentemente a ${user.nombre}? Esta acción no se puede deshacer.`,
        confirmText: 'Sí, Eliminar',
        cancelText: 'Cancelar',
        color: 'warn',
        icon: 'delete_forever'
      }
    });

    dialogRef.afterClosed().subscribe(confirmed => {
      if (confirmed) {
        this.userController.deleteUser(user.id).subscribe({
          next: () => {
            this.snackBar.open('Usuario eliminado permanentemente de la base de datos', 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error al eliminar: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }
}
