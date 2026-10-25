// ==============================================================================
// MODELO (MVC - MODEL)
// Módulo: CU7 - Proveedores y Productos Suministrados
// Ubicación: frontend-web/src/app/models/cu7_gestionar_proveedores_productos_suministrados/proveedor.model.ts
// ==============================================================================

import { Producto } from '../cu5_gestionar_productos/product.model';

export interface ProductoProveedor {
  idproducto: number;
  idproveedor: number;
  costocompra?: number;
  cantidad?: number;
  producto?: Producto;
}

export interface Proveedor {
  id: number;
  tenant_id?: number;
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

// Aliases de compatibilidad
export type Supplier = Proveedor;
export type SupplierCreateDTO = ProveedorCreateDTO;
export type SupplierUpdateDTO = ProveedorUpdateDTO;
