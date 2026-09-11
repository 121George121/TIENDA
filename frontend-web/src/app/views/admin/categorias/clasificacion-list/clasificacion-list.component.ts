import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatTabsModule } from '@angular/material/tabs';
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

import { Categoria, Temporada, Coleccion } from '../../../../models/clasificacion.model';
import { ClasificacionController } from '../../../../controllers/clasificacion.controller';
import { ClasificacionFormDialogComponent, EntityType } from '../clasificacion-form-dialog/clasificacion-form-dialog.component';
import { ConfirmDialogComponent } from '../../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-clasificacion-list',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTabsModule,
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
  templateUrl: './clasificacion-list.component.html',
  styleUrls: ['./clasificacion-list.component.css']
})
export class ClasificacionListComponent implements OnInit, OnDestroy {
  searchControl = new FormControl('');
  loading$!: Observable<boolean>;
  private destroy$ = new Subject<void>();

  // Data Sources
  categoriasDS = new MatTableDataSource<Categoria>([]);
  temporadasDS = new MatTableDataSource<Temporada>([]);
  coleccionesDS = new MatTableDataSource<Coleccion>([]);

  // Columns
  catColumns: string[] = ['id', 'nombre', 'descripcion', 'activo', 'acciones'];
  tempColumns: string[] = ['id', 'nombre', 'fechainicio', 'fechafin', 'activo', 'acciones'];
  colColumns: string[] = ['id', 'imagen', 'nombre', 'temporada', 'activo', 'acciones'];

  // KPIs
  totalCategorias = 0;
  totalTemporadas = 0;
  totalColecciones = 0;

  temporadasList: Temporada[] = [];

  constructor(
    public controller: ClasificacionController,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loading$ = this.controller.loading$;

    this.controller.categorias$.pipe(takeUntil(this.destroy$)).subscribe(list => {
      this.categoriasDS.data = list;
      this.totalCategorias = list.length;
    });

    this.controller.temporadas$.pipe(takeUntil(this.destroy$)).subscribe(list => {
      this.temporadasDS.data = list;
      this.temporadasList = list;
      this.totalTemporadas = list.length;
    });

    this.controller.colecciones$.pipe(takeUntil(this.destroy$)).subscribe(list => {
      this.coleccionesDS.data = list;
      this.totalColecciones = list.length;
    });

    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe((val) => this.applySearch(val || ''));

    this.loadAllData();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadAllData(): void {
    this.controller.loadCategorias();
    this.controller.loadTemporadas();
    this.controller.loadColecciones();
  }

  applySearch(query: string): void {
    this.controller.loadCategorias(query);
    this.controller.loadTemporadas(query);
    this.controller.loadColecciones(query);
  }

  // DIÁLOGOS Y ACCIONES CRUD
  openCreateDialog(type: EntityType): void {
    const dialogRef = this.dialog.open(ClasificacionFormDialogComponent, {
      width: '520px',
      data: { type, isEdit: false, temporadas: this.temporadasList }
    });

    dialogRef.afterClosed().subscribe(res => {
      if (res) {
        if (type === 'categoria') {
          this.controller.createCategoria(res).subscribe({
            next: () => this.snackBar.open('Categoría creada en PostgreSQL', 'Cerrar', { duration: 3000 }),
            error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
          });
        } else if (type === 'temporada') {
          this.controller.createTemporada(res).subscribe({
            next: () => this.snackBar.open('Temporada creada en PostgreSQL', 'Cerrar', { duration: 3000 }),
            error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
          });
        } else if (type === 'coleccion') {
          this.controller.createColeccion(res).subscribe({
            next: () => this.snackBar.open('Colección creada en PostgreSQL', 'Cerrar', { duration: 3000 }),
            error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
          });
        }
      }
    });
  }

  openEditDialog(type: EntityType, item: any): void {
    const dialogRef = this.dialog.open(ClasificacionFormDialogComponent, {
      width: '520px',
      data: { type, item, isEdit: true, temporadas: this.temporadasList }
    });

    dialogRef.afterClosed().subscribe(res => {
      if (res) {
        if (type === 'categoria') {
          this.controller.updateCategoria(item.id, res).subscribe({
            next: () => this.snackBar.open('Categoría actualizada', 'Cerrar', { duration: 3000 }),
            error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
          });
        } else if (type === 'temporada') {
          this.controller.updateTemporada(item.id, res).subscribe({
            next: () => this.snackBar.open('Temporada actualizada', 'Cerrar', { duration: 3000 }),
            error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
          });
        } else if (type === 'coleccion') {
          this.controller.updateColeccion(item.id, res).subscribe({
            next: () => this.snackBar.open('Colección actualizada', 'Cerrar', { duration: 3000 }),
            error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
          });
        }
      }
    });
  }

  deleteItem(type: EntityType, item: any): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '400px',
      data: {
        title: `¿Dar de baja ${type}?`,
        message: `¿Estás seguro de desactivar "${item.nombre}"?`,
        confirmText: 'Desactivar',
        cancelText: 'Cancelar',
        color: 'warn'
      }
    });

    dialogRef.afterClosed().subscribe(confirmed => {
      if (confirmed) {
        if (type === 'categoria') {
          this.controller.deleteCategoria(item.id).subscribe({
            next: () => this.snackBar.open('Categoría dada de baja', 'Cerrar', { duration: 3000 })
          });
        } else if (type === 'temporada') {
          this.controller.deleteTemporada(item.id).subscribe({
            next: () => this.snackBar.open('Temporada dada de baja', 'Cerrar', { duration: 3000 })
          });
        } else if (type === 'coleccion') {
          this.controller.deleteColeccion(item.id).subscribe({
            next: () => this.snackBar.open('Colección dada de baja', 'Cerrar', { duration: 3000 })
          });
        }
      }
    });
  }
}
