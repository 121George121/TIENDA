// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FRONTEND ANGULAR)
// Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
// Ubicación: frontend-web/src/app/models/cu8_consultar_catalogo_disponibilidad/inventory.model.ts
// ==============================================================================

export interface SucursalItem {
  id: number;
  nombre: string;
  ciudad?: string;
  direccion?: string;
  telefono?: string;
}

export interface DisponibilidadVariante {
  variante_id: number;
  sku?: string;
  talla?: string;
  color?: string;
  codigohex?: string;
  precio: number;
  stock: number;
  disponible: boolean;
}

export interface DisponibilidadSucursalDetalle {
  sucursal_id: number;
  sucursal_nombre: string;
  ciudad?: string;
  direccion?: string;
  telefono?: string;
  stock_total: number;
  variantes: DisponibilidadVariante[];
}

export interface DisponibilidadProducto {
  producto_id: number;
  producto_nombre: string;
  marca?: string;
  preciobase: number;
  imagenprincipal?: string;
  sucursales: DisponibilidadSucursalDetalle[];
}

export interface ProductoCatalogoItem {
  id: number;
  nombre: string;
  descripcion?: string;
  marca?: string;
  genero?: string;
  preciobase: number;
  imagenprincipal?: string;
  categoria_id?: number;
  categoria_nombre?: string;
  stock_sucursal: number;
  stock_total: number;
  disponible: boolean;
  variantes: DisponibilidadVariante[];
}
