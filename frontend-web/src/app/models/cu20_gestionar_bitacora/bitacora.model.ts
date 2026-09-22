// ==============================================================================
// CU20 - GESTIONAR BITACORA Y AUDITORIA -> MODELOS TYPESCRIPT (FRONTEND)
// Ubicacion: frontend-web/src/app/models/cu20_gestionar_bitacora/bitacora.model.ts
// ==============================================================================

export interface BitacoraUsuario {
  id: number;
  nombre: string;
  apellido?: string;
  email: string;
  rol_nombre?: string;
}

export interface BitacoraEntry {
  id: number;
  usuarioid?: number;
  accion: string;
  modulo: string;
  detalle?: string;
  ip?: string;
  fechahora: string;
  datosprevios?: string;
  datosnuevos?: string;
  usuario?: BitacoraUsuario;
}

export interface BitacoraListResponse {
  total: number;
  items: BitacoraEntry[];
  limit: number;
  offset: number;
}

export interface BitacoraStats {
  total_hoy: number;
  total_semana: number;
  total_mes: number;
  modulos_distribucion: Record<string, number>;
  acciones_distribucion: Record<string, number>;
}

export interface BitacoraFilter {
  fecha_inicio?: string;
  fecha_fin?: string;
  modulo?: string;
  accion?: string;
  usuario_id?: number;
  search?: string;
  limit?: number;
  offset?: number;
}
