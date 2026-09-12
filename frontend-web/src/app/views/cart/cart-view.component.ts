// ==============================================================================
// CAPA VISTA / CONTROLADOR (MVC - VIEW & CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU09 - Gestionar Carrito de Compras
// Ubicación: frontend-web/src/app/views/cart/cart-view.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';

import { CartService } from '../../services/cart.service';
import { InventoryService } from '../../services/inventory.service';
import { Carrito, CarritoItem } from '../../models/cart.model';
import { SucursalItem } from '../../models/inventory.model';

@Component({
  selector: 'app-cart-view',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatTooltipModule
  ],
  templateUrl: './cart-view.component.html',
  styleUrls: ['./cart-view.component.css']
})
export class CartViewComponent implements OnInit {
  carrito: Carrito | null = null;
  sucursales: SucursalItem[] = [];
  loading = true;
  procesandoId: number | null = null;

  constructor(
    private cartService: CartService,
    private inventoryService: InventoryService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // 1. Cargar tiendas físicas
    this.inventoryService.getSucursales().subscribe({
      next: (s) => this.sucursales = s,
      error: (e) => console.error('Error al cargar sucursales:', e)
    });

    // 2. Suscribirse reactivamente al carrito
    this.cartService.cart$.subscribe({
      next: (c) => {
        this.carrito = c;
        this.loading = false;
      },
      error: (e) => {
        console.error('Error al cargar carrito:', e);
        this.loading = false;
      }
    });

    // Carga inicial
    this.cartService.cargarCarrito().subscribe();
  }

  incrementar(item: CarritoItem): void {
    if (item.cantidad >= item.stock_disponible) {
      alert(`No puedes agregar más unidades. Stock disponible en tienda: ${item.stock_disponible} uds.`);
      return;
    }
    this.procesandoId = item.variante_id;
    this.cartService.actualizarCantidad(item.variante_id, item.cantidad + 1).subscribe({
      next: () => this.procesandoId = null,
      error: (err) => {
        this.procesandoId = null;
        alert(err.error?.detail || 'Error al actualizar cantidad');
      }
    });
  }

  decrementar(item: CarritoItem): void {
    this.procesandoId = item.variante_id;
    if (item.cantidad <= 1) {
      this.eliminar(item);
      return;
    }

    this.cartService.actualizarCantidad(item.variante_id, item.cantidad - 1).subscribe({
      next: () => this.procesandoId = null,
      error: (err) => {
        this.procesandoId = null;
        alert(err.error?.detail || 'Error al decrementar cantidad');
      }
    });
  }

  eliminar(item: CarritoItem): void {
    if (confirm(`¿Quitar ${item.producto_nombre} (Talla: ${item.talla}) del carrito?`)) {
      this.procesandoId = item.variante_id;
      this.cartService.eliminarItem(item.variante_id).subscribe({
        next: () => this.procesandoId = null,
        error: (err) => {
          this.procesandoId = null;
          alert(err.error?.detail || 'Error al eliminar ítem');
        }
      });
    }
  }

  onCambioSucursal(event: any): void {
    const sucursalId = Number(event.target.value);
    if (!sucursalId) return;

    this.cartService.asignarSucursal(sucursalId).subscribe({
      next: () => {},
      error: (err) => alert(err.error?.detail || 'Error al cambiar sucursal')
    });
  }

  vaciar(): void {
    if (confirm('¿Estás seguro de que deseas vaciar todo el carrito?')) {
      this.cartService.vaciarCarrito().subscribe();
    }
  }

  procederAReserva(): void {
    if (!this.carrito || this.carrito.items.length === 0) return;

    if (!this.carrito.sucursal_id) {
      alert('Por favor selecciona la sucursal física donde retirarás tu pedido antes de continuar.');
      return;
    }

    if (this.carrito.tiene_alertas_stock) {
      alert('Hay prendas en tu carrito que superan el stock de la sucursal seleccionada. Por favor ajusta las cantidades.');
      return;
    }

    alert(`¡Excelente! Carrito validado para ${this.carrito.sucursal_nombre}.\nListo para generar la Reserva (CU10).`);
  }
}
