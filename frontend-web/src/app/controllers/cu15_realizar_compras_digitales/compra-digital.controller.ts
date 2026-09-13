import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap, finalize } from 'rxjs';
import { CompraDigitalService, OrdenCreateDTO, OrdenResponseDTO } from '../../services/cu15_realizar_compras_digitales/compra-digital.service';

export interface CartWebItem {
  producto: any;
  cantidad: number;
  tallaSeleccionada?: string;
  colorSeleccionado?: string;
  precioUnitario: number;
  subtotal: number;
}

@Injectable({
  providedIn: 'root'
})
export class CompraDigitalController {
  private cartSubject = new BehaviorSubject<CartWebItem[]>([]);
  public cart$: Observable<CartWebItem[]> = this.cartSubject.asObservable();

  private misOrdenesSubject = new BehaviorSubject<OrdenResponseDTO[]>([]);
  public misOrdenes$: Observable<OrdenResponseDTO[]> = this.misOrdenesSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private service: CompraDigitalService) {}

  public get cart(): CartWebItem[] {
    return this.cartSubject.value;
  }

  public get totalItems(): number {
    return this.cart.reduce((sum, item) => sum + item.cantidad, 0);
  }

  public get subtotal(): number {
    return this.cart.reduce((sum, item) => sum + item.subtotal, 0);
  }

  addToCart(producto: any, cantidad: number = 1, talla: string = 'M', color: string = 'Negro'): void {
    const current = this.cartSubject.value;
    const existingIndex = current.findIndex(
      i => i.producto.id === producto.id && i.tallaSeleccionada === talla && i.colorSeleccionado === color
    );

    const precio = Number(producto.preciobase || producto.precio || 85.00);

    if (existingIndex !== -1) {
      const updated = [...current];
      updated[existingIndex].cantidad += cantidad;
      updated[existingIndex].subtotal = updated[existingIndex].cantidad * precio;
      this.cartSubject.next(updated);
    } else {
      this.cartSubject.next([
        ...current,
        {
          producto,
          cantidad,
          tallaSeleccionada: talla,
          colorSeleccionado: color,
          precioUnitario: precio,
          subtotal: precio * cantidad
        }
      ]);
    }
  }

  updateQuantity(item: CartWebItem, delta: number): void {
    const current = this.cartSubject.value;
    const index = current.indexOf(item);
    if (index === -1) return;

    const newQty = item.cantidad + delta;
    if (newQty <= 0) {
      this.removeFromCart(item);
    } else {
      const updated = [...current];
      updated[index].cantidad = newQty;
      updated[index].subtotal = newQty * item.precioUnitario;
      this.cartSubject.next(updated);
    }
  }

  removeFromCart(item: CartWebItem): void {
    const filtered = this.cartSubject.value.filter(i => i !== item);
    this.cartSubject.next(filtered);
  }

  clearCart(): void {
    this.cartSubject.next([]);
  }

  procesarOrden(direccionEnvio: string, sucursalId?: number): Observable<OrdenResponseDTO> {
    this.loadingSubject.next(true);

    const dto: OrdenCreateDTO = {
      direccion_envio: direccionEnvio,
      sucursal_id: sucursalId,
      items: this.cart.map(c => ({
        producto_id: c.producto.id,
        cantidad: c.cantidad
      }))
    };

    return this.service.crearOrdenDigital(dto).pipe(
      tap((nuevaOrden) => {
        this.clearCart();
        const currentOrders = this.misOrdenesSubject.value;
        this.misOrdenesSubject.next([nuevaOrden, ...currentOrders]);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  loadMisOrdenes(): void {
    this.loadingSubject.next(true);
    this.service.getMisOrdenes()
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (ordenes) => this.misOrdenesSubject.next(ordenes),
        error: (err) => console.error('Error al cargar pedidos del cliente:', err)
      });
  }
}
