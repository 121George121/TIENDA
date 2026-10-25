// ==============================================================================
// SERVICIO (MVC - SERVICE)
// Módulo: CU7 - Proveedores y Productos Suministrados
// Ubicación: frontend-web/src/app/services/cu7_gestionar_proveedores_productos_suministrados/proveedor.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Proveedor, ProveedorCreateDTO, ProveedorUpdateDTO, ProductoProveedor
} from '../../models/cu7_gestionar_proveedores_productos_suministrados/proveedor.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProveedorService {
  private apiUrl = `${environment.apiUrl}/proveedores`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de proveedores del tenant con filtros opcionales.
   */
  obtenerProveedores(search?: string, activo?: boolean): Observable<Proveedor[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());

    return this.http.get<Proveedor[]>(this.apiUrl, { params });
  }

  /**
   * Obtiene el detalle de un proveedor por su ID.
   */
  obtenerProveedorPorId(id: number): Observable<Proveedor> {
    return this.http.get<Proveedor>(`${this.apiUrl}/${id}`);
  }

  /**
   * Registra un nuevo proveedor en el tenant.
   */
  crearProveedor(data: ProveedorCreateDTO): Observable<Proveedor> {
    return this.http.post<Proveedor>(this.apiUrl, data);
  }

  /**
   * Actualiza los datos de un proveedor existente.
   */
  actualizarProveedor(id: number, data: ProveedorUpdateDTO): Observable<Proveedor> {
    return this.http.put<Proveedor>(`${this.apiUrl}/${id}`, data);
  }

  /**
   * Cambia el estado comercial (activo / inactivo) de un proveedor.
   */
  cambiarEstadoProveedor(id: number, activo: boolean): Observable<Proveedor> {
    return this.http.patch<Proveedor>(`${this.apiUrl}/${id}/estado`, null, {
      params: new HttpParams().set('activo', activo.toString())
    });
  }

  /**
   * Elimina un proveedor definitivamente o aplica baja lógica.
   */
  eliminarProveedor(id: number): Observable<{ message: string; id: number; desactivado?: boolean }> {
    return this.http.delete<{ message: string; id: number; desactivado?: boolean }>(`${this.apiUrl}/${id}`);
  }

  /**
   * Vincula un producto del catálogo con su respectivo costo de suministro.
   */
  vincularProductoSuministrado(data: { idproducto: number; idproveedor: number; costocompra: number; cantidad: number }): Observable<ProductoProveedor> {
    return this.http.post<ProductoProveedor>(`${this.apiUrl}/suministro`, data);
  }

  /**
   * Obtiene la lista de suministros vinculados a un proveedor.
   */
  obtenerProductosSuministrados(proveedorId: number): Observable<ProductoProveedor[]> {
    return this.http.get<ProductoProveedor[]>(`${this.apiUrl}/${proveedorId}/suministros`);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  getProveedores(search?: string, activo?: boolean): Observable<Proveedor[]> {
    return this.obtenerProveedores(search, activo);
  }

  getProveedorById(id: number): Observable<Proveedor> {
    return this.obtenerProveedorPorId(id);
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

  vincularProducto(data: { idproducto: number; idproveedor: number; costocompra: number; cantidad: number }): Observable<ProductoProveedor> {
    return this.vincularProductoSuministrado(data);
  }
}

export { ProveedorService as SupplierService };
