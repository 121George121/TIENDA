// ==============================================================================
// CAPA VISTA / CONTROLADOR (MVC - VIEW & CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
// Ubicación: frontend-web/src/app/views/product-catalog/product-catalog.component.ts
// ==============================================================================

import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Subject, Subscription } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

import { InventoryService } from '../../../services/cu8_consultar_catalogo_disponibilidad/inventory.service';
import { CartService } from '../../../services/cu9_gestionar_carrito_compras/cart.service';
import { AuthService } from '../../../core/services/auth.service';
import {
  ProductoCatalogoItem,
  SucursalItem,
  DisponibilidadProducto,
  DisponibilidadVariante
} from '../../../models/cu8_consultar_catalogo_disponibilidad/inventory.model';

@Component({
  selector: 'app-product-catalog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatChipsModule,
    MatTooltipModule
  ],
  templateUrl: './product-catalog.component.html',
  styleUrls: ['./product-catalog.component.css']
})
export class ProductCatalogComponent implements OnInit, OnDestroy {
  // Datos principales
  productos: ProductoCatalogoItem[] = [];
  sucursales: SucursalItem[] = [];
  loading = true;

  // Filtros interactivos y búsqueda reactiva
  sucursalSeleccionadaId: number | null = null;
  generoSeleccionado: string = 'TODOS';
  searchTerm: string = '';
  soloDisponibles: boolean = false;
  private searchSubject = new Subject<string>();
  private searchSub?: Subscription;

  // Mapa de variante seleccionada por producto (id_producto -> variante)
  variantesSeleccionadas: { [productoId: number]: DisponibilidadVariante } = {};

  // Estado del Modal de Disponibilidad Multitienda
  modalDisponibilidadAbierto = false;
  productoDisponibilidad: DisponibilidadProducto | null = null;
  cargandoDisponibilidad = false;

  // Carrito local rápido (contador para el header)
  itemsCarritoCount = 0;
  isAdmin = false;

  constructor(
    private inventoryService: InventoryService,
    private cartService: CartService,
    public authService: AuthService
  ) {}

  ngOnInit(): void {
    this.isAdmin = this.authService.isAdmin();
    this.cargarSucursales();
    this.cargarCatalogo();

    // Sincronizar contador del carrito
    this.cartService.cartCount$.subscribe(count => {
      this.itemsCarritoCount = count;
    });

    // Búsqueda con debounce reactivo de 300ms
    this.searchSub = this.searchSubject.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(term => {
      this.searchTerm = term;
      this.cargarCatalogo();
    });
  }

  ngOnDestroy(): void {
    this.searchSub?.unsubscribe();
  }

  cargarSucursales(): void {
    this.inventoryService.getSucursales().subscribe({
      next: (data) => {
        this.sucursales = data;
        // Por defecto pre-seleccionar la primera sucursal si existe
        if (data && data.length > 0) {
          this.sucursalSeleccionadaId = data[0].id;
          this.cargarCatalogo();
        }
      },
      error: (err) => console.error('Error al cargar sucursales:', err)
    });
  }

  cargarCatalogo(): void {
    this.loading = true;
    this.inventoryService.getCatalogo(
      this.sucursalSeleccionadaId,
      null,
      this.generoSeleccionado,
      this.searchTerm,
      this.soloDisponibles
    ).subscribe({
      next: (data) => {
        this.productos = data;
        // Auto-seleccionar la primera variante con stock para cada producto
        this.productos.forEach(p => {
          if (p.variantes && p.variantes.length > 0) {
            const conStock = p.variantes.find(v => v.stock > 0);
            this.variantesSeleccionadas[p.id] = conStock || p.variantes[0];
          }
        });
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al consultar catálogo:', err);
        this.loading = false;
      }
    });
  }

  onCambioSucursal(): void {
    this.cargarCatalogo();
  }

  onFiltroGenero(genero: string): void {
    this.generoSeleccionado = genero;
    this.cargarCatalogo();
  }

  onBusqueda(): void {
    this.searchSubject.next(this.searchTerm);
  }

  toggleSoloDisponibles(): void {
    this.soloDisponibles = !this.soloDisponibles;
    this.cargarCatalogo();
  }

  seleccionarVariante(productoId: number, variante: DisponibilidadVariante): void {
    this.variantesSeleccionadas[productoId] = variante;
  }

  getVarianteSeleccionada(productoId: number): DisponibilidadVariante | null {
    return this.variantesSeleccionadas[productoId] || null;
  }

  getNombreSucursalActual(): string {
    if (!this.sucursalSeleccionadaId) return 'Todas las sucursales';
    const suc = this.sucursales.find(s => s.id === this.sucursalSeleccionadaId);
    return suc ? suc.nombre : 'Sucursal seleccionada';
  }

  // --- CU08: Modal de Disponibilidad Multitienda ---
  abrirModalDisponibilidad(productoId: number): void {
    this.cargandoDisponibilidad = true;
    this.modalDisponibilidadAbierto = true;
    this.productoDisponibilidad = null;

    this.inventoryService.getDisponibilidadProducto(productoId).subscribe({
      next: (data) => {
        this.productoDisponibilidad = data;
        this.cargandoDisponibilidad = false;
      },
      error: (err) => {
        console.error('Error al consultar disponibilidad:', err);
        this.cargandoDisponibilidad = false;
      }
    });
  }

  cerrarModalDisponibilidad(): void {
    this.modalDisponibilidadAbierto = false;
    this.productoDisponibilidad = null;
  }

  agregarAlCarrito(producto: ProductoCatalogoItem): void {
    const variante = this.getVarianteSeleccionada(producto.id);
    if (!variante || variante.stock <= 0) return;

    this.cartService.agregarItem(variante.variante_id, 1, this.sucursalSeleccionadaId).subscribe({
      next: () => {
        // Feedback visual inmediato
        alert(`¡Añadido al carrito con éxito!\n${producto.nombre}\nTalla: ${variante.talla} | Color: ${variante.color}`);
      },
      error: (err) => {
        alert(err.error?.detail || 'Error al agregar al carrito');
      }
    });
  }
}
