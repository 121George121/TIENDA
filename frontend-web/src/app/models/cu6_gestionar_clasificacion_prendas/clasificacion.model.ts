export interface Categoria {
  id: number;
  nombre: string;
  descripcion?: string;
  activo: boolean;
}

export interface Temporada {
  id: number;
  nombre: string;
  descripcion?: string;
  fechainicio?: string;
  fechafin?: string;
  activo: boolean;
}

export interface Coleccion {
  id: number;
  nombre: string;
  descripcion?: string;
  imagenurl?: string;
  temporadaid?: number;
  temporada?: Temporada;
  activo: boolean;
}
