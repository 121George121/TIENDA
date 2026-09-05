import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Proveedor, ProveedorCreateDTO, ProveedorUpdateDTO, ProductoProveedor } from '../models/proveedor.model';

@Injectable({
  providedIn: 'root'
})
export class ProveedorService {
  private apiUrl = 'http://localhost:8000/api/v1/proveedores';

  constructor(private http: HttpClient) {}

  getProveedores(search?: string, activo?: boolean): Observable<Proveedor[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());

    return this.http.get<Proveedor[]>(this.apiUrl, { params });
  }

  getProveedorById(id: number): Observable<Proveedor> {
    return this.http.get<Proveedor>(`${this.apiUrl}/${id}`);
  }

  createProveedor(data: ProveedorCreateDTO): Observable<Proveedor> {
    return this.http.post<Proveedor>(this.apiUrl, data);
  }

  updateProveedor(id: number, data: ProveedorUpdateDTO): Observable<Proveedor> {
    return this.http.put<Proveedor>(`${this.apiUrl}/${id}`, data);
  }

  deleteProveedor(id: number): Observable<{ message: string; id: number }> {
    return this.http.delete<{ message: string; id: number }>(`${this.apiUrl}/${id}`);
  }

  vincularProducto(data: { idproducto: number; idproveedor: number; costocompra: number; cantidad: number }): Observable<ProductoProveedor> {
    return this.http.post<ProductoProveedor>(`${this.apiUrl}/suministro`, data);
  }
}
