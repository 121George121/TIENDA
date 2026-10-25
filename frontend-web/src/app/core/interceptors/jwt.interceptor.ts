import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  
  let authReq = req;
  const token = typeof window !== 'undefined' ? (localStorage.getItem('access_token') || localStorage.getItem('token')) : null;
  const tenantId = typeof window !== 'undefined' ? (localStorage.getItem('tenant_id') || '1') : '1';

  // Inyectar Token de Autorización y Cabecera de Tenant Multi-tenant
  let headers = req.headers;
  if (token) {
    headers = headers.set('Authorization', `Bearer ${token}`);
  }
  if (tenantId) {
    headers = headers.set('X-Tenant-ID', tenantId);
  }

  authReq = req.clone({ headers });

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        // Token expirado o inválido: limpiar sesión residual y redirigir al login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          localStorage.removeItem('usuario');
          localStorage.removeItem('rol');
          localStorage.removeItem('user_role');
          localStorage.removeItem('tenant_id');
          localStorage.removeItem('tenant_slug');
          localStorage.removeItem('tenant_nombre');

          if (!window.location.pathname.includes('/login')) {
            router.navigate(['/login']);
          }
        }
      }
      return throwError(() => error);
    })
  );
};
