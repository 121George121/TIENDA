// ==============================================================================
// CU17 - CONSULTAR HISTORIAL DE COMPRAS Y RESERVAS -> CAPA MODELO (MVC)
// Ubicación: frontend-web/src/app/models/cu17_consultar_historial_compras_reservas/historial.model.ts
// ==============================================================================

export interface TrackingStep {
  paso: number;
  titulo: string;
  fecha: string;
  completado: boolean;
}

export interface DetalleItemCompra {
  id: number;
  producto: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
  imagen_url?: string;
}

export interface CompraHistorial {
  id: number;
  codigo_venta: string;
  tipo_venta: string;
  estado: string;
  total: number;
  fecha: string;
  sucursal: string;
  metodo_pago: string;
  tracking: TrackingStep[];
  items_count: number;
  items: DetalleItemCompra[];
  comprobante_url: string;
}

export interface ReservaHistorial {
  id: number;
  codigo_reserva: string;
  estado: string;
  total_estimado: number;
  fecha_reserva: string;
  fecha_limite: string;
  horas_restantes: number;
  sucursal_nombre: string;
  sucursal_direccion: string;
  qr_retiro: string;
  items: DetalleItemCompra[];
}

export interface ResumenCliente {
  cliente_nombre: string;
  total_pedidos: number;
  total_invertido_bs: number;
  total_reservas: number;
  reservas_activas: number;
}
