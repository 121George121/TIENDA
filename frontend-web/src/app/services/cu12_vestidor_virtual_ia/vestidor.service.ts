// ==============================================================================
// CAPA SERVICIO (MVC - SERVICE EN FRONTEND ANGULAR)
// Módulo: CU12 - Utilizar Vestidor Virtual mediante IA
// Ubicación: frontend-web/src/app/services/cu12_vestidor_virtual_ia/vestidor.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AnalisisFisonomiaResponse, TryOnResponse } from '../../models/cu12_vestidor_virtual_ia/vestidor.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class VestidorService {
  private apiUrl = `${environment.apiUrl}/vestidor`;

  constructor(private http: HttpClient) {}

  /** CU12: Diagnóstico fisonómico y recomendación ergonómica de talla mediante Google Gemini AI */
  analizarFisonomia(
    productoNombre: string,
    tallaActual: string = 'M',
    colorSeleccionado: string = 'Grafito',
    imagen?: File
  ): Observable<AnalisisFisonomiaResponse> {
    const formData = new FormData();
    formData.append('producto_nombre', productoNombre);
    formData.append('talla_actual', tallaActual);
    formData.append('color_seleccionado', colorSeleccionado);
    if (imagen) {
      formData.append('imagen', imagen, imagen.name);
    }
    return this.http.post<AnalisisFisonomiaResponse>(`${this.apiUrl}/analisis-ia`, formData);
  }

  /** CU12: Generación de prueba fotorrealista de ropa (Virtual Try-On con IA) */
  generarTryOn(
    prendaUrl: string,
    productoNombre: string,
    talla: string,
    color: string,
    imagenUsuario: File
  ): Observable<TryOnResponse> {
    const formData = new FormData();
    formData.append('prenda_url', prendaUrl);
    formData.append('producto_nombre', productoNombre);
    formData.append('talla', talla);
    formData.append('color', color);
    formData.append('imagen_usuario', imagenUsuario, imagenUsuario.name);

    return this.http.post<TryOnResponse>(`${this.apiUrl}/try-on-fotorrealista`, formData);
  }

  /** CU12: Retorna la URL del backend que extrae el fondo transparente con IA */
  obtenerPrendaTransparenteUrl(imagenUrl: string): string {
    return `${this.apiUrl}/prenda-transparente?imagen_url=${encodeURIComponent(imagenUrl)}`;
  }

  // --- Aliases de compatibilidad ---
  analizarFisonomiaIA = this.analizarFisonomia.bind(this);
  probarPrendaFotorrealista = this.generarTryOn.bind(this);
}
