import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface OrdenItemDTO {
  producto_id: number;
  cantidad: number;
  variante_id?: number;
}

export interface OrdenCreateDTO {
  direccion_envio?: string;
  sucursal_id?: number;
  items: OrdenItemDTO[];
}

export interface OrdenResponseDTO {
  id: number;
  codigoventa: string;
  estado: string;
  tipoventa: string;
  subtotal: number;
  descuento: number;
  total: number;
  fecha?: string;
  sucursal_nombre?: string;
  cliente_nombre?: string;
  metodo_pago?: string;
  recibo_id?: number;
  mensaje?: string;
  items?: any[];
}

export interface TrackingStepDTO {
  numero: number;
  titulo: string;
  descripcion: string;
  completado: boolean;
  activo: boolean;
  fecha?: string;
}

export interface OrdenTrackingDTO {
  orden_id: number;
  codigoventa: string;
  estado: string;
  tipo_venta: string;
  total: number;
  fecha?: string;
  sucursal_nombre?: string;
  cliente_nombre?: string;
  metodo_pago?: string;
  paso_actual: number;
  pasos: TrackingStepDTO[];
  items: any[];
}

import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CompraDigitalService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getProductos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/productos`);
  }

  crearOrdenDigital(dto: OrdenCreateDTO): Observable<OrdenResponseDTO> {
    return this.http.post<OrdenResponseDTO>(`${this.apiUrl}/ordenes`, dto);
  }

  getMisOrdenes(): Observable<OrdenResponseDTO[]> {
    return this.http.get<OrdenResponseDTO[]>(`${this.apiUrl}/ordenes/me`);
  }

  consultarTracking(ordenId: number): Observable<OrdenTrackingDTO> {
    return this.http.get<OrdenTrackingDTO>(`${this.apiUrl}/ordenes/${ordenId}/tracking`);
  }

  actualizarEstadoOrden(ordenId: number, nuevoEstado: string, comentario?: string): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/ordenes/${ordenId}/estado`, {
      nuevo_estado: nuevoEstado,
      comentario: comentario
    });
  }
}
