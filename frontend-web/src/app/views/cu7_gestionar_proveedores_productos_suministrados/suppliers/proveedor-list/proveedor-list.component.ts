import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { Subject, Observable } from 'rxjs';
import { debounceTime, distinctUntilChanged, takeUntil } from 'rxjs/operators';

import { Proveedor } from '../../../../models/cu7_gestionar_proveedores_productos_suministrados/proveedor.model';
import { ProveedorController } from '../../../../controllers/cu7_gestionar_proveedores_productos_suministrados/proveedor.controller';
import { ProveedorFormDialogComponent } from '../proveedor-form-dialog/proveedor-form-dialog.component';
import { ConfirmDialogComponent } from '../../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-proveedor-list',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatCardModule,
    MatSnackBarModule,
    MatProgressBarModule,
    MatTooltipModule,
    MatDialogModule
  ],
  templateUrl: './proveedor-list.component.html',
  styleUrls: ['./proveedor-list.component.css']
})
export class ProveedorListComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['id', 'proveedor', 'contacto', 'nit', 'suministros', 'activo', 'acciones'];
  dataSource = new MatTableDataSource<Proveedor>([]);
  searchControl = new FormControl('');

  loading$!: Observable<boolean>;
  private destroy$ = new Subject<void>();

  // KPIs
  totalProveedores = 0;
  proveedoresActivos = 0;
  totalSuministros = 0;

  constructor(
    public controller: ProveedorController,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loading$ = this.controller.loading$;

    this.controller.proveedores$.pipe(takeUntil(this.destroy$)).subscribe(list => {
      this.dataSource.data = list;
      this.calculateKpis(list);
    });

    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe((query) => this.controller.loadProveedores(query || ''));

    this.controller.loadProveedores();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculateKpis(list: Proveedor[]): void {
    this.totalProveedores = list.length;
    this.proveedoresActivos = list.filter(p => p.activo).length;
    this.totalSuministros = list.reduce((sum, p) => sum + (p.productos_suministrados?.length || 0), 0);
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(ProveedorFormDialogComponent, {
      width: '560px',
      data: { isEdit: false }
    });

    dialogRef.afterClosed().subscribe(res => {
      if (res) {
        this.controller.createProveedor(res).subscribe({
          next: () => this.snackBar.open('Proveedor registrado exitosamente en PostgreSQL', 'Cerrar', { duration: 3000 }),
          error: (err) => {
            const msg = typeof err === 'string' ? err : (err?.error?.detail || err?.message || 'Error al registrar proveedor');
            this.snackBar.open(`Error: ${msg}`, 'Cerrar', { duration: 5000 });
          }
        });
      }
    });
  }

  openEditDialog(proveedor: Proveedor): void {
    const dialogRef = this.dialog.open(ProveedorFormDialogComponent, {
      width: '560px',
      data: { proveedor, isEdit: true }
    });

    dialogRef.afterClosed().subscribe(res => {
      if (res) {
        this.controller.updateProveedor(proveedor.id, res).subscribe({
          next: () => this.snackBar.open('Proveedor actualizado correctamente', 'Cerrar', { duration: 3000 }),
          error: (err) => {
            const msg = typeof err === 'string' ? err : (err?.error?.detail || err?.message || 'Error al actualizar');
            this.snackBar.open(`Error: ${msg}`, 'Cerrar', { duration: 5000 });
          }
        });
      }
    });
  }

  toggleStatusProveedor(proveedor: Proveedor): void {
    const nuevoEstado = !proveedor.activo;
    const accion = nuevoEstado ? 'activado' : 'desactivado';
    this.controller.updateProveedor(proveedor.id, { activo: nuevoEstado }).subscribe({
      next: () => this.snackBar.open(`Proveedor ${proveedor.nombre} ${accion} correctamente`, 'Cerrar', { duration: 3000 }),
      error: (err) => {
        const msg = typeof err === 'string' ? err : (err?.error?.detail || err?.message || 'Error al cambiar estado');
        this.snackBar.open(`Error: ${msg}`, 'Cerrar', { duration: 5000 });
      }
    });
  }

  deleteProveedor(proveedor: Proveedor): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '420px',
      data: {
        title: '¿Eliminar Proveedor?',
        message: `¿Estás seguro de eliminar al proveedor "${proveedor.nombre}"? Esta acción removerá el registro definitivamente.`,
        confirmText: 'Eliminar',
        cancelText: 'Cancelar',
        icon: 'delete_forever',
        color: 'warn'
      }
    });

    dialogRef.afterClosed().subscribe(confirmed => {
      if (confirmed) {
        this.controller.deleteProveedor(proveedor.id).subscribe({
          next: () => this.snackBar.open(`Proveedor "${proveedor.nombre}" eliminado correctamente`, 'Cerrar', { duration: 3000 }),
          error: (err) => {
            const msg = typeof err === 'string' ? err : (err?.error?.detail || err?.message || 'Error al eliminar');
            this.snackBar.open(`Error: ${msg}`, 'Cerrar', { duration: 5000 });
          }
        });
      }
    });
  }
}

