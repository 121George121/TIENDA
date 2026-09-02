// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FRONTEND ANGULAR)
// Representación de las entidades de datos recibidas desde la API FastAPI
// ==============================================================================

export interface Producto {
  id: number;
  nombre: string;
  descripcion?: string;
  precio: number;
  stock: number;
  categoria_id?: number;
  imagen_url?: string;
  activo: boolean;
}

export interface Categoria {
  id: number;
  nombre: string;
  descripcion?: string;
}
