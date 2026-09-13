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
} from '../../models/cu8_consultar_catalogo_disponibilidad/inventory.model';
import { InventoryService } from '../../services/cu8_consultar_catalogo_disponibilidad/inventory.service';

@Injectable({
  providedIn: 'root'
})
export class InventoryController {
  private productosSubject = new BehaviorSubject<ProductoCatalogoItem[]>([]);
  public productos$: Observable<ProductoCatalogoItem[]> = this.productosSubject.asObservable();

  private sucursalesSubject = new BehaviorSubject<SucursalItem[]>([]);
  public sucursales$: Observable<SucursalItem[]> = this.sucursalesSubject.asObservable();

  private disponibilidadSubject = new BehaviorSubject<DisponibilidadProducto | null>(null);
  public disponibilidad$: Observable<DisponibilidadProducto | null> = this.disponibilidadSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private inventoryService: InventoryService) {}

  public get productos(): ProductoCatalogoItem[] {
    return this.productosSubject.value;
  }

  public get sucursales(): SucursalItem[] {
    return this.sucursalesSubject.value;
  }

  loadSucursales(): void {
    this.inventoryService.getSucursales().subscribe({
      next: (sucursales) => this.sucursalesSubject.next(sucursales),
      error: (err) => console.error('Error al cargar sucursales:', err)
    });
  }

  loadCatalogo(
    sucursalId?: number | null,
    categoriaId?: number | null,
    genero?: string | null,
    search?: string | null,
    soloDisponibles: boolean = false
  ): void {
    this.loadingSubject.next(true);
    this.inventoryService.getCatalogo(sucursalId, categoriaId, genero, search, soloDisponibles)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (items) => this.productosSubject.next(items),
        error: (err) => console.error('Error al cargar catálogo:', err)
      });
  }

  loadDisponibilidad(productoId: number): Observable<DisponibilidadProducto> {
    this.loadingSubject.next(true);
    const req = this.inventoryService.getDisponibilidadProducto(productoId);
    req.pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (disp) => this.disponibilidadSubject.next(disp),
        error: (err) => console.error('Error al consultar disponibilidad:', err)
      });
    return req;
  }
}
