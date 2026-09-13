import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Usuario, UsuarioCreateDTO, UsuarioUpdateDTO } from '../../models/cu2_gestionar_usuarios_roles/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000/api/v1/usuarios';

  constructor(private http: HttpClient) {}

  getUsers(search?: string, rolId?: number, activo?: boolean): Observable<Usuario[]> {
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

  getUserById(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.apiUrl}/${id}`);
  }

  createUser(user: UsuarioCreateDTO): Observable<Usuario> {
    return this.http.post<Usuario>(this.apiUrl, user);
  }

  updateUser(id: number, user: UsuarioUpdateDTO): Observable<Usuario> {
    return this.http.put<Usuario>(`${this.apiUrl}/${id}`, user);
  }

  toggleUserStatus(id: number, activo: boolean): Observable<Usuario> {
    return this.http.patch<Usuario>(`${this.apiUrl}/${id}/estado`, { activo });
  }

  assignUserRole(id: number, rolId: number): Observable<Usuario> {
    return this.http.patch<Usuario>(`${this.apiUrl}/${id}/rol`, { rol_id: rolId });
  }

  deleteUser(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
}
