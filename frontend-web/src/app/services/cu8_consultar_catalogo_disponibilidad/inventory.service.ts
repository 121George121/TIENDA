// ==============================================================================
// CAPA SERVICIO (MVC - SERVICE EN FRONTEND ANGULAR)
// Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
// Ubicación: frontend-web/src/app/services/cu8_consultar_catalogo_disponibilidad/inventory.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  SucursalItem,
  ProductoCatalogoItem,
  DisponibilidadProducto
} from '../../models/cu8_consultar_catalogo_disponibilidad/inventory.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class InventoryService {
  private baseUrl = `${environment.apiUrl}/inventario`;

  constructor(private http: HttpClient) {}

  /** Obtiene la lista de sucursales físicas activas */
  getSucursales(): Observable<SucursalItem[]> {
    return this.http.get<SucursalItem[]>(`${this.baseUrl}/sucursales`);
  }

  /**
   * CU08: Consulta el catálogo con stock en tiempo real según sucursal y filtros
   */
  getCatalogo(
    sucursalId?: number | null,
    categoriaId?: number | null,
    genero?: string | null,
    search?: string | null,
    soloDisponibles: boolean = false
  ): Observable<ProductoCatalogoItem[]> {
    let params = new HttpParams();

    if (sucursalId) {
      params = params.set('sucursal_id', sucursalId.toString());
    }
    if (categoriaId) {
      params = params.set('categoria_id', categoriaId.toString());
    }
    if (genero && genero !== 'TODOS') {
      params = params.set('genero', genero);
    }
    if (search && search.trim() !== '') {
      params = params.set('search', search.trim());
    }
    if (soloDisponibles) {
      params = params.set('solo_disponibles', 'true');
    }

    return this.http.get<ProductoCatalogoItem[]>(`${this.baseUrl}/catalogo`, { params });
  }

  /**
   * CU08: Consulta la disponibilidad de un producto en todas las sucursales físicas
   */
  getDisponibilidadProducto(productoId: number): Observable<DisponibilidadProducto> {
    return this.http.get<DisponibilidadProducto>(`${this.baseUrl}/producto/${productoId}/disponibilidad`);
  }
}
