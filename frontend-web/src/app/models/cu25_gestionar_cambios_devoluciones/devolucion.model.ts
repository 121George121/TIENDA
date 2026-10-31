// ==============================================================================
// CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> MODELOS Y DTOs (FRONTEND)
// Ubicación: frontend-web/src/app/models/cu25_gestionar_cambios_devoluciones/devolucion.model.ts
// ==============================================================================

export interface ItemDevolucionRequest {
  variante_devuelta_id: number;
  variante_nueva_id?: number | null;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
  estado_prenda: 'PERFECTO_ESTADO' | 'DEFECTUOSO_FABRICA' | 'DAÑADO';
}

export interface SolicitudDevolucionRequest {
  venta_id: number;
  sucursal_id: number;
  cliente_id?: number | null;
  tipo_devolucion: 'CAMBIO_TALLA' | 'CAMBIO_PRENDA' | 'REEMBOLSO_TOTAL' | 'NOTA_CREDITO';
  motivo: string;
  monto_reembolso: number;
  items: ItemDevolucionRequest[];
}

export interface ValidarVentaDevolucionResponse {
  venta_valida: boolean;
  venta_id: number;
  codigoventa: string;
  fecha_venta: string;
  dias_transcurridos: number;
  dentro_de_plazo: boolean;
  plazo_maximo_dias: number;
  cliente_nombre: string;
  sucursal_nombre: string;
  total_venta: number;
  items_comprados: {
    variante_id: number;
    sku: string;
    producto_nombre: string;
    talla: string;
    color: string;
    cantidad_comprada: number;
    precio_unitario: number;
    subtotal: number;
  }[];
  mensaje?: string;
}

export interface DetalleDevolucionItem {
  id: number;
  variante_devuelta_id: number;
  variante_devuelta_sku?: string;
  producto_devuelto_nombre: string;
  talla_devuelta?: string;
  color_devuelto?: string;
  variante_nueva_id?: number;
  variante_nueva_sku?: string;
  producto_nuevo_nombre?: string;
  talla_nueva?: string;
  color_nueva?: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
  estado_prenda: string;
}

export interface DevolucionResponse {
  id: number;
  codigo_devolucion: string;
  tenant_id: number;
  venta_id: number;
  codigoventa?: string;
  cliente_id?: number;
  cliente_nombre?: string;
  usuario_id?: number;
  usuario_nombre?: string;
  sucursal_id: number;
  sucursal_nombre?: string;
  tipo_devolucion: string;
  motivo: string;
  estado: string;
  monto_reembolso: number;
  reingreso_inventario: boolean;
  fecha_solicitud: string;
  fecha_resolucion?: string;
  detalles: DetalleDevolucionItem[];
}

export interface DevolucionKpisDTO {
  total_operaciones: number;
  cambios_talla_prenda: number;
  reembolsos_notas_credito: number;
  prendas_aptas_reincorporadas: number;
  prendas_baja_defecto: number;
  monto_total_reembolsado_bob: number;
  plazo_garantia_dias: number;
}
