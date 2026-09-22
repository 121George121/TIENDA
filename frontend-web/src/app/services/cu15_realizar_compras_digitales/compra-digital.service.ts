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
  mensaje?: string;
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
}
