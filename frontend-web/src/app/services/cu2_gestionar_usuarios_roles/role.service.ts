import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Rol, RolCreateDTO } from '../../models/cu2_gestionar_usuarios_roles/role.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RoleService {
  private apiUrl = `${environment.apiUrl}/roles`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista completa de roles del sistema.
   */
  obtenerRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(this.apiUrl);
  }

  /**
   * Obtiene el detalle de un rol por su ID.
   */
  obtenerRolPorId(id: number): Observable<Rol> {
    return this.http.get<Rol>(`${this.apiUrl}/${id}`);
  }

  /**
   * Registra un nuevo rol con su respectiva matriz de permisos.
   */
  crearRol(role: RolCreateDTO): Observable<Rol> {
    return this.http.post<Rol>(this.apiUrl, role);
  }

  /**
   * Actualiza los datos de un rol.
   */
  actualizarRol(id: number, role: RolCreateDTO): Observable<Rol> {
    return this.http.put<Rol>(`${this.apiUrl}/${id}`, role);
  }

  /**
   * Actualiza la lista de permisos asignados a un rol.
   */
  actualizarPermisosRol(id: number, permisos: string[]): Observable<Rol> {
    return this.http.put<Rol>(`${this.apiUrl}/${id}/permisos`, { permisos });
  }

  /**
   * Elimina un rol del sistema si no tiene usuarios asociados.
   */
  eliminarRol(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD (EVITA REGRESIONES)
  // ============================================================================
  getRoles(): Observable<Rol[]> {
    return this.obtenerRoles();
  }

  getRoleById(id: number): Observable<Rol> {
    return this.obtenerRolPorId(id);
  }

  createRole(role: RolCreateDTO): Observable<Rol> {
    return this.crearRol(role);
  }

  updateRole(id: number, role: RolCreateDTO): Observable<Rol> {
    return this.actualizarRol(id, role);
  }

  updateRolePermissions(id: number, permisos: string[]): Observable<Rol> {
    return this.actualizarPermisosRol(id, permisos);
  }

  deleteRole(id: number): Observable<any> {
    return this.eliminarRol(id);
  }
}

export { RoleService as RolService };
