// ==============================================================================
// MODELO (MVC - MODEL)
// Módulo: CU6 - Clasificación de Prendas (Categorías, Temporadas, Colecciones)
// Ubicación: frontend-web/src/app/models/cu6_gestionar_clasificacion_prendas/clasificacion.model.ts
// ==============================================================================

export interface Categoria {
  id: number;
  tenant_id?: number;
  nombre: string;
  descripcion?: string;
  activo: boolean;
}

export interface CategoriaCreateDTO {
  nombre: string;
  descripcion?: string;
  activo?: boolean;
}

export interface CategoriaUpdateDTO {
  nombre?: string;
  descripcion?: string;
  activo?: boolean;
}

export interface Temporada {
  id: number;
  tenant_id?: number;
  nombre: string;
  descripcion?: string;
  fechainicio?: string;
  fechafin?: string;
  activo: boolean;
}

export interface TemporadaCreateDTO {
  nombre: string;
  descripcion?: string;
  fechainicio?: string;
  fechafin?: string;
  activo?: boolean;
}

export interface TemporadaUpdateDTO {
  nombre?: string;
  descripcion?: string;
  fechainicio?: string;
  fechafin?: string;
  activo?: boolean;
}

export interface Coleccion {
  id: number;
  tenant_id?: number;
  nombre: string;
  descripcion?: string;
  imagenurl?: string;
  temporadaid?: number;
  temporada?: Temporada;
  activo: boolean;
}

export interface ColeccionCreateDTO {
  nombre: string;
  descripcion?: string;
  imagenurl?: string;
  temporadaid?: number;
  activo?: boolean;
}

export interface ColeccionUpdateDTO {
  nombre?: string;
  descripcion?: string;
  imagenurl?: string;
  temporadaid?: number;
  activo?: boolean;
}

// Aliases de compatibilidad
export type Category = Categoria;
export type Season = Temporada;
export type Collection = Coleccion;
