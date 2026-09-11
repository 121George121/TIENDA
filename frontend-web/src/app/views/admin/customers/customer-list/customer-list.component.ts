import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

import { Subject, Observable } from 'rxjs';
import { debounceTime, distinctUntilChanged, takeUntil } from 'rxjs/operators';

import { Cliente } from '../../../../models/customer.model';
import { CustomerController } from '../../../../controllers/customer.controller';
import { CustomerFormDialogComponent } from '../customer-form-dialog/customer-form-dialog.component';
import { CustomerDetailDialogComponent } from '../customer-detail-dialog/customer-detail-dialog.component';
import { ConfirmDialogComponent } from '../../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-customer-list',
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
    MatChipsModule,
    MatCardModule,
    MatSlideToggleModule,
    MatSnackBarModule,
    MatProgressBarModule,
    MatTooltipModule,
    MatPaginatorModule,
    MatDialogModule
  ],
  templateUrl: './customer-list.component.html',
  styleUrls: ['./customer-list.component.css']
})
export class CustomerListComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['id', 'cliente', 'email', 'telefono', 'activo', 'fechacreacion', 'acciones'];
  dataSource = new MatTableDataSource<Cliente>([]);

  searchControl = new FormControl('');
  estadoFilterControl = new FormControl<boolean | null>(null);

  loading$!: Observable<boolean>;
  private destroy$ = new Subject<void>();

  // KPIs
  totalClientes = 0;
  clientesActivos = 0;
  clientesInactivos = 0;

  constructor(
    public customerController: CustomerController,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loading$ = this.customerController.loading$;

    this.customerController.customers$.pipe(takeUntil(this.destroy$)).subscribe(clientes => {
      this.dataSource.data = clientes;
      this.calculateKpis(clientes);
    });

    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.estadoFilterControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.applyFilters());

    this.customerController.loadClientes();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculateKpis(clientes: Cliente[]): void {
    this.totalClientes = clientes.length;
    this.clientesActivos = clientes.filter(c => c.activo).length;
    this.clientesInactivos = clientes.filter(c => !c.activo).length;
  }

  applyFilters(): void {
    const search = this.searchControl.value || undefined;
    const estado = this.estadoFilterControl.value !== null ? this.estadoFilterControl.value : undefined;
    this.customerController.loadClientes(search, estado);
  }

  resetFilters(): void {
    this.searchControl.setValue('');
    this.estadoFilterControl.setValue(null);
    this.customerController.loadClientes();
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(CustomerFormDialogComponent, {
      width: '520px',
      data: { isEdit: false }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.customerController.createCliente(result).subscribe({
          next: () => {
            this.snackBar.open('Cliente registrado exitosamente', 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

  openEditDialog(cliente: Cliente): void {
    const dialogRef = this.dialog.open(CustomerFormDialogComponent, {
      width: '520px',
      data: { cliente, isEdit: true }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.customerController.updateCliente(cliente.id, result).subscribe({
          next: () => {
            this.snackBar.open('Cliente actualizado correctamente', 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }

  openViewDialog(cliente: Cliente): void {
    this.dialog.open(CustomerDetailDialogComponent, {
      width: '640px',
      data: { cliente }
    });
  }

  onToggleStatus(cliente: Cliente): void {
    this.customerController.toggleStatus(cliente.id, cliente.activo).subscribe({
      next: () => {
        const action = !cliente.activo ? 'activado' : 'desactivado (baja lógica)';
        this.snackBar.open(`Cliente ${cliente.nombre} ${action} correctamente`, 'Cerrar', { duration: 3000 });
      },
      error: (err) => {
        this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
      }
    });
  }

  onDeleteCliente(cliente: Cliente): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '420px',
      data: {
        title: '¿Dar de Baja al Cliente?',
        message: `¿Estás seguro de desactivar al cliente "${cliente.nombre}" del sistema retail?`,
        confirmText: 'Dar de Baja',
        cancelText: 'Cancelar',
        color: 'warn',
        icon: 'person_off'
      }
    });

    dialogRef.afterClosed().subscribe(confirmed => {
      if (confirmed) {
        this.customerController.deleteCliente(cliente.id).subscribe({
          next: () => {
            this.snackBar.open(`Cliente ${cliente.nombre} fue dado de baja correctamente`, 'Cerrar', { duration: 3000 });
          },
          error: (err) => {
            this.snackBar.open(`Error: ${err}`, 'Cerrar', { duration: 4000 });
          }
        });
      }
    });
  }
}
