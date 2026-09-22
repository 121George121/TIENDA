// ==============================================================================
// CU16 - GESTIONAR PAGOS Y COMPROBANTES -> CAPA MODELO (MVC)
// Ubicación: frontend-web/src/app/models/cu16_gestionar_pagos_comprobantes/pago.model.ts
// ==============================================================================

export interface MetodoPago {
  id: number;
  nombre: string;
  icono: string;
  descripcion: string;
  activo: boolean;
}

export interface IniciarPagoRequest {
  venta_id: number;
  metodo_id: number;
  return_url?: string;
  cancel_url?: string;
}

export interface IniciarPagoResponse {
  metodo: string;
  requiere_redireccion: boolean;
  url_redireccion?: string;
  token?: string;
  qr_image?: string;
  codigo_pago?: string;
  cuenta_bancaria?: string;
  titular?: string;
  tiempo_expiracion_minutos?: number;
  referencia?: string;
  monto_total: number;
  monto_usd?: number;
  mensaje: string;
}

export interface ComprobantePago {
  id: number;
  venta_id: number;
  numero_factura: string;
  codigo_autorizacion: string;
  fecha_emision: string;
  monto_total: number;
  metodo_pago: string;
  cliente_nombre: string;
  cliente_nit_ci: string;
  qr_comprobante?: string;
  items: {
    producto: string;
    cantidad: number;
    precio_unitario: number;
    subtotal: number;
  }[];
}
