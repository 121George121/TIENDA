import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Producto, ProductoCreateDTO, ProductoUpdateDTO } from '../../models/cu5_gestionar_productos/product.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = `${environment.apiUrl}/productos`;

  constructor(private http: HttpClient) {}

  getProductos(search?: string, categoria_id?: number, genero?: string, activo?: boolean): Observable<Producto[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (categoria_id) params = params.set('categoria_id', categoria_id.toString());
    if (genero) params = params.set('genero', genero);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());

    return this.http.get<Producto[]>(this.apiUrl, { params });
  }

  getProductoById(id: number): Observable<Producto> {
    return this.http.get<Producto>(`${this.apiUrl}/${id}`);
  }

  createProducto(data: ProductoCreateDTO): Observable<Producto> {
    return this.http.post<Producto>(this.apiUrl, data);
  }

  updateProducto(id: number, data: ProductoUpdateDTO): Observable<Producto> {
    return this.http.put<Producto>(`${this.apiUrl}/${id}`, data);
  }

  toggleStatus(id: number, activo: boolean): Observable<Producto> {
    return this.http.patch<Producto>(`${this.apiUrl}/${id}/estado`, null, {
      params: new HttpParams().set('activo', activo.toString())
    });
  }

  deleteProducto(id: number): Observable<{ message: string; id: number }> {
    return this.http.delete<{ message: string; id: number }>(`${this.apiUrl}/${id}`);
  }
}
