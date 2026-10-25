// ==============================================================================
// CONTROLADOR (MVC - CONTROLLER)
// Módulo: CU6 - Clasificación de Prendas (Categorías, Temporadas, Colecciones)
// Ubicación: frontend-web/src/app/controllers/cu6_gestionar_clasificacion_prendas/clasificacion.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize, tap } from 'rxjs';
import {
  Categoria, CategoriaCreateDTO, CategoriaUpdateDTO,
  Temporada, TemporadaCreateDTO, TemporadaUpdateDTO,
  Coleccion, ColeccionCreateDTO, ColeccionUpdateDTO
} from '../../models/cu6_gestionar_clasificacion_prendas/clasificacion.model';
import { ClasificacionService } from '../../services/cu6_gestionar_clasificacion_prendas/clasificacion.service';

@Injectable({
  providedIn: 'root'
})
export class ClasificacionController {
  private categoriasSubject = new BehaviorSubject<Categoria[]>([]);
  public categorias$: Observable<Categoria[]> = this.categoriasSubject.asObservable();

  private temporadasSubject = new BehaviorSubject<Temporada[]>([]);
  public temporadas$: Observable<Temporada[]> = this.temporadasSubject.asObservable();

  private coleccionesSubject = new BehaviorSubject<Coleccion[]>([]);
  public colecciones$: Observable<Coleccion[]> = this.coleccionesSubject.asObservable();

  private cargandoSubject = new BehaviorSubject<boolean>(false);
  public cargando$: Observable<boolean> = this.cargandoSubject.asObservable();
  public loading$: Observable<boolean> = this.cargando$;

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private service: ClasificacionService) {}

  // ============================================================================
  // SECCIÓN CATEGORÍAS
  // ============================================================================
  cargarCategorias(search?: string, activo?: boolean): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);
    this.service.obtenerCategorias(search, activo)
      .pipe(finalize(() => this.cargandoSubject.next(false)))
      .subscribe({
        next: (res) => this.categoriasSubject.next(res),
        error: (err) => {
          console.error('Error al cargar categorías:', err);
          this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar las categorías');
        }
      });
  }

  crearCategoria(data: Partial<CategoriaCreateDTO>): Observable<Categoria> {
    this.cargandoSubject.next(true);
    return this.service.crearCategoria(data).pipe(
      tap((res) => this.categoriasSubject.next([res, ...this.categoriasSubject.value])),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  actualizarCategoria(id: number, data: Partial<CategoriaUpdateDTO>): Observable<Categoria> {
    this.cargandoSubject.next(true);
    return this.service.actualizarCategoria(id, data).pipe(
      tap((updated) => {
        const list = this.categoriasSubject.value.map(c => c.id === id ? updated : c);
        this.categoriasSubject.next(list);
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  cambiarEstadoCategoria(id: number, activo: boolean): Observable<Categoria> {
    return this.service.cambiarEstadoCategoria(id, activo).pipe(
      tap((updated) => {
        const list = this.categoriasSubject.value.map(c => c.id === id ? updated : c);
        this.categoriasSubject.next(list);
      })
    );
  }

  eliminarCategoria(id: number): Observable<{ message: string; id: number; desactivado?: boolean }> {
    this.cargandoSubject.next(true);
    return this.service.eliminarCategoria(id).pipe(
      tap((res) => {
        if (res.desactivado) {
          const list = this.categoriasSubject.value.map(c => c.id === id ? { ...c, activo: false } : c);
          this.categoriasSubject.next(list);
        } else {
          const list = this.categoriasSubject.value.filter(c => c.id !== id);
          this.categoriasSubject.next(list);
        }
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  // ============================================================================
  // SECCIÓN TEMPORADAS
  // ============================================================================
  cargarTemporadas(search?: string, activo?: boolean): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);
    this.service.obtenerTemporadas(search, activo)
      .pipe(finalize(() => this.cargandoSubject.next(false)))
      .subscribe({
        next: (res) => this.temporadasSubject.next(res),
        error: (err) => {
          console.error('Error al cargar temporadas:', err);
          this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar las temporadas');
        }
      });
  }

  crearTemporada(data: Partial<TemporadaCreateDTO>): Observable<Temporada> {
    this.cargandoSubject.next(true);
    return this.service.crearTemporada(data).pipe(
      tap((res) => this.temporadasSubject.next([res, ...this.temporadasSubject.value])),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  actualizarTemporada(id: number, data: Partial<TemporadaUpdateDTO>): Observable<Temporada> {
    this.cargandoSubject.next(true);
    return this.service.actualizarTemporada(id, data).pipe(
      tap((updated) => {
        const list = this.temporadasSubject.value.map(t => t.id === id ? updated : t);
        this.temporadasSubject.next(list);
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  cambiarEstadoTemporada(id: number, activo: boolean): Observable<Temporada> {
    return this.service.cambiarEstadoTemporada(id, activo).pipe(
      tap((updated) => {
        const list = this.temporadasSubject.value.map(t => t.id === id ? updated : t);
        this.temporadasSubject.next(list);
      })
    );
  }

  eliminarTemporada(id: number): Observable<{ message: string; id: number; desactivado?: boolean }> {
    this.cargandoSubject.next(true);
    return this.service.eliminarTemporada(id).pipe(
      tap((res) => {
        if (res.desactivado) {
          const list = this.temporadasSubject.value.map(t => t.id === id ? { ...t, activo: false } : t);
          this.temporadasSubject.next(list);
        } else {
          const list = this.temporadasSubject.value.filter(t => t.id !== id);
          this.temporadasSubject.next(list);
        }
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  // ============================================================================
  // SECCIÓN COLECCIONES
  // ============================================================================
  cargarColecciones(search?: string, activo?: boolean): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);
    this.service.obtenerColecciones(search, activo)
      .pipe(finalize(() => this.cargandoSubject.next(false)))
      .subscribe({
        next: (res) => this.coleccionesSubject.next(res),
        error: (err) => {
          console.error('Error al cargar colecciones:', err);
          this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar las colecciones');
        }
      });
  }

  crearColeccion(data: Partial<ColeccionCreateDTO>): Observable<Coleccion> {
    this.cargandoSubject.next(true);
    return this.service.crearColeccion(data).pipe(
      tap((res) => this.coleccionesSubject.next([res, ...this.coleccionesSubject.value])),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  actualizarColeccion(id: number, data: Partial<ColeccionUpdateDTO>): Observable<Coleccion> {
    this.cargandoSubject.next(true);
    return this.service.actualizarColeccion(id, data).pipe(
      tap((updated) => {
        const list = this.coleccionesSubject.value.map(c => c.id === id ? updated : c);
        this.coleccionesSubject.next(list);
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  cambiarEstadoColeccion(id: number, activo: boolean): Observable<Coleccion> {
    return this.service.cambiarEstadoColeccion(id, activo).pipe(
      tap((updated) => {
        const list = this.coleccionesSubject.value.map(c => c.id === id ? updated : c);
        this.coleccionesSubject.next(list);
      })
    );
  }

  eliminarColeccion(id: number): Observable<{ message: string; id: number; desactivado?: boolean }> {
    this.cargandoSubject.next(true);
    return this.service.eliminarColeccion(id).pipe(
      tap((res) => {
        if (res.desactivado) {
          const list = this.coleccionesSubject.value.map(c => c.id === id ? { ...c, activo: false } : c);
          this.coleccionesSubject.next(list);
        } else {
          const list = this.coleccionesSubject.value.filter(c => c.id !== id);
          this.coleccionesSubject.next(list);
        }
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  loadCategorias(search?: string, activo?: boolean): void {
    this.cargarCategorias(search, activo);
  }
  createCategoria(data: Partial<CategoriaCreateDTO>): Observable<Categoria> {
    return this.crearCategoria(data);
  }
  updateCategoria(id: number, data: Partial<CategoriaUpdateDTO>): Observable<Categoria> {
    return this.actualizarCategoria(id, data);
  }
  deleteCategoria(id: number): Observable<any> {
    return this.eliminarCategoria(id);
  }

  loadTemporadas(search?: string, activo?: boolean): void {
    this.cargarTemporadas(search, activo);
  }
  createTemporada(data: Partial<TemporadaCreateDTO>): Observable<Temporada> {
    return this.crearTemporada(data);
  }
  updateTemporada(id: number, data: Partial<TemporadaUpdateDTO>): Observable<Temporada> {
    return this.actualizarTemporada(id, data);
  }
  deleteTemporada(id: number): Observable<any> {
    return this.eliminarTemporada(id);
  }

  loadColecciones(search?: string, activo?: boolean): void {
    this.cargarColecciones(search, activo);
  }
  createColeccion(data: Partial<ColeccionCreateDTO>): Observable<Coleccion> {
    return this.crearColeccion(data);
  }
  updateColeccion(id: number, data: Partial<ColeccionUpdateDTO>): Observable<Coleccion> {
    return this.actualizarColeccion(id, data);
  }
  deleteColeccion(id: number): Observable<any> {
    return this.eliminarColeccion(id);
  }
}

export { ClasificacionController as ClassificationController };
