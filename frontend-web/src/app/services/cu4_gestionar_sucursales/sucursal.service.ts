import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Sucursal, SucursalCreateDTO, SucursalUpdateDTO } from '../../models/cu4_gestionar_sucursales/sucursal.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SucursalService {
  private apiUrl = `${environment.apiUrl}/sucursales`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de sucursales del tenant aplicando filtros opcionales.
   */
  obtenerSucursales(search?: string, ciudad?: string, activo?: boolean): Observable<Sucursal[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (ciudad) params = params.set('ciudad', ciudad);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());

    return this.http.get<Sucursal[]>(this.apiUrl, { params });
  }

  /**
   * Obtiene el detalle de una sucursal física por ID.
   */
  obtenerSucursalPorId(id: number): Observable<Sucursal> {
    return this.http.get<Sucursal>(`${this.apiUrl}/${id}`);
  }

  /**
   * Registra una nueva sucursal en el tenant.
   */
  crearSucursal(sucursal: SucursalCreateDTO): Observable<Sucursal> {
    return this.http.post<Sucursal>(this.apiUrl, sucursal);
  }

  /**
   * Actualiza los datos comerciales y de localización de la sucursal.
   */
  actualizarSucursal(id: number, sucursal: SucursalUpdateDTO): Observable<Sucursal> {
    return this.http.put<Sucursal>(`${this.apiUrl}/${id}`, sucursal);
  }

  /**
   * Cambia el estado activo/suspendido de la sucursal.
   */
  cambiarEstadoSucursal(id: number, activo: boolean): Observable<Sucursal> {
    return this.http.patch<Sucursal>(`${this.apiUrl}/${id}/estado`, null, {
      params: new HttpParams().set('activo', activo.toString())
    });
  }

  /**
   * Aplica baja lógica a una sucursal del sistema.
   */
  eliminarSucursal(id: number): Observable<{ message: string; id: number }> {
    return this.http.delete<{ message: string; id: number }>(`${this.apiUrl}/${id}`);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  getSucursales(search?: string, ciudad?: string, activo?: boolean): Observable<Sucursal[]> {
    return this.obtenerSucursales(search, ciudad, activo);
  }

  getSucursalById(id: number): Observable<Sucursal> {
    return this.obtenerSucursalPorId(id);
  }

  createSucursal(sucursal: SucursalCreateDTO): Observable<Sucursal> {
    return this.crearSucursal(sucursal);
  }

  updateSucursal(id: number, sucursal: SucursalUpdateDTO): Observable<Sucursal> {
    return this.actualizarSucursal(id, sucursal);
  }

  toggleStatus(id: number, activo: boolean): Observable<Sucursal> {
    return this.cambiarEstadoSucursal(id, activo);
  }

  deleteSucursal(id: number): Observable<{ message: string; id: number }> {
    return this.eliminarSucursal(id);
  }
}

export { SucursalService as BranchService };
