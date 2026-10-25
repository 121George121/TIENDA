// ==============================================================================
// SERVICIO (MVC - SERVICE)
// Módulo: CU6 - Clasificación de Prendas (Categorías, Temporadas, Colecciones)
// Ubicación: frontend-web/src/app/services/cu6_gestionar_clasificacion_prendas/clasificacion.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Categoria, CategoriaCreateDTO, CategoriaUpdateDTO,
  Temporada, TemporadaCreateDTO, TemporadaUpdateDTO,
  Coleccion, ColeccionCreateDTO, ColeccionUpdateDTO
} from '../../models/cu6_gestionar_clasificacion_prendas/clasificacion.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ClasificacionService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // ============================================================================
  // SECCIÓN CATEGORÍAS
  // ============================================================================
  obtenerCategorias(search?: string, activo?: boolean): Observable<Categoria[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());
    return this.http.get<Categoria[]>(`${this.baseUrl}/categorias`, { params });
  }

  obtenerCategoriaPorId(id: number): Observable<Categoria> {
    return this.http.get<Categoria>(`${this.baseUrl}/categorias/${id}`);
  }

  crearCategoria(data: Partial<CategoriaCreateDTO>): Observable<Categoria> {
    return this.http.post<Categoria>(`${this.baseUrl}/categorias`, data);
  }

  actualizarCategoria(id: number, data: Partial<CategoriaUpdateDTO>): Observable<Categoria> {
    return this.http.put<Categoria>(`${this.baseUrl}/categorias/${id}`, data);
  }

  cambiarEstadoCategoria(id: number, activo: boolean): Observable<Categoria> {
    return this.http.patch<Categoria>(`${this.baseUrl}/categorias/${id}/estado`, null, {
      params: new HttpParams().set('activo', activo.toString())
    });
  }

  eliminarCategoria(id: number): Observable<{ message: string; id: number; desactivado?: boolean }> {
    return this.http.delete<{ message: string; id: number; desactivado?: boolean }>(`${this.baseUrl}/categorias/${id}`);
  }

  // ============================================================================
  // SECCIÓN TEMPORADAS
  // ============================================================================
  obtenerTemporadas(search?: string, activo?: boolean): Observable<Temporada[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());
    return this.http.get<Temporada[]>(`${this.baseUrl}/temporadas`, { params });
  }

  obtenerTemporadaPorId(id: number): Observable<Temporada> {
    return this.http.get<Temporada>(`${this.baseUrl}/temporadas/${id}`);
  }

  crearTemporada(data: Partial<TemporadaCreateDTO>): Observable<Temporada> {
    return this.http.post<Temporada>(`${this.baseUrl}/temporadas`, data);
  }

  actualizarTemporada(id: number, data: Partial<TemporadaUpdateDTO>): Observable<Temporada> {
    return this.http.put<Temporada>(`${this.baseUrl}/temporadas/${id}`, data);
  }

  cambiarEstadoTemporada(id: number, activo: boolean): Observable<Temporada> {
    return this.http.patch<Temporada>(`${this.baseUrl}/temporadas/${id}/estado`, null, {
      params: new HttpParams().set('activo', activo.toString())
    });
  }

  eliminarTemporada(id: number): Observable<{ message: string; id: number; desactivado?: boolean }> {
    return this.http.delete<{ message: string; id: number; desactivado?: boolean }>(`${this.baseUrl}/temporadas/${id}`);
  }

  // ============================================================================
  // SECCIÓN COLECCIONES
  // ============================================================================
  obtenerColecciones(search?: string, activo?: boolean): Observable<Coleccion[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());
    return this.http.get<Coleccion[]>(`${this.baseUrl}/colecciones`, { params });
  }

  obtenerColeccionPorId(id: number): Observable<Coleccion> {
    return this.http.get<Coleccion>(`${this.baseUrl}/colecciones/${id}`);
  }

  crearColeccion(data: Partial<ColeccionCreateDTO>): Observable<Coleccion> {
    return this.http.post<Coleccion>(`${this.baseUrl}/colecciones`, data);
  }

  actualizarColeccion(id: number, data: Partial<ColeccionUpdateDTO>): Observable<Coleccion> {
    return this.http.put<Coleccion>(`${this.baseUrl}/colecciones/${id}`, data);
  }

  cambiarEstadoColeccion(id: number, activo: boolean): Observable<Coleccion> {
    return this.http.patch<Coleccion>(`${this.baseUrl}/colecciones/${id}/estado`, null, {
      params: new HttpParams().set('activo', activo.toString())
    });
  }

  eliminarColeccion(id: number): Observable<{ message: string; id: number; desactivado?: boolean }> {
    return this.http.delete<{ message: string; id: number; desactivado?: boolean }>(`${this.baseUrl}/colecciones/${id}`);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  getCategorias(search?: string, activo?: boolean): Observable<Categoria[]> {
    return this.obtenerCategorias(search, activo);
  }
  createCategoria(data: Partial<Categoria>): Observable<Categoria> {
    return this.crearCategoria(data);
  }
  updateCategoria(id: number, data: Partial<Categoria>): Observable<Categoria> {
    return this.actualizarCategoria(id, data);
  }
  deleteCategoria(id: number): Observable<any> {
    return this.eliminarCategoria(id);
  }

  getTemporadas(search?: string, activo?: boolean): Observable<Temporada[]> {
    return this.obtenerTemporadas(search, activo);
  }
  createTemporada(data: Partial<Temporada>): Observable<Temporada> {
    return this.crearTemporada(data);
  }
  updateTemporada(id: number, data: Partial<Temporada>): Observable<Temporada> {
    return this.actualizarTemporada(id, data);
  }
  deleteTemporada(id: number): Observable<any> {
    return this.eliminarTemporada(id);
  }

  getColecciones(search?: string, activo?: boolean): Observable<Coleccion[]> {
    return this.obtenerColecciones(search, activo);
  }
  createColeccion(data: Partial<Coleccion>): Observable<Coleccion> {
    return this.crearColeccion(data);
  }
  updateColeccion(id: number, data: Partial<Coleccion>): Observable<Coleccion> {
    return this.actualizarColeccion(id, data);
  }
  deleteColeccion(id: number): Observable<any> {
    return this.eliminarColeccion(id);
  }
}
