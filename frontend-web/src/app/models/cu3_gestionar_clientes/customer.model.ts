export interface Cliente {
  id: number;
  nombre: string;
  apellido?: string;
  email: string;
  telefono?: string;
  activo: boolean;
  sucursalid?: number;
  rolid?: number;
  fechacreacion?: string;
  created_at?: string;
  total_compras?: number;
  total_reservas?: number;
}

export interface ClienteCreate {
  nombre: string;
  apellido?: string;
  email: string;
  password: string;
  telefono?: string;
  sucursalid?: number;
}

export interface ClienteUpdate {
  nombre?: string;
  apellido?: string;
  email?: string;
  telefono?: string;
  password?: string;
}

export interface HistorialCompra {
  id: number;
  codigo_orden: string;
  fecha: string;
  total: number;
  estado: string;
  total_items: number;
}

export interface HistorialReserva {
  id: number;
  codigo_reserva: string;
  fecha_reserva: string;
  estado: string;
  prenda_interes?: string;
}
