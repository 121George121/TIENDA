// ==============================================================================
// CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> MODELOS Y DTOs (FRONTEND)
// Ubicación: frontend-web/src/app/models/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento-reserva.model.ts
// ==============================================================================

export interface PurgaVencimientoResultado {
  reservas_vencidas_canceladas: number;
  prendas_liberadas_al_stock: number;
  valor_monetario_liberado_bob: number;
  fecha_ejecucion: string;
  detalles?: {
    reserva_id: number;
    codigo: string;
    prendas_liberadas: number;
    monto_estimado_bob: number;
  }[];
}

export interface ReservaPrendaDetalleDTO {
  variante_id: number;
  sku?: string;
  producto_nombre: string;
  talla?: string;
  color?: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
}

export interface ReservaExpiracionItem {
  id: number;
  codigoreserva: string;
  fechareserva: string;
  fecha_expiracion: string;
  horas_restantes: number;
  en_riesgo: boolean;
  es_expirada: boolean;
  estado: string;
  observaciones?: string;
  sucursalid: number;
  sucursal_nombre: string;
  clienteid: number;
  cliente_nombre: string;
  cliente_email?: string;
  total_prendas: number;
  monto_total_estimado: number;
  detalles: ReservaPrendaDetalleDTO[];
}

export interface VencimientoReservaKpisDTO {
  total_reservas_activas: number;
  reservas_en_riesgo: number;
  reservas_vencidas_historicas: number;
  reservas_canceladas_manual: number;
  total_prendas_reintegradas: number;
  valor_total_liberado_bob: number;
  horas_politica_defecto: number;
}

export interface CancelarReservaRequest {
  motivo: string;
}

export interface EjecutarPurgaRequest {
  horas_limite: number;
  sucursal_id?: number;
}
