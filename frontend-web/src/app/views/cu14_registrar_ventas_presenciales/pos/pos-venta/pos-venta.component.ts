import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule, FormsModule, Validators } from '@angular/forms';
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
import { MatCheckboxModule } from '@angular/material/checkbox';
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
    FormsModule,
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
    MatTooltipModule,
    MatCheckboxModule
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

  // QR Simulado
  qrConfirmadoManual = false;

  // Tarjeta Simulado
  tarjetaNumero = '4532 8920 1144 7820';
  tarjetaTitular = 'CONSUMIDOR FINAL';
  tarjetaVencimiento = '12/28';
  tarjetaCvv = '842';
  procesandoTarjeta = false;

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
      if (sucursales.length > 0) {
        const idToSet = this.sucursalControl.value || sucursales[0].id;
        this.sucursalControl.setValue(idToSet, { emitEvent: false });
        this.cargarInventarioSucursal(idToSet);
      }
    });

    // 2. Cargar Métodos de Pago (Filtrando estrictamente online / digital)
    this.ventaController.metodosPago$.pipe(takeUntil(this.destroy$)).subscribe(metodos => {
      this.metodosPago = metodos.filter(m => 
        !m.nombre.toLowerCase().includes('digital') && 
        !m.nombre.toLowerCase().includes('online')
      );
      if (this.metodosPago.length > 0 && !this.metodoPagoControl.value) {
        const efectivo = this.metodosPago.find(m => m.nombre.toLowerCase().includes('efectivo')) || this.metodosPago[0];
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

    // Resetear confirmaciones al cambiar método de pago
    this.metodoPagoControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.qrConfirmadoManual = false;
      });

    this.sucursalController.loadSucursales();
    this.ventaController.loadMetodosPago();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  // Getters de método de pago
  get metodoSeleccionado(): MetodoPago | undefined {
    return this.metodosPago.find(m => m.id === this.metodoPagoControl.value);
  }

  get esEfectivo(): boolean {
    return !!this.metodoSeleccionado?.nombre.toLowerCase().includes('efectivo');
  }

  get esQR(): boolean {
    const n = this.metodoSeleccionado?.nombre.toLowerCase() || '';
    return n.includes('qr') || n.includes('transferencia');
  }

  get esTarjeta(): boolean {
    const n = this.metodoSeleccionado?.nombre.toLowerCase() || '';
    return n.includes('tarjeta') || n.includes('crédito') || n.includes('débito') || n.includes('visa');
  }

  cargarInventarioSucursal(sucursalId: number): void {
    this.loading = true;
    this.inventarioService.getInventario(sucursalId).subscribe({
      next: (items) => {
        this.productosCatalogo = items.map(it => ({
          ...it,
          talla: it.talla || it.talla_nombre || 'Única',
          color: it.color || it.color_nombre || 'Estándar',
          imagen_url: it.imagen_url || ''
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
      const precioUnit = item.producto_precio ? Number(item.producto_precio) : 85.00;
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
    this.qrConfirmadoManual = false;
  }

  // --- Totales ---
  get subtotal(): number {
    return this.cart.reduce((acc, it) => acc + it.subtotal, 0);
  }

  get total(): number {
    return this.subtotal;
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
      this.snackBar.open('El ticket de venta está vacío', 'Cerrar', { duration: 3000 });
      return;
    }

    const sucursalId = this.sucursalControl.value;
    const metodoPagoId = this.metodoPagoControl.value;

    if (!sucursalId || !metodoPagoId) {
      this.snackBar.open('Seleccione una sucursal y un método de pago válidos', 'Cerrar', { duration: 3000 });
      return;
    }

    // Validación Efectivo
    if (this.esEfectivo) {
      const montoRecibido = Number(this.montoRecibidoControl.value || 0);
      if (montoRecibido < this.total) {
        this.snackBar.open(`El monto en efectivo (Bs. ${montoRecibido.toFixed(2)}) es menor al total a cobrar (Bs. ${this.total.toFixed(2)})`, 'Cerrar', { duration: 3500 });
        return;
      }
      this.ejecutarRegistroVenta(sucursalId, metodoPagoId, montoRecibido);
      return;
    }

    // Validación QR con confirmación manual del cajero
    if (this.esQR) {
      if (!this.qrConfirmadoManual) {
        this.snackBar.open('Debe marcar la casilla "Confirmar recepción de pago QR" una vez verificado el abono en cuenta.', 'Atención', { duration: 4000 });
        return;
      }
      this.ejecutarRegistroVenta(sucursalId, metodoPagoId, this.total);
      return;
    }

    // Simulación Cobro Tarjeta Visa
    if (this.esTarjeta) {
      if (!this.tarjetaNumero || this.tarjetaNumero.trim().length < 10) {
        this.snackBar.open('Por favor ingrese los datos de la tarjeta Visa para procesar.', 'Cerrar', { duration: 3000 });
        return;
      }

      this.procesandoTarjeta = true;
      this.procesandoVenta = true;
      setTimeout(() => {
        this.procesandoTarjeta = false;
        this.ejecutarRegistroVenta(sucursalId, metodoPagoId, this.total);
      }, 1500);
      return;
    }

    // Cualquier otro método
    this.ejecutarRegistroVenta(sucursalId, metodoPagoId, this.total);
  }

  private ejecutarRegistroVenta(sucursalId: number, metodoPagoId: number, montoRecibido: number): void {
    const dto: VentaPresencialCreateDTO = {
      sucursal_id: sucursalId,
      cliente_nombre: this.clienteNombreControl.value || 'Consumidor Final',
      metodo_pago_id: metodoPagoId,
      monto_recibido: montoRecibido,
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
            montoRecibido: this.esEfectivo ? montoRecibido : this.total,
            cambio: this.esEfectivo ? this.cambio : 0
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

