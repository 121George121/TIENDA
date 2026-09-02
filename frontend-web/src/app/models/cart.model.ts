// ==============================================================================
// CAPA MODELO (MVC - MODEL EN ANGULAR)
// Estructuras de datos para el Carrito de Compras
// ==============================================================================

import { Producto } from './product.model';

export interface CartItem {
  producto: Producto;
  cantidad: number;
  subtotal: number;
}

export interface OrdenRequest {
  direccion_envio: string;
  items: {
    producto_id: number;
    cantidad: number;
  }[];
}
