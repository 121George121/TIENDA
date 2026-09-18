import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface MetodoPagoDTO {
  id: number;
  nombre: string;
  icono: string;
  descripcion: string;
  activo: boolean;
}

export interface IniciarPagoResponseDTO {
  metodo: string;
  requiere_redireccion: boolean;
  url_redireccion?: string;
  token?: string;
  qr_image?: string;
  codigo_pago?: string;
  cuenta_bancaria?: string;
  titular?: string;
  tiempo_expiracion_minutos?: number;
  referencia?: string;
  monto_total: number;
  monto_usd?: number;
  mensaje: string;
}

@Injectable({
  providedIn: 'root'
})
export class PagoService {
  private apiUrl = 'http://localhost:8000/api/v1/pagos';

  constructor(private http: HttpClient) {}

  getMetodosPago(): Observable<MetodoPagoDTO[]> {
    return this.http.get<MetodoPagoDTO[]>(`${this.apiUrl}/metodos`);
  }

  iniciarPago(ventaId: number, metodoId: number, returnUrl?: string, cancelUrl?: string): Observable<IniciarPagoResponseDTO> {
    return this.http.post<IniciarPagoResponseDTO>(`${this.apiUrl}/iniciar`, {
      venta_id: ventaId,
      metodo_id: metodoId,
      return_url: returnUrl,
      cancel_url: cancelUrl
    });
  }

  capturarPayPal(ventaId: number, token?: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/paypal/capturar`, {
      venta_id: ventaId,
      token: token
    });
  }

  getComprobante(ventaId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${ventaId}/comprobante`);
  }

  getComprobanteUrl(ventaId: number): string {
    return `${this.apiUrl}/${ventaId}/comprobante-html`;
  }
}
