// ==============================================================================
// CAPA SERVICIO (DATA ACCESS / API CLIENT)
// Módulo: CU1 - Gestionar Autenticación
// Ubicación: frontend-web/src/app/services/cu1_gestionar_autenticacion/auth.service.ts
// ==============================================================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  CredencialesLoginDTO,
  RespuestaAutenticacionDTO,
  RegistroUsuarioDTO,
  VerificacionOtpDTO,
  RecuperacionContraseniaDTO,
  RestablecerContraseniaDTO
} from '../../models/cu1_gestionar_autenticacion/auth.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;

  constructor(private http: HttpClient) {}

  /**
   * Inicia sesión enviando credenciales y ámbito opcional de tenant vía JSON
   */
  iniciarSesion(email: string, password: string, tenantSlug?: string): Observable<RespuestaAutenticacionDTO> {
    const payload: CredencialesLoginDTO = {
      email: email.trim().toLowerCase(),
      password: (password || '').trim(),
      tenant_slug: tenantSlug ? tenantSlug.trim() : undefined
    };
    return this.http.post<RespuestaAutenticacionDTO>(`${this.apiUrl}/login/json`, payload);
  }

  /**
   * Registra un nuevo usuario/cliente en el sistema
   */
  registrarUsuario(datos: RegistroUsuarioDTO): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/registro`, datos);
  }

  /**
   * Valida el código de verificación OTP enviado al usuario
   */
  verificarCodigoOtp(email: string, codigo: string): Observable<any> {
    const payload: VerificacionOtpDTO = {
      email: email.trim().toLowerCase(),
      codigo: codigo.trim()
    };
    return this.http.post<any>(`${this.apiUrl}/verificar-codigo`, payload);
  }

  /**
   * Solicita el restablecimiento de contraseña mediante correo
   */
  solicitarRecuperacionContrasenia(email: string): Observable<any> {
    const payload: RecuperacionContraseniaDTO = {
      email: email.trim().toLowerCase()
    };
    return this.http.post<any>(`${this.apiUrl}/recuperar-password`, payload);
  }

  /**
   * Restablece la contraseña utilizando el token firmado
   */
  restablecerContrasenia(token: string, nuevaContrasenia: string): Observable<any> {
    const payload: RestablecerContraseniaDTO = {
      token: token.trim(),
      new_password: nuevaContrasenia
    };
    return this.http.post<any>(`${this.apiUrl}/reset-password`, payload);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  login(email: string, password: string): Observable<RespuestaAutenticacionDTO> {
    return this.iniciarSesion(email, password);
  }

  registro(datos: RegistroUsuarioDTO): Observable<any> {
    return this.registrarUsuario(datos);
  }

  verificarCodigo(email: string, codigo: string): Observable<any> {
    return this.verificarCodigoOtp(email, codigo);
  }

  requestPasswordRecovery(email: string): Observable<any> {
    return this.solicitarRecuperacionContrasenia(email);
  }

  resetPassword(token: string, newPassword: string): Observable<any> {
    return this.restablecerContrasenia(token, newPassword);
  }
}
