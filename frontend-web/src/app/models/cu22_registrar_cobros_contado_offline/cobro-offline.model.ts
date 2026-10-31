// CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> MODEL
export interface CobroOfflineDTO {
  id: number;
  sucursal_id: number;
  monto: number;
  moneda: string;
  nro_recibo_provisional: string;
  uuid_operacion: string;
  cliente_nombre?: string;
  cliente_nit?: string;
  fecha_cobro: string;
  sincronizado: boolean;
}

export interface RegistroCobroOfflineRequest {
  sucursal_id: number;
  monto: number;
  nro_recibo_provisional: string;
  uuid_operacion?: string;
  cliente_nombre?: string;
  cliente_nit?: string;
  observaciones?: string;
}
