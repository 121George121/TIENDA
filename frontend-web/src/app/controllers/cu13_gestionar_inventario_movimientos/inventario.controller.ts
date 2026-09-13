import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap, finalize } from 'rxjs';
import { InventarioItem, MovimientoInventarioCreateDTO, MovimientoInventarioItem } from '../../models/cu13_gestionar_inventario_movimientos/inventario.model';
import { InventarioService } from '../../services/cu13_gestionar_inventario_movimientos/inventario.service';

@Injectable({
  providedIn: 'root'
})
export class InventarioController {
  private inventarioSubject = new BehaviorSubject<InventarioItem[]>([]);
  public inventario$: Observable<InventarioItem[]> = this.inventarioSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private inventarioService: InventarioService) {}

  public get inventario(): InventarioItem[] {
    return this.inventarioSubject.value;
  }

  loadInventario(sucursalId?: number, search?: string, soloBajoStock?: boolean): void {
    this.loadingSubject.next(true);
    this.inventarioService.getInventario(sucursalId, search, soloBajoStock)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (items) => this.inventarioSubject.next(items),
        error: (err) => console.error('Error al cargar inventario:', err)
      });
  }

  registrarMovimiento(inventarioId: number, dto: MovimientoInventarioCreateDTO): Observable<any> {
    this.loadingSubject.next(true);
    return this.inventarioService.registrarMovimiento(inventarioId, dto).pipe(
      tap((res) => {
        // Actualizar el item en el subject
        const current = this.inventarioSubject.value;
        const index = current.findIndex(i => i.id === inventarioId);
        if (index !== -1) {
          const updatedList = [...current];
          updatedList[index] = {
            ...updatedList[index],
            stockfisico: res.stock_actualizado,
            stockdisponible: res.stock_actualizado
          };
          this.inventarioSubject.next(updatedList);
        }
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  actualizarStockMinimo(inventarioId: number, stockMinimo: number): Observable<any> {
    return this.inventarioService.actualizarStockMinimo(inventarioId, stockMinimo).pipe(
      tap(() => {
        const current = this.inventarioSubject.value;
        const index = current.findIndex(i => i.id === inventarioId);
        if (index !== -1) {
          const updatedList = [...current];
          updatedList[index] = { ...updatedList[index], stockminimo: stockMinimo };
          this.inventarioSubject.next(updatedList);
        }
      })
    );
  }

  getKardex(inventarioId: number): Observable<MovimientoInventarioItem[]> {
    return this.inventarioService.getKardex(inventarioId);
  }
}
