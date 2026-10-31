// ==============================================================================
// CAPA MODELO (MVC - MODEL EN ANGULAR)
// Módulo: CU12 - Utilizar Vestidor Virtual mediante IA
// Ubicación: frontend-web/src/app/models/cu12_vestidor_virtual_ia/vestidor.model.ts
// ==============================================================================

export interface AnalisisFisonomiaResponse {
  contextura_detectada: string;
  talla_recomendada: string;
  porcentaje_calce: number;
  caida_prenda: string;
  consejo_estilista: string;
  compatibilidad_color: string;
  ajuste_sugerido_escala?: number;
  fuente?: string;
}

export interface TryOnResponse {
  status: 'success' | 'error';
  imagen_base64: string;
  motor: string;
  talla_aplicada: string;
  color_aplicado: string;
  calidad: string;
  mensaje: string;
}

export interface PrendaProbador {
  id: number;
  nombre: string;
  marca?: string;
  precio: number;
  imagen_url: string;
  talla_seleccionada: string;
  color_seleccionado: string;
  codigo_hex?: string;
  variante_id?: number;
}
