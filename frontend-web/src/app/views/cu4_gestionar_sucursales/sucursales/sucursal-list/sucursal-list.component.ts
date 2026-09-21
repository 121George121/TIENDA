import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatCardModule } from '@angular/material/card';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

import { Subject, Observable } from 'rxjs';
import { debounceTime, distinctUntilChanged, takeUntil } from 'rxjs/operators';

import { Sucursal } from '../../../../models/cu4_gestionar_sucursales/sucursal.model';
import { SucursalController } from '../../../../controllers/cu4_gestionar_sucursales/sucursal.controller';
import { SucursalFormDialogComponent } from '../sucursal-form-dialog/sucursal-form-dialog.component';
import { ConfirmDialogComponent } from '../../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-sucursal-list',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatSelectModule,
    MatCardModule,
    MatSlideToggleModule,
    MatSnackBarModule,
    MatProgressBarModule,
    MatTooltipModule,
    MatDialogModule
  ],
  templateUrl: './sucursal-list.component.html',
  styleUrls: ['./sucursal-list.component.css']
})
export class SucursalListComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['id', 'sucursal', 'ciudad', 'direccion', 'telefono', 'activo', 'fechacreacion', 'acciones'];
  dataSource = new MatTableDataSource<Sucursal>([]);

  searchControl = new FormControl('');
  ciudadFilterControl = new FormControl<string>('');
  estadoFilterControl = new FormControl<boolean | null>(null);

  loading$!: Observable<boolean>;
  private destroy$ = new Subject<void>();

  // KPIs
  totalSucursales = 0;
  sucursalesActivas = 0;
  ciudadesCount = 0;

  ciudadesList: string[] = ['Santa Cruz', 'La Paz', 'Cochabamba', 'Tarija', 'Sucre'];

  constructor(
    public sucursalController: SucursalController,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loading$ = this.sucursalController.loading$;

    this.sucursalController.sucursales$.pipe(takeUntil(this.destroy$)).subscribe(sucursales => {
      this.dataSource.data = sucursales;
      this.calculateKpis(sucursales);
    });

    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.ciudadFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.estadoFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.sucursalController.loadSucursales();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculateKpis(sucursales: Sucursal[]): void {
    this.totalSucursales = sucursales.length;
    this.sucursalesActivas = sucursales.filter(s => s.activo).length;
    const ciudades = new Set(sucursales.map(s => s.ciudad).filter(Boolean));
    this.ciudadesCount = ciudades.size;
  }

  applyFilters(): void {
    const search = this.searchControl.value || undefined;
    const ciudad = this.ciudadFilterControl.value || undefined;
    const estado = this.estadoFilterControl.value !== null ? this.estadoFilterControl.value : undefined;
    this.sucursalController.loadSucursales(search, ciudad, estado);
  }

  resetFilters(): void {
    this.searchControl.setValue('');
    this.ciudadFilterControl.setValue('');
    this.estadoFilterControl.setValue(null);
    this.sucursalController.loadSucursales();
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(SucursalFormDialogComponent, {
      width: '560px',
      data: { isEdit: false }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.sucursalController.createSucursal(result).subscribe({
          next: () => {
            this.snackBar.open('Sucursal registrada exitosamente en PostgreSQL', 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

  openEditDialog(sucursal: Sucursal): void {
    const dialogRef = this.dialog.open(SucursalFormDialogComponent, {
      width: '560px',
      data: { sucursal, isEdit: true }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.sucursalController.updateSucursal(sucursal.id, result).subscribe({
          next: () => {
            this.snackBar.open('Sucursal actualizada correctamente', 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

  onToggleStatus(sucursal: Sucursal): void {
    this.sucursalController.toggleStatus(sucursal.id, sucursal.activo).subscribe({
      next: () => {
        const action = !sucursal.activo ? 'activada' : 'desactivada (baja lógica)';
        this.snackBar.open(`Sucursal ${sucursal.nombre} ${action} correctamente`, 'Cerrar', { duration: 3000 });
      },
      error: (err) => {
        this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
      }
    });
  }

  onDeleteSucursal(sucursal: Sucursal): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '420px',
      data: {
        title: '¿Eliminar Sucursal?',
        message: `¿Estás seguro de eliminar la sucursal "${sucursal.nombre}"? Esta acción removerá el punto de venta.`,
        confirmText: 'Eliminar',
        cancelText: 'Cancelar',
        color: 'warn',
        icon: 'delete_forever'
      }
    });

    dialogRef.afterClosed().subscribe(confirmed => {
      if (confirmed) {
        this.sucursalController.deleteSucursal(sucursal.id).subscribe({
          next: () => {
            this.snackBar.open(`Sucursal "${sucursal.nombre}" eliminada correctamente`, 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error al eliminar: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

}
