// CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> SERVICE
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { CobroOfflineDTO, RegistroCobroOfflineRequest } from '../../models/cu22_registrar_cobros_contado_offline/cobro-offline.model';

@Injectable({
  providedIn: 'root'
})
export class CobroOfflineService {
  private readonly apiUrl = `${environment.apiUrl}/cobros-offline`;

  constructor(private http: HttpClient) {}

  registrarCobro(payload: RegistroCobroOfflineRequest): Observable<{ exito: boolean; cobro_offline: CobroOfflineDTO }> {
    return this.http.post<{ exito: boolean; cobro_offline: CobroOfflineDTO }>(`${this.apiUrl}/registrar`, payload);
  }

  listarPendientes(sucursalId?: number): Observable<{ exito: boolean; pendientes: CobroOfflineDTO[] }> {
    const url = sucursalId ? `${this.apiUrl}/pendientes?sucursal_id=${sucursalId}` : `${this.apiUrl}/pendientes`;
    return this.http.get<{ exito: boolean; pendientes: CobroOfflineDTO[] }>(url);
  }
}
