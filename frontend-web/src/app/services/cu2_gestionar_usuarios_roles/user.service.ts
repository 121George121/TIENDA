import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Usuario, UsuarioCreateDTO, UsuarioUpdateDTO } from '../../models/cu2_gestionar_usuarios_roles/user.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = `${environment.apiUrl}/usuarios`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de usuarios filtrando opcionalmente por término, rol o estado.
   */
  obtenerUsuarios(search?: string, rolId?: number, activo?: boolean): Observable<Usuario[]> {
    let params = new HttpParams();
    if (search) {
      params = params.set('search', search);
    }
    if (rolId !== undefined && rolId !== null) {
      params = params.set('rol_id', rolId.toString());
    }
    if (activo !== undefined && activo !== null) {
      params = params.set('activo', activo.toString());
    }

    return this.http.get<Usuario[]>(this.apiUrl, { params });
  }

  /**
   * Obtiene un usuario por su identificador único.
   */
  obtenerUsuarioPorId(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.apiUrl}/${id}`);
  }

  /**
   * Registra un nuevo usuario en la base de datos para el tenant activo.
   */
  crearUsuario(user: UsuarioCreateDTO): Observable<Usuario> {
    return this.http.post<Usuario>(this.apiUrl, user);
  }

  /**
   * Actualiza los datos de un usuario existente.
   */
  actualizarUsuario(id: number, user: UsuarioUpdateDTO): Observable<Usuario> {
    return this.http.put<Usuario>(`${this.apiUrl}/${id}`, user);
  }

  /**
   * Activa o desactiva el acceso del usuario al sistema.
   */
  cambiarEstadoUsuario(id: number, activo: boolean): Observable<Usuario> {
    return this.http.patch<Usuario>(`${this.apiUrl}/${id}/estado`, { activo });
  }

  /**
   * Asigna un rol específico al usuario.
   */
  asignarRolUsuario(id: number, rolId: number): Observable<Usuario> {
    return this.http.patch<Usuario>(`${this.apiUrl}/${id}/rol`, { rol_id: rolId });
  }

  /**
   * Elimina permanentemente un usuario si no tiene operaciones asociadas.
   */
  eliminarUsuario(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD (EVITA REGRESIONES)
  // ============================================================================
  getUsers(search?: string, rolId?: number, activo?: boolean): Observable<Usuario[]> {
    return this.obtenerUsuarios(search, rolId, activo);
  }

  getUserById(id: number): Observable<Usuario> {
    return this.obtenerUsuarioPorId(id);
  }

  createUser(user: UsuarioCreateDTO): Observable<Usuario> {
    return this.crearUsuario(user);
  }

  updateUser(id: number, user: UsuarioUpdateDTO): Observable<Usuario> {
    return this.actualizarUsuario(id, user);
  }

  toggleUserStatus(id: number, activo: boolean): Observable<Usuario> {
    return this.cambiarEstadoUsuario(id, activo);
  }

  assignUserRole(id: number, rolId: number): Observable<Usuario> {
    return this.asignarRolUsuario(id, rolId);
  }

  deleteUser(id: number): Observable<any> {
    return this.eliminarUsuario(id);
  }
}

export { UserService as UsuarioService };
