import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Sucursal, SucursalCreateDTO, SucursalUpdateDTO } from '../../models/cu4_gestionar_sucursales/sucursal.model';

@Injectable({
  providedIn: 'root'
})
export class SucursalService {
  private apiUrl = 'http://localhost:8000/api/v1/sucursales';

  constructor(private http: HttpClient) {}

  getSucursales(search?: string, ciudad?: string, activo?: boolean): Observable<Sucursal[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (ciudad) params = params.set('ciudad', ciudad);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());

    return this.http.get<Sucursal[]>(this.apiUrl, { params });
  }

  getSucursalById(id: number): Observable<Sucursal> {
    return this.http.get<Sucursal>(`${this.apiUrl}/${id}`);
  }

  createSucursal(sucursal: SucursalCreateDTO): Observable<Sucursal> {
    return this.http.post<Sucursal>(this.apiUrl, sucursal);
  }

  updateSucursal(id: number, sucursal: SucursalUpdateDTO): Observable<Sucursal> {
    return this.http.put<Sucursal>(`${this.apiUrl}/${id}`, sucursal);
  }

  toggleStatus(id: number, activo: boolean): Observable<Sucursal> {
    return this.http.patch<Sucursal>(`${this.apiUrl}/${id}/estado`, null, {
      params: new HttpParams().set('activo', activo.toString())
    });
  }

  deleteSucursal(id: number): Observable<{ message: string; id: number }> {
    return this.http.delete<{ message: string; id: number }>(`${this.apiUrl}/${id}`);
  }
}
