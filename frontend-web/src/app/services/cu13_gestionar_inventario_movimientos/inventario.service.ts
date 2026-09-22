import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { InventarioItem, MovimientoInventarioCreateDTO, MovimientoInventarioItem } from '../../models/cu13_gestionar_inventario_movimientos/inventario.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class InventarioService {
  private apiUrl = `${environment.apiUrl}/inventario`;

  constructor(private http: HttpClient) {}

  getInventario(sucursalId?: number, search?: string, soloBajoStock?: boolean): Observable<InventarioItem[]> {
    let params = new HttpParams();
    if (sucursalId) params = params.set('sucursal_id', sucursalId.toString());
    if (search) params = params.set('search', search);
    if (soloBajoStock) params = params.set('solo_bajo_stock', 'true');

    return this.http.get<InventarioItem[]>(this.apiUrl, { params });
  }

  registrarMovimiento(inventarioId: number, dto: MovimientoInventarioCreateDTO): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/${inventarioId}/movimiento`, dto);
  }

  actualizarStockMinimo(inventarioId: number, stockMinimo: number): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${inventarioId}/stock-minimo`, { stockminimo: stockMinimo });
  }

  getKardex(inventarioId: number): Observable<MovimientoInventarioItem[]> {
    return this.http.get<MovimientoInventarioItem[]>(`${this.apiUrl}/${inventarioId}/movimientos`);
  }
}
