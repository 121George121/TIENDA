import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { Subject, Observable } from 'rxjs';
import { distinctUntilChanged, takeUntil } from 'rxjs/operators';

import { VentaCompleta } from '../../../../models/cu14_registrar_ventas_presenciales/venta.model';
import { VentaController } from '../../../../controllers/cu14_registrar_ventas_presenciales/venta.controller';
import { SucursalController } from '../../../../controllers/cu4_gestionar_sucursales/sucursal.controller';
import { Sucursal } from '../../../../models/cu4_gestionar_sucursales/sucursal.model';
import { VentaDetailDialogComponent } from '../venta-detail-dialog/venta-detail-dialog.component';

@Component({
  selector: 'app-ventas-list',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatSelectModule,
    MatCardModule,
    MatProgressBarModule,
    MatTooltipModule,
    MatDialogModule
  ],
  templateUrl: './ventas-list.component.html',
  styleUrls: ['./ventas-list.component.css']
})
export class VentasListComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['codigo', 'tipo', 'sucursal', 'cliente', 'metodo', 'fecha', 'total', 'acciones'];
  dataSource = new MatTableDataSource<VentaCompleta>([]);

  tipoFilterControl = new FormControl<string>('');
  sucursalFilterControl = new FormControl<number | null>(null);

  loading$!: Observable<boolean>;
  sucursales: Sucursal[] = [];
  private destroy$ = new Subject<void>();

  // KPIs
  totalVentas = 0;
  totalMontoFacturado = 0;
  ventasPresenciales = 0;
  ventasDigitales = 0;

  constructor(
    public ventaController: VentaController,
    public sucursalController: SucursalController,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loading$ = this.ventaController.loading$;

    this.ventaController.ventas$.pipe(takeUntil(this.destroy$)).subscribe(ventas => {
      this.dataSource.data = ventas;
      this.calculateKpis(ventas);
    });

    this.sucursalController.sucursales$.pipe(takeUntil(this.destroy$)).subscribe(sucursales => {
      this.sucursales = sucursales;
    });

    this.tipoFilterControl.valueChanges
      .pipe(distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.sucursalFilterControl.valueChanges
      .pipe(distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.sucursalController.loadSucursales();
    this.ventaController.loadVentas();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculateKpis(ventas: VentaCompleta[]): void {
    this.totalVentas = ventas.length;
    this.totalMontoFacturado = ventas.reduce((acc, v) => acc + Number(v.total || 0), 0);
    this.ventasPresenciales = ventas.filter(v => v.tipoventa?.toLowerCase().includes('presencial')).length;
    this.ventasDigitales = ventas.filter(v => v.tipoventa?.toLowerCase().includes('digital') || v.tipoventa?.toLowerCase().includes('online')).length;
  }

  applyFilters(): void {
    const tipo = this.tipoFilterControl.value || undefined;
    const sucursalId = this.sucursalFilterControl.value || undefined;
    this.ventaController.loadVentas(tipo, sucursalId);
  }

  resetFilters(): void {
    this.tipoFilterControl.setValue('');
    this.sucursalFilterControl.setValue(null);
    this.ventaController.loadVentas();
  }

  openDetalle(venta: VentaCompleta): void {
    this.dialog.open(VentaDetailDialogComponent, {
      width: '680px',
      data: { ventaId: venta.id }
    });
  }
}
