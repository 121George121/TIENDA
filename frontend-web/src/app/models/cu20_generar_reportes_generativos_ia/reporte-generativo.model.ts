// ==============================================================================
// CU20 - GENERAR REPORTES GENERATIVOS CON IA -> MODELOS (MVC - MODEL)
// Ubicación: frontend-web/src/app/models/cu20_generar_reportes_generativos_ia/reporte-generativo.model.ts
// ==============================================================================

export interface ReporteKPI {
  etiqueta: string;
  valor: string;
  variacion: string;
  tipo: 'positivo' | 'alerta' | 'neutral';
}

export interface ReporteDataset {
  label: string;
  data: number[];
  backgroundColor?: string[];
  borderColor?: string;
}

export interface ReporteGrafico {
  labels: string[];
  datasets: ReporteDataset[];
}

export interface ReporteGenerativoData {
  id?: number;
  titulo: string;
  resumen_ejecutivo: string;
  kpis: ReporteKPI[];
  tipo_grafico_sugerido: 'BAR' | 'LINE' | 'PIE' | 'DOUGHNUT';
  grafico: ReporteGrafico;
  tabla_columnas: string[];
  tabla_filas: string[][];
  recomendaciones_estrategicas: string[];
  fecha_generacion?: string;
  modelo_usado?: string;
  es_favorito?: boolean;
}

export interface ConsultaIAPrompt {
  prompt: string;
  filtros?: string;
}

export interface ConsultaSugerida {
  icono: string;
  titulo: string;
  prompt: string;
}

export interface HistorialReporteItem {
  id: number;
  titulo: string;
  prompt: string;
  fecha: string;
  tipo_grafico: string;
  es_favorito: boolean;
  modelo: string;
}
