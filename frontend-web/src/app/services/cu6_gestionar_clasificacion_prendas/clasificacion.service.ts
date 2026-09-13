import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Categoria, Temporada, Coleccion } from '../../models/cu6_gestionar_clasificacion_prendas/clasificacion.model';

@Injectable({
  providedIn: 'root'
})
export class ClasificacionService {
  private baseUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  // CATEGORÍAS
  getCategorias(search?: string, activo?: boolean): Observable<Categoria[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());
    return this.http.get<Categoria[]>(`${this.baseUrl}/categorias`, { params });
  }

  createCategoria(data: Partial<Categoria>): Observable<Categoria> {
    return this.http.post<Categoria>(`${this.baseUrl}/categorias`, data);
  }

  updateCategoria(id: number, data: Partial<Categoria>): Observable<Categoria> {
    return this.http.put<Categoria>(`${this.baseUrl}/categorias/${id}`, data);
  }

  deleteCategoria(id: number): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/categorias/${id}`);
  }

  // TEMPORADAS
  getTemporadas(search?: string, activo?: boolean): Observable<Temporada[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());
    return this.http.get<Temporada[]>(`${this.baseUrl}/temporadas`, { params });
  }

  createTemporada(data: Partial<Temporada>): Observable<Temporada> {
    return this.http.post<Temporada>(`${this.baseUrl}/temporadas`, data);
  }

  updateTemporada(id: number, data: Partial<Temporada>): Observable<Temporada> {
    return this.http.put<Temporada>(`${this.baseUrl}/temporadas/${id}`, data);
  }

  deleteTemporada(id: number): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/temporadas/${id}`);
  }

  // COLECCIONES
  getColecciones(search?: string, activo?: boolean): Observable<Coleccion[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());
    return this.http.get<Coleccion[]>(`${this.baseUrl}/colecciones`, { params });
  }

  createColeccion(data: Partial<Coleccion>): Observable<Coleccion> {
    return this.http.post<Coleccion>(`${this.baseUrl}/colecciones`, data);
  }

  updateColeccion(id: number, data: Partial<Coleccion>): Observable<Coleccion> {
    return this.http.put<Coleccion>(`${this.baseUrl}/colecciones/${id}`, data);
  }

  deleteColeccion(id: number): Observable<any> {
    return this.http.delete<any>(`${this.baseUrl}/colecciones/${id}`);
  }
}
