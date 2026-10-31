// CU21 - ADMINISTRAR PLANES DE SUSCRIPCIÓN Y TENANTS -> MODEL
export interface PlanSuscripcionDTO {
  id: number;
  nombre: string;
  descripcion?: string;
  precio_mensual: number;
  precio_anual: number;
  limite_sucursales: number;
  limite_usuarios: number;
  limite_productos: number;
  activo: boolean;
}

export interface TenantDTO {
  id: number;
  nombre: string;
  slug: string;
  activo: boolean;
  created_at: string;
}

export interface NuevoTenantRequest {
  nombre: string;
  slug: string;
  plan_id: number;
  email: string;
}
