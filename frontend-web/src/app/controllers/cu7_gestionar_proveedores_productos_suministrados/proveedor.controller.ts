// ==============================================================================
// CONTROLADOR (MVC - CONTROLLER)
// Módulo: CU7 - Proveedores y Productos Suministrados
// Ubicación: frontend-web/src/app/controllers/cu7_gestionar_proveedores_productos_suministrados/proveedor.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize, tap } from 'rxjs';
import {
  Proveedor, ProveedorCreateDTO, ProveedorUpdateDTO, ProductoProveedor
} from '../../models/cu7_gestionar_proveedores_productos_suministrados/proveedor.model';
import { ProveedorService } from '../../services/cu7_gestionar_proveedores_productos_suministrados/proveedor.service';

@Injectable({
  providedIn: 'root'
})
export class ProveedorController {
  private proveedoresSubject = new BehaviorSubject<Proveedor[]>([]);
  public proveedores$: Observable<Proveedor[]> = this.proveedoresSubject.asObservable();

  private cargandoSubject = new BehaviorSubject<boolean>(false);
  public cargando$: Observable<boolean> = this.cargandoSubject.asObservable();
  public loading$: Observable<boolean> = this.cargando$;

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private service: ProveedorService) {}

  public get proveedores(): Proveedor[] {
    return this.proveedoresSubject.value;
  }

  /**
   * Carga la lista de proveedores del tenant con filtros.
   */
  cargarProveedores(search?: string, activo?: boolean): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);
    this.service.obtenerProveedores(search, activo)
      .pipe(finalize(() => this.cargandoSubject.next(false)))
      .subscribe({
        next: (res) => this.proveedoresSubject.next(res),
        error: (err) => {
          console.error('Error al cargar proveedores:', err);
          this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar los proveedores');
        }
      });
  }

  /**
   * Registra un nuevo proveedor en el estado reactivo.
   */
  crearProveedor(data: ProveedorCreateDTO): Observable<Proveedor> {
    this.cargandoSubject.next(true);
    return this.service.crearProveedor(data).pipe(
      tap((newProv) => {
        const current = this.proveedoresSubject.value;
        this.proveedoresSubject.next([newProv, ...current]);
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  /**
   * Actualiza los datos de un proveedor en el estado reactivo.
   */
  actualizarProveedor(id: number, data: ProveedorUpdateDTO): Observable<Proveedor> {
    this.cargandoSubject.next(true);
    return this.service.actualizarProveedor(id, data).pipe(
      tap((updated) => {
        const current = this.proveedoresSubject.value;
        const index = current.findIndex(p => p.id === id);
        if (index !== -1) {
          const list = [...current];
          list[index] = updated;
          this.proveedoresSubject.next(list);
        }
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  /**
   * Cambia el estado activo / inactivo de un proveedor.
   */
  cambiarEstado(id: number, currentStatus: boolean): Observable<Proveedor> {
    const nuevoEstado = !currentStatus;
    return this.service.cambiarEstadoProveedor(id, nuevoEstado).pipe(
      tap((updated) => {
        const current = this.proveedoresSubject.value;
        const index = current.findIndex(p => p.id === id);
        if (index !== -1) {
          const list = [...current];
          list[index] = updated;
          this.proveedoresSubject.next(list);
        }
      })
    );
  }

  /**
   * Elimina o desactiva un proveedor del estado reactivo.
   */
  eliminarProveedor(id: number): Observable<{ message: string; id: number; desactivado?: boolean }> {
    this.cargandoSubject.next(true);
    return this.service.eliminarProveedor(id).pipe(
      tap((res) => {
        const current = this.proveedoresSubject.value;
        if (res.desactivado) {
          const updatedList = current.map(p => p.id === id ? { ...p, activo: false } : p);
          this.proveedoresSubject.next(updatedList);
        } else {
          const updatedList = current.filter(p => p.id !== id);
          this.proveedoresSubject.next(updatedList);
        }
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  /**
   * Vincula un producto suministrado al proveedor.
   */
  vincularProductoSuministrado(data: { idproducto: number; idproveedor: number; costocompra: number; cantidad: number }): Observable<ProductoProveedor> {
    return this.service.vincularProductoSuministrado(data).pipe(
      tap(() => this.cargarProveedores())
    );
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  loadProveedores(search?: string, activo?: boolean): void {
    this.cargarProveedores(search, activo);
  }

  createProveedor(data: ProveedorCreateDTO): Observable<Proveedor> {
    return this.crearProveedor(data);
  }

  updateProveedor(id: number, data: ProveedorUpdateDTO): Observable<Proveedor> {
    return this.actualizarProveedor(id, data);
  }

  deleteProveedor(id: number): Observable<{ message: string; id: number }> {
    return this.eliminarProveedor(id);
  }
}

export { ProveedorController as SupplierController };
