import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/v1/auth';

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<any> {
    const body = new URLSearchParams();
    body.set('username', email); // OAuth2 form uses 'username' instead of 'email'
    body.set('password', password);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post(`${this.apiUrl}/login`, body.toString(), { headers });
  }

  requestPasswordRecovery(email: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/recuperar-password`, { email });
  }

  resetPassword(token: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/reset-password`, {
      token: token,
      new_password: newPassword
    });
  }

  getToken(): string | null {
    return localStorage.getItem('access_token') || localStorage.getItem('token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getCurrentUser(): any {
    const userStr = localStorage.getItem('usuario') || localStorage.getItem('user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }

  getUserRole(): string {
    const directRol = localStorage.getItem('rol') || localStorage.getItem('user_role');
    if (directRol) return directRol.toUpperCase();

    const user = this.getCurrentUser();
    if (user) {
      if (typeof user.rol === 'string') return user.rol.toUpperCase();
      if (user.rol && typeof user.rol.nombre === 'string') return user.rol.nombre.toUpperCase();
      if (user.rol_id === 1 || user.rolid === 1) return 'ADMIN';
      if (user.rol_id === 2 || user.rolid === 2) return 'CLIENTE';
    }
    return '';
  }

  isAdmin(): boolean {
    const role = this.getUserRole();
    return role === 'ADMIN' || role === 'ADMINISTRADOR' || role === 'SUPERVISOR';
  }

  isCliente(): boolean {
    const role = this.getUserRole();
    return role === 'CLIENTE' || (!this.isAdmin() && this.isAuthenticated());
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    localStorage.removeItem('user');
    localStorage.removeItem('rol');
    localStorage.removeItem('user_role');
  }
}

