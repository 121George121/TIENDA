// CU23 - SINCRONIZAR OPERACIONES OFFLINE -> MODEL
export interface SyncOperacionItem {
  uuid_operacion: string;
  tipo: string;
  payload: any;
}

export interface SyncLogDTO {
  id: number;
  tipo_operacion: string;
  uuid_operacion: string;
  estado: string;
  estrategia_conflicto?: string;
  reintentos: number;
  fecha_recibido: string;
}
