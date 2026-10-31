// CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> MODEL
export interface DevolucionDTO {
  id: number;
  codigo_devolucion: string;
  venta_id: number;
  sucursal_id: number;
  tipo_devolucion: string;
  motivo: string;
  estado: string;
  monto_reembolso: number;
  fecha_solicitud: string;
}

export interface SolicitudDevolucionDTO {
  venta_id: number;
  sucursal_id: number;
  tipo_devolucion: string;
  motivo: string;
  monto_reembolso: number;
  items: Array<{
    variante_devuelta_id: number;
    variante_nueva_id?: number;
    cantidad: number;
    precio_unitario: number;
    subtotal: number;
    estado_prenda?: string;
  }>;
}
