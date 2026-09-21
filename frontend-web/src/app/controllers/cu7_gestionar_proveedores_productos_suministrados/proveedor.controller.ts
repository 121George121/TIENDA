import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, finalize, tap } from 'rxjs';
import { Proveedor, ProveedorCreateDTO, ProveedorUpdateDTO } from '../../models/cu7_gestionar_proveedores_productos_suministrados/proveedor.model';
import { ProveedorService } from '../../services/cu7_gestionar_proveedores_productos_suministrados/proveedor.service';

@Injectable({
  providedIn: 'root'
})
export class ProveedorController {
  private proveedoresSubject = new BehaviorSubject<Proveedor[]>([]);
  public proveedores$: Observable<Proveedor[]> = this.proveedoresSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private service: ProveedorService) {}

  public get proveedores(): Proveedor[] {
    return this.proveedoresSubject.value;
  }

  loadProveedores(search?: string, activo?: boolean): void {
    this.loadingSubject.next(true);
    this.service.getProveedores(search, activo)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (res) => this.proveedoresSubject.next(res),
        error: (err) => console.error('Error al cargar proveedores:', err)
      });
  }

  createProveedor(data: ProveedorCreateDTO): Observable<Proveedor> {
    this.loadingSubject.next(true);
    return this.service.createProveedor(data).pipe(
      tap((newProv) => {
        const current = this.proveedoresSubject.value;
        this.proveedoresSubject.next([newProv, ...current]);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  updateProveedor(id: number, data: ProveedorUpdateDTO): Observable<Proveedor> {
    this.loadingSubject.next(true);
    return this.service.updateProveedor(id, data).pipe(
      tap((updated) => {
        const current = this.proveedoresSubject.value;
        const index = current.findIndex(p => p.id === id);
        if (index !== -1) {
          const list = [...current];
          list[index] = updated;
          this.proveedoresSubject.next(list);
        }
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  deleteProveedor(id: number): Observable<{ message: string; id: number }> {
    this.loadingSubject.next(true);
    return this.service.deleteProveedor(id).pipe(
      tap(() => {
        const list = this.proveedoresSubject.value.filter(p => p.id !== id);
        this.proveedoresSubject.next(list);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }
}

