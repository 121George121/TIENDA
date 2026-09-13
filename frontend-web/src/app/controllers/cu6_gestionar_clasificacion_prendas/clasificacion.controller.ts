import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize, tap } from 'rxjs';
import { Categoria, Temporada, Coleccion } from '../../models/cu6_gestionar_clasificacion_prendas/clasificacion.model';
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

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private service: ClasificacionService) {}

  // CATEGORÍAS
  loadCategorias(search?: string, activo?: boolean): void {
    this.loadingSubject.next(true);
    this.service.getCategorias(search, activo)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (res) => this.categoriasSubject.next(res),
        error: (err) => console.error('Error al cargar categorías:', err)
      });
  }

  createCategoria(data: Partial<Categoria>): Observable<Categoria> {
    return this.service.createCategoria(data).pipe(
      tap((res) => this.categoriasSubject.next([res, ...this.categoriasSubject.value]))
    );
  }

  updateCategoria(id: number, data: Partial<Categoria>): Observable<Categoria> {
    return this.service.updateCategoria(id, data).pipe(
      tap((updated) => {
        const list = this.categoriasSubject.value.map(c => c.id === id ? updated : c);
        this.categoriasSubject.next(list);
      })
    );
  }

  deleteCategoria(id: number): Observable<any> {
    return this.service.deleteCategoria(id).pipe(
      tap(() => {
        const list = this.categoriasSubject.value.map(c => c.id === id ? { ...c, activo: false } : c);
        this.categoriasSubject.next(list);
      })
    );
  }

  // TEMPORADAS
  loadTemporadas(search?: string, activo?: boolean): void {
    this.loadingSubject.next(true);
    this.service.getTemporadas(search, activo)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (res) => this.temporadasSubject.next(res),
        error: (err) => console.error('Error al cargar temporadas:', err)
      });
  }

  createTemporada(data: Partial<Temporada>): Observable<Temporada> {
    return this.service.createTemporada(data).pipe(
      tap((res) => this.temporadasSubject.next([res, ...this.temporadasSubject.value]))
    );
  }

  updateTemporada(id: number, data: Partial<Temporada>): Observable<Temporada> {
    return this.service.updateTemporada(id, data).pipe(
      tap((updated) => {
        const list = this.temporadasSubject.value.map(t => t.id === id ? updated : t);
        this.temporadasSubject.next(list);
      })
    );
  }

  deleteTemporada(id: number): Observable<any> {
    return this.service.deleteTemporada(id).pipe(
      tap(() => {
        const list = this.temporadasSubject.value.map(t => t.id === id ? { ...t, activo: false } : t);
        this.temporadasSubject.next(list);
      })
    );
  }

  // COLECCIONES
  loadColecciones(search?: string, activo?: boolean): void {
    this.loadingSubject.next(true);
    this.service.getColecciones(search, activo)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (res) => this.coleccionesSubject.next(res),
        error: (err) => console.error('Error al cargar colecciones:', err)
      });
  }

  createColeccion(data: Partial<Coleccion>): Observable<Coleccion> {
    return this.service.createColeccion(data).pipe(
      tap((res) => this.coleccionesSubject.next([res, ...this.coleccionesSubject.value]))
    );
  }

  updateColeccion(id: number, data: Partial<Coleccion>): Observable<Coleccion> {
    return this.service.updateColeccion(id, data).pipe(
      tap((updated) => {
        const list = this.coleccionesSubject.value.map(c => c.id === id ? updated : c);
        this.coleccionesSubject.next(list);
      })
    );
  }

  deleteColeccion(id: number): Observable<any> {
    return this.service.deleteColeccion(id).pipe(
      tap(() => {
        const list = this.coleccionesSubject.value.map(c => c.id === id ? { ...c, activo: false } : c);
        this.coleccionesSubject.next(list);
      })
    );
  }
}
