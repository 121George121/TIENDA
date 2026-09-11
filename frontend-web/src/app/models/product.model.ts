import { Categoria } from './clasificacion.model';

export interface Producto {
  id: number;
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
