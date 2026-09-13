import { Rol } from './role.model';

export type { Rol };

export interface Usuario {
  id: number;
  nombre: string;
  apellido?: string;
  email: string;
  telefono?: string;
  activo: boolean;
  rol_id?: number;
  rolid?: number;
  created_at?: string | Date;
  fechacreacion?: string | Date;
  rol?: Rol;
}

export interface UsuarioCreateDTO {
  nombre: string;
  apellido?: string;
  email: string;
  password?: string;
  telefono?: string;
  rol_id?: number;
  activo?: boolean;
}

export interface UsuarioUpdateDTO {
  nombre?: string;
  apellido?: string;
  email?: string;
  telefono?: string;
  rol_id?: number;
  activo?: boolean;
}
