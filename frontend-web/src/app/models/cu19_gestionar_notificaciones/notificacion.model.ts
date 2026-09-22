// ==============================================================================
// CU19 - GESTIONAR NOTIFICACIONES -> CAPA MODELO (MVC)
// Ubicación: frontend-web/src/app/models/cu19_gestionar_notificaciones/notificacion.model.ts
// ==============================================================================

export interface NotificacionItem {
  id: number;
  titulo: string;
  mensaje: string;
  tipo: 'pedido' | 'reserva' | 'stock' | 'sistema' | string;
  leido: boolean;
  enlace?: string;
  fecha: string;
}

export type TipoNotificacionFiltro = 'todas' | 'no_leidas' | 'pedidos' | 'reservas';
