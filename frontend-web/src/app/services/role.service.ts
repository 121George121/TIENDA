import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Rol, RolCreateDTO } from '../models/role.model';

@Injectable({
  providedIn: 'root'
})
export class RoleService {
  private apiUrl = 'http://localhost:8000/api/v1/roles';

  constructor(private http: HttpClient) {}

  getRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(this.apiUrl);
  }

  getRoleById(id: number): Observable<Rol> {
    return this.http.get<Rol>(`${this.apiUrl}/${id}`);
  }

  createRole(role: RolCreateDTO): Observable<Rol> {
    return this.http.post<Rol>(this.apiUrl, role);
  }

  updateRole(id: number, role: RolCreateDTO): Observable<Rol> {
    return this.http.put<Rol>(`${this.apiUrl}/${id}`, role);
  }

  updateRolePermissions(id: number, permisos: string[]): Observable<Rol> {
    return this.http.put<Rol>(`${this.apiUrl}/${id}/permisos`, { permisos });
  }

  deleteRole(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
}
