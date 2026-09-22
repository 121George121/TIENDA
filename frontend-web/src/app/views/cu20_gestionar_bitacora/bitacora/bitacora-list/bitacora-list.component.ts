// ==============================================================================
// CU20 - GESTIONAR BITACORA Y AUDITORIA -> COMPONENTE VISTA (FRONTEND)
// Ubicacion: frontend-web/src/app/views/cu20_gestionar_bitacora/bitacora/bitacora-list/bitacora-list.component.ts
// ==============================================================================

import { Component, OnInit, OnDestroy, TemplateRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormControl } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatCardModule } from '@angular/material/card';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Subject, Observable } from 'rxjs';
import { debounceTime, takeUntil } from 'rxjs/operators';

import { BitacoraEntry, BitacoraStats, BitacoraFilter } from '../../../../models/cu20_gestionar_bitacora/bitacora.model';
import { BitacoraController } from '../../../../controllers/cu20_gestionar_bitacora/bitacora.controller';

@Component({
  selector: 'app-bitacora-list',
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
    MatChipsModule,
    MatDialogModule,
    MatSnackBarModule,
    MatProgressBarModule,
    MatCardModule,
    MatTooltipModule
  ],
  templateUrl: './bitacora-list.component.html',
  styleUrls: ['./bitacora-list.component.css']
})
export class BitacoraListComponent implements OnInit, OnDestroy {
  @ViewChild('detailDialog') detailDialogRef!: TemplateRef<any>;

  displayedColumns: string[] = ['id', 'fechahora', 'usuario', 'modulo', 'accion', 'detalle', 'ip', 'acciones'];
  dataSource = new MatTableDataSource<BitacoraEntry>([]);

  // Estados reactivos
  loading$: Observable<boolean>;
  exporting$: Observable<boolean>;
  stats$: Observable<BitacoraStats | null>;
  total$: Observable<number>;

  // Filtros
  searchControl = new FormControl('');
  selectedModulo = 'TODOS';
  selectedAccion = 'TODAS';
  fechaDesde = '';
  fechaHasta = '';

  // Paginación
  pageSize = 25;
  pageIndex = 0;
  totalRecords = 0;

  // Registro seleccionado para modal
  selectedItem: BitacoraEntry | null = null;

  // Catálogos para filtros
  modulos: string[] = [
    'TODOS',
    'AUTENTICACION',
    'USUARIOS',
    'ROLES',
    'PRODUCTOS',
    'CLASIFICACION',
    'SUCURSALES',
    'PROVEEDORES',
    'INVENTARIO',
    'VENTAS',
    'RESERVAS',
    'BITACORA'
  ];

  acciones: string[] = [
    'TODAS',
    'LOGIN',
    'LOGOUT',
    'LOGIN_FALLIDO',
    'CREAR',
    'MODIFICAR',
    'ELIMINAR',
    'CAMBIO_ESTADO',
    'CAMBIO_ROL',
    'VENTA_POS',
    'RESERVA_ATENDIDA',
    'EXPORTAR',
    'INSPECCION_SISTEMA'
  ];

  private destroy$ = new Subject<void>();

  constructor(
    private bitacoraCtrl: BitacoraController,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {
    this.loading$ = this.bitacoraCtrl.loading$;
    this.exporting$ = this.bitacoraCtrl.exporting$;
    this.stats$ = this.bitacoraCtrl.stats$;
    this.total$ = this.bitacoraCtrl.total$;
  }

  ngOnInit(): void {
    // Escuchar cambios de registros
    this.bitacoraCtrl.logs$.pipe(takeUntil(this.destroy$)).subscribe((logs) => {
      this.dataSource.data = logs;
    });

    this.bitacoraCtrl.total$.pipe(takeUntil(this.destroy$)).subscribe((total) => {
      this.totalRecords = total;
    });

    // Escuchar errores
    this.bitacoraCtrl.error$.pipe(takeUntil(this.destroy$)).subscribe((err) => {
      if (err) {
        this.snackBar.open(err, 'Cerrar', { duration: 4000, panelClass: ['error-snackbar'] });
      }
    });

    // Búsqueda en vivo con debounce
    this.searchControl.valueChanges
      .pipe(debounceTime(400), takeUntil(this.destroy$))
      .subscribe(() => {
        this.pageIndex = 0;
        this.aplicarFiltros();
      });

    // Carga inicial
    this.aplicarFiltros();
    this.bitacoraCtrl.loadStats();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  aplicarFiltros(): void {
    const filter: BitacoraFilter = {
      limit: this.pageSize,
      offset: this.pageIndex * this.pageSize,
      modulo: this.selectedModulo,
      accion: this.selectedAccion,
      search: this.searchControl.value || undefined,
      fecha_inicio: this.fechaDesde ? `${this.fechaDesde}T00:00:00` : undefined,
      fecha_fin: this.fechaHasta ? `${this.fechaHasta}T23:59:59` : undefined
    };

    this.bitacoraCtrl.loadLogs(filter);
  }

  onPageChange(event: PageEvent): void {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    this.aplicarFiltros();
  }

  limpiarFiltros(): void {
    this.searchControl.setValue('');
    this.selectedModulo = 'TODOS';
    this.selectedAccion = 'TODAS';
    this.fechaDesde = '';
    this.fechaHasta = '';
    this.pageIndex = 0;
    this.aplicarFiltros();
  }

  exportarCSV(): void {
    const filter: BitacoraFilter = {
      modulo: this.selectedModulo,
      accion: this.selectedAccion,
      search: this.searchControl.value || undefined,
      fecha_inicio: this.fechaDesde ? `${this.fechaDesde}T00:00:00` : undefined,
      fecha_fin: this.fechaHasta ? `${this.fechaHasta}T23:59:59` : undefined
    };
    this.bitacoraCtrl.exportCsv(filter);
  }

  verDetalle(item: BitacoraEntry): void {
    this.selectedItem = item;
    this.dialog.open(this.detailDialogRef, {
      width: '720px',
      maxHeight: '85vh',
      panelClass: 'bitacora-dialog-container'
    });
  }

  formatJson(val?: string): string {
    if (!val) return 'Ninguno';
    try {
      const parsed = JSON.parse(val);
      return JSON.stringify(parsed, null, 2);
    } catch {
      return val;
    }
  }

  getBadgeClass(accion: string): string {
    const act = (accion || '').toUpperCase();
    if (act.includes('LOGIN') && !act.includes('FALLIDO')) return 'badge-login';
    if (act.includes('FALLIDO') || act.includes('ELIMINAR')) return 'badge-danger';
    if (act.includes('CREAR')) return 'badge-create';
    if (act.includes('MODIFICAR') || act.includes('CAMBIO')) return 'badge-modify';
    if (act.includes('VENTA') || act.includes('RESERVA')) return 'badge-commerce';
    return 'badge-default';
  }

  getModuloBadgeClass(modulo: string): string {
    const mod = (modulo || '').toUpperCase();
    switch (mod) {
      case 'AUTENTICACION': return 'mod-auth';
      case 'USUARIOS':
      case 'ROLES': return 'mod-users';
      case 'PRODUCTOS':
      case 'CLASIFICACION': return 'mod-products';
      case 'VENTAS': return 'mod-sales';
      case 'INVENTARIO': return 'mod-inv';
      case 'RESERVAS': return 'mod-res';
      default: return 'mod-default';
    }
  }
}
