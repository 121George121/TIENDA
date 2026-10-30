// ==============================================================================
// CAPA SERVICIO (MVC - SERVICE EN FRONTEND ANGULAR)
// Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
// Ubicación: frontend-web/src/app/services/cu8_consultar_catalogo_disponibilidad/inventory.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject, of, throwError } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import {
  SucursalItem,
  ProductoCatalogoItem,
  DisponibilidadProducto,
  CatalogoCacheLocal
} from '../../models/cu8_consultar_catalogo_disponibilidad/catalogo.model';
import { environment } from '../../../environments/environment';

const CACHE_CATALOGO_KEY = 'cu08_catalogo_cache';
const CACHE_SUCURSALES_KEY = 'cu08_sucursales_cache';

@Injectable({
  providedIn: 'root'
})
export class InventoryService {
  private baseUrl = `${environment.apiUrl}/inventario`;

  // Estado reactivo de conectividad y frescura de datos (CU08 Offline)
  private datosDesactualizadosSubject = new BehaviorSubject<boolean>(false);
  public datosDesactualizados$: Observable<boolean> = this.datosDesactualizadosSubject.asObservable();

  private offlineModeSubject = new BehaviorSubject<boolean>(!navigator.onLine);
  public offlineMode$: Observable<boolean> = this.offlineModeSubject.asObservable();

  private ultimaSincronizacionSubject = new BehaviorSubject<string | null>(this.getStoredTimestamp());
  public ultimaSincronizacion$: Observable<string | null> = this.ultimaSincronizacionSubject.asObservable();

  constructor(private http: HttpClient) {
    if (typeof window !== 'undefined') {
      window.addEventListener('online', () => {
        this.offlineModeSubject.next(false);
      });
      window.addEventListener('offline', () => {
        this.offlineModeSubject.next(true);
        this.datosDesactualizadosSubject.next(true);
      });
    }
  }

  private getStoredTimestamp(): string | null {
    try {
      const cached = localStorage.getItem(CACHE_CATALOGO_KEY);
      if (cached) {
        const parsed = JSON.parse(cached) as CatalogoCacheLocal;
        return parsed.timestamp || null;
      }
    } catch {
      // Ignorar error de parsing en SSR o storage deshabilitado
    }
    return null;
  }

  /**
   * Obtiene la lista de sucursales físicas activas con soporte offline
   */
  obtenerSucursales(): Observable<SucursalItem[]> {
    if (!navigator.onLine) {
      const cached = this.getCachedSucursales();
      if (cached.length > 0) {
        this.datosDesactualizadosSubject.next(true);
        return of(cached);
      }
    }

    return this.http.get<SucursalItem[]>(`${this.baseUrl}/sucursales`).pipe(
      tap((sucursales) => {
        try {
          localStorage.setItem(CACHE_SUCURSALES_KEY, JSON.stringify(sucursales));
        } catch (e) {
          console.warn('[CU08 CACHE] No se pudo guardar sucursales en localStorage:', e);
        }
      }),
      catchError((err: any) => {
        const cached = this.getCachedSucursales();
        if (cached.length > 0) {
          console.warn('[CU08 OFFLINE] Sirviendo sucursales desde caché local');
          this.datosDesactualizadosSubject.next(true);
          return of(cached);
        }
        return throwError(() => err);
      })
    );
  }

  /**
   * CU08: Consulta el catálogo con stock en tiempo real según sucursal y filtros.
   * Incluye persistencia y consulta offline con aviso de datos desactualizados.
   */
  consultarCatalogo(
    sucursalId?: number | null,
    categoriaId?: number | null,
    genero?: string | null,
    search?: string | null,
    soloDisponibles: boolean = false
  ): Observable<ProductoCatalogoItem[]> {
    // Si el navegador no tiene conexión a internet, recurrir inmediatamente a caché
    if (!navigator.onLine) {
      console.warn('[CU08 OFFLINE] Dispositivo sin conexión. Cargando catálogo guardado localmente.');
      this.offlineModeSubject.next(true);
      this.datosDesactualizadosSubject.next(true);
      return of(this.filtrarCatalogoEnMemoria(sucursalId, categoriaId, genero, search, soloDisponibles));
    }

    let params = new HttpParams();
    if (sucursalId) params = params.set('sucursal_id', sucursalId.toString());
    if (categoriaId) params = params.set('categoria_id', categoriaId.toString());
    if (genero && genero !== 'TODOS') params = params.set('genero', genero);
    if (search && search.trim() !== '') params = params.set('search', search.trim());
    if (soloDisponibles) params = params.set('solo_disponibles', 'true');

    return this.http.get<ProductoCatalogoItem[]>(`${this.baseUrl}/catalogo`, { params }).pipe(
      tap((items) => {
        // En conexión exitosa, actualizar caché local y marcar datos como frescos
        this.offlineModeSubject.next(false);
        this.datosDesactualizadosSubject.next(false);
        const timestamp = new Date().toISOString();
        this.ultimaSincronizacionSubject.next(timestamp);

        // Guardar catálogo en caché local sólo si es consulta global o sin filtros restrictivos
        if (!search && (!genero || genero === 'TODOS') && !soloDisponibles) {
          try {
            const cacheObj: CatalogoCacheLocal = {
              timestamp,
              sucursalId,
              items
            };
            localStorage.setItem(CACHE_CATALOGO_KEY, JSON.stringify(cacheObj));
          } catch (e) {
            console.warn('[CU08 CACHE] No se pudo guardar catálogo en localStorage:', e);
          }
        }
      }),
      catchError((err: any) => {
        // En caso de fallo de red (servidor caído o sin internet), recurrir al caché local
        console.warn('[CU08 ERROR RED] Fallo en la solicitud. Intentando recuperar catálogo offline...', err);
        const cachedItems = this.filtrarCatalogoEnMemoria(sucursalId, categoriaId, genero, search, soloDisponibles);
        if (cachedItems.length > 0) {
          this.offlineModeSubject.next(true);
          this.datosDesactualizadosSubject.next(true);
          return of(cachedItems);
        }
        return throwError(() => err);
      })
    );
  }

  /**
   * CU08: Consulta la disponibilidad de un producto en todas las sucursales físicas
   */
  consultarDisponibilidad(productoId: number): Observable<DisponibilidadProducto> {
    return this.http.get<DisponibilidadProducto>(`${this.baseUrl}/producto/${productoId}/disponibilidad`);
  }

  /**
   * Actualizar stock de variante en sucursal (para administración rápida)
   */
  actualizarStock(
    varianteId: number,
    sucursalId: number,
    cantidad: number,
    stockMinimo?: number
  ): Observable<any> {
    const payload = {
      variante_id: varianteId,
      sucursal_id: sucursalId,
      cantidad,
      stock_minimo: stockMinimo || 5
    };
    return this.http.put(`${this.baseUrl}/stock`, payload);
  }

  // --- MÉTODOS AUXILIARES DE CACHÉ OFFLINE ---

  private getCachedSucursales(): SucursalItem[] {
    try {
      const data = localStorage.getItem(CACHE_SUCURSALES_KEY);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  }

  private filtrarCatalogoEnMemoria(
    sucursalId?: number | null,
    categoriaId?: number | null,
    genero?: string | null,
    search?: string | null,
    soloDisponibles: boolean = false
  ): ProductoCatalogoItem[] {
    try {
      const cached = localStorage.getItem(CACHE_CATALOGO_KEY);
      if (!cached) return [];
      const cacheObj = JSON.parse(cached) as CatalogoCacheLocal;
      let items = cacheObj.items || [];

      if (categoriaId) {
        items = items.filter(p => p.categoria_id === categoriaId);
      }
      if (genero && genero !== 'TODOS') {
        items = items.filter(p => (p.genero || '').toLowerCase() === genero.toLowerCase());
      }
      if (search && search.trim() !== '') {
        const q = search.trim().toLowerCase();
        items = items.filter(p =>
          (p.nombre || '').toLowerCase().includes(q) ||
          (p.marca || '').toLowerCase().includes(q) ||
          (p.descripcion || '').toLowerCase().includes(q)
        );
      }
      if (soloDisponibles) {
        items = items.filter(p => (p.stock_sucursal > 0 || p.stock_total > 0));
      }
      return items;
    } catch (e) {
      console.warn('[CU08 CACHE] Error al leer caché local:', e);
      return [];
    }
  }

  // --- ALIASES DE COMPATIBILIDAD HACIA ATRÁS ---
  getSucursales(): Observable<SucursalItem[]> {
    return this.obtenerSucursales();
  }

  getCatalogo(
    sucursalId?: number | null,
    categoriaId?: number | null,
    genero?: string | null,
    search?: string | null,
    soloDisponibles: boolean = false
  ): Observable<ProductoCatalogoItem[]> {
    return this.consultarCatalogo(sucursalId, categoriaId, genero, search, soloDisponibles);
  }

  getDisponibilidadProducto(productoId: number): Observable<DisponibilidadProducto> {
    return this.consultarDisponibilidad(productoId);
  }
}
