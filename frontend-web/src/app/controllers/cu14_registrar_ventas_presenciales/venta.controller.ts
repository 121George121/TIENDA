import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap, finalize } from 'rxjs';
import { MetodoPago, VentaCompleta, VentaDetallada, VentaPresencialCreateDTO } from '../../models/cu14_registrar_ventas_presenciales/venta.model';
import { VentaService } from '../../services/cu14_registrar_ventas_presenciales/venta.service';

@Injectable({
  providedIn: 'root'
})
export class VentaController {
  private ventasSubject = new BehaviorSubject<VentaCompleta[]>([]);
  public ventas$: Observable<VentaCompleta[]> = this.ventasSubject.asObservable();

  private metodosPagoSubject = new BehaviorSubject<MetodoPago[]>([]);
  public metodosPago$: Observable<MetodoPago[]> = this.metodosPagoSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  constructor(private ventaService: VentaService) {}

  public get ventas(): VentaCompleta[] {
    return this.ventasSubject.value;
  }

  loadVentas(tipo?: string, sucursalId?: number): void {
    this.loadingSubject.next(true);
    this.ventaService.getVentas(tipo, sucursalId)
      .pipe(finalize(() => this.loadingSubject.next(false)))
      .subscribe({
        next: (ventas) => this.ventasSubject.next(ventas),
        error: (err) => console.error('Error al cargar ventas:', err)
      });
  }

  loadMetodosPago(): void {
    this.ventaService.getMetodosPago().subscribe({
      next: (metodos) => this.metodosPagoSubject.next(metodos),
      error: (err) => console.error('Error al cargar métodos de pago:', err)
    });
  }

  registrarVentaPresencial(dto: VentaPresencialCreateDTO): Observable<VentaCompleta> {
    this.loadingSubject.next(true);
    return this.ventaService.registrarVentaPresencial(dto).pipe(
      tap((nuevaVenta) => {
        const current = this.ventasSubject.value;
        this.ventasSubject.next([nuevaVenta, ...current]);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  getVentaDetalle(id: number): Observable<VentaDetallada> {
    return this.ventaService.getVentaById(id);
  }
}
