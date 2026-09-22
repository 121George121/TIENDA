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

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private productService: ProductService) {}

  public get productos(): Producto[] {
    return this.productosSubject.value;
  }

  loadProductos(search?: string, categoria_id?: number, genero?: string, activo?: boolean): void {
    this.loadingSubject.next(true);
    this.productService.getProductos(search, categoria_id, genero, activo)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (res) => this.productosSubject.next(res),
        error: (err) => console.error('Error al cargar productos:', err)
      });
  }

  createProducto(data: ProductoCreateDTO): Observable<Producto> {
    this.loadingSubject.next(true);
    return this.productService.createProducto(data).pipe(
      tap((newProd) => {
        const current = this.productosSubject.value;
        this.productosSubject.next([newProd, ...current]);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  updateProducto(id: number, data: ProductoUpdateDTO): Observable<Producto> {
    this.loadingSubject.next(true);
    return this.productService.updateProducto(id, data).pipe(
      tap((updated) => {
        const current = this.productosSubject.value;
        const index = current.findIndex(p => p.id === id);
        if (index !== -1) {
          const list = [...current];
          list[index] = updated;
          this.productosSubject.next(list);
        }
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  toggleStatus(id: number, currentStatus: boolean): Observable<Producto> {
    const newStatus = !currentStatus;
    return this.productService.toggleStatus(id, newStatus).pipe(
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

  deleteProducto(id: number): Observable<{ message: string; id: number }> {
    this.loadingSubject.next(true);
    return this.productService.deleteProducto(id).pipe(
      tap(() => {
        const current = this.productosSubject.value;
        const updatedList = current.filter(p => p.id !== id);
        this.productosSubject.next(updatedList);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }
}
