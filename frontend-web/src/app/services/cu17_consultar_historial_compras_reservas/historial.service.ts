import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface TrackingStep {
  paso: number;
  titulo: string;
  fecha: string;
  completado: boolean;
}

export interface DetalleItemCompra {
  id: number;
  producto: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
  imagen_url?: string;
}

export interface CompraHistorialDTO {
  id: number;
  codigo_venta: string;
  tipo_venta: string;
  estado: string;
  total: number;
  fecha: string;
  sucursal: string;
  metodo_pago: string;
  tracking: TrackingStep[];
  items_count: number;
  items: DetalleItemCompra[];
  comprobante_url: string;
}

export interface ReservaHistorialDTO {
  id: number;
  codigo_reserva: string;
  estado: string;
  total_estimado: number;
  fecha_reserva: string;
  fecha_limite: string;
  horas_restantes: number;
  sucursal_nombre: string;
  sucursal_direccion: string;
  qr_retiro: string;
  items: DetalleItemCompra[];
}

export interface ResumenClienteDTO {
  cliente_nombre: string;
  total_pedidos: number;
  total_invertido_bs: number;
  total_reservas: number;
  reservas_activas: number;
}

import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class HistorialService {
  private readonly apiUrl = `${environment.apiUrl}/historial`;

  constructor(private http: HttpClient) {}

  obtenerResumen(): Observable<ResumenClienteDTO> {
    return this.http.get<ResumenClienteDTO>(`${this.apiUrl}/resumen`);
  }

  obtenerCompras(): Observable<CompraHistorialDTO[]> {
    return this.http.get<CompraHistorialDTO[]>(`${this.apiUrl}/compras`);
  }

  obtenerReservas(): Observable<ReservaHistorialDTO[]> {
    return this.http.get<ReservaHistorialDTO[]>(`${this.apiUrl}/reservas`);
  }
}
