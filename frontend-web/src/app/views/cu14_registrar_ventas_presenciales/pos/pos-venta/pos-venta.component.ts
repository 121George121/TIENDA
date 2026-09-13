import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatDividerModule } from '@angular/material/divider';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, takeUntil } from 'rxjs/operators';

import { InventarioItem } from '../../../../models/cu13_gestionar_inventario_movimientos/inventario.model';
import { MetodoPago, VentaPresencialCreateDTO } from '../../../../models/cu14_registrar_ventas_presenciales/venta.model';
import { Sucursal } from '../../../../models/cu4_gestionar_sucursales/sucursal.model';
import { InventarioService } from '../../../../services/cu13_gestionar_inventario_movimientos/inventario.service';
import { VentaController } from '../../../../controllers/cu14_registrar_ventas_presenciales/venta.controller';
import { SucursalController } from '../../../../controllers/cu4_gestionar_sucursales/sucursal.controller';
import { ReceiptDialogComponent } from '../receipt-dialog/receipt-dialog.component';

export interface PosCartItem {
  inventarioItem: InventarioItem;
  cantidad: number;
  precioUnitario: number;
  subtotal: number;
}

@Component({
  selector: 'app-pos-venta',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatSelectModule,
    MatDividerModule,
    MatSnackBarModule,
    MatProgressBarModule,
    MatDialogModule,
    MatTooltipModule
  ],
  templateUrl: './pos-venta.component.html',
  styleUrls: ['./pos-venta.component.css']
})
export class PosVentaComponent implements OnInit, OnDestroy {
  sucursales: Sucursal[] = [];
  metodosPago: MetodoPago[] = [];
  productosCatalogo: InventarioItem[] = [];
  productosFiltrados: InventarioItem[] = [];

  // Form Controls
  sucursalControl = new FormControl<number | null>(null, [Validators.required]);
  searchControl = new FormControl('');
  clienteNombreControl = new FormControl('Consumidor Final', [Validators.required]);
  metodoPagoControl = new FormControl<number | null>(null, [Validators.required]);
  montoRecibidoControl = new FormControl<number | null>(null);

  // Cart
  cart: PosCartItem[] = [];
  loading = false;
  procesandoVenta = false;
  private destroy$ = new Subject<void>();

  constructor(
    private inventarioService: InventarioService,
    public ventaController: VentaController,
    public sucursalController: SucursalController,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    // 1. Cargar Sucursales
    this.sucursalController.sucursales$.pipe(takeUntil(this.destroy$)).subscribe(sucursales => {
      this.sucursales = sucursales;
      if (sucursales.length > 0 && !this.sucursalControl.value) {
        this.sucursalControl.setValue(sucursales[0].id);
      }
    });

    // 2. Cargar Métodos de Pago
    this.ventaController.metodosPago$.pipe(takeUntil(this.destroy$)).subscribe(metodos => {
      this.metodosPago = metodos;
      if (metodos.length > 0 && !this.metodoPagoControl.value) {
        const efectivo = metodos.find(m => m.nombre.toLowerCase().includes('efectivo')) || metodos[0];
        this.metodoPagoControl.setValue(efectivo.id);
      }
    });

    // 3. Reactividad al cambiar de sucursal
    this.sucursalControl.valueChanges
      .pipe(distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(sucursalId => {
        if (sucursalId) {
          this.cargarInventarioSucursal(sucursalId);
          this.cart = []; // Vaciar carrito si cambia de tienda
        }
      });

    // 4. Búsqueda de productos
    this.searchControl.valueChanges
      .pipe(debounceTime(250), distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(term => {
        this.filtrarProductos(term || '');
      });

    this.sucursalController.loadSucursales();
    this.ventaController.loadMetodosPago();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  cargarInventarioSucursal(sucursalId: number): void {
    this.loading = true;
    this.inventarioService.getInventario(sucursalId).subscribe({
      next: (items) => {
        this.productosCatalogo = items.map(it => ({
          ...it,
          talla: it.talla || it.talla_nombre || 'Única',
          color: it.color || it.color_nombre || 'Estándar'
        }));
        this.filtrarProductos(this.searchControl.value || '');
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar catálogo de sucursal:', err);
        this.loading = false;
      }
    });
  }

  filtrarProductos(term: string): void {
    const q = term.toLowerCase().trim();
    if (!q) {
      this.productosFiltrados = [...this.productosCatalogo];
    } else {
      this.productosFiltrados = this.productosCatalogo.filter(p =>
        p.producto_nombre.toLowerCase().includes(q) ||
        (p.color ? p.color.toLowerCase().includes(q) : false) ||
        (p.talla ? p.talla.toLowerCase().includes(q) : false)
      );
    }
  }

  // --- Operaciones de Carrito ---
  addToCart(item: InventarioItem): void {
    if (item.stockfisico <= 0) {
      this.snackBar.open(`¡Sin stock físico de ${item.producto_nombre}!`, 'Cerrar', { duration: 2500 });
      return;
    }

    const existing = this.cart.find(c => c.inventarioItem.id === item.id);
    if (existing) {
      if (existing.cantidad + 1 > item.stockfisico) {
        this.snackBar.open(`Stock máximo disponible en sucursal alcanzado (${item.stockfisico} un.)`, 'Cerrar', { duration: 2500 });
        return;
      }
      existing.cantidad += 1;
      existing.subtotal = existing.cantidad * existing.precioUnitario;
    } else {
      // Precio base estimado o predeterminado para boutique t-shirts si no viene en inventario
      const precioUnit = 85.00;
      this.cart.push({
        inventarioItem: item,
        cantidad: 1,
        precioUnitario: precioUnit,
        subtotal: precioUnit
      });
    }

    this.snackBar.open(`Agregado al carrito: ${item.producto_nombre} (${item.talla})`, 'OK', { duration: 1500 });
  }

  incrementQty(cartItem: PosCartItem): void {
    if (cartItem.cantidad + 1 > cartItem.inventarioItem.stockfisico) {
      this.snackBar.open(`Stock disponible: ${cartItem.inventarioItem.stockfisico}`, 'OK', { duration: 2000 });
      return;
    }
    cartItem.cantidad += 1;
    cartItem.subtotal = cartItem.cantidad * cartItem.precioUnitario;
  }

  decrementQty(cartItem: PosCartItem): void {
    if (cartItem.cantidad > 1) {
      cartItem.cantidad -= 1;
      cartItem.subtotal = cartItem.cantidad * cartItem.precioUnitario;
    } else {
      this.removeItem(cartItem);
    }
  }

  removeItem(cartItem: PosCartItem): void {
    this.cart = this.cart.filter(c => c !== cartItem);
  }

  clearCart(): void {
    this.cart = [];
    this.montoRecibidoControl.setValue(null);
  }

  // --- Totales ---
  get subtotal(): number {
    return this.cart.reduce((acc, it) => acc + it.subtotal, 0);
  }

  get total(): number {
    return this.subtotal; // Descuentos se pueden aplicar aquí
  }

  get cambio(): number {
    const recibido = Number(this.montoRecibidoControl.value || 0);
    if (recibido >= this.total && this.total > 0) {
      return recibido - this.total;
    }
    return 0;
  }

  setMontoRapido(monto: number): void {
    this.montoRecibidoControl.setValue(monto);
  }

  // --- Cobro / Checkout POS ---
  procesarCobro(): void {
    if (this.cart.length === 0) {
      this.snackBar.open('El carrito de venta está vacío', 'Cerrar', { duration: 3000 });
      return;
    }

    const sucursalId = this.sucursalControl.value;
    const metodoPagoId = this.metodoPagoControl.value;

    if (!sucursalId || !metodoPagoId) {
      this.snackBar.open('Seleccione una sucursal y un método de pago válidos', 'Cerrar', { duration: 3000 });
      return;
    }

    const montoRecibido = Number(this.montoRecibidoControl.value || 0);
    const metodoSeleccionado = this.metodosPago.find(m => m.id === metodoPagoId);
    const esEfectivo = metodoSeleccionado?.nombre.toLowerCase().includes('efectivo');

    if (esEfectivo && montoRecibido < this.total) {
      this.snackBar.open(`El monto en efectivo ingresado (Bs. ${montoRecibido}) es menor al total a pagar (Bs. ${this.total})`, 'Cerrar', { duration: 3500 });
      return;
    }

    const dto: VentaPresencialCreateDTO = {
      sucursal_id: sucursalId,
      cliente_nombre: this.clienteNombreControl.value || 'Consumidor Final',
      metodo_pago_id: metodoPagoId,
      monto_recibido: esEfectivo ? montoRecibido : this.total,
      items: this.cart.map(c => ({
        producto_id: c.inventarioItem.producto_id,
        cantidad: c.cantidad,
        variante_id: c.inventarioItem.variante_id
      }))
    };

    this.procesandoVenta = true;
    this.ventaController.registrarVentaPresencial(dto).subscribe({
      next: (ventaCreada) => {
        this.procesandoVenta = false;
        
        // Abrir diálogo de comprobante / ticket
        this.dialog.open(ReceiptDialogComponent, {
          width: '520px',
          data: {
            venta: ventaCreada,
            items: this.cart.map(c => ({
              nombre: c.inventarioItem.producto_nombre,
              variante: `Talla: ${c.inventarioItem.talla} | Color: ${c.inventarioItem.color}`,
              cantidad: c.cantidad,
              precio: c.precioUnitario,
              subtotal: c.subtotal
            })),
            montoRecibido: esEfectivo ? montoRecibido : undefined,
            cambio: esEfectivo ? this.cambio : undefined
          }
        });

        // Limpiar carrito y recargar inventario local de la sucursal
        this.clearCart();
        this.cargarInventarioSucursal(sucursalId);
        this.snackBar.open('¡Venta presencial registrada y stock descontado exitosamente!', 'Excelente', { duration: 4000 });
      },
      error: (err) => {
        this.procesandoVenta = false;
        const msg = err.error?.detail || 'Error al procesar la venta en caja';
        this.snackBar.open(`Error: ${msg}`, 'Cerrar', { duration: 5000 });
      }
    });
  }
}
