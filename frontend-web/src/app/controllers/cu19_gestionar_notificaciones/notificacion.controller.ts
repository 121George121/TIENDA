// ==============================================================================
// CU19 - GESTIONAR NOTIFICACIONES -> CAPA CONTROLADOR (MVC)
// Ubicación: frontend-web/src/app/controllers/cu19_gestionar_notificaciones/notificacion.controller.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { NotificacionService, NotificacionDTO } from '../../services/cu19_gestionar_notificaciones/notificacion.service';

@Injectable({
  providedIn: 'root'
})
export class NotificacionController {
  public notificaciones$: Observable<NotificacionDTO[]>;
  public noLeidasCount$: Observable<number>;

  constructor(private service: NotificacionService) {
    this.notificaciones$ = this.service.notificaciones$;
    this.noLeidasCount$ = this.service.noLeidas$;
  }

  public cargarNotificaciones(): void {
    this.service.cargarNotificaciones();
  }

  public marcarComoLeida(id: number): void {
    this.service.marcarLeida(id).subscribe();
  }

  public marcarTodasComoLeidas(): void {
    this.service.marcarTodasLeidas().subscribe();
  }
}
