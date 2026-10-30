// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU09 - Gestionar Carrito de Compras
// Ubicación: frontend-web/src/app/controllers/cu9_gestionar_carrito_compras/cart.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Carrito } from '../../models/cu9_gestionar_carrito_compras/carrito.model';
import { CartService } from '../../services/cu9_gestionar_carrito_compras/cart.service';

@Injectable({
  providedIn: 'root'
})
export class CartController {
  // Observables canónicos en español
  public carrito$: Observable<Carrito | null> = this.cartService.carrito$;
  public totalItems$: Observable<number> = this.cartService.totalItems$;
  public totalPrecio$: Observable<number> = this.cartService.totalPrecio$;

  // Aliases retrocompatibles
  public cart$: Observable<Carrito | null> = this.carrito$;
  public cartCount$: Observable<number> = this.totalItems$;
  public cartTotal$: Observable<number> = this.totalPrecio$;

  constructor(private cartService: CartService) {}

  obtenerCarrito(): Observable<Carrito> {
    return this.cartService.obtenerCarrito();
  }

  cargarCarrito(): Observable<Carrito> {
    return this.obtenerCarrito();
  }

  agregarItem(varianteId: number, cantidad: number = 1, sucursalId?: number | null): Observable<Carrito> {
    return this.cartService.agregarItem(varianteId, cantidad, sucursalId);
  }

  actualizarCantidad(varianteId: number, cantidad: number): Observable<Carrito> {
    return this.cartService.actualizarCantidad(varianteId, cantidad);
  }

  eliminarItem(varianteId: number): Observable<Carrito> {
    return this.cartService.eliminarItem(varianteId);
  }

  asignarSucursal(sucursalId: number): Observable<Carrito> {
    return this.cartService.asignarSucursal(sucursalId);
  }

  vaciarCarrito(): Observable<Carrito> {
    return this.cartService.vaciarCarrito();
  }
}
