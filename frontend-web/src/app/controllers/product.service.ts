// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FRONTEND ANGULAR)
// Servicio Angular que gestiona las peticiones HTTP a la API y el estado
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { Producto } from '../models/product.model';
import { CartItem, OrdenRequest } from '../models/cart.model';

@Injectable({
  providedIn: 'root'
})
export class ProductControllerService {
  private apiUrl = 'http://localhost:8000/api/v1/productos';
  private orderUrl = 'http://localhost:8000/api/v1/ordenes';

  // Estado reactivo del Carrito de Compras
  private cartItemsSubject = new BehaviorSubject<CartItem[]>([]);
  public cartItems$ = this.cartItemsSubject.asObservable();

  constructor(private http: HttpClient) {}

  /** Obtiene la lista de productos desde la API (FastAPI) */
  getProductos(): Observable<Producto[]> {
    return this.http.get<Producto[]>(this.apiUrl);
  }

  /** Lógica del controlador para agregar productos al carrito */
  addToCart(producto: Producto): void {
    const currentItems = this.cartItemsSubject.value;
    const existingIndex = currentItems.findIndex(item => item.producto.id === producto.id);

    if (existingIndex > -1) {
      currentItems[existingIndex].cantidad += 1;
      currentItems[existingIndex].subtotal = currentItems[existingIndex].cantidad * producto.precio;
    } else {
      currentItems.push({
        producto,
        cantidad: 1,
        subtotal: producto.precio
      });
    }
    this.cartItemsSubject.next([...currentItems]);
  }

  /** Procesa el checkout enviando la orden a FastAPI */
  checkout(direccionEnvio: string): Observable<any> {
    const items = this.cartItemsSubject.value.map(item => ({
      producto_id: item.producto.id,
      cantidad: item.cantidad
    }));

    const payload: OrdenRequest = {
      direccion_envio: direccionEnvio,
      items: items
    };

    return this.http.post(this.orderUrl, payload);
  }

  clearCart(): void {
    this.cartItemsSubject.next([]);
  }
}
