// ==============================================================================
// CU16 - GESTIONAR PAGOS Y COMPROBANTES -> CAPA CONTROLADOR (MVC)
// Ubicación: frontend-web/src/app/controllers/cu16_gestionar_pagos_comprobantes/pago.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, catchError, finalize, of, tap } from 'rxjs';
import { PagoService } from '../../services/cu16_gestionar_pagos_comprobantes/pago.service';
import { MetodoPago, IniciarPagoResponse, ComprobantePago } from '../../models/cu16_gestionar_pagos_comprobantes/pago.model';

@Injectable({
  providedIn: 'root'
})
export class PagoController {
  private metodosSubject = new BehaviorSubject<MetodoPago[]>([]);
  public metodos$: Observable<MetodoPago[]> = this.metodosSubject.asObservable();

  private pagoActualSubject = new BehaviorSubject<IniciarPagoResponse | null>(null);
  public pagoActual$: Observable<IniciarPagoResponse | null> = this.pagoActualSubject.asObservable();

  private comprobanteSubject = new BehaviorSubject<ComprobantePago | null>(null);
  public comprobante$: Observable<ComprobantePago | null> = this.comprobanteSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private service: PagoService) {}

  public cargarMetodosPago(): void {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    this.service.getMetodosPago().pipe(
      tap((metodos) => this.metodosSubject.next(metodos)),
      catchError((err) => {
        console.warn('[PagoController] Usando métodos de pago por defecto:', err);
        // Fallback robusto con los métodos oficiales del negocio
        const metodosDefault: MetodoPago[] = [
          { id: 1, nombre: 'QR Simple / Pago Móvil', icono: 'qr_code_2', descripcion: 'Transferencia bancaria instantánea mediante código QR interoperable BCB', activo: true },
          { id: 2, nombre: 'Tarjeta de Débito / Crédito', icono: 'credit_card', descripcion: 'Procesamiento seguro Visa, Mastercard y tarjetas nacionales', activo: true },
          { id: 3, nombre: 'Efectivo en Caja / Sucursal', icono: 'payments', descripcion: 'Pago directo en mostrador al retirar tus prendas reservadas', activo: true },
          { id: 4, nombre: 'PayPal Internacional', icono: 'account_balance_wallet', descripcion: 'Cobros en dólares para clientes y pedidos internacionales', activo: true }
        ];
        this.metodosSubject.next(metodosDefault);
        return of(metodosDefault);
      }),
      finalize(() => this.loadingSubject.next(false))
    ).subscribe();
  }

  public iniciarPagoVenta(ventaId: number, metodoId: number): Observable<IniciarPagoResponse> {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    return this.service.iniciarPago(ventaId, metodoId).pipe(
      tap((resp) => {
        this.pagoActualSubject.next(resp);
      }),
      catchError((err) => {
        const msg = err.error?.detail || 'Error al iniciar la transacción de pago.';
        this.errorSubject.next(msg);
        throw err;
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  public consultarComprobante(ventaId: number): void {
    this.loadingSubject.next(true);
    this.service.getComprobante(ventaId).pipe(
      tap((comp) => this.comprobanteSubject.next(comp)),
      catchError((err) => {
        console.warn('Error al obtener comprobante:', err);
        return of(null);
      }),
      finalize(() => this.loadingSubject.next(false))
    ).subscribe();
  }
}
