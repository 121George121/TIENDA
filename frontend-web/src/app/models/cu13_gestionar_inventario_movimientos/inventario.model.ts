export interface InventarioItem {
  id: number;
  sucursal_id: number;
  sucursal_nombre: string;
  variante_id: number;
  producto_id: number;
  producto_nombre: string;
  producto_marca?: string;
  producto_precio: number;
  color_nombre?: string;
  color_hex?: string;
  talla_nombre?: string;
  color?: string;
  talla?: string;
  imagen_url?: string;
  sku?: string;
  stockfisico: number;
  stockreservado: number;
  stockdisponible?: number;
  stockminimo: number;
  bajo_stock?: boolean;
  estado_stock: 'NORMAL' | 'BAJO_STOCK' | 'AGOTADO' | string;
  fechaactualizacion?: string;
}

export interface MovimientoInventarioCreateDTO {
  tipomovimiento: 'Entrada' | 'Salida' | 'Ajuste' | string;
  cantidad: number;
  motivo?: string;
  referencia?: string;
}

export interface MovimientoInventarioItem {
  id: number;
  tipomovimiento: string;
  cantidad: number;
  motivo?: string;
  referencia?: string;
  fecha: string;
  fechahora?: string;
  stockresultante?: number;
  usuario_nombre?: string;
}

export interface TrasladoStockDTO {
  sucursal_destino_id: number;
  cantidad: number;
  motivo?: string;
  referencia?: string;
}

export interface TrasladoStockResponseDTO {
  mensaje: string;
  inventario_origen_id: number;
  inventario_destino_id: number;
  sucursal_origen_id: number;
  sucursal_destino_id: number;
  sucursal_origen_nombre?: string;
  sucursal_destino_nombre?: string;
  cantidad_trasladada: number;
  stock_origen_restante: number;
  stock_destino_actual: number;
}

