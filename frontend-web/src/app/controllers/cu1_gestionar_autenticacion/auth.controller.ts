import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap, finalize } from 'rxjs';
import { AuthService } from '../../services/cu1_gestionar_autenticacion/auth.service';
import { LoginResponseDTO } from '../../models/cu1_gestionar_autenticacion/auth.model';

@Injectable({
  providedIn: 'root'
})
export class AuthController {
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  private currentUserSubject = new BehaviorSubject<any>(null);
  public currentUser$: Observable<any> = this.currentUserSubject.asObservable();

  constructor(private authService: AuthService) {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        this.currentUserSubject.next(JSON.parse(userStr));
      } catch (e) {
        console.error('Error parsing current user', e);
      }
    }
  }

  get currentUser(): any {
    return this.currentUserSubject.value;
  }

  get isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  login(email: string, pass: string): Observable<LoginResponseDTO> {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    return this.authService.login(email, pass).pipe(
      tap((res) => {
        localStorage.setItem('token', res.access_token);
        if (res.user) {
          localStorage.setItem('user', JSON.stringify(res.user));
          localStorage.setItem('user_role', res.user.rol || 'EMPLEADO');
          this.currentUserSubject.next(res.user);
        }
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('user_role');
    this.currentUserSubject.next(null);
  }

  recoverPassword(email: string): Observable<{ message: string }> {
    this.loadingSubject.next(true);
    return this.authService.requestPasswordRecovery(email).pipe(
      finalize(() => this.loadingSubject.next(false))
    );
  }

  resetPassword(token: string, newPass: string): Observable<{ message: string }> {
    this.loadingSubject.next(true);
    return this.authService.resetPassword(token, newPass).pipe(
      finalize(() => this.loadingSubject.next(false))
    );
  }
}
