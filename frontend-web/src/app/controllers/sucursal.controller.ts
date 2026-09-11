import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap, finalize } from 'rxjs';
import { Sucursal, SucursalCreateDTO, SucursalUpdateDTO } from '../models/sucursal.model';
import { SucursalService } from '../services/sucursal.service';

@Injectable({
  providedIn: 'root'
})
export class SucursalController {
  private sucursalesSubject = new BehaviorSubject<Sucursal[]>([]);
  public sucursales$: Observable<Sucursal[]> = this.sucursalesSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private sucursalService: SucursalService) {}

  public get sucursales(): Sucursal[] {
    return this.sucursalesSubject.value;
  }

  loadSucursales(search?: string, ciudad?: string, activo?: boolean): void {
    this.loadingSubject.next(true);
    this.sucursalService.getSucursales(search, ciudad, activo)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (sucursales) => this.sucursalesSubject.next(sucursales),
        error: (err) => console.error('Error al cargar sucursales:', err)
      });
  }

  createSucursal(data: SucursalCreateDTO): Observable<Sucursal> {
    this.loadingSubject.next(true);
    return this.sucursalService.createSucursal(data).pipe(
      tap((newSucursal) => {
        const current = this.sucursalesSubject.value;
        this.sucursalesSubject.next([newSucursal, ...current]);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  updateSucursal(id: number, data: SucursalUpdateDTO): Observable<Sucursal> {
    this.loadingSubject.next(true);
    return this.sucursalService.updateSucursal(id, data).pipe(
      tap((updated) => {
        const current = this.sucursalesSubject.value;
        const index = current.findIndex(s => s.id === id);
        if (index !== -1) {
          const updatedList = [...current];
          updatedList[index] = updated;
          this.sucursalesSubject.next(updatedList);
        }
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  toggleStatus(id: number, currentStatus: boolean): Observable<Sucursal> {
    const newStatus = !currentStatus;
    return this.sucursalService.toggleStatus(id, newStatus).pipe(
      tap((updated) => {
        const current = this.sucursalesSubject.value;
        const index = current.findIndex(s => s.id === id);
        if (index !== -1) {
          const updatedList = [...current];
          updatedList[index] = updated;
          this.sucursalesSubject.next(updatedList);
        }
      })
    );
  }

  deleteSucursal(id: number): Observable<{ message: string; id: number }> {
    this.loadingSubject.next(true);
    return this.sucursalService.deleteSucursal(id).pipe(
      tap(() => {
        const current = this.sucursalesSubject.value;
        const index = current.findIndex(s => s.id === id);
        if (index !== -1) {
          const updatedList = [...current];
          updatedList[index] = { ...updatedList[index], activo: false };
          this.sucursalesSubject.next(updatedList);
        }
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }
}
