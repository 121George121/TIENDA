export interface Sucursal {
  id: number;
  nombre: str;
  ciudad?: str;
  direccion?: str;
  telefono?: str;
  latitud?: number;
  longitud?: number;
  activo: boolean;
  fechacreacion?: string;
}

export type str = string;

export interface SucursalCreateDTO {
  nombre: string;
  ciudad?: string;
  direccion?: string;
  telefono?: string;
  latitud?: number;
  longitud?: number;
  activo?: boolean;
}

export interface SucursalUpdateDTO {
  nombre?: string;
  ciudad?: string;
  direccion?: string;
  telefono?: string;
  latitud?: number;
  longitud?: number;
  activo?: boolean;
}
