// ==============================================================================
// CAPA MODELO (MVC - MODEL)
// Módulo: CU1 - Gestionar Autenticación (Multi-Tenant SaaS)
// Ubicación: frontend-web/src/app/models/cu1_gestionar_autenticacion/auth.model.ts
// ==============================================================================

export interface CredencialesLoginDTO {
  email: string;
  password: string;
  tenant_slug?: string;
}

export interface UsuarioDTO {
  id: number;
  nombre: string;
  apellido?: string;
  email: string;
  telefono?: string;
  rol?: string;
  rol_id?: number;
  rolid?: number;
  tenant_id?: number;
  tenant_slug?: string;
  tenant_nombre?: string;
  activo?: boolean;
  verificado?: boolean;
  sucursales?: number[];
}

export interface TenantSesionDTO {
  id: number;
  slug: string;
  nombre: string;
}

export interface RespuestaAutenticacionDTO {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  rol?: string;
  tenant_id?: number;
  tenant_slug?: string;
  tenant_nombre?: string;
  usuario?: UsuarioDTO;
  // Compatibilidad con código previo que leía 'user'
  user?: UsuarioDTO;
}

export interface RegistroUsuarioDTO {
  nombre: string;
  apellido?: string;
  email: string;
  password: string;
  telefono?: string;
  tenant_id?: number;
  tenant_slug?: string;
}

export interface VerificacionOtpDTO {
  email: string;
  codigo: string;
}

export interface RecuperacionContraseniaDTO {
  email: string;
}

export interface RestablecerContraseniaDTO {
  token: string;
  new_password: string;
}

// ==============================================================================
// ALIASES DE COMPATIBILIDAD (EVITA ROMPER IMPORTACIONES EXISTENTES)
// ==============================================================================
export type LoginRequestDTO = CredencialesLoginDTO;
export type LoginResponseDTO = RespuestaAutenticacionDTO;
export type PasswordRecoveryDTO = RecuperacionContraseniaDTO;
export type PasswordResetDTO = RestablecerContraseniaDTO;
