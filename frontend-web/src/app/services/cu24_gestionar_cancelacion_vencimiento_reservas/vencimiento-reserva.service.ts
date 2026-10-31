// CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> SERVICE
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { PurgaVencimientoResultado } from '../../models/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.model';

@Injectable({
  providedIn: 'root'
})
export class VencimientoReservaService {
  private readonly apiUrl = `${environment.apiUrl}/vencimiento-reservas`;

  constructor(private http: HttpClient) {}

  cancelarVencidas(): Observable<{ exito: boolean; resultado: PurgaVencimientoResultado }> {
    return this.http.post<{ exito: boolean; resultado: PurgaVencimientoResultado }>(`${this.apiUrl}/cancelar-vencidas`, {});
  }
}
