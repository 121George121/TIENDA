// ==============================================================================
// CU23 - SINCRONIZAR OPERACIONES OFFLINE -> MODELOS Y DTOs (FRONTEND)
// Ubicación: frontend-web/src/app/models/cu23_sincronizar_operaciones_offline/sincronizacion-offline.model.ts
// ==============================================================================

export interface SyncOperacionItem {
  uuid_operacion: string;
  tipo: string;
  sucursal_id?: number;
  payload: any;
  fecha_operacion?: string;
}

export interface SyncResultadoOperacion {
  uuid_operacion: string;
  tipo: string;
  estado: string; // SINCRONIZADO, CONFLICTO_RESUELTO, ERROR, DUPLICADO_IGNORADO, CONFLICTO_PENDIENTE
  mensaje: string;
  venta_id?: number;
  nro_recibo?: string;
  conflicto_detectado: boolean;
  estrategia_aplicada?: string;
}

export interface SyncLoteResponse {
  total: number;
  procesadas: number;
  sincronizadas: number;
  conflictos_resueltos: number;
  errores: number;
  resultados: SyncResultadoOperacion[];
}

export interface SyncLogDTO {
  id: number;
  tenant_id: number;
  usuario_id?: number;
  usuario_nombre?: string;
  sucursal_id: number;
  sucursal_nombre?: string;
  tipo_operacion: string;
  uuid_operacion: string;
  estado: string;
  estrategia_conflicto?: string;
  reintentos: number;
  error_detalle?: string;
  fecha_operacion_origen: string;
  fecha_recibido?: string;
  fecha_procesado?: string;
  payload?: any;
}

export interface SyncKpisDTO {
  total_operaciones: number;
  sincronizadas: number;
  conflictos_resueltos: number;
  errores: number;
  cobros_pendientes_en_cola: number;
  monto_pendiente_en_cola: number;
  estado_motor: string;
}

export interface SincronizarPendientesRequest {
  sucursal_id?: number;
  estrategia_preferida: string;
}

export interface ResolverConflictoRequest {
  estrategia: string;
  notas?: string;
}
