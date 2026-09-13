import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LoginResponseDTO } from '../../models/cu1_gestionar_autenticacion/auth.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/v1/auth';

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<LoginResponseDTO> {
    const body = new URLSearchParams();
    body.set('username', email);
    body.set('password', password);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post<LoginResponseDTO>(`${this.apiUrl}/login`, body.toString(), { headers });
  }

  requestPasswordRecovery(email: string): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.apiUrl}/recuperar-password`, { email });
  }

  resetPassword(token: string, newPassword: string): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.apiUrl}/reset-password`, {
      token: token,
      new_password: newPassword
    });
  }

  registro(data: { nombre: string; apellido?: string; email: string; password: string; telefono?: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/registro`, data);
  }

  verificarCodigo(email: string, codigo: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/verificar-codigo`, { email, codigo });
  }
}
