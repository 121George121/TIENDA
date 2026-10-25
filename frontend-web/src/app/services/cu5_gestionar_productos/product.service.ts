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

  /**
   * Obtiene la lista de productos del catálogo del tenant con filtros opcionales.
   */
  obtenerProductos(search?: string, categoria_id?: number, genero?: string, activo?: boolean): Observable<Producto[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (categoria_id) params = params.set('categoria_id', categoria_id.toString());
    if (genero) params = params.set('genero', genero);
    if (activo !== undefined && activo !== null) params = params.set('activo', activo.toString());

    return this.http.get<Producto[]>(this.apiUrl, { params });
  }

  /**
   * Obtiene el detalle de un producto por ID.
   */
  obtenerProductoPorId(id: number): Observable<Producto> {
    return this.http.get<Producto>(`${this.apiUrl}/${id}`);
  }

  /**
   * Registra un nuevo producto en el catálogo.
   */
  crearProducto(data: ProductoCreateDTO): Observable<Producto> {
    return this.http.post<Producto>(this.apiUrl, data);
  }

  /**
   * Actualiza los datos de un producto en el catálogo.
   */
  actualizarProducto(id: number, data: ProductoUpdateDTO): Observable<Producto> {
    return this.http.put<Producto>(`${this.apiUrl}/${id}`, data);
  }

  /**
   * Activa o desactiva la visibilidad del producto en el catálogo.
   */
  cambiarEstadoProducto(id: number, activo: boolean): Observable<Producto> {
    return this.http.patch<Producto>(`${this.apiUrl}/${id}/estado`, null, {
      params: new HttpParams().set('activo', activo.toString())
    });
  }

  /**
   * Elimina un producto de la base de datos o lo desactiva.
   */
  eliminarProducto(id: number): Observable<{ message: string; id: number }> {
    return this.http.delete<{ message: string; id: number }>(`${this.apiUrl}/${id}`);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  getProductos(search?: string, categoria_id?: number, genero?: string, activo?: boolean): Observable<Producto[]> {
    return this.obtenerProductos(search, categoria_id, genero, activo);
  }

  getProductoById(id: number): Observable<Producto> {
    return this.obtenerProductoPorId(id);
  }

  createProducto(data: ProductoCreateDTO): Observable<Producto> {
    return this.crearProducto(data);
  }

  updateProducto(id: number, data: ProductoUpdateDTO): Observable<Producto> {
    return this.actualizarProducto(id, data);
  }

  toggleStatus(id: number, activo: boolean): Observable<Producto> {
    return this.cambiarEstadoProducto(id, activo);
  }

  deleteProducto(id: number): Observable<{ message: string; id: number }> {
    return this.eliminarProducto(id);
  }
}

export { ProductService as ProductoService };
