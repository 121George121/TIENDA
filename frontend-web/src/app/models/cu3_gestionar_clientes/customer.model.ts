export interface Cliente {
  id: number;
  nombre: string;
  apellido?: string;
  email: string;
  telefono?: string;
  activo: boolean;
  sucursalid?: number;
  rolid?: number;
  rol_id?: number;
  fechacreacion?: string;
  created_at?: string;
  fechanac?: string;
  genero?: string;
  total_ordenes?: number;
  total_gastado?: number;
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
  activo?: boolean;
  fechanac?: string;
  genero?: string;
}

export interface HistorialCompra {
  id: number;
  codigo_orden?: string;
  fecha?: string;
  created_at?: string;
  total: number;
  estado: string;
  total_items?: number;
  direccion_envio?: string;
}

export interface HistorialReserva {
  id: number;
  cliente_id?: number;
  codigo_reserva: string;
  fecha_reserva: string;
  estado: string;
  total_estimado?: number;
  notas?: string;
  prenda_interes?: string;
}

// Aliases de compatibilidad
export type Customer = Cliente;
export type CustomerCreate = ClienteCreate;
export type CustomerUpdate = ClienteUpdate;
