// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FRONTEND ANGULAR)
// Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
// Ubicación: frontend-web/src/app/controllers/cu8_consultar_catalogo_disponibilidad/inventory.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize } from 'rxjs';
import {
  ProductoCatalogoItem,
  SucursalItem,
  DisponibilidadProducto
} from '../../models/cu8_consultar_catalogo_disponibilidad/catalogo.model';
import { InventoryService } from '../../services/cu8_consultar_catalogo_disponibilidad/inventory.service';

@Injectable({
  providedIn: 'root'
})
export class InventoryController {
  // Observables reactivos de estado
  private productosSubject = new BehaviorSubject<ProductoCatalogoItem[]>([]);
  public productos$: Observable<ProductoCatalogoItem[]> = this.productosSubject.asObservable();

  private sucursalesSubject = new BehaviorSubject<SucursalItem[]>([]);
  public sucursales$: Observable<SucursalItem[]> = this.sucursalesSubject.asObservable();

  private disponibilidadSubject = new BehaviorSubject<DisponibilidadProducto | null>(null);
  public disponibilidad$: Observable<DisponibilidadProducto | null> = this.disponibilidadSubject.asObservable();

  private cargandoSubject = new BehaviorSubject<boolean>(false);
  public cargando$: Observable<boolean> = this.cargandoSubject.asObservable();
  public loading$: Observable<boolean> = this.cargando$; // Alias retrocompatible

  // Observables para el soporte offline y aviso de datos desactualizados
  public datosDesactualizados$: Observable<boolean> = this.inventoryService.datosDesactualizados$;
  public offlineMode$: Observable<boolean> = this.inventoryService.offlineMode$;
  public ultimaSincronizacion$: Observable<string | null> = this.inventoryService.ultimaSincronizacion$;

  constructor(private inventoryService: InventoryService) {}

  public get productos(): ProductoCatalogoItem[] {
    return this.productosSubject.value;
  }

  public get sucursales(): SucursalItem[] {
    return this.sucursalesSubject.value;
  }

  /**
   * Carga la lista de sucursales activas en el estado reactivo
   */
  cargarSucursales(): void {
    this.inventoryService.obtenerSucursales().subscribe({
      next: (sucursales) => this.sucursalesSubject.next(sucursales),
      error: (err: any) => console.error('[CU08 CONTROLLER] Error al cargar sucursales:', err)
    });
  }

  /**
   * CU08: Consulta el catálogo aplicando filtros de sucursal, categoría, género y búsqueda
   */
  consultarCatalogo(
    sucursalId?: number | null,
    categoriaId?: number | null,
    genero?: string | null,
    search?: string | null,
    soloDisponibles: boolean = false
  ): void {
    this.cargandoSubject.next(true);
    this.inventoryService.consultarCatalogo(sucursalId, categoriaId, genero, search, soloDisponibles)
      .pipe(finalize(() => this.cargandoSubject.next(false)))
      .subscribe({
        next: (items) => this.productosSubject.next(items),
        error: (err: any) => console.error('[CU08 CONTROLLER] Error al consultar catálogo:', err)
      });
  }

  /**
   * CU08: Consulta la disponibilidad detallada de un producto en todas las sucursales
   */
  consultarDisponibilidad(productoId: number): Observable<DisponibilidadProducto> {
    this.cargandoSubject.next(true);
    const req = this.inventoryService.consultarDisponibilidad(productoId);
    req.pipe(finalize(() => this.cargandoSubject.next(false)))
      .subscribe({
        next: (disp) => this.disponibilidadSubject.next(disp),
        error: (err: any) => console.error('[CU08 CONTROLLER] Error al consultar disponibilidad:', err)
      });
    return req;
  }

  /**
   * Actualiza existencias físicas en sucursal
   */
  actualizarStock(
    varianteId: number,
    sucursalId: number,
    cantidad: number,
    stockMinimo?: number
  ): Observable<any> {
    return this.inventoryService.actualizarStock(varianteId, sucursalId, cantidad, stockMinimo);
  }

  // --- ALIASES RETROCOMPATIBLES ---
  loadSucursales(): void {
    this.cargarSucursales();
  }

  loadCatalogo(
    sucursalId?: number | null,
    categoriaId?: number | null,
    genero?: string | null,
    search?: string | null,
    soloDisponibles: boolean = false
  ): void {
    this.consultarCatalogo(sucursalId, categoriaId, genero, search, soloDisponibles);
  }

  loadDisponibilidad(productoId: number): Observable<DisponibilidadProducto> {
    return this.consultarDisponibilidad(productoId);
  }
}
