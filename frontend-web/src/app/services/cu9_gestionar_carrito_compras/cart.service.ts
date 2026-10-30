// ==============================================================================
// CAPA SERVICIO (MVC - SERVICE EN FRONTEND ANGULAR)
// Módulo: CU09 - Gestionar Carrito de Compras
// Ubicación: frontend-web/src/app/services/cu9_gestionar_carrito_compras/cart.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap, map } from 'rxjs';
import { Carrito, AgregarItemCarritoDTO } from '../../models/cu9_gestionar_carrito_compras/carrito.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private apiUrl = `${environment.apiUrl}/carrito`;

  // Estado reactivo del Carrito
  private cartSubject = new BehaviorSubject<Carrito | null>(null);
  public cart$ = this.cartSubject.asObservable();
  public carrito$ = this.cart$; // Alias canónico en español

  // Observables derivados para la UI
  public cartCount$ = this.cart$.pipe(map(c => c ? c.total_items : 0));
  public totalItems$ = this.cartCount$; // Alias canónico en español

  public cartTotal$ = this.cart$.pipe(map(c => c ? c.total_precio : 0));
  public totalPrecio$ = this.cartTotal$; // Alias canónico en español

  constructor(private http: HttpClient) {
    this.obtenerCarrito().subscribe({
      error: (err: any) => console.warn('[CU09 SERVICE] Inicialización de carrito silenciosa:', err)
    });
  }

  /** Consulta el carrito activo desde la API de FastAPI */
  obtenerCarrito(): Observable<Carrito> {
    return this.http.get<Carrito>(this.apiUrl).pipe(
      tap(carrito => this.cartSubject.next(carrito))
    );
  }

  /** Alias retrocompatible para obtenerCarrito */
  cargarCarrito(): Observable<Carrito> {
    return this.obtenerCarrito();
  }

  /** Agrega una prenda o variante al carrito */
  agregarItem(varianteId: number, cantidad: number = 1, sucursalId?: number | null): Observable<Carrito> {
    const payload: AgregarItemCarritoDTO = {
      variante_id: varianteId,
      cantidad: cantidad,
      sucursal_id: sucursalId
    };

    return this.http.post<Carrito>(`${this.apiUrl}/items`, payload).pipe(
      tap(carrito => this.cartSubject.next(carrito))
    );
  }

  /** Modifica la cantidad solicitada de una prenda */
  actualizarCantidad(varianteId: number, cantidad: number): Observable<Carrito> {
    return this.http.put<Carrito>(`${this.apiUrl}/items/${varianteId}`, { cantidad }).pipe(
      tap(carrito => this.cartSubject.next(carrito))
    );
  }

  /** Elimina una prenda del carrito */
  eliminarItem(varianteId: number): Observable<Carrito> {
    return this.http.delete<Carrito>(`${this.apiUrl}/items/${varianteId}`).pipe(
      tap(carrito => this.cartSubject.next(carrito))
    );
  }

  /** Asigna la tienda física de retiro o compra */
  asignarSucursal(sucursalId: number): Observable<Carrito> {
    return this.http.patch<Carrito>(`${this.apiUrl}/sucursal`, { sucursal_id: sucursalId }).pipe(
      tap(carrito => this.cartSubject.next(carrito))
    );
  }

  /** Vacía todos los ítems del carrito */
  vaciarCarrito(): Observable<Carrito> {
    return this.http.delete<Carrito>(this.apiUrl).pipe(
      tap(carrito => this.cartSubject.next(carrito))
    );
  }
}
