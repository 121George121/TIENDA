// CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> MODEL
export interface PurgaVencimientoResultado {
  reservas_vencidas_canceladas: number;
  prendas_liberadas_al_stock: number;
  fecha_ejecucion: string;
}
