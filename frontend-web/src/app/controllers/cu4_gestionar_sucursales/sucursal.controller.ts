import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap, finalize } from 'rxjs';
import { Sucursal, SucursalCreateDTO, SucursalUpdateDTO } from '../../models/cu4_gestionar_sucursales/sucursal.model';
import { SucursalService } from '../../services/cu4_gestionar_sucursales/sucursal.service';

@Injectable({
  providedIn: 'root'
})
export class SucursalController {
  private sucursalesSubject = new BehaviorSubject<Sucursal[]>([]);
  public sucursales$: Observable<Sucursal[]> = this.sucursalesSubject.asObservable();

  private cargandoSubject = new BehaviorSubject<boolean>(false);
  public cargando$: Observable<boolean> = this.cargandoSubject.asObservable();
  public loading$: Observable<boolean> = this.cargando$;

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private sucursalService: SucursalService) {}

  public get sucursales(): Sucursal[] {
    return this.sucursalesSubject.value;
  }

  /**
   * Carga las sucursales desde el servicio filtrando por criterios opcionales.
   */
  cargarSucursales(search?: string, ciudad?: string, activo?: boolean): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);

    this.sucursalService.obtenerSucursales(search, ciudad, activo)
      .pipe(finalize(() => this.cargandoSubject.next(false)))
      .subscribe({
        next: (sucursales) => this.sucursalesSubject.next(sucursales),
        error: (err) => {
          console.error('Error al cargar sucursales:', err);
          this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar las sucursales');
        }
      });
  }

  /**
   * Registra una nueva sucursal en el estado local tras confirmación de la API.
   */
  crearSucursal(data: SucursalCreateDTO): Observable<Sucursal> {
    this.cargandoSubject.next(true);
    return this.sucursalService.crearSucursal(data).pipe(
      tap((newSucursal) => {
        const current = this.sucursalesSubject.value;
        this.sucursalesSubject.next([newSucursal, ...current]);
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  /**
   * Actualiza una sucursal física en el estado reactivo.
   */
  actualizarSucursal(id: number, data: SucursalUpdateDTO): Observable<Sucursal> {
    this.cargandoSubject.next(true);
    return this.sucursalService.actualizarSucursal(id, data).pipe(
      tap((updated) => {
        const current = this.sucursalesSubject.value;
        const index = current.findIndex(s => s.id === id);
        if (index !== -1) {
          const updatedList = [...current];
          updatedList[index] = updated;
          this.sucursalesSubject.next(updatedList);
        }
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  /**
   * Cambia el estado activo o suspendido de una sucursal.
   */
  cambiarEstado(id: number, currentStatus: boolean): Observable<Sucursal> {
    const newStatus = !currentStatus;
    return this.sucursalService.cambiarEstadoSucursal(id, newStatus).pipe(
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

  /**
   * Aplica baja lógica a una sucursal actualizando su estado a inactiva.
   */
  eliminarSucursal(id: number): Observable<{ message: string; id: number }> {
    this.cargandoSubject.next(true);
    return this.sucursalService.eliminarSucursal(id).pipe(
      tap(() => {
        const current = this.sucursalesSubject.value;
        const index = current.findIndex(s => s.id === id);
        if (index !== -1) {
          const updatedList = [...current];
          updatedList[index] = { ...updatedList[index], activo: false };
          this.sucursalesSubject.next(updatedList);
        }
      }),
      finalize(() => this.cargandoSubject.next(false))
    );
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  loadSucursales(search?: string, ciudad?: string, activo?: boolean): void {
    this.cargarSucursales(search, ciudad, activo);
  }

  createSucursal(data: SucursalCreateDTO): Observable<Sucursal> {
    return this.crearSucursal(data);
  }

  updateSucursal(id: number, data: SucursalUpdateDTO): Observable<Sucursal> {
    return this.actualizarSucursal(id, data);
  }

  toggleStatus(id: number, currentStatus: boolean): Observable<Sucursal> {
    return this.cambiarEstado(id, currentStatus);
  }

  deleteSucursal(id: number): Observable<{ message: string; id: number }> {
    return this.eliminarSucursal(id);
  }
}

export { SucursalController as BranchController };
