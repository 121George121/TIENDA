import { Categoria } from '../cu6_gestionar_clasificacion_prendas/clasificacion.model';

export interface Producto {
  id: number;
  tenant_id?: number;
  nombre: string;
  descripcion?: string;
  marca?: string;
  genero?: string;
  grupoedad?: string;
  preciobase: number;
  imagenprincipal?: string;
  categoriaid?: number;
  categoria?: Categoria;
  activo: boolean;
  fechacreacion?: string;
  fechaactualizacion?: string;
}

export interface ProductoCreateDTO {
  nombre: string;
  descripcion?: string;
  marca?: string;
  genero?: string;
  grupoedad?: string;
  preciobase: number;
  imagenprincipal?: string;
  categoriaid?: number;
  activo?: boolean;
}

export interface ProductoUpdateDTO {
  nombre?: string;
  descripcion?: string;
  marca?: string;
  genero?: string;
  grupoedad?: string;
  preciobase?: number;
  imagenprincipal?: string;
  categoriaid?: number;
  activo?: boolean;
}

// Aliases de compatibilidad
export type Product = Producto;
export type ProductCreateDTO = ProductoCreateDTO;
export type ProductUpdateDTO = ProductoUpdateDTO;
