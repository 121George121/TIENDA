// ==============================================================================
// CU18 - GESTIONAR RECOMENDACIONES MEDIANTE IA -> SERVICIO ANGULAR
// Ubicación: frontend-web/src/app/services/cu18_gestionar_recomendaciones_ia/recomendacion.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface RecomendacionOutfitDTO {
  producto_id: number;
  nombre: string;
  precio: number;
  imagen_url?: string;
  razon_estilo: string;
  afinidad_porcentaje: number;
  fuente: string;
}

export interface TendenciaDTO {
  producto_id: number;
  nombre: string;
  precio: number;
  imagen_url?: string;
  etiqueta: string;
  razon: string;
}

import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RecomendacionService {
  private readonly apiUrl = `${environment.apiUrl}/recomendaciones`;

  constructor(private http: HttpClient) {}

  obtenerRecomendacionOutfit(productoId?: number, carritoIds?: number[], limite: number = 3): Observable<RecomendacionOutfitDTO[]> {
    return this.http.post<RecomendacionOutfitDTO[]>(`${this.apiUrl}/outfit`, {
      producto_id: productoId,
      carrito_ids: carritoIds,
      limite: limite
    });
  }

  obtenerTendencias(limite: number = 4): Observable<TendenciaDTO[]> {
    return this.http.get<TendenciaDTO[]>(`${this.apiUrl}/tendencias?limite=${limite}`);
  }
}
