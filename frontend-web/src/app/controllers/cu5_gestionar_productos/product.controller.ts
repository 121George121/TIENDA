import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize, tap } from 'rxjs';
import { Producto, ProductoCreateDTO, ProductoUpdateDTO } from '../../models/cu5_gestionar_productos/product.model';
import { ProductService } from '../../services/cu5_gestionar_productos/product.service';

@Injectable({
  providedIn: 'root'
})
export class ProductController {
  private productosSubject = new BehaviorSubject<Producto[]>([]);
  public productos$: Observable<Producto[]> = this.productosSubject.asObservable();

  private cargandoSubject = new BehaviorSubject<boolean>(false);
  public cargando$: Observable<boolean> = this.cargandoSubject.asObservable();
  public loading$: Observable<boolean> = this.cargando$;

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private productService: ProductService) {}

  public get productos(): Producto[] {
    return this.productosSubject.value;
  }

  /**
   * Carga el catálogo de productos con filtros y paginación.
   */
  cargarProductos(search?: string, categoria_id?: number, genero?: string, activo?: boolean): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);

    this.productService.obtenerProductos(search, categoria_id, genero, activo)
      .pipe(finalize(() => this.cargandoSubject.next(false)))
      .subscribe({
        next: (res) => this.productosSubject.next(res),
        error: (err) => {
          console.error('Error al cargar productos:', err);
          this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar los productos');
        }
      });
  }

  /**
   * Registra un nuevo producto en el catálogo.
   */
  crearProducto(data: ProductoCreateDTO): Observable<Producto> {
    this.cargandoSubject.next(true);
    return this.productService.crearProducto(data).pipe(
      tap((newProd) => {
        const current = this.productosSubject.value;
        this.productosSubject.next([newProd, ...current]);
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  /**
   * Actualiza los datos de un producto en el estado observable.
   */
  actualizarProducto(id: number, data: ProductoUpdateDTO): Observable<Producto> {
    this.cargandoSubject.next(true);
    return this.productService.actualizarProducto(id, data).pipe(
      tap((updated) => {
        const current = this.productosSubject.value;
        const index = current.findIndex(p => p.id === id);
        if (index !== -1) {
          const list = [...current];
          list[index] = updated;
          this.productosSubject.next(list);
        }
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  /**
   * Activa o suspende un producto del catálogo.
   */
  cambiarEstado(id: number, currentStatus: boolean): Observable<Producto> {
    const newStatus = !currentStatus;
    return this.productService.cambiarEstadoProducto(id, newStatus).pipe(
      tap((updated) => {
        const current = this.productosSubject.value;
        const index = current.findIndex(p => p.id === id);
        if (index !== -1) {
          const list = [...current];
          list[index] = updated;
          this.productosSubject.next(list);
        }
      })
    );
  }

  /**
   * Elimina un producto de la base de datos o lo desactiva.
   */
  eliminarProducto(id: number): Observable<{ message: string; id: number }> {
    this.cargandoSubject.next(true);
    return this.productService.eliminarProducto(id).pipe(
      tap(() => {
        const current = this.productosSubject.value;
        const updatedList = current.filter(p => p.id !== id);
        this.productosSubject.next(updatedList);
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  loadProductos(search?: string, categoria_id?: number, genero?: string, activo?: boolean): void {
    this.cargarProductos(search, categoria_id, genero, activo);
  }

  createProducto(data: ProductoCreateDTO): Observable<Producto> {
    return this.crearProducto(data);
  }

  updateProducto(id: number, data: ProductoUpdateDTO): Observable<Producto> {
    return this.actualizarProducto(id, data);
  }

  toggleStatus(id: number, currentStatus: boolean): Observable<Producto> {
    return this.cambiarEstado(id, currentStatus);
  }

  deleteProducto(id: number): Observable<{ message: string; id: number }> {
    return this.eliminarProducto(id);
  }
}

export { ProductController as ProductoController };
