import { Producto } from './product.model';

export interface ProductoProveedor {
  idproducto: number;
  idproveedor: number;
  costocompra?: number;
  cantidad?: number;
  producto?: Producto;
}

export interface Proveedor {
  id: number;
  nombre: string;
  razonsocial?: string;
  nit?: string;
  contacto?: string;
  telefono?: string;
  email?: string;
  direccion?: string;
  activo: boolean;
  fechacreacion?: string;
  productos_suministrados?: ProductoProveedor[];
}

export interface ProveedorCreateDTO {
  nombre: string;
  razonsocial?: string;
  nit?: string;
  contacto?: string;
  telefono?: string;
  email?: string;
  direccion?: string;
  activo?: boolean;
}

export interface ProveedorUpdateDTO {
  nombre?: string;
  razonsocial?: string;
  nit?: string;
  contacto?: string;
  telefono?: string;
  email?: string;
  direccion?: string;
  activo?: boolean;
}
