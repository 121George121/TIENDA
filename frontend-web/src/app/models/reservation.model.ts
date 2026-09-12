// ==============================================================================
// CAPA MODELO (MVC - MODEL EN ANGULAR)
// Módulo: CU10 - Gestionar Reservas de Prendas
// Ubicación: frontend-web/src/app/models/reservation.model.ts
// ==============================================================================

export interface ReservaDetalle {
  variante_id: number;
  producto_nombre: string;
  talla?: string;
  color?: string;
  codigo_hex?: string;
  imagen_url?: string;
  precio_unitario: number;
  cantidad: number;
  subtotal: number;
}

export interface ReservaSucursal {
  id: number;
  nombre: string;
  ciudad?: string;
  direccion?: string;
  telefono?: string;
}

export interface Reserva {
  id: number;
  codigo_reserva: string;
  fecha_reserva: string;
  estado: 'PENDIENTE' | 'CONFIRMADA' | 'ENTREGADA' | 'CANCELADA' | 'EXPIRADA' | string;
  observaciones?: string;
  sucursal?: ReservaSucursal;
  detalles: ReservaDetalle[];
  total_items: number;
  total_estimado: number;
}

export interface CrearReservaDTO {
  sucursal_id?: number;
  observaciones?: string;
}

export interface CancelarReservaDTO {
  motivo?: string;
}
