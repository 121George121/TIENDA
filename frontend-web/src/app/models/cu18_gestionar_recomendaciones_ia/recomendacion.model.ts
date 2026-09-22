// ==============================================================================
// CU18 - GESTIONAR RECOMENDACIONES MEDIANTE IA -> CAPA MODELO (MVC)
// Ubicación: frontend-web/src/app/models/cu18_gestionar_recomendaciones_ia/recomendacion.model.ts
// ==============================================================================

export interface RecomendacionOutfit {
  producto_id: number;
  nombre: string;
  precio: number;
  imagen_url?: string;
  razon_estilo: string;
  afinidad_porcentaje: number;
  fuente: string;
}

export interface TendenciaModa {
  producto_id: number;
  nombre: string;
  precio: number;
  imagen_url?: string;
  etiqueta: string;
  razon: string;
}

export interface RecomendacionRequest {
  producto_id?: number;
  carrito_ids?: number[];
  limite?: number;
}
