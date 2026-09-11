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

import { Producto } from '../../../../models/product.model';
import { Categoria } from '../../../../models/clasificacion.model';
import { ProductController } from '../../../../controllers/product.controller';
import { ClasificacionController } from '../../../../controllers/clasificacion.controller';
import { ProductFormDialogComponent } from '../product-form-dialog/product-form-dialog.component';
import { ConfirmDialogComponent } from '../../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-product-list',
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
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['id', 'producto', 'categoria', 'precio', 'genero', 'activo', 'acciones'];
  dataSource = new MatTableDataSource<Producto>([]);

  searchControl = new FormControl('');
  categoriaFilterControl = new FormControl<number | null>(null);
  generoFilterControl = new FormControl<string>('');
  estadoFilterControl = new FormControl<boolean | null>(null);

  loading$!: Observable<boolean>;
  private destroy$ = new Subject<void>();

  // KPIs
  totalProductos = 0;
  productosActivos = 0;
  precioPromedio = 0;

  categoriasList: Categoria[] = [];
  generosList: string[] = ['Damas', 'Caballeros', 'Unisex'];

  constructor(
    public productController: ProductController,
    public clasificacionController: ClasificacionController,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loading$ = this.productController.loading$;

    this.productController.productos$.pipe(takeUntil(this.destroy$)).subscribe(productos => {
      this.dataSource.data = productos;
      this.calculateKpis(productos);
    });

    this.clasificacionController.categorias$.pipe(takeUntil(this.destroy$)).subscribe(cats => {
      this.categoriasList = cats;
    });

    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.categoriaFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.generoFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.estadoFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.clasificacionController.loadCategorias();
    this.productController.loadProductos();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculateKpis(productos: Producto[]): void {
    this.totalProductos = productos.length;
    this.productosActivos = productos.filter(p => p.activo).length;
    const totalPrecio = productos.reduce((sum, p) => sum + Number(p.preciobase || 0), 0);
    this.precioPromedio = this.totalProductos > 0 ? Math.round(totalPrecio / this.totalProductos) : 0;
  }

  applyFilters(): void {
    const search = this.searchControl.value || undefined;
    const catId = this.categoriaFilterControl.value || undefined;
    const genero = this.generoFilterControl.value || undefined;
    const estado = this.estadoFilterControl.value !== null ? this.estadoFilterControl.value : undefined;
    this.productController.loadProductos(search, catId, genero, estado);
  }

  resetFilters(): void {
    this.searchControl.setValue('');
    this.categoriaFilterControl.setValue(null);
    this.generoFilterControl.setValue('');
    this.estadoFilterControl.setValue(null);
    this.productController.loadProductos();
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(ProductFormDialogComponent, {
      width: '580px',
      data: { isEdit: false, categorias: this.categoriasList }
    });

    dialogRef.afterClosed().subscribe(res => {
      if (res) {
        this.productController.createProducto(res).subscribe({
          next: () => this.snackBar.open('Producto registrado exitosamente en PostgreSQL', 'Cerrar', { duration: 3000 }),
          error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
        });
      }
    });
  }

  openEditDialog(producto: Producto): void {
    const dialogRef = this.dialog.open(ProductFormDialogComponent, {
      width: '580px',
      data: { producto, isEdit: true, categorias: this.categoriasList }
    });

    dialogRef.afterClosed().subscribe(res => {
      if (res) {
        this.productController.updateProducto(producto.id, res).subscribe({
          next: () => this.snackBar.open('Producto actualizado correctamente', 'Cerrar', { duration: 3000 }),
          error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
        });
      }
    });
  }

  onToggleStatus(producto: Producto): void {
    this.productController.toggleStatus(producto.id, producto.activo).subscribe({
      next: () => {
        const statusText = !producto.activo ? 'activado' : 'desactivado (baja lógica)';
        this.snackBar.open(`Producto ${producto.nombre} ${statusText} correctamente`, 'Cerrar', { duration: 3000 });
      },
      error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
    });
  }

  onDeleteProducto(producto: Producto): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '420px',
      data: {
        title: '¿Dar de Baja el Producto?',
        message: `¿Estás seguro de desactivar la prenda "${producto.nombre}" del catálogo retail?`,
        confirmText: 'Dar de Baja',
        cancelText: 'Cancelar',
        color: 'warn'
      }
    });

    dialogRef.afterClosed().subscribe(confirmed => {
      if (confirmed) {
        this.productController.deleteProducto(producto.id).subscribe({
          next: () => this.snackBar.open(`Producto ${producto.nombre} dado de baja correctamente`, 'Cerrar', { duration: 3000 }),
          error: (err) => this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 })
        });
      }
    });
  }
}
