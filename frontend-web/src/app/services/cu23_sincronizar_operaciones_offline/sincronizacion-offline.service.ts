// CU23 - SINCRONIZAR OPERACIONES OFFLINE -> SERVICE
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { SyncOperacionItem, SyncLogDTO } from '../../models/cu23_sincronizar_operaciones_offline/sincronizacion-offline.model';

@Injectable({
  providedIn: 'root'
})
export class SincronizacionOfflineService {
  private readonly apiUrl = `${environment.apiUrl}/sincronizacion-offline`;

  constructor(private http: HttpClient) {}

  enviarLote(sucursalId: number, operaciones: SyncOperacionItem[]): Observable<{ exito: boolean; resultado: any }> {
    return this.http.post<{ exito: boolean; resultado: any }>(`${this.apiUrl}/lote`, {
      sucursal_id: sucursalId,
      operaciones: operaciones
    });
  }

  obtenerHistorial(): Observable<{ exito: boolean; logs: SyncLogDTO[] }> {
    return this.http.get<{ exito: boolean; logs: SyncLogDTO[] }>(`${this.apiUrl}/historial`);
  }
}
