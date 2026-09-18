// ==============================================================================
// CU19 - GESTIONAR NOTIFICACIONES -> SERVICIO ANGULAR
// Ubicación: frontend-web/src/app/services/cu19_gestionar_notificaciones/notificacion.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';

export interface NotificacionDTO {
  id: number;
  titulo: string;
  mensaje: string;
  tipo: string;
  leido: boolean;
  enlace?: string;
  fecha: string;
}

@Injectable({
  providedIn: 'root'
})
export class NotificacionService {
  private readonly apiUrl = 'http://localhost:8000/api/v1/notificaciones';

  private notificacionesSubject = new BehaviorSubject<NotificacionDTO[]>([]);
  public notificaciones$ = this.notificacionesSubject.asObservable();

  private noLeidasSubject = new BehaviorSubject<number>(0);
  public noLeidas$ = this.noLeidasSubject.asObservable();

  constructor(private http: HttpClient) {}

  cargarNotificaciones(): void {
    this.http.get<NotificacionDTO[]>(this.apiUrl).subscribe({
      next: (data) => {
        this.notificacionesSubject.next(data);
        const count = data.filter(n => !n.leido).length;
        this.noLeidasSubject.next(count);
      },
      error: (e) => console.warn('Error al cargar notificaciones:', e)
    });
  }

  marcarLeida(id: number): Observable<any> {
    return this.http.patch(`${this.apiUrl}/${id}/leer`, {}).pipe(
      tap(() => this.cargarNotificaciones())
    );
  }

  marcarTodasLeidas(): Observable<any> {
    return this.http.post(`${this.apiUrl}/marcar-todas-leidas`, {}).pipe(
      tap(() => this.cargarNotificaciones())
    );
  }
}
