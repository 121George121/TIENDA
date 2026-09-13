export interface MetodoPago {
  id: number;
  nombre: string;
  estado: boolean;
}

export interface VentaItemDTO {
  producto_id: number;
  cantidad: number;
  variante_id?: number;
}

export interface VentaPresencialCreateDTO {
  sucursal_id: number;
  cliente_id?: number;
  cliente_nombre?: string;
  metodo_pago_id: number;
  monto_recibido?: number;
  items: VentaItemDTO[];
}

export interface VentaCompleta {
  id: number;
  codigoventa: string;
  tipoventa: 'Presencial' | 'Digital' | string;
  estado: string;
  subtotal: number;
  descuento: number;
  total: number;
  fecha: string;
  sucursalid: number;
  sucursal_nombre?: string;
  cliente_nombre?: string;
  metodo_pago_nombre?: string;
  cambio?: number;
}

export interface VentaDetalleItem {
  variante_id: number;
  producto_nombre: string;
  talla?: string;
  color?: string;
  cantidad: number;
  preciounitario: number;
  descuento: number;
  subtotal: number;
}

export interface VentaDetallada extends VentaCompleta {
  detalles: VentaDetalleItem[];
}
