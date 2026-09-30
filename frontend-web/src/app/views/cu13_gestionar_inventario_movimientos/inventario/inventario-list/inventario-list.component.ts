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

import { InventarioItem } from '../../../../models/cu13_gestionar_inventario_movimientos/inventario.model';
import { InventarioController } from '../../../../controllers/cu13_gestionar_inventario_movimientos/inventario.controller';
import { SucursalController } from '../../../../controllers/cu4_gestionar_sucursales/sucursal.controller';
import { Sucursal } from '../../../../models/cu4_gestionar_sucursales/sucursal.model';
import { MovimientoDialogComponent } from '../movimiento-dialog/movimiento-dialog.component';
import { KardexDialogComponent } from '../kardex-dialog/kardex-dialog.component';

@Component({
  selector: 'app-inventario-list',
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
  templateUrl: './inventario-list.component.html',
  styleUrls: ['./inventario-list.component.css']
})
export class InventarioListComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['producto', 'variante', 'sucursal', 'stockfisico', 'stockminimo', 'estado', 'acciones'];
  dataSource = new MatTableDataSource<InventarioItem>([]);

  searchControl = new FormControl('');
  sucursalFilterControl = new FormControl<number | null>(null);
  soloBajoStockControl = new FormControl<boolean>(false);

  loading$!: Observable<boolean>;
  sucursales: Sucursal[] = [];
  private destroy$ = new Subject<void>();

  // KPIs
  totalItems = 0;
  totalUnidadesFisicas = 0;
  itemsBajoStock = 0;

  constructor(
    public inventarioController: InventarioController,
    public sucursalController: SucursalController,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loading$ = this.inventarioController.loading$;

    this.inventarioController.inventario$.pipe(takeUntil(this.destroy$)).subscribe(items => {
      this.dataSource.data = items;
      this.calculateKpis(items);
    });

    this.sucursalController.sucursales$.pipe(takeUntil(this.destroy$)).subscribe(sucursales => {
      this.sucursales = sucursales;
    });

    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.sucursalFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.soloBajoStockControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.sucursalController.loadSucursales();
    this.inventarioController.loadInventario();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculateKpis(items: InventarioItem[]): void {
    this.totalItems = items.length;
    this.totalUnidadesFisicas = items.reduce((acc, it) => acc + (it.stockfisico || 0), 0);
    this.itemsBajoStock = items.filter(it => it.bajo_stock || it.stockfisico <= it.stockminimo).length;
  }

  applyFilters(): void {
    const search = this.searchControl.value || undefined;
    const sucursalId = this.sucursalFilterControl.value || undefined;
    const soloBajoStock = this.soloBajoStockControl.value || undefined;
    this.inventarioController.loadInventario(sucursalId, search, soloBajoStock);
  }

  setSucursalFilter(sucursalId: number | null): void {
    this.sucursalFilterControl.setValue(sucursalId);
  }

  resetFilters(): void {
    this.searchControl.setValue('');
    this.sucursalFilterControl.setValue(null);
    this.soloBajoStockControl.setValue(false);
    this.inventarioController.loadInventario();
  }

  getColorName(row: InventarioItem): string {
    const raw = (row.color || row.color_nombre || '').trim();
    if (raw && raw !== 'Único' && raw !== 'Estándar' && raw !== '--') {
      return raw;
    }
    const name = (row.producto_nombre || '').toLowerCase();
    if (name.includes('beige')) return 'Beige';
    if (name.includes('blanc')) return 'Blanco';
    if (name.includes('roj') || name.includes('bordo') || name.includes('vino')) return 'Rojo';
    if (name.includes('negr')) return 'Negro';
    if (name.includes('verd') || name.includes('olivo')) return 'Verde';
    if (name.includes('azul')) return 'Azul';
    if (name.includes('amarill')) return 'Amarillo';
    if (name.includes('gris')) return 'Gris';
    if (name.includes('terracota')) return 'Terracota';
    return raw || 'Estándar';
  }

  getColorHex(row: InventarioItem): string {
    const cName = this.getColorName(row).toLowerCase();
    if (cName.includes('beige')) return '#D4B996';
    if (cName.includes('blanc')) return '#FFFFFF';
    if (cName.includes('roj') || cName.includes('borgoña')) return '#DC2626';
    if (cName.includes('negr')) return '#1E293B';
    if (cName.includes('verd') || cName.includes('olivo')) return '#059669';
    if (cName.includes('azul')) return '#2563EB';
    if (cName.includes('amarill')) return '#EAB308';
    if (cName.includes('gris')) return '#64748B';
    if (cName.includes('terracota')) return '#B45309';
    if (row.color_hex && row.color_hex !== '#111827') {
      return row.color_hex;
    }
    return '#334155';
  }

  getColorBg(row: InventarioItem): string {
    const hex = this.getColorHex(row);
    if (hex.toUpperCase() === '#FFFFFF') return '#F8FAFC';
    return hex + '18';
  }

  getColorBorder(row: InventarioItem): string {
    const hex = this.getColorHex(row);
    if (hex.toUpperCase() === '#FFFFFF') return '#CBD5E1';
    return hex + '55';
  }

  getColorTextColor(row: InventarioItem): string {
    const hex = this.getColorHex(row);
    if (hex.toUpperCase() === '#FFFFFF') return '#334155';
    return hex;
  }

  getSizeName(row: InventarioItem): string {
    const s = row.talla || row.talla_nombre;
    if (s && s !== '--') return s;
    return 'M';
  }

  openMovimientoDialog(item: InventarioItem): void {
    const dialogRef = this.dialog.open(MovimientoDialogComponent, {
      width: '580px',
      data: { item }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.inventarioController.registrarMovimiento(item.id, result).subscribe({
          next: (res) => {
            this.snackBar.open(
              `Movimiento registrado: Stock de ${item.producto_nombre} actualizado a ${res.stock_actualizado} un.`,
              'Cerrar',
              { duration: 4000 }
            );
          },
          error: (err) => {
            const msg = err.error?.detail || 'Error al registrar movimiento';
            this.snackBar.open(`Error: ${msg}`, 'Cerrar', { duration: 4500 });
          }
        });
      }
    });
  }

  openKardexDialog(item: InventarioItem): void {
    this.dialog.open(KardexDialogComponent, {
      width: '850px',
      data: { item }
    });
  }
}
