// CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> SERVICE
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DevolucionDTO, SolicitudDevolucionDTO } from '../../models/cu25_gestionar_cambios_devoluciones/devolucion.model';

@Injectable({
  providedIn: 'root'
})
export class DevolucionService {
  private readonly apiUrl = `${environment.apiUrl}/devoluciones`;

  constructor(private http: HttpClient) {}

  listarDevoluciones(): Observable<{ exito: boolean; devoluciones: DevolucionDTO[] }> {
    return this.http.get<{ exito: boolean; devoluciones: DevolucionDTO[] }>(`${this.apiUrl}/`);
  }

  solicitarDevolucion(payload: SolicitudDevolucionDTO): Observable<{ exito: boolean; devolucion: DevolucionDTO }> {
    return this.http.post<{ exito: boolean; devolucion: DevolucionDTO }>(`${this.apiUrl}/solicitar`, payload);
  }
}
