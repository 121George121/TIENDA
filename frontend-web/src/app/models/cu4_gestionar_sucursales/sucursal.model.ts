export interface Sucursal {
  id: number;
  tenant_id?: number;
  nombre: string;
  ciudad?: string;
  direccion?: string;
  telefono?: string;
  latitud?: number;
  longitud?: number;
  activo: boolean;
  fechacreacion?: string;
}

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

// Aliases de compatibilidad
export type Branch = Sucursal;
export type BranchCreateDTO = SucursalCreateDTO;
export type BranchUpdateDTO = SucursalUpdateDTO;
